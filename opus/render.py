"""Render frames.txt into sheet.png (native size) and walk.gif (8x, looping).

Pure standard library: small PNG and GIF encoders are included below.
Usage: python3 render.py
"""

import struct
import zlib
from pathlib import Path

HERE = Path(__file__).parent
SIZE = 32
SCALE = 8
FRAME_MS = 100


def load(path):
    palette, frames, section = {}, [], None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line in ("palette", "frame"):
            section = line
            if line == "frame":
                frames.append([])
        elif section == "palette":
            char, value = line.split()
            palette[char] = None if value == "transparent" else bytes.fromhex(value)
        else:
            frames[-1].append(line)

    for i, rows in enumerate(frames, 1):
        assert len(rows) == SIZE, f"frame {i}: {len(rows)} rows"
        for y, row in enumerate(rows):
            assert len(row) == SIZE, f"frame {i} row {y}: {len(row)} columns"
            unknown = set(row) - palette.keys()
            assert not unknown, f"frame {i} row {y}: unknown {unknown}"
    return palette, frames


def to_indices(palette, frames):
    """Map chars to palette indices. Index 0 is always transparent."""
    chars = ["."] + [c for c in palette if c != "."]
    index = {c: i for i, c in enumerate(chars)}
    colors = [palette[c] or b"\0\0\0" for c in chars]
    grids = [[[index[c] for c in row] for row in rows] for rows in frames]
    return colors, grids


def write_png(path, colors, grid):
    h, w = len(grid), len(grid[0])
    raw = b"".join(
        b"\0" + b"".join(colors[i] + (b"\0" if i == 0 else b"\xff") for i in row)
        for row in grid
    )

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def lzw(pixels, min_size):
    clear, end = 1 << min_size, (1 << min_size) + 1
    out, acc, nbits = bytearray(), 0, 0

    def emit(code, size):
        nonlocal acc, nbits
        acc |= code << nbits
        nbits += size
        while nbits >= 8:
            out.append(acc & 0xFF)
            acc >>= 8
            nbits -= 8

    def reset():
        return {bytes([i]): i for i in range(clear)}, end + 1, min_size + 1

    table, next_code, size = reset()
    emit(clear, size)
    word = b""
    for p in pixels:
        candidate = word + bytes([p])
        if candidate in table:
            word = candidate
            continue
        emit(table[word], size)
        table[candidate] = next_code
        next_code += 1
        if next_code > (1 << size) and size < 12:
            size += 1
        if next_code == 4096:
            emit(clear, size)
            table, next_code, size = reset()
        word = bytes([p])
    emit(table[word], size)
    emit(end, size)
    if nbits:
        out.append(acc & 0xFF)
    return bytes(out)


def write_gif(path, colors, grids, delay_ms):
    h, w = len(grids[0]), len(grids[0][0])
    depth = max(2, (len(colors) - 1).bit_length())
    table = b"".join(colors) + b"\0\0\0" * ((1 << depth) - len(colors))

    gif = b"GIF89a" + struct.pack("<HHBBB", w, h, 0x80 | ((depth - 1) << 4) | (depth - 1), 0, 0)
    gif += table
    gif += b"\x21\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00"  # loop forever
    for grid in grids:
        # Disposal 2 (restore to background) so transparent pixels clear each frame.
        gif += b"\x21\xf9\x04" + struct.pack("<BHB", 0x09, delay_ms // 10, 0) + b"\0"
        gif += b"\x2c" + struct.pack("<HHHHB", 0, 0, w, h, 0)
        data = lzw([i for row in grid for i in row], depth)
        gif += bytes([depth])
        gif += b"".join(bytes([len(data[i:i + 255])]) + data[i:i + 255] for i in range(0, len(data), 255))
        gif += b"\0"
    gif += b"\x3b"
    path.write_bytes(gif)


def scale(grid, factor):
    return [[i for i in row for _ in range(factor)] for row in grid for _ in range(factor)]


def main():
    palette, frames = load(HERE / "frames.txt")
    colors, grids = to_indices(palette, frames)
    sheet = [sum((grid[y] for grid in grids), []) for y in range(SIZE)]
    write_png(HERE / "sheet.png", colors, sheet)
    write_gif(HERE / "walk.gif", colors, [scale(g, SCALE) for g in grids], FRAME_MS)
    print(f"{len(grids)} frames, {len(colors) - 1} colors + transparent")


if __name__ == "__main__":
    main()
