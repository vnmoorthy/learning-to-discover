<!-- model: gpt-6-astra | system prompt: see viz/astra.py SYSTEM -->

# Brief: "Hadamard City" for the maximal-determinant problem (order 51)

Project: "Learning to Discover", an AI lab that gets better at discovering mathematics by doing it. The
current record for the largest determinant of a 51x51 matrix with entries +1/-1 has log10|det| = 43.3375.
This image turns that exact record matrix into an extruded city / terrain at night. It must look stunning,
premium and clean.

## Data (JSON at --data; real record matrix, do not invent anything)
```
{ "n": 51, "matrix": [[1, -1, ...], ...],   # 51 rows x 51 cols, entries exactly 1 or -1
  "log10_det": 43.33745596194037, "holder": "kgrey" }
```

## Scene (art direction)
- Cell (i, j) (row i, column j) is a block on a 51x51 grid (spacing 1.0, block footprint ~0.86 x 0.86,
  centered on the origin, row 0 at the back).
- Height comes from the data only: +1 cells are towers, -1 cells are low plinths. To give it a city/terrain
  rhythm, modulate height by the local agreement of the matrix: s(i,j) = mean of the entries in the 5x5
  neighbourhood (clipped at the borders). Use exactly h_plus = 0.9 + 2.6 * (s + 1) / 2 for +1 cells and
  h_minus = 0.12 + 0.2 * (s + 1) / 2 for -1 cells (purely data-derived; no random or decorative height terms).
- Materials: dark architectural glass/graphite towers (#101318, roughness ~0.3) with an emissive cyan #3DF5FF
  cap / top edge on +1 towers (thin glowing roof slab), and the -1 plinths carrying a dim warm amber #FFB547
  glow on their tops (lower strength than the cyan) so the sign pattern reads from above like city lights.
- Dark studio environment (#07080B world, low strength), a dark reflective ground plane under the city, slight
  haze is optional (skip volumetrics if slow).
- Lighting: cool soft area light from high back-left as rim; emissive caps do the rest.
- Camera: aerial 3/4 view at ~35-45 degrees elevation from a corner, lens ~50-85 mm, the whole 51x51 city in
  frame with some breathing room but filling most of the frame. Tilt-shift / miniature feel through depth of
  field: focus on the city center, fstop ~1.4-2.0 so front and back edges blur.
- Post: compositor Glare 'Bloom', AgX view transform with a punchy look. No text.

## Script contract (args after `--`)
- `--data PATH` (hadamard JSON), `--out PATH` (absolute .png)
- `--res WxH` (default 1920x1080), `--samples N` (EEVEE taa_render_samples, default 64)
- Build all 2601 blocks as ONE mesh (plus one mesh for the emissive caps), not 2601 objects.


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
