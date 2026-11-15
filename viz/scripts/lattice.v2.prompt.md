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
- Lights also have `light.specular_factor` / `light.diffuse_factor` (0..1). A big area light reflecting in a
  glossy floor shows up as a bright rectangle: lower its `specular_factor` (e.g. 0.0-0.15) or move it.
  Objects have `visible_camera`, `visible_glossy`, `visible_shadow` booleans.


## Your current script (previous version)

```python
# Written by gpt-6-astra (OpenAI Responses API), version 1, 2026-11-15 06:29. Prompt: lattice.v1.prompt.md
#!/usr/bin/env python3
"""
The Lattice — Blender 5.2.1 / EEVEE

Blender -b --factory-startup -P script.py -- \
    --data lattice.json --out /absolute/path/hero.png

Blender -b --factory-startup -P script.py -- \
    --data lattice.json --out /absolute/path/orbit.mp4 \
    --mode loop --res 1280x720 --samples 8 --frames 192 --fps 24

All mathematical content comes from --data. Numeric constants below control
presentation, geometry tessellation, validation tolerances, or CLI defaults;
they never substitute for search results.
"""

import argparse
import json
import math
import os
import sys
import time

import bpy


def progress(message):
    print("[Lattice] " + message, flush=True)


def positive_int(text):
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    return value


def resolution(text):
    try:
        width, height = text.lower().split("x")
        return positive_int(width), positive_int(height)
    except (ValueError, argparse.ArgumentTypeError):
        raise argparse.ArgumentTypeError("Resolution must be WxH, e.g. 1920x1080.")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=("still", "loop"), default="still")
    parser.add_argument("--res", type=resolution, default=(1920, 1080))
    parser.add_argument("--samples", type=positive_int, default=64)
    parser.add_argument("--frames", type=positive_int, default=192)
    parser.add_argument("--fps", type=positive_int, default=24)
    args = parser.parse_args(argv)
    args.data = os.path.abspath(os.path.expanduser(args.data))
    args.out = os.path.abspath(os.path.expanduser(args.out))
    expected = ".png" if args.mode == "still" else ".mp4"
    if os.path.splitext(args.out)[1].lower() != expected:
        parser.error("--out must end in " + expected)
    if args.mode == "loop" and args.frames < 2:
        parser.error("A loop requires at least two frames.")
    return args


def load_data(path):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    n = data["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("'n' must be an integer greater than one.")

    def grid_point(value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("Invalid grid coordinate.")
        if any(isinstance(v, bool) or not isinstance(v, int) for v in value):
            raise ValueError("Grid coordinates must be integers.")
        if any(v < 0 or v >= n for v in value):
            raise ValueError("Grid coordinate is outside the supplied lattice.")
        return tuple(value)

    points = [grid_point(p) for p in data["points"]]
    chosen = set(points)
    if len(chosen) != len(points):
        raise ValueError("Duplicate chosen points.")
    if data["count"] != len(points):
        raise ValueError("'count' does not match 'points'.")
    lines = data["violated_lines"]
    if data["violated"] != len(lines):
        raise ValueError("'violated' does not match 'violated_lines'.")

    conflicts = set()
    for index, line in enumerate(lines):
        a, b = grid_point(line["a"]), grid_point(line["b"])
        if a == b or a not in chosen or b not in chosen:
            raise ValueError(f"Invalid defining points on line {index}.")
        on = [grid_point(p) for p in line["on"]]
        if len(set(on)) != len(on) or len(on) != line["m"] or line["m"] < 3:
            raise ValueError(f"Invalid multiplicity on line {index}.")

        dx, dy = b[0] - a[0], b[1] - a[1]
        actual = {
            p for p in chosen
            if (p[0] - a[0]) * dy == (p[1] - a[1]) * dx
        }
        if set(on) != actual:
            raise ValueError(f"'on' is inconsistent with chosen points on line {index}.")

        ends = line["ends"]
        if len(ends) != 2:
            raise ValueError(f"Invalid clipped endpoints on line {index}.")
        tolerance = 1.0e-5 * max(1, n)
        for endpoint in ends:
            if len(endpoint) != 2:
                raise ValueError(f"Invalid endpoint on line {index}.")
            x, y = map(float, endpoint)
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError("Non-finite endpoint.")
            if not (-tolerance <= x <= n - 1 + tolerance and
                    -tolerance <= y <= n - 1 + tolerance):
                raise ValueError(f"Endpoint outside the lattice on line {index}.")
            distance = abs((x - a[0]) * dy - (y - a[1]) * dx) / math.hypot(dx, dy)
            if distance > tolerance:
                raise ValueError(f"Endpoint is not on line {index}.")
        if math.dist(ends[0], ends[1]) <= tolerance:
            raise ValueError(f"Degenerate beam on line {index}.")
        conflicts.update(on)

    # record_points is intentionally neither inspected nor rendered.
    return data, points, chosen, conflicts


def linear_color(hex_color):
    values = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]

    def convert(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return tuple(convert(c) for c in values) + (1.0,)


def surface_material(name, color, roughness, metallic=0.0, emission=0.0):
    material = bpy.data.materials.new(name)
    bsdf = material.node_tree.nodes["Principled BSDF"]
    rgba = linear_color(color)
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Specular IOR Level"].default_value = 0.45
    if emission:
        bsdf.inputs["Emission Color"].default_value = rgba
        bsdf.inputs["Emission Strength"].default_value = emission
    return material


def emission_material(name, color, strength):
    material = bpy.data.materials.new(name)
    nodes = material.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = linear_color(color)
    emission.inputs["Strength"].default_value = strength
    output = nodes.new("ShaderNodeOutputMaterial")
    material.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
    return material


class MeshBatch:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.material_indices = []

    def box(self, x, y, width, z0, z1, material=0):
        start = len(self.vertices)
        half = width * 0.5
        self.vertices.extend([
            (x - half, y - half, z0),
            (x + half, y - half, z0),
            (x + half, y + half, z0),
            (x - half, y + half, z0),
            (x - half, y - half, z1),
            (x + half, y - half, z1),
            (x + half, y + half, z1),
            (x - half, y + half, z1),
        ])
        for face in (
            (0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 6, 5),
            (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7),
        ):
            self.faces.append(tuple(start + i for i in face))
            self.material_indices.append(material)

    def beam(self, a, b, height, radius, sides=6):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        ux, uy = -dy / length, dx / length
        start = len(self.vertices)
        for endpoint in (a, b):
            for i in range(sides):
                angle = math.tau * i / sides
                lateral = radius * math.cos(angle)
                self.vertices.append((
                    endpoint[0] + ux * lateral,
                    endpoint[1] + uy * lateral,
                    height + radius * math.sin(angle),
                ))
        self.faces.append(tuple(start + i for i in reversed(range(sides))))
        self.faces.append(tuple(start + sides + i for i in range(sides)))
        self.material_indices.extend((0, 0))
        for i in range(sides):
            j = (i + 1) % sides
            self.faces.append((start + i, start + j,
                               start + sides + j, start + sides + i))
            self.material_indices.append(0)

    def create(self, name, materials, parent):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        mesh.from_pydata(self.vertices, [], self.faces)
        for material in materials:
            mesh.materials.append(material)
        mesh.polygons.foreach_set("material_index", self.material_indices)
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.parent = parent
        return obj


def empty(name, parent=None, location=(0.0, 0.0, 0.0)):
    obj = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = location
    return obj


def aim_at(obj, target):
    constraint = obj.constraints.new("TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"


def area_light(name, parent, location, target, color, energy, size):
    data = bpy.data.lights.new(name, type="AREA")
    data.energy = energy
    data.size = size
    data.color = linear_color(color)[:3]
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = location
    aim_at(obj, target)
    return obj


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def fitted_distance(span, azimuths, elevation, lens, aspect, target_z):
    # Fit the actual square, including its top corners, not an invented dataset.
    tan_x = 36.0 / (2.0 * lens)
    tan_y = tan_x / aspect
    half = span * 0.5 + 0.18
    corners = [
        (x, y, z - target_z)
        for x in (-half, half)
        for y in (-half, half)
        for z in (0.0, 1.16)
    ]
    distance = 0.0
    ce, se = math.cos(elevation), math.sin(elevation)
    for azimuth in azimuths:
        ca, sa = math.cos(azimuth), math.sin(azimuth)
        outward = (ce * ca, ce * sa, se)
        right = (-sa, ca, 0.0)
        up = (-se * ca, -se * sa, ce)
        for corner in corners:
            required = dot(corner, outward) + max(
                abs(dot(corner, right)) / tan_x,
                abs(dot(corner, up)) / tan_y,
            )
            distance = max(distance, required)
    return distance * 1.10


def build_scene(args, data, points, chosen, conflicts):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = args.samples
    # Still-only screen tracing adds floor reflections without burdening the loop.
    scene.eevee.use_raytracing = args.mode == "still"
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.film_transparent = False
    scene.render.fps = args.fps
    scene.render.fps_base = 1.0
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = -0.20

    world = scene.world or bpy.data.worlds.new("Dark_Studio")
    scene.world = world
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = linear_color("07080B")
    background.inputs["Strength"].default_value = 0.055

    n = data["n"]
    span = float(n - 1)
    center = span * 0.5

    # Geometry retains unit grid spacing in local coordinates. A uniform stage
    # scale gives a product-film-sized set, including lights and camera positions.
    stage_scale = 0.20
    stage = empty("Stage_Grid_Units")
    stage.scale = (stage_scale,) * 3

    graphite = surface_material("Graphite", "14161C", 0.31, metallic=0.32)
    floor_material = surface_material("Obsidian_Floor", "090B10", 0.25, metallic=0.22)
    cyan = surface_material("Chosen_Cyan", "3DF5FF", 0.23, emission=2.7)
    amber = surface_material("Conflict_Amber", "FFB547", 0.23, emission=2.7)
    cyan_cap = emission_material("Cyan_Caps", "3DF5FF", 8.0)
    amber_cap = emission_material("Amber_Caps", "FFB547", 8.0)
    red = emission_material("Violation_Red", "FF2A3A", 5.0)

    bases = MeshBatch()
    for y in range(n):
        for x in range(n):
            # Stable coordinate hash: visual surface variation only.
            h = ((x * 73856093) ^ (y * 19349663)) & 0xFFFFFFFF
            h ^= h >> 13
            jitter = (h & 65535) / 65535.0
            bases.box(x - center, y - center, 0.32, 0.0,
                      0.18 + 0.03 * jitter)
    bases.create("Complete_Lattice", [graphite], stage)

    pillars, caps = MeshBatch(), MeshBatch()
    for point in points:
        x, y = point[0] - center, point[1] - center
        material = 1 if point in conflicts else 0
        pillars.box(x, y, 0.32, 0.18, 1.10, material)
        caps.box(x, y, 0.345, 1.10, 1.155, material)
    if points:
        pillars.create("Chosen_Pillars", [cyan, amber], stage)
        caps.create("Chosen_Caps", [cyan_cap, amber_cap], stage)

    beams = MeshBatch()
    for line in data["violated_lines"]:
        a, b = line["ends"]
        beams.beam((a[0] - center, a[1] - center),
                   (b[0] - center, b[1] - center),
                   height=1.12, radius=0.025)
    if data["violated_lines"]:
        beams.create("All_Violated_Lines", [red], stage)

    floor = MeshBatch()
    extent = max(span, 1.0) * 100.0
    floor.vertices = [
        (-extent, -extent, -0.012), (extent, -extent, -0.012),
        (extent, extent, -0.012), (-extent, extent, -0.012),
    ]
    floor.faces = [(0, 1, 2, 3)]
    floor.material_indices = [0]
    floor.create("Horizonless_Studio_Floor", [floor_material], stage)

    target_z = 0.55
    target = empty("Camera_Target", stage, (0.0, 0.0, target_z))
    light_target = empty("Light_Target", stage, (0.0, 0.0, 0.0))

    area_light(
        "Cool_Back_Left_Key", stage,
        (-span * 0.48, span * 0.42, span * 0.62),
        light_target, "B8D8FF",
        energy=span * span * 18.0 * stage_scale ** 2,
        size=span * 0.58,
    )
    area_light(
        "Faint_Warm_Fill", stage,
        (span * 0.62, -span * 0.08, span * 0.28),
        light_target, "FFD7AD",
        energy=span * span * 1.8 * stage_scale ** 2,
        size=span * 0.50,
    )

    azimuth = math.radians(-55.0)
    elevation = math.radians(14.0)
    lens = 58.0
    aspect = args.res[0] / args.res[1]
    if args.mode == "loop":
        azimuths = [azimuth + math.tau * i / args.frames
                    for i in range(args.frames)]
    else:
        azimuths = [azimuth]
    distance = fitted_distance(
        span, azimuths, elevation, lens, aspect, target_z
    )

    orbit = empty("Camera_Orbit", stage, (0.0, 0.0, target_z))
    orbit.rotation_euler[2] = azimuth
    camera_data = bpy.data.cameras.new("Hero_Camera")
    camera_data.lens = lens
    camera_data.sensor_width = 36.0
    camera_data.sensor_fit = "HORIZONTAL"
    camera_data.clip_start = 0.02
    camera_data.clip_end = max(span, 1.0) * stage_scale * 300.0
    camera = bpy.data.objects.new("Hero_Camera", camera_data)
    scene.collection.objects.link(camera)
    camera.parent = orbit
    camera.location = (
        distance * math.cos(elevation), 0.0,
        distance * math.sin(elevation),
    )
    aim_at(camera, target)
    scene.camera = camera

    focus_location = (0.0, 0.0, 1.10)
    if args.mode == "still" and points:
        # Prefer a real conflict cluster in the near third of the lattice.
        candidates = sorted(conflicts) if conflicts else points
        forward = (math.cos(azimuth), math.sin(azimuth))
        right = (-forward[1], forward[0])
        desired = (
            center + span * (forward[0] / 6.0 - right[0] / 7.0),
            center + span * (forward[1] / 6.0 - right[1] / 7.0),
        )
        radius_squared = max(span * 0.075, 1.0) ** 2

        def focus_score(point):
            proximity = (
                (point[0] - desired[0]) ** 2 +
                (point[1] - desired[1]) ** 2
            ) / max(span * span, 1.0)
            neighbors = sum(
                (point[0] - q[0]) ** 2 + (point[1] - q[1]) ** 2
                <= radius_squared for q in candidates
            )
            return proximity - 0.0015 * neighbors

        focus_point = min(candidates, key=focus_score)
        focus_location = (
            focus_point[0] - center, focus_point[1] - center, 1.12
        )

    focus = empty("Depth_Of_Field_Focus", stage, focus_location)
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = focus
    camera_data.dof.aperture_fstop = 2.2

    if args.mode == "loop":
        scene.frame_start = 1
        scene.frame_end = args.frames
        # Every rendered frame has an exact angular sample. This avoids any
        # dependency on the layered Action/F-Curve API or Bezier interpolation.
        for frame in range(1, args.frames + 2):
            orbit.rotation_euler[2] = (
                azimuth + math.tau * (frame - 1) / args.frames
            )
            orbit.keyframe_insert(
                data_path="rotation_euler", index=2, frame=frame
            )

    compositor = bpy.data.node_groups.new("Lattice_Compositor", "CompositorNodeTree")
    scene.compositing_node_group = compositor
    compositor.interface.new_socket(
        "Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    render_layers = compositor.nodes.new("CompositorNodeRLayers")
    glare = compositor.nodes.new("CompositorNodeGlare")
    glare.inputs["Type"].default_value = "Bloom"
    glare.inputs["Quality"].default_value = "High"
    glare.inputs["Threshold"].default_value = 1.2
    glare.inputs["Strength"].default_value = 0.32
    glare.inputs["Size"].default_value = 0.36
    output = compositor.nodes.new("NodeGroupOutput")
    compositor.links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    compositor.links.new(glare.outputs["Image"], output.inputs["Image"])

    scene.frame_set(1)
    return scene


def main():
    args = parse_args()
    started = time.perf_counter()
    data, points, chosen, conflicts = load_data(args.data)
    progress(
        f"Loaded {data['n']}×{data['n']} grid; "
        f"{data['count']} chosen; {data['violated']} violated lines."
    )

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    scene = build_scene(args, data, points, chosen, conflicts)
    scene.render.filepath = args.out
    scene.render.use_file_extension = True

    if args.mode == "still":
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGB"
        scene.render.image_settings.color_depth = "8"
    else:
        images = scene.render.image_settings
        images.media_type = "VIDEO"
        images.file_format = "FFMPEG"
        ffmpeg = scene.render.ffmpeg
        ffmpeg.format = "MPEG4"
        ffmpeg.codec = "H264"
        ffmpeg.constant_rate_factor = "HIGH"
        ffmpeg.ffmpeg_preset = "GOOD"

    progress(f"Build time: {time.perf_counter() - started:.2f}s")
    progress(f"Rendering {args.mode} to {args.out}")
    render_started = time.perf_counter()

    if args.mode == "still":
        bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)

    progress(f"Render time: {time.perf_counter() - render_started:.2f}s")
    if not os.path.isfile(args.out):
        raise RuntimeError("Rendering completed, but the requested output file is missing.")
    progress("Output written successfully.")


if __name__ == "__main__":
    main()

```

