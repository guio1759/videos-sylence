"""Tiny pseudo-3D football pitch renderer (PIL). World: x along pitch length (+x = attacking goal), y across, z up, metres."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PL, PWD = 105.0, 68.0
HX, HY = PL / 2, PWD / 2

def norm(v): v = np.asarray(v, float); n = np.linalg.norm(v); return v / n if n else v
def lerp(a, b, u): return np.asarray(a, float) * (1 - u) + np.asarray(b, float) * u
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

class Cam:
    def __init__(self, pos, target, fov=52, W=2160, H=3840, near=0.4):
        self.p = np.asarray(pos, float); self.W, self.H, self.near = W, H, near
        f = norm(np.asarray(target, float) - self.p)
        r = norm(np.cross(f, [0, 0, 1])); u = np.cross(r, f)
        self.f, self.r, self.u = f, r, u
        self.F = (H / 2) / math.tan(math.radians(fov) / 2)
    def cam(self, X):
        d = np.asarray(X, float) - self.p
        return np.array([d @ self.r, d @ self.u, d @ self.f])
    def proj_c(self, c):
        return (self.W / 2 + self.F * c[0] / c[2], self.H / 2 - self.F * c[1] / c[2])
    def proj(self, X):
        c = self.cam(X)
        if c[2] < self.near: return None
        return self.proj_c(c) + (c[2],)
    def scale(self, X, size):
        c = self.cam(X)
        return self.F * size / c[2] if c[2] > self.near else 0

def clip_poly(cam, pts):
    cs = [cam.cam(p) for p in pts]; out = []; n = len(cs)
    for i in range(n):
        a, b = cs[i], cs[(i + 1) % n]; ia, ib = a[2] >= cam.near, b[2] >= cam.near
        if ia: out.append(a)
        if ia != ib:
            t = (cam.near - a[2]) / (b[2] - a[2]); out.append(a + (b - a) * t)
    return [cam.proj_c(c) for c in out]

def poly(d, cam, pts, fill):
    q = clip_poly(cam, pts)
    if len(q) >= 3: d.polygon(q, fill=fill)

def polyline(d, cam, pts, col, wm=0.12, minw=2, maxw=14, dash=None, phase=0.0):
    """pts in world; width in metres; optional dash length (m)"""
    acc = phase
    for a, b in zip(pts[:-1], pts[1:]):
        a = np.asarray(a, float); b = np.asarray(b, float); L = np.linalg.norm(b - a)
        n = max(1, int(L / 0.8))
        for k in range(n):
            p0 = a + (b - a) * k / n; p1 = a + (b - a) * (k + 1) / n
            seg = L / n
            if dash:
                on = int(acc / dash) % 2 == 0; acc += seg
                if not on: continue
            c0, c1 = cam.cam(p0), cam.cam(p1)
            if c0[2] < cam.near or c1[2] < cam.near: continue
            w = max(minw, min(maxw, cam.F * wm / ((c0[2] + c1[2]) / 2)))
            d.line([cam.proj_c(c0), cam.proj_c(c1)], fill=col, width=int(w))

def circle_pts(cx, cy, r, a0=0, a1=360, n=48, z=0.02):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), z) for i in range(n + 1)]

GROUND = (17, 19, 21); PITCH_A = (27, 31, 33); PITCH_B = (24, 28, 30); LINE = (205, 210, 215, 150)
def draw_pitch(d, cam):
    big = [(-150, -110, 0), (150, -110, 0), (150, 110, 0), (-150, 110, 0)]
    poly(d, cam, big, GROUND)
    poly(d, cam, [(-HX - 4, -HY - 4, 0), (HX + 4, -HY - 4, 0), (HX + 4, HY + 4, 0), (-HX - 4, HY + 4, 0)], PITCH_B)
    n = 16
    for i in range(n):
        if i % 2: continue
        x0 = -HX + PL * i / n; x1 = -HX + PL * (i + 1) / n
        poly(d, cam, [(x0, -HY, 0), (x1, -HY, 0), (x1, HY, 0), (x0, HY, 0)], PITCH_A)
    z = 0.01
    L = lambda pts: polyline(d, cam, pts, LINE, 0.12, 1, 10)
    L([(-HX, -HY, z), (HX, -HY, z), (HX, HY, z), (-HX, HY, z), (-HX, -HY, z)])
    L([(0, -HY, z), (0, HY, z)]); L(circle_pts(0, 0, 9.15))
    for s in (-1, 1):
        gx = s * HX
        L([(gx, -20.16, z), (gx - s * 16.5, -20.16, z), (gx - s * 16.5, 20.16, z), (gx, 20.16, z)])
        L([(gx, -9.16, z), (gx - s * 5.5, -9.16, z), (gx - s * 5.5, 9.16, z), (gx, 9.16, z)])
        a = math.degrees(math.acos(5.5 / 9.15))
        cxs = gx - s * 11
        L(circle_pts(cxs, 0, 9.15, (180 if s > 0 else 0) - a, (180 if s > 0 else 0) + a, 20))
        for cy in (-HY, HY):
            a0 = 0 if (s < 0 and cy < 0) else 90 if (s > 0 and cy < 0) else 270 if (s < 0 and cy > 0) else 180
            L(circle_pts(gx, cy, 1.0, a0, a0 + 90, 8))
    for s in (-1, 1):
        p = cam.proj((s * (HX - 11), 0, z))
        if p: r = max(2, cam.F * 0.15 / p[2]); d.ellipse((p[0] - r, p[1] - r * 0.5, p[0] + r, p[1] + r * 0.5), fill=LINE)

# ---------- sprites ----------
def make_player(jersey, shorts=(30, 32, 36), socks=None, skin=(200, 150, 115), H=360):
    socks = socks or jersey
    W = int(H * 0.5); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = H / 100
    cx = W / 2
    sh = tuple(int(c * 0.72) for c in jersey); jl = tuple(min(255, int(c * 1.12)) for c in jersey)
    # legs
    for s in (-1, 1):
        x = cx + s * 6 * u
        d.rounded_rectangle((x - 4.5 * u, 58 * u, x + 4.5 * u, 92 * u), int(3 * u), fill=skin)
        d.rounded_rectangle((x - 4.8 * u, 74 * u, x + 4.8 * u, 95 * u), int(3 * u), fill=socks)
        d.rounded_rectangle((x - 5.5 * u, 94 * u, x + 6.5 * u, 99.5 * u), int(2.5 * u), fill=(25, 25, 28))
    d.rounded_rectangle((cx - 13 * u, 50 * u, cx + 13 * u, 66 * u), int(4 * u), fill=shorts)
    # arms
    for s in (-1, 1):
        d.rounded_rectangle((cx + s * 15 * u - 4 * u, 24 * u, cx + s * 15 * u + 4 * u, 52 * u), int(4 * u), fill=skin)
        d.rounded_rectangle((cx + s * 15 * u - 4.5 * u, 22 * u, cx + s * 15 * u + 4.5 * u, 34 * u), int(4 * u), fill=jersey)
    d.rounded_rectangle((cx - 13 * u, 20 * u, cx + 13 * u, 54 * u), int(6 * u), fill=jersey)
    d.rounded_rectangle((cx + 6 * u, 22 * u, cx + 13 * u, 53 * u), int(5 * u), fill=sh)
    d.ellipse((cx - 8 * u, 2 * u, cx + 8 * u, 20 * u), fill=skin)
    d.chord((cx - 8.5 * u, 1 * u, cx + 8.5 * u, 14 * u), 180, 360, fill=(40, 30, 25))
    return im
_spr_cache = {}
def sprite(base, hpx, flip=False):
    key = (id(base), int(hpx / 3), flip)
    if len(_spr_cache) > 120: _spr_cache.clear()
    if key not in _spr_cache:
        h = max(4, int(hpx)); w = max(2, int(base.width * h / base.height))
        im = base.resize((w, h), Image.LANCZOS)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if hpx > 700: return im
        _spr_cache[key] = im
    return _spr_cache[key]

def draw_shadow(d, cam, x, y, r=0.45, a=110):
    pts = clip_poly(cam, [(x + r * math.cos(t), y + r * 0.8 * math.sin(t), 0.02) for t in np.linspace(0, 2 * math.pi, 14)])
    if len(pts) >= 3: d.polygon(pts, fill=(0, 0, 0, a))

def draw_billboard(img, cam, X, base, height_m=2.05, alpha=1.0, flip=False):
    p = cam.proj(X)
    if not p: return
    hp = cam.F * height_m / p[2]
    if hp < 3: return
    s = sprite(base, hp, flip)
    if alpha < 1:
        s = s.copy(); s.putalpha(s.split()[3].point(lambda v: int(v * alpha)))
    _safe(img, s, int(p[0] - s.width / 2), int(p[1] - s.height))
def _safe(img, s, x, y):
    l, t = max(0, -x), max(0, -y); r, b = min(s.width, img.width - x), min(s.height, img.height - y)
    if r > l and b > t:
        c = s.crop((l, t, r, b)); img.paste(c, (x + l, y + t), c)

def draw_ball(img, d, cam, X):
    p = cam.proj(X)
    if not p: return
    r = max(3, cam.F * 0.12 / p[2])
    d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=(245, 245, 245), outline=(40, 40, 40), width=max(1, int(r * 0.15)))
    d.ellipse((p[0] - r * 0.35, p[1] - r * 0.35, p[0] + r * 0.35, p[1] + r * 0.35), fill=(50, 50, 55))

def draw_goal(d, cam, s, bar="bar", t=0.0, col=(240, 240, 240)):
    gx = s * HX; dep = s * 2.0
    net = (220, 220, 225, 55)
    for k in range(9):
        y = -3.66 + 7.32 * k / 8
        polyline(d, cam, [(gx, y, 2.44), (gx + dep, y, 2.0), (gx + dep, y, 0)], net, 0.03, 1, 3)
    for k in range(5):
        z = 2.44 * k / 4
        polyline(d, cam, [(gx + dep, -3.66, z), (gx + dep, 3.66, z)], net, 0.03, 1, 3)
    for y in (-3.66, 3.66):
        polyline(d, cam, [(gx, y, 0), (gx, y, 2.44)], col, 0.12, 2, 22)
    if bar == "bar":
        polyline(d, cam, [(gx, -3.66, 2.44), (gx, 3.66, 2.44)], col, 0.12, 2, 22)
    elif bar == "tape":
        pts = [(gx, -3.66 + 7.32 * i / 30, 2.44 - 0.18 * math.sin(math.pi * i / 30) + 0.06 * math.sin(i * 0.7 + t * 7)) for i in range(31)]
        polyline(d, cam, pts, (225, 205, 160), 0.05, 1, 8)

def ring(d, cam, x, y, col, r=1.1, phase=0.0, w=0.09):
    polyline(d, cam, circle_pts(x, y, r, phase * 40, phase * 40 + 360, 40), col, w, 2, 10, dash=0.45)

def project_label(cam, X):
    p = cam.proj(X); return (p[0] / 2, p[1] / 2) if p else None   # in 1x output coords
