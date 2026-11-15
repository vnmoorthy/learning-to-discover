<!-- model: gpt-6-astra | system prompt: see viz/astra.py SYSTEM -->

# Brief: "Hadamard City" for the maximal-determinant problem (order 51)

Project: "Phoenixastar", an AI lab that gets better at discovering mathematics by doing it. The
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
- Lights also have `light.specular_factor` / `light.diffuse_factor` (0..1). A big area light reflecting in a
  glossy floor shows up as a bright rectangle: lower its `specular_factor` (e.g. 0.0-0.15) or move it.
  Objects have `visible_camera`, `visible_glossy`, `visible_shadow` booleans.


## Your current script (previous version)

```python
# Written by gpt-6-astra (OpenAI Responses API), version 2, 2026-11-15 06:33. Prompt: hadamard_city.v2.prompt.md
#!/usr/bin/env python3
"""Hadamard City: render the supplied record matrix, without synthetic data."""

import argparse
import json
import math
import os
import sys
import time

import bpy


# Rendering/art-direction constants, not mathematical data.
# Geometry retains unit-spaced coordinates in its meshes. A uniform scene
# scale gives the camera real miniature-scale DOF without changing proportions.
MINIATURE_SCALE = 0.04
FOOTPRINT = 0.86


def positive_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    if value <= 0:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    return value


def resolution(text):
    try:
        width, height = text.lower().split("x")
        return positive_int(width), positive_int(height)
    except (ValueError, argparse.ArgumentTypeError):
        raise argparse.ArgumentTypeError("Resolution must be WxH.")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--res", type=resolution, default=(1920, 1080))
    parser.add_argument("--samples", type=positive_int, default=64)
    return parser.parse_args(argv)


def load_data(path):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    n = data.get("n")
    matrix = data.get("matrix")
    if type(n) is not int or n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if not isinstance(matrix, list) or len(matrix) != n:
        raise ValueError("'matrix' must contain exactly n rows.")

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"Row {i} must contain exactly n entries.")
        for j, value in enumerate(row):
            if type(value) not in (int, float) or value not in (-1, 1):
                raise ValueError(f"Entry ({i}, {j}) must be exactly +1 or -1.")

    log_det = data.get("log10_det")
    if type(log_det) not in (int, float) or not math.isfinite(log_det):
        raise ValueError("'log10_det' must be a finite number.")
    if not isinstance(data.get("holder"), str):
        raise ValueError("'holder' must be a string.")

    return data


def linear_rgb(hex_color):
    text = hex_color.lstrip("#")
    values = [int(text[k:k + 2], 16) / 255.0 for k in (0, 2, 4)]
    return tuple(
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in values
    )


def surface_material(name, color, roughness, metallic, coat=0.0):
    mat = bpy.data.materials.new(name)
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*linear_rgb(color), 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = coat
    return mat


def glow_material(name, color, strength):
    # Pure emission prevents a softbox reflection from whitening the roofs.
    mat = bpy.data.materials.new(name)
    nodes = mat.node_tree.nodes
    output = nodes["Material Output"]
    nodes.remove(nodes["Principled BSDF"])
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*linear_rgb(color), 1.0)
    emission.inputs["Strength"].default_value = strength
    mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


def append_box(vertices, faces, indices, x, y, width, bottom, top, slot=0):
    offset = len(vertices)
    r = width / 2.0
    vertices.extend([
        (x - r, y - r, bottom),
        (x + r, y - r, bottom),
        (x + r, y + r, bottom),
        (x - r, y + r, bottom),
        (x - r, y - r, top),
        (x + r, y - r, top),
        (x + r, y + r, top),
        (x - r, y + r, top),
    ])
    for face in (
        (3, 2, 1, 0),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
        (4, 5, 6, 7),
    ):
        faces.append(tuple(offset + k for k in face))
        indices.append(slot)


def append_cyan_roof(vertices, faces, indices, x, y, bottom, top):
    """A thin roof slab: luminous perimeter and fascia, graphite inset."""
    offset = len(vertices)
    outer = FOOTPRINT / 2.0
    inner = outer - 0.060

    for radius, z in ((outer, bottom), (outer, top), (inner, top)):
        vertices.extend([
            (x - radius, y - radius, z),
            (x + radius, y - radius, z),
            (x + radius, y + radius, z),
            (x - radius, y + radius, z),
        ])

    def face(corners, slot):
        faces.append(tuple(offset + k for k in corners))
        indices.append(slot)

    # Cap slots: cyan=0, amber=1, graphite=2.
    face((3, 2, 1, 0), 2)
    for k in range(4):
        nxt = (k + 1) % 4
        face((k, nxt, 4 + nxt, 4 + k), 0)
        face((4 + k, 4 + nxt, 8 + nxt, 8 + k), 0)
    face((8, 9, 10, 11), 2)


def mesh_object(name, vertices, faces, materials, indices=None):
    mesh = bpy.data.meshes.new(name + " Mesh")
    mesh.from_pydata(vertices, [], faces)
    for mat in materials:
        mesh.materials.append(mat)
    if indices is not None:
        mesh.polygons.foreach_set("material_index", indices)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.scale = (MINIATURE_SCALE,) * 3
    return obj


def scaled_location(location):
    return tuple(v * MINIATURE_SCALE for v in location)


def aim_at(obj, target):
    constraint = obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"


def area_light(name, location, energy, size, color, target):
    light = bpy.data.lights.new(name, type="AREA")
    light.energy = energy * MINIATURE_SCALE ** 2
    light.size = size * MINIATURE_SCALE
    light.color = linear_rgb(color)

    # Remove the rectangular softbox reflection on the ground. The grazing
    # diffuse contribution still reveals the tower sidewalls.
    light.specular_factor = 0.0
    light.diffuse_factor = 1.0

    obj = bpy.data.objects.new(name, light)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = scaled_location(location)
    aim_at(obj, target)
    return obj


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def main():
    args = parse_args()
    started = time.perf_counter()

    data_path = os.path.abspath(os.path.expanduser(args.data))
    out_path = os.path.abspath(os.path.expanduser(args.out))
    if os.path.splitext(out_path)[1].lower() != ".png":
        raise ValueError("--out must name a PNG file.")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    data = load_data(data_path)
    n = data["n"]
    matrix = data["matrix"]

    print(
        f"[Hadamard City] {n}x{n}; holder={data['holder']}; "
        f"log10|det|={data['log10_det']}",
        flush=True,
    )

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = args.samples
    scene.eevee.use_raytracing = True
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.film_transparent = False

    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = -0.7

    world = scene.world or bpy.data.worlds.new("Night Studio")
    scene.world = world
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = (*linear_rgb("#07080B"), 1.0)
    background.inputs["Strength"].default_value = 0.16

    graphite = surface_material(
        "Graphite | #101318", "#101318",
        roughness=0.30, metallic=0.25, coat=0.20,
    )
    cyan = glow_material("Cyan Roof Perimeters | #3DF5FF", "#3DF5FF", 2.2)
    amber = glow_material("Amber Plinth Tops | #FFB547", "#FFB547", 1.1)
    ground_mat = surface_material(
        "Near-Black Reflective Ground", "#05070A",
        roughness=0.42, metallic=0.18, coat=0.0,
    )

    # Integral image: exact clipped 5x5 arithmetic means, no wrapping or noise.
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, row in enumerate(matrix):
        row_sum = 0
        for j, value in enumerate(row):
            row_sum += value
            prefix[i + 1][j + 1] = prefix[i][j + 1] + row_sum

    body_vertices, body_faces, body_indices = [], [], []
    cap_vertices, cap_faces, cap_indices = [], [], []
    half_grid = (n - 1) / 2.0
    max_height = 0.0

    for i, row in enumerate(matrix):
        i0, i1 = max(0, i - 2), min(n, i + 3)
        for j, sign in enumerate(row):
            j0, j1 = max(0, j - 2), min(n, j + 3)
            total = (
                prefix[i1][j1] - prefix[i0][j1]
                - prefix[i1][j0] + prefix[i0][j0]
            )
            s = total / ((i1 - i0) * (j1 - j0))
            height = (
                0.9 + 2.6 * (s + 1.0) / 2.0
                if sign == 1 else
                0.12 + 0.2 * (s + 1.0) / 2.0
            )
            max_height = max(max_height, height)

            x = j - half_grid
            y = half_grid - i  # Row zero is at positive Y, at the back.
            thickness = 0.022 if sign == 1 else 0.012
            seam = height - thickness

            # One shared position and seam per cell. No independent cap
            # indexing, offsets, overhangs, or added decorative heights.
            append_box(
                body_vertices, body_faces, body_indices,
                x, y, FOOTPRINT, 0.0, seam,
            )
            if sign == 1:
                append_cyan_roof(
                    cap_vertices, cap_faces, cap_indices,
                    x, y, seam, height,
                )
            else:
                append_box(
                    cap_vertices, cap_faces, cap_indices,
                    x, y, FOOTPRINT, seam, height, slot=1,
                )

    # Explicitly check the cap footprint before creating either object.
    extent = half_grid + FOOTPRINT / 2.0
    if any(
        abs(x) > extent + 1e-9 or abs(y) > extent + 1e-9
        for x, y, z in cap_vertices
    ):
        raise RuntimeError("A roof vertex lies outside the matrix footprint.")

    mesh_object(
        "City | All Blocks",
        body_vertices, body_faces, [graphite], body_indices,
    )
    mesh_object(
        "City | All Rooftops",
        cap_vertices, cap_faces, [cyan, amber, graphite], cap_indices,
    )

    ground_extent = n * 4.0
    mesh_object(
        "Ground",
        [
            (-ground_extent, -ground_extent, 0.0),
            (ground_extent, -ground_extent, 0.0),
            (ground_extent, ground_extent, 0.0),
            (-ground_extent, ground_extent, 0.0),
        ],
        [(0, 1, 2, 3)],
        [ground_mat],
    )

    target = (0.0, 0.0, max_height * 0.45)
    focus = bpy.data.objects.new("City Center | Focus", None)
    scene.collection.objects.link(focus)
    focus.location = scaled_location(target)

    area_light(
        "Cool Back-Left Rim",
        (-n * 0.62, n * 0.48, n * 0.75),
        energy=n * n * 18.0,
        size=n * 0.40,
        color="#B1D9FF",
        target=focus,
    )
    area_light(
        "Restrained Front Fill",
        (n * 0.35, -n * 0.65, n * 0.50),
        energy=n * n * 4.0,
        size=n * 0.75,
        color="#8CABCA",
        target=focus,
    )

    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 92.0
    camera_data.sensor_width = 36.0
    camera_data.sensor_fit = "HORIZONTAL"
    camera_data.clip_start = 0.01

    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    elevation = math.radians(30.0)
    azimuth = math.radians(43.0)
    ce, se = math.cos(elevation), math.sin(elevation)
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    outward = (ce * ca, -ce * sa, se)
    right = (sa, ca, 0.0)
    up = (-se * ca, se * sa, ce)

    aspect = args.res[0] / args.res[1]
    tan_h = camera_data.sensor_width / (2.0 * camera_data.lens)
    tan_v = tan_h / aspect

    # Fit actual geometry, not a fictitious uniform-height bounding box.
    # 80% horizontal occupancy; preserve vertical breathing room at any res.
    distance = 0.0
    for vertices in (body_vertices, cap_vertices):
        for vertex in vertices:
            relative = tuple(vertex[k] - target[k] for k in range(3))
            distance = max(
                distance,
                dot(relative, outward) + max(
                    abs(dot(relative, right)) / (tan_h * 0.80),
                    abs(dot(relative, up)) / (tan_v * 0.84),
                ),
            )

    camera.location = scaled_location(tuple(
        target[k] + outward[k] * distance for k in range(3)
    ))
    camera_data.clip_end = (
        distance + ground_extent * 4.0
    ) * MINIATURE_SCALE
    aim_at(camera, focus)

    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = focus
    camera_data.dof.aperture_fstop = 1.4

    compositor = bpy.data.node_groups.new(
        "Hadamard | Restrained Bloom", "CompositorNodeTree"
    )
    scene.compositing_node_group = compositor
    compositor.interface.new_socket(
        "Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )

    layers = compositor.nodes.new("CompositorNodeRLayers")
    layers.location = (-320, 0)

    bloom = compositor.nodes.new("CompositorNodeGlare")
    bloom.location = (-80, 0)
    bloom.inputs["Type"].default_value = "Bloom"
    bloom.inputs["Quality"].default_value = "High"
    bloom.inputs["Threshold"].default_value = 1.1
    bloom.inputs["Strength"].default_value = 0.12
    bloom.inputs["Size"].default_value = 0.18

    output = compositor.nodes.new("NodeGroupOutput")
    output.location = (180, 0)
    compositor.links.new(layers.outputs["Image"], bloom.inputs["Image"])
    compositor.links.new(bloom.outputs["Image"], output.inputs["Image"])

    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "16"
    scene.render.filepath = out_path

    print(
        f"[Hadamard City] Build: {time.perf_counter() - started:.2f}s",
        flush=True,
    )
    print(
        f"[Hadamard City] Rendering {args.res[0]}x{args.res[1]}, "
        f"{args.samples} samples...",
        flush=True,
    )

    render_started = time.perf_counter()
    bpy.ops.render.render(write_still=True)

    print(
        f"[Hadamard City] Render: {time.perf_counter() - render_started:.2f}s",
        flush=True,
    )
    print(f"[Hadamard City] Wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()

```

