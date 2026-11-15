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
- Lights also have `light.specular_factor` / `light.diffuse_factor` (0..1). A big area light reflecting in a
  glossy floor shows up as a bright rectangle: lower its `specular_factor` (e.g. 0.0-0.15) or move it.
  Objects have `visible_camera`, `visible_glossy`, `visible_shadow` booleans.


## Your current script (previous version)

```python
# Written by gpt-6-astra (OpenAI Responses API), version 1, 2026-11-15 06:29. Prompt: hadamard_city.v1.prompt.md
#!/usr/bin/env python3
"""Hadamard City — render a supplied ±1 record matrix with Blender EEVEE."""

import argparse
import json
import math
import os
import sys
import time

import bpy


def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    return value


def resolution(value):
    try:
        width, height = value.lower().split("x")
        return positive_int(width), positive_int(height)
    except (ValueError, argparse.ArgumentTypeError):
        raise argparse.ArgumentTypeError("Resolution must be WxH, for example 1920x1080.")


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
        raise ValueError("JSON 'n' must be a positive integer.")
    if not isinstance(matrix, list) or len(matrix) != n:
        raise ValueError("JSON 'matrix' must contain exactly n rows.")

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"Matrix row {i} must contain exactly n entries.")
        for j, value in enumerate(row):
            if type(value) not in (int, float) or value not in (-1, 1):
                raise ValueError(f"Matrix entry ({i}, {j}) is not exactly +1 or -1.")

    log_det = data.get("log10_det")
    if type(log_det) not in (int, float) or not math.isfinite(log_det):
        raise ValueError("JSON 'log10_det' must be a finite number.")
    if not isinstance(data.get("holder"), str):
        raise ValueError("JSON 'holder' must be a string.")

    return data


def linear_color(hex_color):
    """Convert specified display sRGB colors to Blender's linear RGB."""
    color = hex_color.lstrip("#")
    rgb = [int(color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]

    def decode(x):
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

    return tuple(decode(x) for x in rgb)


def material(name, hex_color, roughness, metallic=0.0,
             emission_strength=0.0, coat=0.0):
    mat = bpy.data.materials.new(name)
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    color = (*linear_color(hex_color), 1.0)
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = coat
    if emission_strength:
        bsdf.inputs["Emission Color"].default_value = color
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def append_box(vertices, faces, indices, x, y, width, z_bottom, z_top, slot=0):
    start = len(vertices)
    r = width * 0.5
    vertices.extend([
        (x - r, y - r, z_bottom),
        (x + r, y - r, z_bottom),
        (x + r, y + r, z_bottom),
        (x - r, y + r, z_bottom),
        (x - r, y - r, z_top),
        (x + r, y - r, z_top),
        (x + r, y + r, z_top),
        (x - r, y + r, z_top),
    ])
    for face in (
        (3, 2, 1, 0),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
        (4, 5, 6, 7),
    ):
        faces.append(tuple(start + v for v in face))
        indices.append(slot)


def mesh_object(name, vertices, faces, materials, indices=None):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    mesh.from_pydata(vertices, [], faces)
    for mat in materials:
        mesh.materials.append(mat)
    if indices is not None:
        mesh.polygons.foreach_set("material_index", indices)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def empty(name, location):
    obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    return obj


def aim_at(obj, target):
    constraint = obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"


def area_light(name, location, energy, size, color, target):
    light = bpy.data.lights.new(name, type="AREA")
    light.energy = energy
    light.size = size
    light.color = linear_color(color)
    obj = bpy.data.objects.new(name, light)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
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
        raise ValueError("--out must name a .png file.")
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

    world = scene.world or bpy.data.worlds.new("Night Studio")
    scene.world = world
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = (*linear_color("#07080B"), 1.0)
    background.inputs["Strength"].default_value = 0.18

    graphite = material(
        "Architectural Graphite | #101318", "#101318",
        roughness=0.30, metallic=0.38, coat=0.28,
    )
    cyan = material(
        "Positive | Cyan Roof", "#3DF5FF",
        roughness=0.24, metallic=0.12, emission_strength=3.4, coat=0.15,
    )
    amber = material(
        "Negative | Amber Roof", "#FFB547",
        roughness=0.33, metallic=0.12, emission_strength=0.60,
    )
    ground_mat = material(
        "Polished Charcoal Ground", "#090C12",
        roughness=0.27, metallic=0.42, coat=0.20,
    )

    # All mathematical values come from the JSON. Numerical constants below
    # are the brief's height mapping, neighborhood definition, or art direction.
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, row in enumerate(matrix):
        row_sum = 0
        for j, value in enumerate(row):
            row_sum += value
            prefix[i + 1][j + 1] = prefix[i][j + 1] + row_sum

    body_vertices, body_faces, body_indices = [], [], []
    cap_vertices, cap_faces, cap_indices = [], [], []
    half_grid = (n - 1) * 0.5
    max_height = 0.0

    for i, row in enumerate(matrix):
        i0, i1 = max(0, i - 2), min(n, i + 3)
        for j, sign in enumerate(row):
            j0, j1 = max(0, j - 2), min(n, j + 3)
            neighborhood_sum = (
                prefix[i1][j1] - prefix[i0][j1]
                - prefix[i1][j0] + prefix[i0][j0]
            )
            agreement = neighborhood_sum / ((i1 - i0) * (j1 - j0))
            normalized = (agreement + 1.0) / 2.0
            height = (
                0.9 + 2.6 * normalized
                if sign == 1 else
                0.12 + 0.2 * normalized
            )
            max_height = max(max_height, height)

            x = j - half_grid
            y = half_grid - i  # Row zero is at the back, on positive Y.
            cap_thickness = 0.026 if sign == 1 else 0.012

            # Caps occupy the final slice of h: no decorative added height.
            append_box(
                body_vertices, body_faces, body_indices,
                x, y, 0.86, 0.0, height - cap_thickness,
            )
            append_box(
                cap_vertices, cap_faces, cap_indices,
                x, y, 0.86, height - cap_thickness, height,
                slot=0 if sign == 1 else 1,
            )

    mesh_object(
        "City | All Data Blocks",
        body_vertices, body_faces, [graphite], body_indices,
    )
    mesh_object(
        "City | All Sign Caps",
        cap_vertices, cap_faces, [cyan, amber], cap_indices,
    )

    ground_extent = n * 4.0
    mesh_object(
        "Ground",
        [
            (-ground_extent, -ground_extent, -0.025),
            (ground_extent, -ground_extent, -0.025),
            (ground_extent, ground_extent, -0.025),
            (-ground_extent, ground_extent, -0.025),
        ],
        [(0, 1, 2, 3)],
        [ground_mat],
    )

    focus = empty("City Center | Focus", (0.0, 0.0, max_height * 0.38))

    # Broad reflections reveal graphite sidewalls without washing out the caps.
    area_light(
        "Cool Back-Left Softbox",
        (-n * 0.58, n * 0.42, n * 1.10),
        energy=n * n * 12.0,
        size=n * 0.72,
        color="#B1D9FF",
        target=focus,
    )
    area_light(
        "Subtle Front Fill",
        (n * 0.48, -n * 0.72, n * 0.60),
        energy=n * n * 2.4,
        size=n * 0.62,
        color="#789DBB",
        target=focus,
    )

    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 70.0
    camera_data.sensor_width = 36.0
    camera_data.sensor_fit = "HORIZONTAL"
    camera_data.clip_start = 0.1

    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    elevation = math.radians(40.0)
    azimuth = math.radians(43.0)
    ce, se = math.cos(elevation), math.sin(elevation)
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    outward = (ce * ca, -ce * sa, se)
    right = (sa, ca, 0.0)
    up = (-se * ca, se * sa, ce)
    target = tuple(focus.location)

    # Fit the full data envelope analytically, including perspective depth.
    aspect = args.res[0] / args.res[1]
    tan_half_horizontal = camera_data.sensor_width / (2.0 * camera_data.lens)
    tan_half_vertical = tan_half_horizontal / aspect
    frame_fill = 0.88
    extent = half_grid + 0.43
    distance = 0.0

    for x in (-extent, extent):
        for y in (-extent, extent):
            for z in (0.0, max_height):
                relative = (x - target[0], y - target[1], z - target[2])
                required = dot(relative, outward) + max(
                    abs(dot(relative, right)) / (tan_half_horizontal * frame_fill),
                    abs(dot(relative, up)) / (tan_half_vertical * frame_fill),
                )
                distance = max(distance, required)

    camera.location = tuple(
        target[k] + outward[k] * distance for k in range(3)
    )
    camera_data.clip_end = distance + ground_extent * 4.0
    aim_at(camera, focus)
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = focus
    camera_data.dof.aperture_fstop = 1.6

    compositor = bpy.data.node_groups.new("Hadamard | Bloom", "CompositorNodeTree")
    scene.compositing_node_group = compositor
    compositor.interface.new_socket(
        "Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )

    render_layers = compositor.nodes.new("CompositorNodeRLayers")
    render_layers.location = (-320, 0)
    bloom = compositor.nodes.new("CompositorNodeGlare")
    bloom.location = (-80, 0)
    bloom.inputs["Type"].default_value = "Bloom"
    bloom.inputs["Quality"].default_value = "High"
    bloom.inputs["Threshold"].default_value = 0.8
    bloom.inputs["Strength"].default_value = 0.65
    bloom.inputs["Size"].default_value = 0.35

    output = compositor.nodes.new("NodeGroupOutput")
    output.location = (180, 0)
    compositor.links.new(render_layers.outputs["Image"], bloom.inputs["Image"])
    compositor.links.new(bloom.outputs["Image"], output.inputs["Image"])

    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "16"
    scene.render.filepath = out_path

    print(f"[Hadamard City] Build: {time.perf_counter() - started:.2f}s", flush=True)
    print(f"[Hadamard City] Rendering {args.res[0]}x{args.res[1]}...", flush=True)

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

## Blender output (tail)

```
[Hadamard City] 51x51; holder=kgrey; log10|det|=43.33745596194037
[Hadamard City] Build: 0.20s
[Hadamard City] Rendering 1280x720...
00:43.908  render           | Saved: '<repo>/viz/renders/wip/hadamard_v1.png'
[Hadamard City] Render: 41.42s
[Hadamard City] Wrote <repo>/viz/renders/wip/hadamard_v1.png
Blender 5.2.1 LTS (hash 9e2066aef7ef built 2026-08-25 01:35:57)

