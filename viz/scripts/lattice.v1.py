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
