"""Blender 5.x: three-body candidate orbit as glowing tubes, time extruded as depth (real trajectory data)."""
import bpy, json, math, os, sys
args = sys.argv[sys.argv.index("--") + 1:]
data_path, cand, out = args[0], args[1], os.path.abspath(args[2])
W, H = (int(args[3]), int(args[4])) if len(args) > 4 else (2400, 1200)
d = json.load(open(data_path))[cand]
xy = d["xy"]; n = len(xy)
sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 96
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
w = sc.world or bpy.data.worlds.new("W"); sc.world = w
w.node_tree.nodes["Background"].inputs[0].default_value = (0.006, 0.007, 0.010, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
cols = [(0.31, 0.82, 0.88), (0.91, 0.71, 0.36), (0.88, 0.42, 0.62)]
depth = 11.0
for b in range(3):
    cu = bpy.data.curves.new(f"body{b}", 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(n - 1)
    flat = []
    for i, p in enumerate(xy):
        x, y = p[b]; z = (i / (n - 1) - 0.5) * depth
        flat += [x * 1.6, y * 1.6, z, 1.0]
    sp.points.foreach_set('co', flat)
    cu.bevel_depth = 0.011; cu.bevel_resolution = 3
    ob = bpy.data.objects.new(f"body{b}", cu); sc.collection.objects.link(ob)
    m = bpy.data.materials.new(f"m{b}")
    nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (*cols[b], 1); em.inputs[1].default_value = 2.2
    mo = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], mo.inputs[0])
    ob.data.materials.append(m)
# faint time axis
cam_d = bpy.data.cameras.new("Cam"); cam_d.lens = 46
cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 3.2
cam = bpy.data.objects.new("Cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (11.5, -14.5, 6.2)
tgt = bpy.data.objects.new("T", None); sc.collection.objects.link(tgt); tgt.location = (0, 0, 0)
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
cam_d.dof.focus_object = tgt
ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree"); sc.compositing_node_group = ng
ng.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
rl = ng.nodes.new("CompositorNodeRLayers"); og = ng.nodes.new("NodeGroupOutput"); g = ng.nodes.new("CompositorNodeGlare")
g.inputs['Type'].default_value = 'Bloom'; g.inputs['Quality'].default_value = 'High'
g.inputs['Threshold'].default_value = 0.9; g.inputs['Strength'].default_value = 0.55; g.inputs['Size'].default_value = 0.6
ng.links.new(rl.outputs['Image'], g.inputs['Image']); ng.links.new(g.outputs['Image'], og.inputs['Image'])
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("rendered", out)
