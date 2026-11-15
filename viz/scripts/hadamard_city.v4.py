# Written by gpt-6-astra (OpenAI Responses API), version 4, 2026-11-15 06:39. Prompt: hadamard_city.v4.prompt.md
#!/usr/bin/env python3
"""Render Hadamard City with Blender 5.2.1 / EEVEE.

Usage:
    Blender -b --factory-startup -P script.py -- \
        --data /absolute/path/matrix.json \
        --out /absolute/path/hadamard_city.png \
        --res 1920x1080 --samples 64
"""

import argparse
import json
import math
import os
import sys
import time

import bpy


# Art-direction constants, not matrix data.
# Mesh-local spacing remains exactly one unit. Uniform scene scaling gives
# the camera a miniature depth of field without changing city proportions.
MINIATURE_SCALE = 0.04
FOOTPRINT = 0.86


def positive_int(text):
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected a positive integer.") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    return value


def resolution(text):
    try:
        width, height = text.lower().split("x")
        return positive_int(width), positive_int(height)
    except (ValueError, argparse.ArgumentTypeError) as exc:
        raise argparse.ArgumentTypeError("Resolution must be WxH.") from exc


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

    if not isinstance(data, dict):
        raise ValueError("The JSON root must be an object.")

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
    srgb = [int(text[k:k + 2], 16) / 255.0 for k in (0, 2, 4)]
    return tuple(
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in srgb
    )


def rgba(hex_color):
    return (*linear_rgb(hex_color), 1.0)


def surface_material(name, color, roughness, metallic, coat, specular):
    material = bpy.data.materials.new(name)
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba(color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = coat
    bsdf.inputs["Specular IOR Level"].default_value = specular
    return material


def tower_side_material():
    material = surface_material(
        "Tower Sides | Vertically Luminous Architectural Glass",
        "#141A22",
        roughness=0.25,
        metallic=0.50,
        coat=0.12,
        specular=0.50,
    )
    tree = material.node_tree
    bsdf = tree.nodes["Principled BSDF"]
    bsdf.location = (280, 40)
    bsdf.inputs["Emission Strength"].default_value = 0.85

    coordinates = tree.nodes.new("ShaderNodeTexCoord")
    coordinates.location = (-600, 40)
    coordinates.label = "Generated coordinates of the combined city mesh"

    separate = tree.nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-380, 40)

    ramp = tree.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-160, 40)
    ramp.label = "Faint teal increases with actual elevation"
    ramp.color_ramp.interpolation = "LINEAR"
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = rgba("#05070A")
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = rgba("#0E3A44")

    # Generated Z spans the actual combined body mesh bounds. Consequently
    # taller towers reach brighter teal; no invented per-cell variation.
    tree.links.new(coordinates.outputs["Generated"], separate.inputs["Vector"])
    tree.links.new(separate.outputs["Z"], ramp.inputs["Fac"])
    tree.links.new(ramp.outputs["Color"], bsdf.inputs["Emission Color"])
    return material


def glow_material(name, color, strength):
    material = bpy.data.materials.new(name)
    nodes = material.node_tree.nodes
    output = nodes["Material Output"]
    nodes.remove(nodes["Principled BSDF"])
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = rgba(color)
    emission.inputs["Strength"].default_value = strength
    material.node_tree.links.new(
        emission.outputs["Emission"], output.inputs["Surface"]
    )
    return material


def append_box(vertices, faces, indices, x, y, width, bottom, top,
               side_slot=0, horizontal_slot=0):
    """Append a closed box, with a separate material index for its sides."""
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

    for corners, slot in (
        ((3, 2, 1, 0), horizontal_slot),
        ((0, 1, 5, 4), side_slot),
        ((1, 2, 6, 5), side_slot),
        ((2, 3, 7, 6), side_slot),
        ((3, 0, 4, 7), side_slot),
        ((4, 5, 6, 7), horizontal_slot),
    ):
        faces.append(tuple(offset + k for k in corners))
        indices.append(slot)


def mesh_object(name, vertices, faces, materials, indices=None):
    mesh = bpy.data.meshes.new(name + " Mesh")
    mesh.from_pydata(vertices, [], faces)
    for material in materials:
        mesh.materials.append(material)
    if indices is not None:
        mesh.polygons.foreach_set("material_index", indices)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.scale = (MINIATURE_SCALE,) * 3
    return obj


def scaled_location(location):
    return tuple(value * MINIATURE_SCALE for value in location)


def aim_at(obj, target):
    constraint = obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"