Blender quit

```

The attached image is the current render from this script.

## Art director feedback (fix all of this, keep what works)

1) Massively over-exposed: the cyan caps blow out to white and the whole city reads as a flat glowing pixel map. Reduce cap emission a lot (cyan caps ~2-3, amber ~1-1.5) and lower glare strength so the dark glass tower sides and the height differences are clearly visible; caps should look like thin glowing roof slabs / rooftop light strips, not solid white cubes. Colours must stay saturated cyan and warm amber, not white.
2) The -1 plinths look like flat brown floor tiles. Make their tops a thin dim warm amber glow (emissive, saturated #FFB547) so the sign pattern reads like city lights at night.
3) Bug: some amber slabs float detached outside the grid on the left edge. Every cap must sit exactly on top of its own block; nothing outside the 51x51 footprint.
4) Bug: a pale rectangle (reflection/shadow artifact) shows under the city on the floor. Remove it (light specular_factor low, or move the light, and keep the floor near-black).
5) Camera: more cinematic. Lower elevation (~28-32 degrees) from a corner, lens ~85-100 mm, city filling ~80% of frame width so the skyline relief is visible, strong tilt-shift DOF (fstop ~1.2-1.6) focused on the city centre so the near and far corners blur.
6) Add a subtle cool rim light so tower edges catch thin highlights. Keep single-mesh builds and args.

Return the full corrected script.

[Attached images: viz/renders/wip/hadamard_v1.png]
