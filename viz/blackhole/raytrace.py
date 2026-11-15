"""A physically based black hole: Schwarzschild null geodesics ray-traced on the GPU.

Units: r_s = 2M = 1. Every pixel's light ray is traced backwards from the camera with the exact photon-orbit equation
in Cartesian form, x'' = -(3/2) h^2 x / r^5 with h = |x cross v| conserved. This is the Binet equation
u'' + u = 3 M u^2 of Schwarzschild null geodesics, integrated with RK4 and a step that shrinks as r^2 near the hole.

A thin, opaque, Keplerian accretion disk extends outward from the ISCO (r = 3 r_s). It emits with a Novikov-Thorne-like
temperature profile T ~ r^-3/4 (1 - sqrt(r_in / r))^1/4. The observed temperature is scaled by
g = sqrt(1 - 3M/r) / (1 - Omega L), which combines gravitational redshift with the Doppler shift of the orbiting gas,
and the observed bolometric intensity by g^4. That is why one side of the disk is brighter and bluer.
Turbulent structure is a sheared noise texture (azimuthal arcs, as Keplerian shear produces). Rays that escape
sample a star field, so the background stars are lensed too.

  python3 viz/blackhole/raytrace.py --w 2400 --h 1100 --ss 3 --out viz/blackhole/out/blackhole_rt.png
"""
import argparse, json, math, os, time

import torch
import torch.nn.functional as F
from PIL import Image

LUMA = (0.2126, 0.7152, 0.0722)


def kelvin_rgb(T):
    """Blackbody colour (Tanner Helland fit), returned in linear RGB with unit luminance."""
    t = (T / 100).clamp(10, 400)
    r = torch.where(t <= 66, torch.ones_like(t), 329.698727446 * (t - 60).clamp(min=1e-3) ** -0.1332047592 / 255)
    g = torch.where(t <= 66, (99.4708025861 * torch.log(t) - 161.1195681661) / 255,
                    288.1221695283 * (t - 60).clamp(min=1e-3) ** -0.0755148492 / 255)
    b = torch.where(t >= 66, torch.ones_like(t),
                    torch.where(t <= 19, torch.zeros_like(t), (138.5177312231 * torch.log((t - 10).clamp(min=1e-3)) - 305.0447927307) / 255))
    rgb = torch.stack([r, g, b], -1).clamp(1e-4, 1) ** 2.2
    lum = rgb[..., 0] * LUMA[0] + rgb[..., 1] * LUMA[1] + rgb[..., 2] * LUMA[2]
    return rgb / lum[..., None]


def disk_texture(dev, seed, NR=512, NP=2048):
    """Periodic-in-phi fBm, stretched along phi (long arcs) like sheared turbulence."""
    gen = torch.Generator(device=dev).manual_seed(seed)
    tex = torch.zeros(NR, NP, device=dev)
    amp, tot = 1.0, 0.0
    for nr, npp in [(5, 18), (10, 48), (22, 120), (46, 300), (96, 720), (190, 1500)]:
        g = torch.rand(1, 1, nr, npp, generator=gen, device=dev)
        g = torch.cat([g, g[..., :1]], -1)
        up = F.interpolate(g, size=(NR, NP + 1), mode="bicubic", align_corners=True)[0, 0, :, :NP]
        tex += amp * up; tot += amp; amp *= 0.62
    tex /= tot
    return (tex - tex.min()) / (tex.max() - tex.min())


def sample_tex(tex, s, ph):
    NR, NP = tex.shape
    i = s.clamp(0, 1) * (NR - 1)
    i0 = i.floor().long().clamp(0, NR - 2); fi = i - i0
    j = (ph % 1.0) * NP
    j0 = j.floor().long() % NP; j1 = (j0 + 1) % NP; fj = j - j.floor()
    a = tex[i0, j0] * (1 - fj) + tex[i0, j1] * fj
    b = tex[i0 + 1, j0] * (1 - fj) + tex[i0 + 1, j1] * fj
    return a * (1 - fi) + b * fi


