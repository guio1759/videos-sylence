"""Lances 3D do Ep. 1 (1920x1080). Cambridge (âmbar) sempre ataca +x neste módulo,
exceto o gol do Crewe, em que o Crewe ataca -x."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude/work/tat")
import eng3d as E
from eng3d import Cam, draw_pitch, draw_goal, draw_ball, draw_shadow, draw_billboard, make_player, ring, smooth, lerp

W, H, S = 1920, 1080, 1
AMB = (246, 178, 40)
SPR = {
    "CAM": make_player(AMB, (20, 20, 22), (20, 20, 22)),
    "CAMGK": make_player((30, 120, 70), (20, 20, 22)),
    "CRE": make_player((200, 30, 40), (240, 240, 240)),
    "ACC": make_player((190, 25, 35), (190, 25, 35)),
    "COL": make_player((40, 80, 180), (240, 240, 240)),
    "OPPGK": make_player((235, 220, 40), (20, 20, 22)),
}


def clamp(u):
    return max(0.0, min(1.0, u))


def tr(keys, t):
    if t <= keys[0][0]: return np.array(keys[0][1:], float)
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            return lerp(a[1:], b[1:], smooth(u))
    return np.array(keys[-1][1:], float)


def arc(t, t0, t1, p0, p1, h):
    u = clamp((t - t0) / (t1 - t0)); p = lerp(p0, p1, u)
    return (p[0], p[1], 0.11 + h * 4 * u * (1 - u))


# ---------------- cenas ----------------
def crewe(t, D):
    """Crewe ataca -x. Cruzamento da direita, cabeceio no 2º pau. Gol em ~D*0.6"""
    tg = min(4.2, D * 0.55)
    cam_ = {k: np.array(v, float) for k, v in {"GK": (-50, 0), "D1": (-44, -4), "D2": (-44, 5), "D3": (-40, 12), "D4": (-40, -14), "M1": (-32, 2), "M2": (-30, -8)}.items()}
    cre = {"W": tr([(0, -20, 26), (tg - 1.6, -38, 28)], t), "S1": tr([(0, -28, 2), (tg - 0.3, -44, -1)], t),
           "S2": tr([(0, -26, -6), (tg - 0.2, -45, 8.5)], t), "M": np.array([-22.0, 10])}
    cam_["GK"] = tr([(tg - 0.4, -50, 0), (tg + 0.1, -50.5, 4)], t)
    if t < tg - 1.6: p = cre["W"]; ball = (p[0] - 0.6, p[1] - 0.3, 0.11)
    elif t < tg - 0.15: ball = arc(t, tg - 1.6, tg - 0.15, (-38.6, 27.7), (-45, 8.3), 5.5)
    else: ball = arc(t, tg - 0.15, tg + 0.35, (-45, 8.3), (-52.8, 1.8), 0.8)
    teams = [("CAM", cam_, {"GK"}), ("CRE", cre, set())]
    cam = ((-18 + 2 * t, 34, 20), (-44, 6, 0), 46) if t < tg + 0.4 else ((-36, 22, 9), (-51, 3, 1), 44)
    labels = [("SEM MARCAÇÃO", cre["S2"], tg - 1.4, tg + 1.5, (235, 60, 60))]
    rings = [(cre["S2"], (235, 60, 60))] if tg - 1.6 < t < tg + 0.3 else []
    return teams, ball, cam, labels, rings


def assist(t, D):
    """Murrey recebe de costas e dá de letra para o Okafor finalizar."""
    tp = min(2.2, D * 0.3); tl = tp + 1.3; ts = tl + 1.1
    cam_ = {"MUR": tr([(0, 22, 6), (tp, 26, 4)], t), "OKA": tr([(0, 20, -6), (tl, 30, -4), (ts, 38, -1)], t),
            "LB": np.array([18.0, 18]), "W": np.array([24.0, -20])}
    opp = {"GK": tr([(ts - 0.4, 50, 0), (ts + 0.2, 48.5, -2)], t), "D1": tr([(0, 30, 4), (tl, 29, 3)], t),
           "D2": np.array([34.0, -6]), "D3": np.array([36.0, 10]), "M": np.array([22.0, 0])}
    if t < tp: ball = arc(t, 0, tp, (8, 10), (25.4, 4.2), 2)
    elif t < tl: ball = (25.4, 4.2, 0.11)
    elif t < ts: ball = arc(t, tl, ts, (25.6, 4.0), (37.4, -1.4), 0.4)
    else: ball = arc(t, ts, ts + 0.5, (38, -1.2), (52.8, 2.4), 0.6)
    teams = [("CAM", cam_, set()), ("ACC", opp, {"GK"})]
    cam = (tuple(tr([(0, 6, -30, 18), (tl, 18, -26, 12), (ts + 0.6, 30, -20, 10)], t)), tuple(tr([(0, 22, 2, 0), (tl, 28, 2, 0), (ts + 0.6, 44, 0, 1)], t)), 46)
    labels = [("MURREY", cam_["MUR"], tp - 0.6, tl + 1.0, AMB), ("DE LETRA", cam_["MUR"], tl - 0.1, tl + 1.0, (255, 255, 255))]
    rings = [(cam_["MUR"], AMB)] if tp - 0.3 < t < tl + 0.3 else []
    return teams, ball, cam, labels, rings


def golaco(t, D):
    """Murrey recebe na entrada da área, corta para dentro e acerta o ângulo."""
    tr_ = min(1.6, D * 0.25); tc = tr_ + 1.2; tsh = tc + 0.6
    mur = tr([(0, 28, 14), (tr_, 33, 12), (tc, 34.5, 6), (tsh, 35.5, 4.5)], t)
    cam_ = {"MUR": mur, "ST": np.array([40.0, -6]), "W": np.array([36.0, -20])}
    opp = {"GK": tr([(tsh, 50, 0), (tsh + 0.5, 50.5, 2.8)], t), "D1": tr([(0, 38, 10), (tc, 36.5, 9)], t),
           "D2": np.array([42.0, 2]), "D3": np.array([41.0, -8]), "M": tr([(0, 30, 8), (tc, 31, 7)], t)}
    if t < tr_: ball = arc(t, 0, tr_, (20, 20), (33.6, 12), 1.5)
    elif t < tsh: ball = (mur[0] + 0.6, mur[1] - 0.3, 0.11)
    else: ball = arc(t, tsh, tsh + 0.6, (36.1, 4.2), (52.6, 3.3), 1.9) if t < tsh + 0.6 else (52.9, 3.3, 2.3)
    teams = [("CAM", cam_, set()), ("COL", opp, {"GK"})]
    cam = (tuple(tr([(0, 20, -22, 14), (tc, 26, -18, 9), (tsh + 0.8, 40, -10, 6)], t)), tuple(tr([(0, 32, 8, 0), (tc, 38, 5, 0), (tsh + 0.8, 51, 3, 1.5)], t)), 46)
    labels = [("MURREY", mur, 0.2, tsh + 1.2, AMB)]
    rings = [(mur, AMB)] if t < tsh else []
    return teams, ball, cam, labels, rings


def ambient(t, D, opp="CRE", attack=1):
    """Plano geral girando devagar: time em formação."""
    cam_ = {"GK": (-50, 0), "D1": (-36, -12), "D2": (-38, -3), "D3": (-38, 6), "D4": (-36, 15), "M1": (-20, -8), "M2": (-22, 4), "M3": (-14, 14), "A1": (-6, -14), "A2": (-4, 2), "A3": (-8, 16)}
    op = {k: (-x, -y) for k, (x, y) in cam_.items()}
    cam_ = {k: np.array(v, float) + np.array([3 * math.sin(t * 0.5 + i), 2 * math.cos(t * 0.4 + i)]) for i, (k, v) in enumerate(cam_.items())}
    op = {k: np.array(v, float) + np.array([3 * math.cos(t * 0.45 + i), 2 * math.sin(t * 0.5 + i)]) for i, (k, v) in enumerate(op.items())}
    ball = (6 * math.sin(t * 0.3), 4 * math.cos(t * 0.25), 0.11)
    a = -1.9 + t * 0.04
    cam = ((70 * math.cos(a), 70 * math.sin(a), 40), (0, 0, 0), 46)
    return [("CAM", cam_, {"GK"}), (opp, op, {"GK"})], ball, cam, [], []


def render(fn, t, D):
    teams, ball, (pos, tgt, fov), labels, rings = fn(t, D)
    cam = Cam(np.array(pos, float), np.array(tgt, float), fov, W, H)
    img = Image.new("RGB", (W, H), (12, 13, 15)); d = ImageDraw.Draw(img, "RGBA")
    draw_pitch(d, cam)
    for p, col in rings: ring(d, cam, p[0], p[1], col + (235,), 1.2, t)
    objs = []
    for team, dd, gks in teams:
        for k, p in dd.items():
            spr = SPR["CAMGK" if team == "CAM" else "OPPGK"] if k in gks else SPR[team]
            objs.append((cam.cam((p[0], p[1], 0.9))[2], "p", (p[0], p[1], spr)))
    objs.append((cam.cam(ball)[2] - 0.05, "b", None))
    for sg in (-1, 1): objs.append((cam.cam((sg * E.HX, 0, 1.2))[2] + 0.5, "g", sg))
    for z, kind, dat in objs:
        if kind == "p": draw_shadow(d, cam, dat[0], dat[1])
    draw_shadow(d, cam, ball[0], ball[1], 0.13, 90)
    for z, kind, dat in sorted(objs, key=lambda o: -o[0]):
        if z < cam.near: continue
        if kind == "p": draw_billboard(img, cam, (dat[0], dat[1], 0), dat[2], 2.05)
        elif kind == "b": draw_ball(img, d, cam, ball)
        else: draw_goal(d, cam, dat)
    return img.convert("RGBA"), [(txt, cam.proj((p[0], p[1], 2.4)), a, b, col) for txt, p, a, b, col in labels]
