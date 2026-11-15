# Brief: "The Snake" for the snake-in-the-box problem in dimension 13

Project: "Phoenixastar", an AI lab that gets better at discovering mathematics by doing it. A
snake-in-the-box is a path along edges of the 13-dimensional hypercube that never comes back near itself (no
chords). The record snake has 2950 edges. This image shows that exact snake, linearly projected from 13D to 3D,
as a single glowing tube. It must look stunning, premium and clean.

## Data (JSON at --data; real record snake, already projected; do not invent anything)
```
{ "edges": 2950, "dimension": 13,
  "path": [[x, y, z], ...],          # 2951 points in order (the snake's vertices projected to 3D), roughly
                                     # within a box of half-size 4 centered on the origin
  "cube_vertices": [[x, y, z], ...], # all 8192 vertices of the 13-cube under the same projection
  "actions": [int, ...] }            # coordinate flipped at each step (not needed for drawing)
```
Consecutive path points are joined by straight segments (each is one hypercube edge). The projection is
hierarchical: long segments are rare coordinate flips, tiny wiggles are frequent ones, so the path forms
clusters joined by longer bridges.

## Scene (art direction)
- Dark studio, near-black world (#07080B), no floor needed (or a barely visible dark reflective floor far below).
- The snake: ONE continuous thin tube following `path` exactly (POLY spline; bevel_depth ~0.012-0.02, low
  bevel resolution for speed), emissive, colour graded along its length from warm amber #FFB547 at the start to
  electric cyan #3DF5FF at the end (e.g. split the path into ~24 consecutive splines in one curve object, each
  with its own material slot interpolating the colour; consecutive splines must share their joint point so the
  tube is continuous). Emission strong enough to bloom but the structure must stay readable (not a blown-out blob).
- The 8192 projected cube vertices as faint tiny dust points (very small dim cyan-white specks, e.g. one mesh of
  tiny icospheres or tiny quads, low emission) behind/around the snake to hint at the hypercube.
- Small brighter spheres marking the start (amber) and the end (cyan) of the snake.
- Camera: 3/4 view of the whole structure filling ~70% of a 16:9 frame, lens ~60-85 mm, depth of field focused
  on the nearest dense cluster (fstop ~2.0-2.8) so far clusters soften into bokeh.
- Post: compositor Glare 'Bloom', AgX with a punchy look. No text.

## Script contract (args after `--`)
- `--data PATH` (snake JSON), `--out PATH` (absolute .png, or .mp4 if --mode turntable)
- `--mode still|turntable` (default still); `--res WxH` (default 1920x1080); `--samples N` (default 64)
- `--frames N` (turntable only, default 192), `--fps N` (default 24): turntable = the snake object rotates 360
  degrees about the vertical axis over exactly N frames (seamless loop), rendered as H.264 MP4 (see API notes).
