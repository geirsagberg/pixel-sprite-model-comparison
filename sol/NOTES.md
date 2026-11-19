# Adventurer walk

Six hand-drawn 32×32 frames show a right-facing walk, with contact, down, and passing poses for each step. The head and torso bob one pixel below and above the contact pose.

The palette uses 14 opaque colors and a transparent background. A dark plum outline defines the silhouette, and the far leg is shaded darker than the near leg.

The GIF loops every 600 ms at 100 ms per frame. It uses 8× nearest-neighbor scaling. Run `python3 render.py` with FFmpeg on your PATH to rebuild both images from `frames.json`.
