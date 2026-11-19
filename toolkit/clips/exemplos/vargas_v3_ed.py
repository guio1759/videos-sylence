import sys, json, math, subprocess
sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/clips")
from engine import *  # W,H,FPS, gfx: chip,text_el,stamp,odometer,rays,confetti,back,ease,paste,logo,txt,pop,fade,slide,bg,tag_box,font
import clipedit as CE
import numpy as np, soundfile as sf
D = "/home/claude/clips/vargas3/"
J = json.load(open(D + "words.json")); SEGS = J["segs"]
PLACE = [0.0, 2.3, 12.0, 14.9, 18.0]; TOTAL = 21.0; TG = 7.9
SH = [PLACE[i] - SEGS[i][0] for i in range(5)]
def seg_of(t):
    for i, (a, b) in enumerate(SEGS):
        if a - 0.1 <= t <= b + 0.15: return i
    return None
CAPS = []
for w in J["words"]:
    i = seg_of(w["t0"])
    if i is not None: CAPS.append({"w": w["w"], "t0": w["t0"] + SH[i], "t1": w["t1"] + SH[i]})
FIX = {"erve": "KERWIN", "em": None}
SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "as", "em", "se", "um", "uma", "que", "pra", "com", "aos"}
def caption(img, T):
    cur = None
    for w in CAPS:
        if w["t0"] - 0.03 <= T < w["t1"] + 0.12 and norm(w["w"]) not in SKIP: cur = w
    if not cur: return
    s = re.sub(r"[.,!?:;…-]+", "", cur["w"]).upper()
    if norm(cur["w"]) == "erve": s = "KERWIN"
    if norm(cur["w"]) == "vargas": s = "VARGAS"
    if not s: return
    hot = any(ch.isdigit() for ch in s) or len(s) > 7
    paste(img, chip(s, 92, INK, AMB if hot else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.80, 1, 0.8 + 0.2 * back((T - cur["t0"]) / 0.15))

def frames(src, t0, t1, fps):
    w, h = CE.probe(src)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-to", str(t1), "-i", src, "-r", str(fps), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield Image.frombuffer("RGB", (w, h), b).copy()
def grab(src, t):
    return next(frames(src, t, t + 0.1, 30))

def hud(img, score=True):
    paste(img, tag_box("GOLAÇO DO MEIO-CAMPO", 44, WHITE, INK), W / 2, 130, 1)
    if score:
        paste(img, logo("FLA", 100), W / 2 - 160, 245, 1); paste(img, text_el("0 x 1", font("blk", 64), WHITE, 6), W / 2, 245, 1); paste(img, logo("CAP", 100), W / 2 + 160, 245, 1)

V1, V2 = D + "v1_hq.mp4", D + "v2_hq.mp4"
FREEZE_KICK = grab(V2, 2.5); FREEZE_END = grab(V2, 6.2); CEL = grab(V1, 14.6)

def pitch_anim(img, t):
    # campo vertical (gol do Flamengo em cima); posições ilustrativas
    PW, PH = 860, 1240; X0, Y0 = (W - PW) / 2, 360
    d = ImageDraw.Draw(img)
    for k in range(10): d.rectangle((X0, Y0 + k * PH / 10, X0 + PW, Y0 + (k + 1) * PH / 10), fill=(34, 120, 58) if k % 2 else (40, 132, 64))
    L = (235, 245, 235); w5 = 5
    d.rectangle((X0, Y0, X0 + PW, Y0 + PH), outline=L, width=w5)
    d.line((X0, Y0 + PH / 2, X0 + PW, Y0 + PH / 2), fill=L, width=w5); d.ellipse((W / 2 - 110, Y0 + PH / 2 - 110, W / 2 + 110, Y0 + PH / 2 + 110), outline=L, width=w5)
    d.rectangle((W / 2 - 250, Y0, W / 2 + 250, Y0 + 200), outline=L, width=w5); d.rectangle((W / 2 - 110, Y0, W / 2 + 110, Y0 + 70), outline=L, width=w5)
    d.rectangle((W / 2 - 60, Y0 - 22, W / 2 + 60, Y0), outline=WHITE, width=6)
    paste(img, chip("MEIO-CAMPO", 34, INK, WHITE), X0 + 120, Y0 + PH / 2 - 30, 1)
    kx, ky = W / 2 + 120, Y0 + PH / 2 + 90   # Vargas no próprio campo
    gx, gy = W / 2 - 15, Y0 + 8
    kpx, kpy = W / 2 + 20, Y0 + 215          # goleiro fora da área pequena, na linha da área
    if t > 0.3:
        u = back(min(1, (t - 0.3) / 0.3)); r = 26 * u
        d.ellipse((kx - r, ky - r, kx + r, ky + r), fill=WHITE, outline=INK, width=4); paste(img, chip("VARGAS", 38, INK, WHITE), kx + 110, ky + 30, 1)
    if t > 0.75:
        u = back(min(1, (t - 0.75) / 0.3)); r = 26 * u
        d.ellipse((kpx - r, kpy - r, kpx + r, kpy + r), fill=(80, 170, 255), outline=INK, width=4)
        rr = 60 + 6 * math.sin(t * 10); d.ellipse((kpx - rr, kpy - rr, kpx + rr, kpy + rr), outline=RED, width=8)
        paste(img, chip("GOLEIRO ADIANTADO", 40, WHITE, RED), kpx + 10, kpy + 100, 1, 0.8 + 0.2 * back(min(1, (t - 0.75) / 0.3)))
    if t > 1.5:
        u = min(1, (t - 1.5) / 1.1); pts = []
        for k in range(int(60 * u) + 1):
            s = k / 60; x = kx + (gx - kx) * s - 120 * math.sin(math.pi * s); y = ky + (gy - ky) * s; pts.append((x, y))
        for k in range(0, len(pts) - 1, 2): d.line((pts[k], pts[k + 1]), fill=AMB, width=9)
        bx, by = pts[-1]; d.ellipse((bx - 16, by - 16, bx + 16, by + 16), fill=WHITE, outline=INK, width=3)
    if t > 2.6:
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 150 * (1 - (t - 2.6) / 0.15))))))
    paste(img, text_el("O LANCE", font("blk", 70), WHITE, 7), W / 2, 300, 1)