def gauss_blur(img, sigma):
    """img (1,C,H,W); separable gaussian."""
    k = int(sigma * 3) * 2 + 1
    x = torch.arange(k, device=img.device, dtype=img.dtype) - k // 2
    w = torch.exp(-0.5 * (x / sigma) ** 2); w /= w.sum()
    C = img.shape[1]
    img = F.conv2d(F.pad(img, (k // 2, k // 2, 0, 0), mode="replicate"), w.view(1, 1, 1, k).repeat(C, 1, 1, 1), groups=C)
    img = F.conv2d(F.pad(img, (0, 0, k // 2, k // 2), mode="replicate"), w.view(1, 1, k, 1).repeat(C, 1, 1, 1), groups=C)
    return img


def star_field(dev, seed, W=8192, H=4096, n=26000):
    gen = torch.Generator(device=dev).manual_seed(seed)
    sl = torch.rand(n, generator=gen, device=dev) * 2 - 1
    lon = torch.rand(n, generator=gen, device=dev) * 2 * math.pi - math.pi
    lat = torch.asin(sl)
    xi = ((lon + math.pi) / (2 * math.pi) * W).long().clamp(0, W - 1)
    yi = ((math.pi / 2 - lat) / math.pi * H).long().clamp(0, H - 1)
    bright = 0.01 + 1.6 * torch.rand(n, generator=gen, device=dev) ** 12
    col = kelvin_rgb(3200 + 9000 * torch.rand(n, generator=gen, device=dev)) * bright[:, None]
    tex = torch.zeros(3, H * W, device=dev)
    for c in range(3):
        tex[c].index_add_(0, yi * W + xi, col[:, c])
    return gauss_blur(tex.view(1, 3, H, W), 0.7)[0]


def sample_stars(stars, d):
    lon = torch.atan2(d[:, 2], d[:, 0]); lat = torch.asin(d[:, 1].clamp(-1, 1))
    grid = torch.stack([lon / math.pi, -2 * lat / math.pi], -1).view(1, 1, -1, 2)
    return F.grid_sample(stars[None], grid, mode="bilinear", align_corners=False)[0, :, 0, :].T


def trace(cam, dirs, P):
    N = dirs.shape[0]
    x = cam.expand(N, 3).clone(); v = dirs.clone()
    h = torch.cross(x, v, dim=1); h2 = (h * h).sum(1, keepdim=True)
    r0 = x.norm(dim=1)
    vinf = torch.sqrt((1 - h2[:, 0] / r0 ** 3).clamp(min=1e-9))
    L = -h[:, 1] / vinf                              # photon angular momentum about the disk axis (physical direction)
    alive = torch.ones(N, dtype=torch.bool, device=x.device)
    hit = torch.zeros_like(alive); esc = torch.zeros_like(alive)
    rc = torch.zeros(N, device=x.device); phc = torch.zeros(N, device=x.device)

    def acc(p):
        r2 = (p * p).sum(1, keepdim=True)
        return -1.5 * h2 * p / r2 ** 2.5

    for step in range(P.max_steps):
        r = x.norm(dim=1, keepdim=True)
        dt = (P.k * r * r).clamp(P.dtmin, P.dtmax)
        k1x = v; k1v = acc(x)
        k2x = v + 0.5 * dt * k1v; k2v = acc(x + 0.5 * dt * k1x)
        k3x = v + 0.5 * dt * k2v; k3v = acc(x + 0.5 * dt * k2x)
        k4x = v + dt * k3v; k4v = acc(x + dt * k3x)
        xn = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        vn = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        y0, y1 = x[:, 1], xn[:, 1]
        cross = alive & (y0 * y1 <= 0) & (y0 != y1)
        t = (y0 / (y0 - y1 + 1e-30)).clamp(0, 1)
        p = x + t[:, None] * (xn - x)
        rr = torch.sqrt(p[:, 0] ** 2 + p[:, 2] ** 2)
        nh = cross & (rr >= P.rin) & (rr <= P.rout)
        hit |= nh
        rc = torch.where(nh, rr, rc); phc = torch.where(nh, torch.atan2(p[:, 2], p[:, 0]), phc)
        alive &= ~nh
        rn = xn.norm(dim=1)
        alive &= ~(rn < 1.0)                           # crossed the horizon
        e = alive & (rn > P.resc) & ((xn * vn).sum(1) > 0)
        esc |= e; alive &= ~e
        x = torch.where(alive[:, None], xn, x); v = torch.where(alive[:, None], vn, v)
        if step % 64 == 63 and not bool(alive.any()):
            break
    d = v / v.norm(dim=1, keepdim=True)
    return hit, rc, phc, L, esc, d, step + 1


def shade(hit, rc, phc, L, P, tex):
    rcs = rc.clamp(min=P.rin)
    Tn = (P.rin / rcs) ** 0.75 * (1 - torch.sqrt(P.rin / rcs)).clamp(min=0) ** 0.25
    rg = torch.linspace(P.rin, P.rout, 4000, device=rc.device)
    Tmax = ((P.rin / rg) ** 0.75 * (1 - torch.sqrt(P.rin / rg)) ** 0.25).max()
    Tn = Tn / Tmax
    Om = torch.sqrt(0.5 / rcs ** 3) * P.spin
    g = torch.sqrt(1 - 1.5 / rcs) / (1 - Om * L)
    s = (torch.log(rcs) - math.log(P.rin)) / (math.log(P.rout) - math.log(P.rin))
    turb = sample_tex(tex, s, (phc + P.shear * torch.log(rcs)) / (2 * math.pi))
    fade = ((P.rout - rcs) / (P.rout * 0.45)).clamp(0, 1) ** 1.5
    I = (g * Tn) ** 4 * (0.22 + 1.6 * turb ** 1.7) * fade
    col = kelvin_rgb(g * Tn * P.tpeak) * I[:, None]
    return torch.where(hit[:, None], col, torch.zeros_like(col)), g


def aces(x):
    return ((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14)).clamp(0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", type=int, default=2400); ap.add_argument("--h", type=int, default=1100)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--dist", type=float, default=30.0)
    ap.add_argument("--elev", type=float, default=9.0, help="camera elevation above the disk plane, degrees")
    ap.add_argument("--fov", type=float, default=42.0, help="horizontal field of view, degrees")
    ap.add_argument("--yaw", type=float, default=0.0, help="look offset to the side, degrees")
    ap.add_argument("--pitch", type=float, default=0.0, help="look offset up (+) / down, degrees")
    ap.add_argument("--rin", type=float, default=3.0); ap.add_argument("--rout", type=float, default=15.0)
    ap.add_argument("--tpeak", type=float, default=5600.0); ap.add_argument("--spin", type=float, default=1.0)
    ap.add_argument("--shear", type=float, default=2.4)
    ap.add_argument("--key", type=float, default=1.25, help="exposure: 99.5th percentile disk luminance maps here")
    ap.add_argument("--stars", type=float, default=0.55)
    ap.add_argument("--bloom", type=float, default=1.0)
    ap.add_argument("--sat", type=float, default=1.0, help="display saturation")
    ap.add_argument("--k", type=float, default=0.03); ap.add_argument("--dtmin", type=float, default=0.004)
    ap.add_argument("--dtmax", type=float, default=0.5); ap.add_argument("--resc", type=float, default=50.0)
    ap.add_argument("--max_steps", type=int, default=6000)
    ap.add_argument("--chunk", type=int, default=4_000_000)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", default="viz/blackhole/out/blackhole_rt.png")
    P = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    t0 = time.time()
    W, H, ss = P.w * P.ss, P.h * P.ss, P.ss
    el = math.radians(P.elev)
    cam = torch.tensor([0.0, P.dist * math.sin(el), -P.dist * math.cos(el)], device=dev)
    f = -cam / cam.norm()
    upw = torch.tensor([0.0, 1.0, 0.0], device=dev)
    right = torch.linalg.cross(upw, f); right /= right.norm()
    up = torch.linalg.cross(f, right)
    yaw, pitch = math.radians(P.yaw), math.radians(P.pitch)
    f = f * math.cos(yaw) * math.cos(pitch) + right * math.sin(yaw) * math.cos(pitch) + up * math.sin(pitch)
    f /= f.norm(); right = torch.linalg.cross(upw, f); right /= right.norm(); up = torch.linalg.cross(f, right)
    tx = math.tan(math.radians(P.fov) / 2); ty = tx * H / W
    tex = disk_texture(dev, P.seed)
    stars = star_field(dev, P.seed + 1)
    img = torch.zeros(H * W, 3, device=dev)
    skyimg = torch.zeros(H * W, 3, device=dev)        # display-referred sky, added after exposure
    nhit = 0; steps_max = 0
    rows_per = max(1, P.chunk // W)
    for r0 in range(0, H, rows_per):
        r1 = min(H, r0 + rows_per)
        yy = (torch.arange(r0, r1, device=dev, dtype=torch.float32) + 0.5) / H
        xx = (torch.arange(W, device=dev, dtype=torch.float32) + 0.5) / W
        Y, X = torch.meshgrid(yy, xx, indexing="ij")
        u = (2 * X - 1) * tx; vv = (1 - 2 * Y) * ty
        d = f[None] + u.reshape(-1, 1) * right[None] + vv.reshape(-1, 1) * up[None]
        d = d / d.norm(dim=1, keepdim=True)
        hit, rc, phc, L, esc, dout, nsteps = trace(cam, d, P)
        col, g = shade(hit, rc, phc, L, P, tex)
        sky = sample_stars(stars, dout) * esc[:, None]
        img[r0 * W:r1 * W] = col
        skyimg[r0 * W:r1 * W] = sky
        nhit += int(hit.sum()); steps_max = max(steps_max, nsteps)
        print(f"rows {r0}-{r1} of {H}: steps {nsteps}, disk hits {int(hit.sum())}, escaped {int(esc.sum())}, {time.time()-t0:.1f}s", flush=True)
    img = img.view(H, W, 3).permute(2, 0, 1)[None]
    skyimg = skyimg.view(H, W, 3).permute(2, 0, 1)[None]
    img = F.avg_pool2d(img, ss); skyimg = F.avg_pool2d(skyimg, ss)
    lum = (img[0] * torch.tensor(LUMA, device=dev).view(3, 1, 1)).sum(0).flatten()
    lum = lum[lum > 1e-9]
    if lum.numel() > 4_000_000:
        lum = lum[torch.randperm(lum.numel(), device=dev)[:4_000_000]]
    exposure = P.key / torch.quantile(lum, 0.995)
    img = img * exposure
    bright = (img - 0.9).clamp(min=0)
    s = P.w / 2400
    bloom = 0.30 * gauss_blur(bright, 3 * s) + 0.18 * gauss_blur(bright, 12 * s) + 0.10 * gauss_blur(bright, 40 * s)
    img = img + P.bloom * bloom + P.stars * skyimg
    out = aces(img)
    if P.sat != 1.0:
        l = (out * torch.tensor(LUMA, device=dev).view(1, 3, 1, 1)).sum(1, keepdim=True)
        out = (l + P.sat * (out - l)).clamp(0, 1)
    out = out ** (1 / 2.2)
    out8 = (out[0].permute(1, 2, 0) * 255 + 0.5).clamp(0, 255).to(torch.uint8).cpu().contiguous()
    im = Image.frombytes("RGB", (P.w, P.h), bytes(out8.view(-1).tolist()))
    os.makedirs(os.path.dirname(os.path.abspath(P.out)), exist_ok=True)
    im.save(P.out)
    meta = {k: getattr(P, k) for k in vars(P)}
    meta.update(device=torch.cuda.get_device_name(0) if dev == "cuda" else "cpu", rays=W * H, disk_hits=nhit,
                max_steps_used=steps_max, seconds=round(time.time() - t0, 1))
    json.dump(meta, open(os.path.splitext(P.out)[0] + ".json", "w"), indent=1)
    print("wrote", P.out, meta, flush=True)


if __name__ == "__main__":
    main()
