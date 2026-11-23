"""Shorts nativos verticais (1080x1920) do Ep.1 v2, com final próprio. Uso: python3 shorts2.py n"""
import sys, os, subprocess, math
import numpy as np
from scipy.io import wavfile
n = int(sys.argv[1]); sys.argv = ["x", "shots"]
import make2 as M
from gfx import *
from PIL import ImageDraw
def st(scene): return next(s["t0"] for s in M.SHOTS if s["scene"] == scene)
def en(scene): return [s["t1"] for s in M.SHOTS if s["scene"] == scene][-1]
CUTS = {1: (0.0, en("version")), 2: (st("base_night"), en("gildo_stats")), 3: (st("drama_phone"), en("hug")), 4: (st("email"), en("ab"))}
OUT = {1: (["A MAIOR LOUCURA", "DO FUTEBOL INGLÊS"], "EPISÓDIO COMPLETO NO CANAL"),
       2: (["O ENTREGADOR", "VIRA CRAQUE?"], "COMENTA E VÊ O EPISÓDIO"),
       3: (["DO BANCO", "PRO GOLAÇO"], "EPISÓDIO COMPLETO NO CANAL"),
       4: (["A OU B?"], "COMENTA AGORA")}
a, b = CUTS[n]
SR = 44100
sr, tr = wavfile.read("trilha2.wav"); _, bed = wavfile.read("bed.wav"); _, ov = wavfile.read(f"outro_{n}.wav")
tr = tr.astype(np.float32); bed = bed.astype(np.float32); ov = ov.astype(np.float32)
LO = len(ov) / SR + 0.9
main = tr[int(a * SR): int(b * SR)]
tail = bed[int(b * SR): int(b * SR) + int(LO * SR)].copy()
if len(tail) < int(LO * SR): tail = np.pad(tail, (0, int(LO * SR) - len(tail)))
tail *= 0.7; tail[int(0.15 * SR): int(0.15 * SR) + len(ov)] += ov * 0.9
f = int(0.6 * SR); tail[-f:] *= np.linspace(1, 0, f)
wavfile.write(f"sa{n}.wav", SR, np.clip(np.concatenate([main, tail]), -32000, 32000).astype(np.int16))
W, H = 1080, 1920
def outro(t):
    im = bg(W, H, "amber" if n != 4 else "purple", t); im.alpha_composite(rays(W, H, W / 2, H * 0.4, t, WHITE, 14, 70))
    paste(im, crest(300), W / 2, H * 0.24, 1, back(t / 0.35))
    lines, cta = OUT[n]
    for i, l in enumerate(lines):
        if t > 0.15 + i * 0.25: paste(im, text_el(l, font("blk", 140 if n == 4 else 96), WHITE, 10), W / 2, H * 0.45 + i * 120, 1, 0.4 + 0.6 * back((t - 0.15 - i * 0.25) / 0.3))
    paste(im, chip(cta, 54, WHITE, RED), W / 2, H * 0.66, 1, back((t - 0.7) / 0.3), rot=-3)
    paste(im, chip("INSCREVA-SE", 50, INK, WHITE), W / 2, H * 0.76, 1, back((t - 1.2) / 0.3))
    return im.convert("RGB")
out = f"/home/claude/ep1/v2/short{n}.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                      "-i", f"sa{n}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                      "-pix_fmt", "yuv420p", "-af", "afade=t=in:d=0.15,loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], stdin=subprocess.PIPE)
for k in range(int((b - a) * 30)): p.stdin.write(M.frame(a + k / 30, W, H).tobytes())
for k in range(int(LO * 30)): p.stdin.write(outro(k / 30).tobytes())
p.stdin.close(); p.wait()
if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
print(n, round(b - a + LO, 1))
