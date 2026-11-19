# Adventurer walk

- **Frames:** 6, each 32x32, facing right. Contact → down → passing, then the same with the legs swapped. Arms swing against the legs (back, half-back, neutral, forward, half-forward, neutral).
- **Bob:** the body sits 1 px lower on the down frames (2, 5) and 1 px higher on the passing frames (3, 6).
- **Palette:** 14 colors plus transparent. Outline `#1c1424`, hair, skin, tunic, boots and belt, buckle, pants and backpack, each with a light and a dark shade. The near leg uses the light shades and the far leg the dark ones.
- **Timing:** 100 ms per frame, so one full cycle takes 0.6 s. The GIF loops forever.
- **Files:** `frames.txt` holds the palette and one character grid per frame. `python3 render.py` writes `sheet.png` (192x32) and `walk.gif` (8x, nearest-neighbor). The script uses only the standard library.
