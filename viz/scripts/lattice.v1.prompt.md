<!-- model: gpt-6-astra | system prompt: see viz/astra.py SYSTEM -->

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


## Blender API notes (verified)

# Blender 5.2.1 headless API notes (verified on this machine, Nov 15 2026)

These snippets were run and checked here. Prefer them over older (2.x/3.x/4.x) API habits.

- Run: `Blender -b --factory-startup -P script.py -- <args>`; parse args from `sys.argv[sys.argv.index("--")+1:]`.
- There is no .blend file: `//` relative paths fail. Always use absolute output paths (`os.path.abspath`).
- Start clean: `for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)`.
- Render engine: only `'BLENDER_EEVEE'` exists (no `BLENDER_EEVEE_NEXT`, no legacy bloom setting).
  Samples: `scene.eevee.taa_render_samples = N`. Raytracing: `scene.eevee.use_raytracing = True` (optional).
  There is NO `scene.eevee.use_bloom` / `bloom_*` / `use_gtao` / `use_ssr`: setting them raises AttributeError.
- Color management: `scene.view_settings.view_transform = 'AgX'` and `scene.view_settings.look = 'AgX - Punchy'`
  (or `'AgX - Medium High Contrast'`), both work. `'Filmic'` may not exist; use AgX.
- Glow/bloom = compositor Glare node. The compositor is a node GROUP in 5.x (no `scene.node_tree`):
```python
ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
scene.compositing_node_group = ng
ng.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
rl = ng.nodes.new("CompositorNodeRLayers")
out = ng.nodes.new("NodeGroupOutput")
g = ng.nodes.new("CompositorNodeGlare")
g.inputs['Type'].default_value = 'Bloom'      # options are input sockets now, not node properties
g.inputs['Quality'].default_value = 'High'
g.inputs['Threshold'].default_value = 0.8
g.inputs['Strength'].default_value = 1.0
g.inputs['Size'].default_value = 0.6          # 0..1
ng.links.new(rl.outputs['Image'], g.inputs['Image'])
ng.links.new(g.outputs['Image'], out.inputs['Image'])
```
  Other compositor nodes that exist: CompositorNodeLensdist, CompositorNodeEllipseMask, CompositorNodeBlur,
  CompositorNodeColorBalance, CompositorNodeCurveRGB, CompositorNodeExposure, CompositorNodeDefocus.
  For 2-input math on images use `ShaderNodeMix`-style nodes carefully; if unsure, skip (a vignette is optional).
- Principled BSDF socket names: 'Base Color', 'Metallic', 'Roughness', 'Emission Color', 'Emission Strength',
  'Alpha', 'Coat Weight', 'Specular IOR Level'. Materials: `m = bpy.data.materials.new(n)`; `m.node_tree` already
  exists (use_nodes is deprecated and default True). Get BSDF with `m.node_tree.nodes["Principled BSDF"]`.
  Pure glow: `ShaderNodeEmission` linked into 'Material Output' 'Surface'.
- World: `w = scene.world or bpy.data.worlds.new("W"); scene.world = w`; background node is
  `w.node_tree.nodes["Background"]`.
- Camera: `cd = bpy.data.cameras.new("Cam"); cd.lens = 50; cd.dof.use_dof = True; cd.dof.focus_distance = d`
  (or `cd.dof.focus_object = empty`); `cd.dof.aperture_fstop = 2.8`. Aim with a 'TRACK_TO' constraint
  (`track_axis='TRACK_NEGATIVE_Z'`, `up_axis='UP_Y'`) at an Empty.
- Lights: `bpy.data.lights.new(name, type='AREA')` with `.energy`, `.size`, `.color`; link a new object to
  `scene.collection.objects.link(obj)`.
- PERFORMANCE: thousands of objects are slow to create. Build big instanced sets as ONE mesh with
  `mesh.from_pydata(verts, [], faces)` (e.g. 5625 boxes = 45k verts is fine) and use a per-face color attribute
  or separate material slots (`mesh.polygons.foreach_set("material_index", ...)`) for variation.
  Curves: `cu = bpy.data.curves.new(n, 'CURVE'); cu.dimensions = '3D'; sp = cu.splines.new('POLY');
  sp.points.add(k-1); sp.points.foreach_set('co', flat_xyzw)`; tube with `cu.bevel_depth`, `cu.bevel_resolution`.
- Still output: `scene.render.image_settings.file_format = 'PNG'`, `scene.render.filepath = abs_path`,
  `bpy.ops.render.render(write_still=True)`.
- Video output (verified):
```python
ims = scene.render.image_settings
ims.media_type = 'VIDEO'; ims.file_format = 'FFMPEG'
ff = scene.render.ffmpeg
ff.format = 'MPEG4'; ff.codec = 'H264'; ff.constant_rate_factor = 'HIGH'; ff.ffmpeg_preset = 'GOOD'
scene.render.fps = 24; scene.frame_start = 1; scene.frame_end = N
scene.render.filepath = abs_path_ending_in_.mp4
bpy.ops.render.render(animation=True)
```
- Keyframes for a seamless loop: set `fcurve.keyframe_points[i].interpolation = 'LINEAR'` or drive the camera
  with an Empty rotated 0 -> 2*pi over frames 1..N+1 (render 1..N) so the last frame flows into the first.
  In 5.x actions are layered; the simplest robust way is `obj.keyframe_insert("rotation_euler", frame=f)` for
  every frame (or just start and end) and then set interpolation on `obj.animation_data.action` fcurves if
  accessible; if not accessible, insert a keyframe on every frame (always works).
