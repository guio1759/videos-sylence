"""Shorts nativos verticais (1080x1920) do Ep.1 v2. Uso: python3 shorts2.py n"""
import sys, os, subprocess
n = int(sys.argv[1]); sys.argv = ["x", "shots"]
import make2 as M
from gfx import *
from PIL import ImageDraw
def st(scene): return next(s["t0"] for s in M.SHOTS if s["scene"] == scene)
def en(scene): return [s["t1"] for s in M.SHOTS if s["scene"] == scene][-1]
CUTS = {1: (0.0, en("version")), 2: (st("base_night"), en("gildo_stats")), 3: (st("drama_phone"), en("hug")), 4: (st("email"), en("end"))}
a, b = CUTS[n]
W, H = 1080, 1920
def vf(T):
    im = M.frame(T, W, H)
    if b - T < 3.0 and n != 4:
        im = im.convert("RGBA"); p = chip("EPISÓDIO COMPLETO NO CANAL", 46, WHITE, RED); paste(im, p, W / 2, H * 0.93, 1, back((3.0 - (b - T)) / 0.3)); im = im.convert("RGB")
    return im
out = f"/home/claude/ep1/v2/short{n}.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                      "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", "trilha2.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                      "-pix_fmt", "yuv420p", "-af", f"afade=t=in:d=0.15,afade=t=out:st={b - a - 0.5:.2f}:d=0.5,loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], stdin=subprocess.PIPE)
for k in range(int((b - a) * 30)): p.stdin.write(vf(a + k / 30).tobytes())
p.stdin.close(); p.wait()
if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
print(n, round(b - a, 1))
