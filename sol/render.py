"""Render the hand-drawn frames with Python 3 and FFmpeg."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIZE = 32
SCALE = 8
FPS = 10


def ffmpeg(arguments, pixels):
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *arguments],
        input=pixels,
        check=True,
        cwd=ROOT,
    )


def main():
    data = json.loads((ROOT / "frames.json").read_text())
    palette = {
        key: bytes.fromhex(color + "ff") if color else bytes(4)
        for key, color in data["palette"].items()
    }
    frames = [frame["pixels"] for frame in data["frames"]]
    assert all(
        len(frame) == SIZE and all(len(row) == SIZE for row in frame)
        for frame in frames
    ), "Each frame must be a 32×32 grid"

    def pixels(row):
        return b"".join(palette[key] for key in row)

    raw_input = ["-f", "rawvideo", "-pixel_format", "rgba"]
    sheet = b"".join(pixels(row) for rows in zip(*frames) for row in rows)
    ffmpeg(
        [
            *raw_input, "-video_size", f"{SIZE * len(frames)}x{SIZE}",
            "-i", "pipe:0", "-frames:v", "1", "-update", "1", "sheet.png",
        ],
        sheet,
    )

    animation = b"".join(pixels(row) for frame in frames for row in frame)
    side = SIZE * SCALE
    ffmpeg(
        [
            *raw_input, "-video_size", f"{SIZE}x{SIZE}", "-framerate", str(FPS),
            "-i", "pipe:0", "-filter_complex",
            f"scale={side}:{side}:flags=neighbor,split[a][b];"
            "[a]palettegen[pal];[b][pal]paletteuse=dither=none",
            "-gifflags", "-offsetting-transdiff", "-loop", "0", "walk.gif",
        ],
        animation,
    )


if __name__ == "__main__":
    main()
