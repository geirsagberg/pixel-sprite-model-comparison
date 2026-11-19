"""Render the authored pixel layers with Python 3 and FFmpeg."""
from pathlib import Path
import struct
import subprocess
import zlib
from pixels import PALETTE, BODY, PACK, LEGS, ARMS, FRAMES

ROOT = Path(__file__).resolve().parent
colors = list(PALETTE)
palette = b''.join(bytes.fromhex(rgb) for rgb in PALETTE.values())
frames = []
for far, near, bob, arm in FRAMES:
    frame = [bytearray(32) for _ in range(32)]

    def stamp(x, y, grid, shade=None):
        for dy, row in enumerate(grid.strip().splitlines()):
            for dx, char in enumerate(row):
                if char != '.':
                    frame[y + dy][x + dx] = colors.index((shade or {}).get(char, char))

    stamp(*LEGS[far], shade={'d':'n', 'h':'l', 'l':'b'})
    stamp(*LEGS[near])
    stamp(8, 2 + bob, BODY)
    stamp(7, 13 + bob, PACK)
    x, grid = ARMS[arm]
    stamp(x, 15 + bob, grid)
    frames.append(frame)

def chunk(tag, data):
    return (struct.pack('>I', len(data)) + tag + data
            + struct.pack('>I', zlib.crc32(tag + data)))

rows = b''.join(b'\0' + b''.join(frame[y] for frame in frames) for y in range(32))
sheet = ROOT / 'sheet.png'
sheet.write_bytes(b'\x89PNG\r\n\x1a\n'
    + chunk(b'IHDR', struct.pack('>IIBBBBB', 32*len(frames), 32, 8, 3, 0, 0, 0))
    + chunk(b'PLTE', palette) + chunk(b'tRNS', b'\0')
    + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))

subprocess.run(['ffmpeg','-v','error','-y','-i',str(sheet),
    '-vf',f'untile={len(frames)}x1,settb=1/100,setpts=N*10,scale=256:256:flags=neighbor,split[a][b];[a]palettegen=reserve_transparent=1[p];[b][p]paletteuse=dither=none',
    '-r','10','-loop','0',str(ROOT/'walk.gif')],check=True)