def stat_card(img, t):
    b = CEL.resize((int(CEL.width * H / CEL.height), H)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(16)).convert("RGBA")
    img.alpha_composite(b); img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 140)))
    img.alpha_composite(rays(W, H, W / 2, 620, t, (255, 80, 80), 14, 40))
    pop(img, logo("CAP", 300), W / 2, 620, t, 0.0, 0.35)
    pop(img, txt("KERWIN VARGAS", 110, WHITE), W / 2, 900, t, 0.25)
    pop(img, chip("10' • 1º TEMPO", 64, INK, AMB), W / 2, 1060, t, wt(2, "dez"), 0.25, -3)
    pop(img, chip("MARACANÃ", 64, WHITE, RED), W / 2, 1180, t, wt(2, "maracan"), 0.25, 3)

def wt(i, word):
    for w in CAPS:
        if PLACE[i] - 0.05 <= w["t0"] and norm(w["w"]).startswith(norm(word)) and w["t0"] < PLACE[i] + 4: return w["t0"] - PLACE[i]
    return 0.5

def virada(img, t):
    img.alpha_composite(rays(W, H, W / 2, 760, t, (255, 220, 140), 14, 40))
    pop(img, logo("FLA", 260), 260, 760, t, 0.0); pop(img, logo("CAP", 260), 820, 760, t, 0.1)
    t1, t2 = wt(3, "virou"), wt(3, "dois")
    a = 0 if t < t1 else 1 if t < t2 else 2
    sc = 1 + 0.25 * max(0, 1 - (t - (t2 if a == 2 else t1)) / 0.2) if a else 1
    paste(img, text_el(f"{a} x 1", font("blk", 200), WHITE, 10), W / 2, 760, 1, sc)
    pop(img, chip("FLAMENGO VIROU", 70, WHITE, RED), W / 2, 1020, t, t1)
    pop(img, chip("AINDA NO 1º TEMPO", 56, INK, WHITE), W / 2, 1140, t, wt(3, "primeiro"))
    if a == 2: pop(img, stamp("2 x 1", 120, AMB), W / 2, 1320, t, t2 + 0.2, 0.25, -6)

