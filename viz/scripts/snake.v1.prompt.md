<!-- model: gpt-6-astra | system prompt: see viz/astra.py SYSTEM -->

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