The attached image is the current render from this script.

## Art director feedback (fix all of this, keep what works)

Better exposure, but now it reads as a cyan wireframe, not a city:
1) The roof perimeter-only design looks like wire outlines. Make every +1 roof a solid glowing slab: whole top face emissive cyan #3DF5FF at strength ~1.6-2.2; -1 plinth tops solid emissive amber #FFB547 at ~0.9-1.2. Saturated colours, not white.
2) Tower sides are pure black: the city has no volume. Make the body material dark blue-graphite glass (#1A2029, metallic ~0.5, roughness ~0.22) and add a cool rim/key area light high behind-left plus a faint cool fill from the camera side, and raise the world strength a bit (dark blue #0B0F16, ~0.25), so tower faces show gradients and edge highlights.
3) The detached amber slabs outside the grid at the left are still there. The geometry check passes, so they are floor reflection / screen-space artifacts: make the ground plane matte (roughness ~0.7, no metal) and very dark, so no ghost reflections appear.
4) Camera is still too far and too high. Use elevation ~25-28 deg from a corner, lens ~100 mm, move closer so the city fills ~95% of the frame width (corners may be slightly cropped), focus on the centre, fstop ~1.2 so near and far corners clearly blur (tilt-shift miniature look).
Keep data-driven heights, args and single-mesh builds.

Return the full corrected script.

[Attached images: viz/renders/wip/hadamard_v2.png]
