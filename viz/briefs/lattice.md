# Brief: "The Lattice" (hero still + seamless orbit loop) for the no-three-in-line problem

Project: "Phoenixastar", an AI lab that gets better at discovering mathematics by doing it. Our agents
search for 150 points on a 75x75 integer grid with no three on a common line (record: 148 points). This image is
the hero of the project page and must look stunning: premium, cinematic, clean, like a product launch film.

## Data (JSON at --data; real output of our SAT search, do not invent anything)
```
{ "n": 75,                                   # grid is {0..74}^2
  "points": [[x, y], ...],                   # 150 chosen points of the current SAT model
  "violated_lines": [                        # 122 lines that still contain >= 3 chosen points
     {"a": [x,y], "b": [x,y], "m": 3,        # two chosen points on the line, m = #chosen points on it
      "ends": [[fx,fy],[fx,fy]],             # that line clipped to the square [0,74]^2 (floats, grid units)
      "on": [[x,y], ...]}, ...],             # the chosen points lying on that line
  "count": 150, "violated": 122, "sym": "rot180-150", "round": 23,
  "record_points": [[x,y], ...] }            # the 148-point record (NOT drawn in this image; ignore)
```

## Scene (art direction)
- Dark studio. Near-black environment (#07080B-ish world, very low strength), a large dark glossy floor
  (slight reflection, roughness ~0.25) that fades into darkness. No visible horizon line; no text anywhere.
- The 75x75 lattice as a field of tiny pillars (square cross-section ~0.32 x 0.32 units, grid spacing 1.0,
  centered on the origin). Every one of the 5625 cells has a pillar. Non-chosen pillars: short (height ~0.18 plus a
  tiny deterministic jitter, e.g. 0.03 * hash(x,y)), dark graphite (#14161C) with subtle specular so the field
  reads as a fine texture catching rim light.
- The 150 chosen points: taller pillars (height ~1.1) that GLOW emissive cyan #3DF5FF (emission strength high
  enough to bloom), plus a small bright cap. Chosen points that lie on any violated line (union of all "on")
  glow warm amber #FFB547 instead, so you can see which points are still in conflict.
- Each violated line: a THIN red light beam (#FF2A3A, radius ~0.025, emission ~6-10) running along "ends"
  across the lattice at the height of the glowing pillar tops (z ~ 1.1). 122 beams: keep them thin and
  semi-subtle so the image stays clean, not a red mess (e.g. emission ~5, slightly transparent look is fine).
- Lighting: one soft cool key area light from behind-left (rim light on pillars), very faint warm fill from the
  right. Most light comes from the emissive elements.
- Camera: low, cinematic 3/4 view looking across the lattice (camera ~25-35 units from center, elevation
  ~10-16 degrees, lens 50-70 mm), so the field recedes toward the horizon. Depth of field: focus on a glowing
  amber cluster roughly a third into the frame (fstop ~1.8-2.8) so near and far pillars soften.
- Post: compositor Glare 'Bloom' (moderate), AgX view transform with 'AgX - Punchy' or
  'AgX - Medium High Contrast' look, slight vignette if easy (optional, skip if risky).

## Script contract (args after `--`)
- `--data PATH` (lattice JSON), `--out PATH` (absolute .png for still, .mp4 for loop)
- `--mode still|loop` (default still)
- `--res WxH` (default 1920x1080), `--samples N` (EEVEE taa_render_samples, default 64)
- `--frames N` (loop only, default 192 = 8 s at 24 fps), `--fps N` (default 24)
- still: render one PNG.
- loop: same scene; the camera orbits 360 degrees around the lattice center at fixed elevation and distance,
  looking at the center, in exactly `frames` frames, seamless (frame N+1 would equal frame 1). Render
  H.264 MP4 via FFMPEG (see API notes). DOF focus follows the center. Keep per-frame time small: the loop is
  rendered with --res 1280x720 --samples 8 and must finish in under 10 minutes.
- Build the 5625 pillars as ONE mesh (and the chosen pillars as one or two meshes), not 5625 objects.