## Blender output (tail)

```
[Lattice] Loaded 75×75 grid; 150 chosen; 122 violated lines.
[Lattice] Build time: 0.25s
[Lattice] Rendering still to <repo>/viz/renders/wip/lattice_v1.png
01:38.466  render           | Saved: '<repo>/viz/renders/wip/lattice_v1.png'
[Lattice] Render time: 95.95s
[Lattice] Output written successfully.
Blender 5.2.1 LTS (hash 9e2066aef7ef built 2026-08-25 01:35:57)

Blender quit

```

The attached image is the current render from this script.

## Art director feedback (fix all of this, keep what works)

1) A big pale/white rectangular glow appears on the floor under the lattice (reflection of the cool key area light in the glossy floor). Remove it: set the key light specular_factor to ~0.05 and/or move it so no light reflection is visible; the floor should read as near-black with only the faint reflections of the glowing pillars and beams.
2) Framing is too distant: the lattice is a small plate in the middle of a black frame. I want a low cinematic shot INSIDE the field: camera elevation ~8-12 degrees, closer (do not fit the whole lattice in frame for the still: the near corner/edges can leave the frame), lens ~65-85 mm, field receding toward the top third of the frame and dissolving into darkness/DOF bokeh. The lattice should fill the full width of the frame. Depth of field must be clearly visible (fstop ~1.4-2.0), focused on a bright cluster about 35% into the field.
3) Colour coding: 136 of the 150 chosen points lie on some violated line, so almost everything is amber and the cyan never shows. New rule (data-driven): count for every chosen point how many violated lines pass through it (k = number of lines whose "on" list contains it). k <= 3 -> cyan #3DF5FF; k >= 4 -> amber #FFB547 (the hot spots where the solver is stuck, ~36 points). Make chosen pillars glow more (they read too dim/small): emission strong enough to bloom, slightly taller (~1.4) and with a bright cap.
4) The red beams are a dense red mess that dominates the image. Make them much more subtle: radius ~0.012-0.015, emission ~1.5-2.5, colour #FF2A3A, so they read as fine laser threads and the cyan/amber points dominate. Beams should still be visible across the field.
5) The non-chosen pillar field should catch a bit more rim light so the fine texture of 5625 tiny pillars reads (subtle specular highlights), without washing out. Keep everything else (single-mesh builds, loop mode, args).
6) For loop mode keep the orbit but use the same low elevation and a distance where the whole lattice stays roughly in frame during the orbit (slightly cropped is fine).

Return the full corrected script.

[Attached images: viz/renders/wip/lattice_v1.png]
