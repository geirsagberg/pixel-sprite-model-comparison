"""Render sprite.txt to sheet.png and walk.gif. Standard library only.

Usage: python3 render.py
"""

import struct
import zlib
from pathlib import Path

HERE = Path(__file__).parent
SIZE = 32  # frame width and height in pixels
SCALE = 8  # GIF upscale factor (nearest neighbor)
FRAME_MS = 100  # GIF frame duration


def load(path):
    """Return (colors, frames).

    colors: list of RGB tuples; index 0 is the transparent slot.
    frames: list of SIZE x SIZE grids of color indexes.
    """
    blocks = path.read_text().strip().split("\n\n")
    index = {}
    colors = []
    frames = []
    for block in blocks:
        head, *lines = block.splitlines()
        if head == "palette":
            for line in lines:
                char, value = line.split()[:2]
                index[char] = len(colors)
                rgb = (0, 0, 0) if value == "transparent" else bytes.fromhex(value[1:])
                colors.append(tuple(rgb))
        elif head.startswith("frame"):
            if len(lines) != SIZE:
                raise ValueError(f"{head!r}: {len(lines)} rows, expected {SIZE}")
            for y, line in enumerate(lines):
                if len(line) != SIZE:
                    raise ValueError(f"{head!r} row {y}: {len(line)} pixels, expected {SIZE}")
            frames.append([[index[char] for char in line] for line in lines])
    return colors, frames


def write_png(path, width, height, rgba):
    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    stride = width * 4
    rows = b"".join(b"\x00" + rgba[y * stride : (y + 1) * stride] for y in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


def lzw(pixels, bits):
    """GIF-flavored LZW. Returns the packed code stream."""
    clear = 1 << bits
    end = clear + 1
    out = bytearray()
    acc = 0
    filled = 0

    def emit(code):
        nonlocal acc, filled
        acc |= code << filled
        filled += width
        while filled >= 8:
            out.append(acc & 0xFF)
            acc >>= 8
            filled -= 8

    def reset():
        return {(i,): i for i in range(clear)}, end + 1, bits + 1

    table, next_code, width = reset()
    emit(clear)
    run = ()
    for pixel in pixels:
        longer = run + (pixel,)
        if longer in table:
            run = longer
            continue
        emit(table[run])
        if next_code < 4096:
            table[longer] = next_code
            if next_code == 1 << width:
                width += 1
            next_code += 1
        else:
            emit(clear)
            table, next_code, width = reset()
        run = (pixel,)
    emit(table[run])
    emit(end)
    if filled:
        out.append(acc & 0xFF)
    return bytes(out)


def write_gif(path, width, height, colors, frames, frame_ms):
    """Write a looping GIF. Color index 0 is transparent."""
    bits = max(2, (len(colors) - 1).bit_length())
    table = b"".join(bytes(c) for c in colors).ljust(3 * (1 << bits), b"\x00")
    out = bytearray(b"GIF89a")
    out += struct.pack("<HHBBB", width, height, 0xF0 | (bits - 1), 0, 0)
    out += table
    out += b"\x21\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00"  # loop forever
    for pixels in frames:
        # Disposal 2 clears each frame before the next, so transparency holds.
        out += b"\x21\xf9\x04\x09" + struct.pack("<H", frame_ms // 10) + b"\x00\x00"
        out += b"\x2c" + struct.pack("<HHHHB", 0, 0, width, height, 0)
        out.append(bits)
        data = lzw(pixels, bits)
        for i in range(0, len(data), 255):
            block = data[i : i + 255]
            out.append(len(block))
            out += block
        out.append(0)
    out.append(0x3B)
    path.write_bytes(bytes(out))


def main():
    colors, frames = load(HERE / "sprite.txt")
    rgba = [bytes(c) + b"\xff" for c in colors]
    rgba[0] = b"\x00\x00\x00\x00"

    sheet = b"".join(rgba[frame[y][x]] for y in range(SIZE) for frame in frames for x in range(SIZE))
    write_png(HERE / "sheet.png", SIZE * len(frames), SIZE, sheet)

    big = SIZE * SCALE
    scaled = [[frame[y // SCALE][x // SCALE] for y in range(big) for x in range(big)] for frame in frames]
    write_gif(HERE / "walk.gif", big, big, colors, scaled, FRAME_MS)

    print(f"{len(frames)} frames, {len(colors) - 1} colors -> sheet.png, walk.gif")


if __name__ == "__main__":
    main()
