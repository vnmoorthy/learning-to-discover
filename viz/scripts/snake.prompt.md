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
- Lights also have `light.specular_factor` / `light.diffuse_factor` (0..1). A big area light reflecting in a
  glossy floor shows up as a bright rectangle: lower its `specular_factor` (e.g. 0.0-0.15) or move it.
  Objects have `visible_camera`, `visible_glossy`, `visible_shadow` booleans.


## Your current script (previous version)

```python
# Written by gpt-6-astra (OpenAI Responses API), version 2, 2026-11-15 06:34. Prompt: snake.v2.prompt.md
#!/usr/bin/env python3
"""Render the exact JSON snake using Blender 5.2.1 / EEVEE.

Blender -b --factory-startup -P script.py -- \
    --data snake.json --out /absolute/path/snake.png

All mathematical coordinates and record counts come from the JSON.
Numeric constants below are presentation, tessellation, and CLI settings only.
"""

import argparse
import colorsys
import json
import math
import os
import sys
import time

import bpy
from mathutils import Vector


def arguments():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=("still", "turntable"), default="still")
    parser.add_argument("--res", default="1920x1080")
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--frames", type=int, default=192)
    parser.add_argument("--fps", type=int, default=24)
    args = parser.parse_args(argv)

    try:
        args.width, args.height = map(int, args.res.lower().split("x"))
        if min(args.width, args.height, args.samples, args.frames, args.fps) <= 0:
            raise ValueError
    except ValueError:
        parser.error("--res must be WxH; all dimensions and numeric options must be positive.")

    args.data = os.path.abspath(os.path.expanduser(args.data))
    args.out = os.path.abspath(os.path.expanduser(args.out))
    extension = ".mp4" if args.mode == "turntable" else ".png"
    if os.path.splitext(args.out)[1].lower() != extension:
        parser.error(f"--mode {args.mode} requires an {extension} output.")
    if args.mode == "turntable" and (args.width % 2 or args.height % 2):
        parser.error("H.264 output requires even image dimensions.")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    return args


def load_data(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    for key in ("edges", "dimension"):
        if type(data.get(key)) is not int or data[key] <= 0:
            raise ValueError(f"'{key}' must be a positive integer.")

    def points(key):
        rows = data.get(key)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"'{key}' must be a nonempty array.")
        result = []
        for index, row in enumerate(rows):
            if not isinstance(row, list) or len(row) != 3:
                raise ValueError(f"{key}[{index}] must have three coordinates.")
            if any(type(v) not in (int, float) or not math.isfinite(v) for v in row):
                raise ValueError(f"{key}[{index}] contains invalid coordinates.")
            result.append(tuple(float(v) for v in row))
        return result

    path = points("path")
    cube = points("cube_vertices")
    if len(path) != data["edges"] + 1:
        raise ValueError("The path length does not match 'edges' + 1.")
    if len(cube) != 2 ** data["dimension"]:
        raise ValueError("The cube vertex count does not match 'dimension'.")
    if "actions" in data:
        if not isinstance(data["actions"], list) or len(data["actions"]) != data["edges"]:
            raise ValueError("The actions length does not match 'edges'.")
    return data, path, cube


def hex_rgb(text):
    return tuple(int(text[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def srgb_linear(value):
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def linear_rgba(rgb):
    return tuple(srgb_linear(v) for v in rgb) + (1.0,)


def emission_material(name, rgb, strength):
    material = bpy.data.materials.new(name)
    nodes = material.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = linear_rgba(rgb)
    emission.inputs["Strength"].default_value = strength
    output = nodes.new("ShaderNodeOutputMaterial")
    material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material


def gradient_color(start, end, fraction):
    # RGB interpolation otherwise becomes almost neutral in the middle.
    # Preserve its hue progression, but restore interpolated endpoint
    # saturation and value before converting to scene-linear RGB.
    mixed = tuple(a * (1.0 - fraction) + b * fraction for a, b in zip(start, end))
    hue, _, _ = colorsys.rgb_to_hsv(*mixed)
    _, saturation_a, value_a = colorsys.rgb_to_hsv(*start)
    _, saturation_b, value_b = colorsys.rgb_to_hsv(*end)
    return colorsys.hsv_to_rgb(
        hue,
        saturation_a * (1.0 - fraction) + saturation_b * fraction,
        value_a * (1.0 - fraction) + value_b * fraction,
    )


def new_object(name, data=None, parent=None):
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    if parent is not None:
        obj.parent = parent
    return obj


def mesh_object(name, vertices, faces, materials, parent, indices=None, smooth=False):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    for material in materials:
        mesh.materials.append(material)
    if indices is not None:
        mesh.polygons.foreach_set("material_index", indices)
    if smooth:
        for polygon in mesh.polygons:
            polygon.use_smooth = True
    return new_object(name, mesh, parent)


def make_dust(points, radius, material, parent):
    offsets = (
        (radius, 0.0, 0.0), (-radius, 0.0, 0.0),
        (0.0, radius, 0.0), (0.0, -radius, 0.0),
        (0.0, 0.0, radius), (0.0, 0.0, -radius),
    )
    template_faces = (
        (4, 0, 2), (4, 2, 1), (4, 1, 3), (4, 3, 0),
        (5, 2, 0), (5, 1, 2), (5, 3, 1), (5, 0, 3),
    )
    vertices, faces = [], []
    for point in points:
        base = len(vertices)
        vertices.extend(
            tuple(point[axis] + delta[axis] for axis in range(3))
            for delta in offsets
        )
        faces.extend(tuple(base + index for index in face) for face in template_faces)

    return mesh_object(
        "Projected hypercube — all supplied vertices",
        vertices, faces, [material], parent,
    )


def make_markers(points, radius, materials, parent):
    vertices, faces, indices = [], [], []
    rings, sides = 12, 20

    for material_index, point in enumerate(points):
        top = len(vertices)
        vertices.append((point[0], point[1], point[2] + radius))

        for ring in range(1, rings):
            phi = math.pi * ring / rings
            for side in range(sides):
                theta = math.tau * side / sides
                vertices.append((
                    point[0] + radius * math.sin(phi) * math.cos(theta),
                    point[1] + radius * math.sin(phi) * math.sin(theta),
                    point[2] + radius * math.cos(phi),
                ))

        bottom = len(vertices)
        vertices.append((point[0], point[1], point[2] - radius))
        face_start = len(faces)

        for side in range(sides):
            nxt = (side + 1) % sides
            faces.append((top, top + 1 + side, top + 1 + nxt))
            for ring in range(rings - 2):
                upper = top + 1 + ring * sides
                lower = upper + sides
                faces.append((upper + side, lower + side, lower + nxt, upper + nxt))
            last = top + 1 + (rings - 2) * sides
            faces.append((last + side, bottom, last + nxt))

        indices.extend([material_index] * (len(faces) - face_start))

    return mesh_object(
        "Start and end beacons",
        vertices, faces, materials, parent, indices, smooth=True,
    )


def fit_distance(points, outward, right, up, tan_x, tan_y,
                 occupancy_x, occupancy_y, radius, rotating):
    """Perspective support bound, including the full turntable when needed."""
    distance = 0.0
    for axis, tangent, occupancy in (
        (right, tan_x, occupancy_x),
        (up, tan_y, occupancy_y),
    ):
        for sign in (-1.0, 1.0):
            support = outward + axis * (sign / (tangent * occupancy))
            if rotating:
                horizontal = math.hypot(support.x, support.y)
                bound = max(
                    math.hypot(p[0], p[1]) * horizontal + p[2] * support.z
                    for p in points
                )
            else:
                bound = max(support.dot(Vector(p)) for p in points)
            distance = max(distance, bound + radius * support.length)
    return distance


def main():
    args = arguments()
    build_start = time.perf_counter()
    metadata, path_world, cube_world = load_data(args.data)
    print(
        f"[snake] Loaded {metadata['dimension']}D snake: "
        f"{metadata['edges']} edges, {len(cube_world)} cube vertices.",
        flush=True,
    )

    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = args.samples
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"

    # The previous tube was already at 2.8, not above 5. Raising it alone
    # would worsen the pastel highlights. Use moderate scene emission and
    # lower exposure together; bloom is generated before the view transform.
    scene.view_settings.exposure = -1.35

    world = scene.world or bpy.data.worlds.new("Near-black studio")
    scene.world = world
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = linear_rgba(hex_rgb("07080B"))
    background.inputs["Strength"].default_value = 1.0

    all_world = path_world + cube_world
    lo = Vector(tuple(min(p[a] for p in all_world) for a in range(3)))
    hi = Vector(tuple(max(p[a] for p in all_world) for a in range(3)))
    center = (lo + hi) * 0.5
    span = max(hi - lo)
    if span <= 0.0:
        raise ValueError("The supplied projection has no spatial extent.")

    # Local recentering is compensated by the parent translation. Frame 1
    # therefore preserves every supplied world-space coordinate.
    path = [tuple(Vector(p) - center) for p in path_world]
    cube = [tuple(Vector(p) - center) for p in cube_world]
    root = new_object("Snake assembly — vertical turntable")
    root.location = center

    amber = hex_rgb("FFB547")
    cyan = hex_rgb("3DF5FF")

    # Presentation sizes in the projection's supplied coordinate units.
    tube_radius = 0.0115
    dust_radius = 0.012
    marker_radius = 0.045

    curve = bpy.data.curves.new("Exact projected edge path", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = tube_radius
    curve.bevel_resolution = 2

    bands = min(24, metadata["edges"])
    for band in range(bands):
        fraction = band / max(1, bands - 1)
        color = gradient_color(amber, cyan, fraction)
        curve.materials.append(
            emission_material(f"Snake gradient {band:02d}", color, 3.0)
        )

        first = band * metadata["edges"] // bands
        last = (band + 1) * metadata["edges"] // bands
        coordinates = path[first:last + 1]
        spline = curve.splines.new("POLY")
        spline.points.add(len(coordinates) - 1)
        spline.points.foreach_set(
            "co",
            [component for point in coordinates for component in (*point, 1.0)],
        )
        spline.material_index = band

    new_object("The Snake", curve, root)

    # One small octahedron per actual cube vertex, all in a single mesh.
    # Larger projected coverage makes these survive antialiasing and DOF.
    make_dust(
        cube, dust_radius,
        emission_material("Subtle pale cyan-white dust", hex_rgb("BADFE8"), 0.95),
        root,
    )
    make_markers(
        (path[0], path[-1]), marker_radius,
        [
            emission_material("Start — warm amber", amber, 4.5),
            emission_material("End — electric cyan", cyan, 4.5),
        ],
        root,
    )

    # Lower three-quarter angle. Fit the snake separately from its dust
    # envelope so the main structure, not the outermost speck, drives framing.
    outward = Vector((1.25, -1.7, 0.72)).normalized()
    right = Vector((0.0, 0.0, 1.0)).cross(outward).normalized()
    up = outward.cross(right).normalized()

    camera_data = bpy.data.cameras.new("Mathematical discovery — camera")
    camera_data.lens = 80.0
    camera_data.sensor_width = 36.0
    camera_data.sensor_fit = "HORIZONTAL"

    aspect = args.width / args.height
    tan_x = camera_data.sensor_width / (2.0 * camera_data.lens)
    tan_y = tan_x / aspect
    rotating = args.mode == "turntable"

    distance = max(
        fit_distance(
            path, outward, right, up, tan_x, tan_y,
            0.86, 0.80, marker_radius, rotating,
        ),
        fit_distance(
            cube, outward, right, up, tan_x, tan_y,
            0.94, 0.94, dust_radius, rotating,
        ),
    )

    target = new_object("Camera aim")
    target.location = center
    camera = new_object("Camera", camera_data)
    camera.location = center + outward * distance
    tracking = camera.constraints.new("TRACK_TO")
    tracking.target = target
    tracking.track_axis = "TRACK_NEGATIVE_Z"
    tracking.up_axis = "UP_Y"
    camera_data.clip_start = max(tube_radius * 0.1, span * 0.0001)
    camera_data.clip_end = distance + span * 5.0
    scene.camera = camera

    # Identify dense clusters from the data rather than selecting a
    # hardcoded vertex or focusing on the empty center.
    cell = span / 12.0
    bins = {}
    for point in path:
        key = tuple(math.floor(v / cell) for v in point)
        bucket = bins.setdefault(key, [0, Vector((0.0, 0.0, 0.0))])
        bucket[0] += 1
        bucket[1] += Vector(point)

    maximum_density = max(count for count, total in bins.values())
    dense_centers = [
        total / count
        for count, total in bins.values()
        if count >= maximum_density * 0.55
    ]

    # Static camera-space focus plane: it does not follow the initial
    # cluster around to the back during a turntable or pump between clusters.
    focus_position = max(dense_centers, key=lambda p: p.dot(outward))
    focus = new_object("Focus — foreground dense cluster")
    focus.location = center + focus_position
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = focus
    camera_data.dof.aperture_fstop = 1.6

    compositor = bpy.data.node_groups.new("Controlled saturated bloom", "CompositorNodeTree")
    scene.compositing_node_group = compositor
    compositor.interface.new_socket(
        "Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    render_layers = compositor.nodes.new("CompositorNodeRLayers")
    bloom = compositor.nodes.new("CompositorNodeGlare")
    bloom.inputs["Type"].default_value = "Bloom"
    bloom.inputs["Quality"].default_value = "High"
    bloom.inputs["Threshold"].default_value = 0.85
    bloom.inputs["Strength"].default_value = 0.55
    bloom.inputs["Size"].default_value = 0.24
    output = compositor.nodes.new("NodeGroupOutput")
    compositor.links.new(render_layers.outputs["Image"], bloom.inputs["Image"])
    compositor.links.new(bloom.outputs["Image"], output.inputs["Image"])

    scene.render.filepath = args.out
    scene.render.fps = args.fps

    if rotating:
        # Every rendered integer frame receives its exact angular position.
        # This avoids accessing Blender 5.x layered-action FCurves.
        # N+1 closes the loop but is deliberately not rendered.
        for step in range(args.frames + 1):
            root.rotation_euler = (0.0, 0.0, math.tau * step / args.frames)
            root.keyframe_insert(data_path="rotation_euler", frame=step + 1)

        scene.render.image_settings.media_type = "VIDEO"
        scene.render.image_settings.file_format = "FFMPEG"
        ffmpeg = scene.render.ffmpeg
        ffmpeg.format = "MPEG4"
        ffmpeg.codec = "H264"
        ffmpeg.constant_rate_factor = "HIGH"
        ffmpeg.ffmpeg_preset = "GOOD"
        scene.frame_start = 1
        scene.frame_end = args.frames
    else:
        scene.render.image_settings.file_format = "PNG"

    scene.frame_set(1)
    print(f"[snake] Build: {time.perf_counter() - build_start:.2f}s", flush=True)
    print(f"[snake] Rendering {args.mode} to {args.out}", flush=True)

    render_start = time.perf_counter()
    if rotating:
        bpy.ops.render.render(animation=True)
    else:
        bpy.ops.render.render(write_still=True)

    print(f"[snake] Render: {time.perf_counter() - render_start:.2f}s", flush=True)
    print(f"[snake] Written: {args.out}", flush=True)


if __name__ == "__main__":
    main()

```

The attached image is the current render from this script.

## Art director feedback (fix all of this, keep what works)

Much better. Remaining:
1) The colour gradient goes through green in the middle (RGB interpolation of amber -> cyan). Interpolate amber #FFB547 -> soft warm white (#FFF1DC) at the midpoint -> cyan #3DF5FF instead (two-segment gradient), so no green/olive appears anywhere.
2) Fill more of the frame: the structure should span ~85% of the frame height and ~70% of the width. Lens ~50-60 mm with the camera closer, so there is real perspective depth, and stronger depth of field (fstop ~1.4) focused on the nearest cluster so the far clusters melt into bokeh.
3) Hypercube vertex dust: keep it subtle but a bit more visible and spread (it currently clings to the tube). Fine.
Keep args, turntable mode and the single curve object.

Return the full corrected script.

[Attached images: viz/renders/wip/snake_v2.png]