def render():
    out = D + "v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    T = 0.0
    def emit(img):
        nonlocal T
        caption(img, T); enc.stdin.write(img.convert("RGB").tobytes()); T += 1 / 30
    def flash(img, t0):
        if 0 <= T - t0 < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (T - t0) / 0.12)))))
    # S1 0–2.3: freeze no chute
    c = {"ar": 0.5625, "cx": 0.5}
    while T < 2.3:
        t = T; z = 1.0 + 0.04 * t
        img, _, _ = CE.compose(FREEZE_KICK, dict(c, zoom=z), [{"type": "circle", "x": 0.575, "y": 0.54, "r": 0.06, "color": "amber"}, {"type": "arrow", "from": [0.59, 0.53], "to": [0.68, 0.47], "color": "amber"}], min(1, t / 0.6))
        hud(img); pop(img, txt("ANTES DO", 100, WHITE), W / 2, 520, t, 0.3); pop(img, txt("MEIO-CAMPO!", 120, AMB), W / 2, 640, t, 0.5)
        emit(img)
    # S2 2.3–5.0: animação do campo
    while T < 5.0:
        img = bg(W, H, "night", T); s0 = 2.3; flash(img, s0); pitch_anim(img, T - s0); hud(img, False); emit(img)
    # S3 5.0–8.3: lance real
    keys = [[3.0, 0.68], [3.6, 0.78], [4.4, 0.76], [5.0, 0.66], [5.8, 0.66], [6.3, 0.64]]
    lt = 3.0
    for fr in frames(V2, 3.0, 6.3, 30):
        if T >= 8.3: break
        img, _, _ = CE.compose(fr, {"ar": 0.5625, "cx_keys": keys}, lt=lt); hud(img); flash(img, 5.0)
        if T >= TG:
            u = T - TG; img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 170 * (1 - u / 0.15))))))
            paste(img, txt("GOLAÇO!", 190, AMB), W / 2 + (8 * math.sin(u * 60) if u < 0.3 else 0), 560, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -4)
            img.alpha_composite(confetti(W, H, u))
        emit(img); lt += 1 / 30
    # S4 8.3–10.6: replay câmera lenta (60 fps → 0.5x)
    keys = [[4.75, 0.7], [5.2, 0.66], [5.9, 0.66]]; lt = 4.75
    for fr in frames(V2, 4.75, 6.0, 60):
        if T >= 10.6: break
        img, _, _ = CE.compose(fr, {"ar": 0.5625, "cx_keys": keys}, lt=lt); hud(img); flash(img, 8.3)
        paste(img, chip("REPLAY", 50, INK, AMB), W / 2, 420, 1); emit(img); lt += 1 / 60
    # S5 10.6–12.0: comemoração
    for fr in frames(V1, 13.8, 15.4, 30):
        if T >= 12.0: break
        img, _, _ = CE.compose(fr, {"ar": 0.5625, "cx": 0.5}); hud(img); flash(img, 10.6); emit(img)
    # S6 12.0–14.9: card do autor
    while T < 14.9:
        img = bg(W, H, "dark", T); stat_card(img, T - 12.0); flash(img, 12.0); paste(img, tag_box("GOLAÇO DO MEIO-CAMPO", 44, WHITE, INK), W / 2, 130, 1); emit(img)
    # S7 14.9–18.0: virada
    while T < 18.0:
        img = bg(W, H, "red", T); virada(img, T - 14.9); flash(img, 14.9); paste(img, tag_box("GOLAÇO DO MEIO-CAMPO", 44, WHITE, INK), W / 2, 130, 1); emit(img)
    # S8 18.0–21.0: pergunta final
    while T < TOTAL:
        t = T - 18.0
        img, _, _ = CE.compose(FREEZE_END, {"ar": 0.5625, "cx": 0.64, "zoom": 1.0 + 0.03 * t}); hud(img); flash(img, 18.0)
        pop(img, txt("GOLAÇO", 150, AMB), W / 2, 560, t, 0.1); pop(img, txt("OU FALHA?", 150, RED), W / 2, 720, t, 0.5)
        pop(img, chip("COMENTA AÍ", 64, INK, WHITE), W / 2, 1300, t, 1.2)
        emit(img)
    enc.stdin.close(); enc.wait()

def mix():
    SR = 44100; N = int(TOTAL * SR)
    a, sr = sf.read(D + "narr.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    vo = np.zeros(N, np.float32)
    for i, (s0, s1) in enumerate(SEGS):
        seg = a[int(s0 * sr): int((s1 + 0.05) * sr)]; k = int(PLACE[i] * SR); vo[k:k + len(seg)] += seg[:max(0, N - k)]
    m, msr = sf.read("/home/claude/clips/vargas/music.wav", dtype="float32"); m = m.mean(1) if m.ndim > 1 else m
    off = 12.25 - TG; m = m[int(off * msr): int(off * msr) + N]; m = np.pad(m, (0, N - len(m)))
    t = np.arange(N) / SR
    g = np.full(N, 0.20, np.float32)
    g[(t >= 4.1) & (t < 7.4)] = 0.42
    r = (t >= 7.4) & (t < TG); g[r] = 0.42 + (1.0 - 0.42) * (t[r] - 7.4) / (TG - 7.4)
    g[(t >= TG) & (t < 11.6)] = 1.0
    r = (t >= 11.6) & (t < 12.0); g[r] = 1.0 - 0.8 * (t[r] - 11.6) / 0.4
    g = np.convolve(g, np.ones(2205) / 2205, "same")
    fo = int(0.8 * SR); g[-fo:] *= np.linspace(1, 0, fo)
    m = m * g * 0.55
    fx = np.zeros(N, np.float32)
    sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
    for name, at, gn in [("tambor_impacto", 0.0, 0.4), ("whoosh_2", 2.2, 0.25), ("whoosh_1", 4.9, 0.25), ("torcida_reacao_gol", TG - 0.1, 0.45), ("whoosh_2", 8.2, 0.25), ("whoosh_boom", 11.9, 0.3), ("tambor_impacto", 14.9 + 0.5, 0.3), ("whoosh_1", 17.9, 0.25)]:
        s = sfxlib.load(name) * gn; k = int(at * SR); e = min(N, k + len(s)); fx[k:e] += s[:e - k]
    out = vo * 1.0 + m + fx; out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(D + "mix.wav", out, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {D}mixn.wav", shell=True, check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}v.mp4 -i {D}mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest {D}vargas_v3.mp4", shell=True, check=True)

if __name__ == "__main__":
    if sys.argv[1] == "render": render(); mix()
    elif sys.argv[1] == "mix": mix()
