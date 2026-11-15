"""Blender 5.x: a black hole whose accretion disk is the measured Page curve.
Each disk ring is one evaporation step t of the N = 26 sequential-evaporation run on the A100; its glow is the measured
mean radiation entropy S(R)_t (inner ring = early radiation). Event horizon = black sphere; photon ring = thin emissive torus;
a tilted halo ring stands in for the lensed back side of the disk (artistic, not a ray-traced metric)."""
import bpy, json, math, os, sys
args = sys.argv[sys.argv.index("--") + 1:]
data, out = json.load(open(args[0])), os.path.abspath(args[1])
W, H = int(args[2]), int(args[3])
S = data["S_R_mean"]; smax = max(S)
sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 128
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
w = sc.world or bpy.data.worlds.new("W"); sc.world = w
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.004, 0.005, 0.008, 1)

def emis(name, rgb, strength):
    m = bpy.data.materials.new(name); nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*rgb, 1); e.inputs[1].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0]); return m

def ring(name, R, r, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=256, minor_segments=16, rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.data.materials.append(mat); return ob

# event horizon
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=96, ring_count=48)
hz = bpy.context.active_object; m = bpy.data.materials.new("void"); nt = m.node_tree
bs = nt.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = (0, 0, 0, 1); bs.inputs["Roughness"].default_value = 1.0
bs.inputs["Specular IOR Level"].default_value = 0.0; hz.data.materials.append(m)
# photon ring
ring("photon", 1.32, 0.012, emis("pr", (1.0, 0.86, 0.62), 9.0))
# accretion disk = Page curve: one ring per evaporation step, glow = measured S(R)_t
n = len(S)
for t, s in enumerate(S):
    x = s / smax                                   # 0..1, peaks at the Page time
    R = 1.75 + 2.6 * t / (n - 1)
    warm = (1.0, 0.55 + 0.35 * x, 0.25 + 0.45 * x)  # hotter (whiter) where the entropy is high
    ring(f"disk{t}", R, 0.018 + 0.020 * x, emis(f"d{t}", warm, 0.4 + 7.5 * x ** 1.6))
# lensed back side of the disk (stylized): a tilted halo hugging the horizon
for k, (R, s) in enumerate([(1.55, 3.0), (1.75, 1.6)]):
    ring(f"halo{k}", R, 0.02, emis(f"h{k}", (1.0, 0.72, 0.42), s), rot=(math.radians(90), 0, 0))
# camera just above the disk plane
cd = bpy.data.cameras.new("Cam"); cd.lens = 55
cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0.0, -13.5, 1.55)
tgt = bpy.data.objects.new("T", None); sc.collection.objects.link(tgt); tgt.location = (0, 0, -0.1)
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
# bloom
ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree"); sc.compositing_node_group = ng
ng.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
rl = ng.nodes.new("CompositorNodeRLayers"); og = ng.nodes.new("NodeGroupOutput"); g = ng.nodes.new("CompositorNodeGlare")
g.inputs['Type'].default_value = 'Bloom'; g.inputs['Quality'].default_value = 'High'
g.inputs['Threshold'].default_value = 0.7; g.inputs['Strength'].default_value = 0.9; g.inputs['Size'].default_value = 0.8
ng.links.new(rl.outputs['Image'], g.inputs['Image']); ng.links.new(g.outputs['Image'], og.inputs['Image'])
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("rendered", out)
