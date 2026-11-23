"""Render do vídeo curto vertical nativo 1080x1920. Uso: python3 render_v.py i n"""
import sys, os, subprocess
i, n = int(sys.argv[1]), int(sys.argv[2]); sys.argv = ["x", "shots"]
import make2 as M
W, H = 1080, 1920; nf = int(M.TOTAL * 30); a, b = nf * i // n, nf * (i + 1) // n
out = f"v_{i}.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
for f in range(a, b): p.stdin.write(M.frame(f / 30, W, H).tobytes())
p.stdin.close(); p.wait()
if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
