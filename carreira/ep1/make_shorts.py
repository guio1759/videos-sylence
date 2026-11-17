"""Cortes verticais (1080x1920) do Ep. 1. Uso: python3 make_shorts.py <n> [preview t]"""
import sys, os, subprocess
sys.argv_ = sys.argv[:]; sys.argv = ["x", "preview"]
import make_ep1 as M
from PIL import Image, ImageDraw, ImageFilter
sys.argv = sys.argv_
W, H = 1080, 1920
CUTS = {
    1: (0.0, 53.0, "O MOTORISTA DE ÔNIBUS QUE VIROU TÉCNICO", "No minuto 93 o Cambridge perdeu tudo"),
    2: (334.6, 368.4, "O ENTREGADOR DE PIZZA MAIS RÁPIDO DA INGLATERRA", "Ganhou de um profissional de chinelo"),
    3: (390.3, 440.4, "FALTOU AO TREINO PRA JOGAR VIDEOGAME", "Duas semanas depois salvou o time"),
    4: (451.9, 494.8, "VOCÊ DECIDE: VENDER OU SEGURAR?", "Comente A ou B"),
}


def wrap(s, f, maxw):
    out = [""]
    for w in s.split():
        if f.getlength((out[-1] + " " + w).strip()) > maxw: out.append(w)
        else: out[-1] = (out[-1] + " " + w).strip()
    return out


def vframe(n, T):
    a, b, hook, sub = CUTS[n]
    t = T - a
    s = None
    for i, sh in enumerate(M.SHOTS):
        if sh["t0"] <= T < sh["t1"]: s = sh; break
    s = s or M.SHOTS[-1]
    fr = M.scene(s["scene"], T - s["t0"], s["t1"] - s["t0"], s).convert("RGB")
    bg = fr.resize((W * 16 // 9 + 200, H), Image.BILINEAR).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 10, 12)), 0.55).convert("RGBA")
    v = fr.resize((W, W * 9 // 16), Image.LANCZOS)
    bg.alpha_composite(v.convert("RGBA"), (0, 640))
    d = ImageDraw.Draw(bg)
    f = M.font("blk", 68)
    for i, l in enumerate(wrap(hook, f, 980)):
        d.text((W / 2, 300 + i * 82), l, font=f, fill=M.AMB if i == 0 else (255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    c = M.chip("MODO CARREIRA • EP.1", M.font("blk", 34), M.BG, (255, 255, 255)); bg.alpha_composite(c, (W // 2 - c.width // 2, 140))
    # legenda grande
    for cu in M.CUES["cues"]:
        if cu["t0"] - 0.05 <= T <= cu["t1"] + 0.25:
            fc = M.font("xb", 52); lines = wrap(cu["text"], fc, 960)
            if len(lines) > 3:
                half = (cu["t0"] + cu["t1"]) / 2; lines = lines[:3] if T < half else lines[3:]
            for i, l in enumerate(lines):
                d.text((W / 2, 1330 + i * 70), l, font=fc, fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
            break
    if b - T < 4:
        p = M.chip("EPISÓDIO COMPLETO NO CANAL", M.font("blk", 46), (255, 255, 255), M.RED)
        bg.alpha_composite(p, (W // 2 - p.width // 2, 1700))
    return bg.convert("RGB")


if __name__ == "__main__":
    n = int(sys.argv[1])
    a, b = CUTS[n][:2]
    if len(sys.argv) > 2:
        vframe(n, float(sys.argv[3])).save(f"/tmp/vs{n}.jpg", quality=88); sys.exit()
    out = f"short{n}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-ss", str(a), "-t", str(b - a), "-i", "trilha.wav", "-map", "0:v", "-map", "1:a",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-af", f"afade=t=out:st={b - a - 0.6}:d=0.6,loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for k in range(int((b - a) * 30)):
        p.stdin.write(vframe(n, a + k / 30).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
