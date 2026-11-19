# Adventurer walk cycle

Side view, facing right. Every pixel is hand-authored in `sprite.txt`; `python3 render.py` turns it into `sheet.png` and `walk.gif` (standard library only).

## Frames

8 frames, 32x32 each. `sheet.png` is 256x32, frames left to right.

| Frame | Pose | Body height |
| --- | --- | --- |
| 0 | Contact, near leg forward | mid |
| 1 | Down, weight on near leg | low (1 px down) |
| 2 | Passing, far leg swings through | mid |
| 3 | Up, near leg pushes off | high (1 px up) |
| 4–7 | Same four poses with the legs swapped | |

The near arm swings opposite the near leg. The far arm shows in front of the body in frames 0, 1 and 7. The scarf tail lags the bob: it lifts on the low frames and droops on the high ones.

## Palette

16 colors plus transparency. The outline is `#1b1626`.

| Part | Light | Shadow |
| --- | --- | --- |
| Skin | `#f0b98d` | `#c98562` |
| Hair | `#a8572b` | `#6e3320` |
| Tunic | `#4c9f4e` | `#2d6b40` |
| Sleeve | `#f1e8cf` | `#b8ab8c` |
| Scarf | `#d8423c` | `#96283a` |
| Leather | `#8a5a34` | `#5a3620` |
| Trousers | `#5b6fa8` | `#3b4675` |
| Buckle | `#f4c84a` | |

The far leg and far arm use the shadow shades, so the two sides stay easy to tell apart.

## Timing

100 ms per frame, so one full cycle (two steps) takes 0.8 s. `walk.gif` loops forever at 8x scale (256x256, nearest neighbor) with a transparent background.