def area_light(name, location, energy, size, color, target, specular):
    light = bpy.data.lights.new(name, type="AREA")
    light.energy = energy * MINIATURE_SCALE ** 2
    light.size = size * MINIATURE_SCALE
    light.color = linear_rgb(color)
    light.specular_factor = specular
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

    data = load_data(data_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
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
    scene.eevee.use_raytracing = False

    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.film_transparent = False

    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = -0.45

    world = scene.world or bpy.data.worlds.new("Night Studio")
    scene.world = world
    background = world.node_tree.nodes["Background"]
    background.inputs["Color"].default_value = rgba("#07080B")
    background.inputs["Strength"].default_value = 0.25

    plain_glass = surface_material(
        "Plinth Sides and Hidden Body Tops | Dark Glass",
        "#141A22",
        roughness=0.25,
        metallic=0.50,
        coat=0.12,
        specular=0.50,
    )
    luminous_glass = tower_side_material()
    cyan = glow_material("Solid Cyan Roof Slabs | #3DF5FF", "#3DF5FF", 1.8)
    amber = glow_material("Solid Amber Plinth Tops | #FFB547", "#FFB547", 1.0)

    ground_material = surface_material(
        "Matte Near-Black Ground | No Reflections",
        "#050608",
        roughness=0.8,
        metallic=0.0,
        coat=0.0,
        specular=0.0,
    )

    # Summed-area table: exact clipped 5x5 neighborhood sums.
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
            y = half_grid - i  # Row zero is at the back, positive Y.
            thickness = 0.022 if sign == 1 else 0.012
            seam = height - thickness

            # Only positive-cell vertical walls receive the gradient.
            # Negative-cell sides and all hidden horizontal faces stay plain.
            append_box(
                body_vertices, body_faces, body_indices,
                x, y, FOOTPRINT, 0.0, seam,
                side_slot=1 if sign == 1 else 0,
                horizontal_slot=0,
            )

            # Cap thickness is contained within the exact prescribed height.
            # Every cap is a solid slab, including emissive vertical edges.
            cap_slot = 0 if sign == 1 else 1
            append_box(
                cap_vertices, cap_faces, cap_indices,
                x, y, FOOTPRINT, seam, height,
                side_slot=cap_slot,
                horizontal_slot=cap_slot,
            )

    mesh_object(
        "City | All Blocks",
        body_vertices, body_faces,
        [plain_glass, luminous_glass], body_indices,
    )
    mesh_object(
        "City | All Solid Roof Slabs",
        cap_vertices, cap_faces, [cyan, amber], cap_indices,
    )

    ground_extent = n * 4.0
    mesh_object(
        "Matte Ground",
        [
            (-ground_extent, -ground_extent, 0.0),
            (ground_extent, -ground_extent, 0.0),
            (ground_extent, ground_extent, 0.0),
            (-ground_extent, ground_extent, 0.0),
        ],
        [(0, 1, 2, 3)],
        [ground_material],
    )

    target = (0.0, 0.0, max_height * 0.45)
    focus = bpy.data.objects.new("City Center | Focus", None)
    scene.collection.objects.link(focus)
    focus.location = scaled_location(target)

    # Preserve broad directional highlights; the faint wall emission now
    # supplies readable volume even on faces turned away from these lights.
    area_light(
        "Cool High Back-Left Key",
        (-n * 0.62, n * 0.48, n * 0.85),
        energy=n * n * 120.0,
        size=n * 0.48,
        color="#B1D9FF",
        target=focus,
        specular=0.75,
    )
    area_light(
        "Soft Camera-Side Fill",
        (n * 0.45, -n * 0.70, n * 0.42),
        energy=n * n * 32.0,
        size=n * 0.85,
        color="#9ABDE8",
        target=focus,
        specular=0.40,
    )

    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 100.0
    camera_data.sensor_width = 36.0
    camera_data.sensor_fit = "HORIZONTAL"
    camera_data.clip_start = 0.01

    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    elevation = math.radians(24.0)
    azimuth = math.radians(43.0)
    ce, se = math.cos(elevation), math.sin(elevation)
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    outward = (ce * ca, -ce * sa, se)
    right = (sa, ca, 0.0)
    up = (-se * ca, se * sa, ce)

    aspect = args.res[0] / args.res[1]
    tan_h = camera_data.sensor_width / (2.0 * camera_data.lens)
    tan_v = tan_h / aspect

    # Perspective-correct fitting to actual geometry, slightly tighter than
    # before. A small margin remains for defocus and bloom at the silhouette.
    frame_fill = 0.96
    distance = 0.0
    for vertices in (body_vertices, cap_vertices):
        for vertex in vertices:
            relative = tuple(vertex[k] - target[k] for k in range(3))
            distance = max(
                distance,
                dot(relative, outward) + max(
                    abs(dot(relative, right)) / (tan_h * frame_fill),
                    abs(dot(relative, up)) / (tan_v * frame_fill),
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
    camera_data.dof.aperture_fstop = 1.0

    compositor = bpy.data.node_groups.new(
        "Hadamard | Architectural Bloom", "CompositorNodeTree"
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
    bloom.inputs["Threshold"].default_value = 0.8
    bloom.inputs["Strength"].default_value = 0.5
    bloom.inputs["Size"].default_value = 0.5

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
