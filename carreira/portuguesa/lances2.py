"""Lances 3D do Ep.2 da Lusa (vertical 1080x1920). Lusa ataca +x. Nomes embaixo dos jogadores."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude/work/tat")
import eng3d as E
from eng3d import Cam, draw_pitch, draw_goal, draw_ball, draw_shadow, draw_billboard, make_player, ring, smooth, lerp
SPR = {"POR": make_player((200, 30, 40), (20, 110, 60), (200, 30, 40)), "PORGK": make_player((30, 30, 34), (30, 30, 34)),
       "COR": make_player((240, 240, 240), (25, 25, 28), (25, 25, 28)), "SAO": make_player((245, 245, 245), (245, 245, 245), (200, 30, 40)),
       "OGK": make_player((240, 210, 40), (25, 25, 28))}
def clamp(u): return max(0.0, min(1.0, u))
def tr(keys, t):
    if t <= keys[0][0]: return np.array(keys[0][1:], float)
    for a, b in zip(keys[:-1], keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            return lerp(a[1:], b[1:], smooth(u))
    return np.array(keys[-1][1:], float)
def arc(t, t0, t1, p0, p1, h, z1=0.11):
    u = clamp((t - t0) / (t1 - t0)); p = lerp(p0, p1, u)
    return (p[0], p[1], 0.11 + (z1 - 0.11) * u + h * 4 * u * (1 - u))

TP, TS = 2.0, 3.4   # passe do Levi, chute do Davi
def davi_goal(t):
    por = {"LEVI": tr([(0, 14, -3), (TP, 17, -2.5)], t), "DAVI": tr([(0, 22, 5), (TP, 27, 3.5), (TS, 36, 1.5)], t),
           "CAD": tr([(0, 28, -6), (TS, 40, -5)], t), "TOR": np.array([24.0, -12])}
    cor = {"GK": tr([(TS - 0.2, 51, 0), (TS + 0.35, 50.5, -2.8)], t), "D1": tr([(0, 30, 0), (TS, 34, -1)], t), "D2": tr([(0, 32, -7), (TS, 37, -5)], t),
           "D3": np.array([28.0, 9]), "M1": tr([(0, 19, -6), (TP, 17, -5)], t), "M2": np.array([21.0, 7])}
    if t < TP: ball = (por["LEVI"][0] + 0.6, por["LEVI"][1] + 0.2, 0.11)
    elif t < TS - 0.15: ball = arc(t, TP, TS - 0.15, (17.6, -2.3), (35.5, 1.6), 0.6)
    else: ball = arc(t, TS - 0.15, TS + 0.45, (36.3, 1.5), (52.6, -2.6), 0.4, 0.6) if t < TS + 0.45 else (52.9, -2.6, 0.5)
    cam = (tuple(tr([(0, 4, -2, 9), (TP, 10, -1, 8), (TS + 0.6, 24, 0, 6)], t)), tuple(tr([(0, 28, 0, 0), (TP, 34, 0, 0), (TS + 0.6, 50, -1, 1)], t)), 55)
    labels = [("LEVI", por["LEVI"], -1, TP + 0.9, (255, 205, 60)), ("DAVI • 16", por["DAVI"], TP - 0.6, TS + 1.5, (255, 205, 60))]
    rings = [(por["LEVI"], (255, 205, 60))] if t < TP + 0.2 else [(por["DAVI"], (255, 205, 60))] if t < TS + 0.3 else []
    return [("POR", por, set()), ("COR", cor, {"GK"})], ball, cam, labels, rings

TK = 1.6  # chute do pênalti
def penalty(t, kick=True):
    run = tr([(0, 38.5, -2.5), (TK, 41.4, -0.3)], t) if kick else np.array([39.2, -1.6]) + np.array([0.15 * math.sin(t * 2), 0])
    por = {"CAU": run, "A1": np.array([34.0, 8]), "A2": np.array([33.5, -9]), "A3": np.array([31.0, 2])}
    gk = tr([(TK - 0.05, 52, 0), (TK + 0.4, 51.8, -3.0)], t) if kick else np.array([52.0, 0.3 * math.sin(t * 3)])
    sao = {"GK": gk, "D1": np.array([35.0, 12]), "D2": np.array([34.0, -12]), "D3": np.array([32.0, 6]), "D4": np.array([32.5, -5])}
    if not kick or t < TK: ball = (41.5, 0, 0.11)
    else: ball = arc(t, TK, TK + 0.4, (41.5, 0), (52.7, 2.6), 0.2, 1.4) if t < TK + 0.4 else (53.4, 2.6, 0.9)
    if kick: cam = (tuple(tr([(0, 29, -4, 5.5), (TK + 0.8, 31, -2.5, 4.5)], t)), (51, 0.5, 1.0), 40)
    else: cam = ((28.5 + 0.3 * t, -4 + 0.2 * t, 5.5), (50, 0, 1.0), 40)
    labels = [("CAUARI", run, -1, 99, (255, 205, 60))]
    rings = [(run, (255, 205, 60))] if (not kick or t < TK) else []
    return [("POR", por, set()), ("SAO", sao, {"GK"})], ball, cam, labels, rings

def render(fn, t, W, H):
    teams, ball, (pos, tgt, fov), labels, rings = fn(t)
    cam = Cam(np.array(pos, float), np.array(tgt, float), fov, W, H)
    img = Image.new("RGB", (W, H), (12, 13, 15)); d = ImageDraw.Draw(img, "RGBA")
    draw_pitch(d, cam)
    for p, col in rings: ring(d, cam, p[0], p[1], col + (235,), 1.2, t)
    objs = []
    for team, dd, gks in teams:
        for k, p in dd.items():
            spr = SPR["OGK" if team != "POR" else "PORGK"] if k in gks else SPR[team]
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
    return img.convert("RGBA"), [(s, cam.proj((p[0], p[1], 0.0)), a, b, col) for s, p, a, b, col in labels]
