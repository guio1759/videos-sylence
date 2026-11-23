import sys, json, math, subprocess, re, difflib
sys.path.insert(0, "/home/claude/ter24"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/clips"); sys.path.insert(0, "/home/claude/ed24")
from engine import *
import clipedit as CE
import numpy as np, soundfile as sf
from nscript import MUS
D = "/home/claude/ed24/"
J = json.load(open(D + "n/words.json")); SEGS = J["segs"]
# posição de cada frase da narração na linha do tempo do edit
PLACE = [0.0, 3.7, 7.9, 16.4, 25.1, 27.95, 32.2, 36.3]
TOTAL = 40.9
SH = [PLACE[i] - SEGS[i][0] for i in range(len(SEGS))]

def build_caps():
    caps = []
    for i, (s0, s1) in enumerate(SEGS):
        sw = re.findall(r"\S+", MUS[i][0]); wh = [w for w in J["words"] if s0 - 0.15 <= w["t0"] < s1 + 0.05]
        a = [norm(x) for x in sw]; b = [norm(x["w"]) for x in wh]; tm = [None] * len(sw)
        for bl in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
            for k in range(bl.size): tm[bl.a + k] = (wh[bl.b + k]["t0"], wh[bl.b + k]["t1"])
        L = [max(1, len(norm(x))) for x in sw]; tot = sum(L); acc = 0
        for k in range(len(sw)):
            if tm[k] is None: st = s0 + (s1 - s0) * acc / tot; tm[k] = (st, st + (s1 - s0) * L[k] / tot)
            acc += L[k]
        for k in range(len(sw)): caps.append({"w": sw[k], "t0": max(s0, tm[k][0]) + SH[i], "t1": min(s1 + 0.2, tm[k][1]) + SH[i]})
    return caps
CAPS = build_caps()
SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "as", "em", "se", "um", "uma", "que", "pra", "com", "aos", "pros"}
def caption(img, T):
    cur = None
    for w in CAPS:
        if w["t0"] - 0.03 <= T < w["t1"] + 0.12 and norm(w["w"]) not in SKIP: cur = w
    if not cur: return
    s = re.sub(r"[.,!?:;…-]+", "", cur["w"]).upper()
    if not s: return
    hot = any(ch.isdigit() for ch in s) or len(s) > 7 or cur["w"].endswith("!")
    paste(img, chip(s, 92, INK, AMB if hot else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.80, 1, 0.8 + 0.2 * back((T - cur["t0"]) / 0.15))

def frames(src, t0, t1, fps):
    w, h = CE.probe(src)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-to", str(t1), "-i", src, "-r", str(fps), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield Image.frombuffer("RGB", (w, h), b).copy()
def grab(src, t): return next(frames(src, t, t + 0.1, 30))
V1, V2, V3 = D + "hq1.mp4", D + "hq2.mp4", D + "hq3.mp4"
TOPIC = "O CARRASCO DO FLAMENGO"
SAVES = [0]
def hud(img):
    paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1)
    paste(img, logo("EST", 90), W / 2 - 200, 245, 1)
    n = SAVES[0]; s = chip(f"DEFESAS: {n}/3", 52, INK, AMB if n else WHITE)
    paste(img, s, W / 2 + 60, 245, 1)

def wt(i, word):
    for w in CAPS:
        if PLACE[i] - 0.05 <= w["t0"] < PLACE[i] + 5 and norm(w["w"]).startswith(norm(word)): return w["t0"] - PLACE[i]
    return 0.5

def goal2d(img, t):
    GX0, GX1, GY0, GY1 = 120, 960, 560, 1000
    d = ImageDraw.Draw(img)
    d.rectangle((0, GY1, W, GY1 + 400), fill=(40, 130, 62))
    for k in range(0, 40):
        x = GX0 + k * (GX1 - GX0) / 40; d.line((x, GY0, x, GY1), fill=(255, 255, 255, 60), width=2)
    for k in range(0, 12):
        y = GY0 + k * (GY1 - GY0) / 12; d.line((GX0, y, GX1, y), fill=(255, 255, 255, 60), width=2)
    d.rectangle((GX0 - 18, GY0 - 18, GX1 + 18, GY0), fill=WHITE); d.rectangle((GX0 - 18, GY0, GX0, GY1), fill=WHITE); d.rectangle((GX1, GY0, GX1 + 18, GY1), fill=WHITE)
    # goleiro (ilustrativo) no centro mergulhando para a ESQUERDA da tela = direita dele
    kx = W / 2; ky = GY1 - 150
    u = ease(clamp((t - 2.2) / 0.6))
    gx, gy = kx - 230 * u, ky + 30 * u
    paste(img, chip("MUSLERA", 40, INK, (255, 215, 40)), gx, gy - 170, 1)
    d.ellipse((gx - 40, gy - 130, gx + 40, gy - 50), fill=(255, 215, 40), outline=INK, width=4)
    d.rounded_rectangle((gx - 60, gy - 50, gx + 60, gy + 110), 30, fill=(255, 215, 40), outline=INK, width=4)
    names = [("JORGINHO", 0.16, 0.86), ("PAQUETÁ", 0.27, 0.9), ("B. HENRIQUE", 0.21, 0.8)]
    for k, (nm, fx, fy) in enumerate(names):
        t0 = 0.3 + k * 0.45
        if t < t0: continue
        bx, by = GX0 + fx * (GX1 - GX0), GY0 + fy * (GY1 - GY0)
        r = 30 * back(min(1, (t - t0) / 0.25)); d.ellipse((bx - r, by - r, bx + r, by + r), fill=WHITE, outline=INK, width=5)
        paste(img, chip(nm, 36, WHITE, RED), bx + 40, GY1 + 70 + k * 80, 1)
    if t > 1.6:
        rr = 190 + 8 * math.sin(t * 8); cx_, cy_ = GX0 + 0.21 * (GX1 - GX0), GY0 + 0.86 * (GY1 - GY0)
        d.ellipse((cx_ - rr, cy_ - rr * 0.7, cx_ + rr, cy_ + rr * 0.7), outline=AMB, width=10)
    pop(img, txt("MESMO CANTO!", 120, AMB), W / 2, 420, t, 0.0, 0.3, -3)
    pop(img, chip("LADO DIREITO DO MUSLERA", 50, INK, WHITE), W / 2, 1290, t, 2.8)
    paste(img, text_el("visão do batedor • posições ilustrativas", font("sb", 28), (230, 230, 230), 3), W / 2, 1360, 0.8)

CEL = grab(V3, 10.6); KICK = grab(V1, 12.3)
def blurbg(fr, dim=150):
    b = fr.resize((int(fr.width * H / fr.height), H)); x = (b.width - W) // 2
    b = b.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    b.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim))); return b

def render():
    out = D + "v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    T = [0.0]; cuts = []
    def emit(img):
        caption(img, T[0]); enc.stdin.write(img.convert("RGB").tobytes()); T[0] += 1 / 30
    def flash(img, t0):
        if 0 <= T[0] - t0 < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (T[0] - t0) / 0.12)))))
    def play(src, t0, t1, keys, until=None, speed=1.0, over=None):
        fps = 30 / speed; lt = t0; s0 = T[0]; cuts.append(s0)
        for fr in frames(src, t0, t1, fps):
            if until and T[0] >= until: break
            img, _, _ = CE.compose(fr, {"ar": 0.5625, "cx_keys": keys}, lt=lt); hud(img); flash(img, s0)
            if over: over(img, T[0] - s0, lt)
            emit(img); lt += 1 / fps
    def saved(at_src):
        def f(img, t, lt):
            if lt >= at_src:
                u = lt - at_src
                paste(img, stamp("DEFENDEU!", 120, RED), W / 2 + (8 * math.sin(u * 60) if u < 0.3 else 0), 600, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -6)
        return f
    # A 0–3.7 gancho: freeze do replay
    s0 = T[0]
    while T[0] < 3.7:
        t = T[0]; img, _, _ = CE.compose(KICK, {"ar": 0.5625, "cx": 0.38, "zoom": 1.0 + 0.03 * t})
        hud(img)
        sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
        paste(img, txt("ESSE CARA", 120, WHITE, 12), W / 2, 450, 1, sc, -3)
        paste(img, txt("PODE PARAR", 120, WHITE, 12), W / 2, 580, 1, sc, -3)
        paste(img, txt("O PALMEIRAS!", 130, AMB, 12), W / 2, 720, 1, sc, -3)
        if t > 1.6: pop(img, chip("40 ANOS", 64, INK, WHITE), W / 2, 1300, t, 1.6, 0.25, 3)
        emit(img)
    # B 3.7–7.9: Muslera (close) + card
    def card_over(img, t, lt):
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
        pop(img, txt("FERNANDO", 100, WHITE), W / 2, 470, t, 0.1); pop(img, txt("MUSLERA", 150, AMB), W / 2, 600, t, 0.25)
        pop(img, chip("GOLEIRO DO ESTUDIANTES", 52, WHITE, RED), W / 2, 740, t, 0.6)
        pop(img, chip("3 PÊNALTIS DO FLAMENGO", 60, INK, AMB), W / 2, 1180, t, wt(1, "três"), 0.25, -2)
        pop(img, chip("NO MARACANÃ", 60, WHITE, INK), W / 2, 1300, t, wt(1, "maracan"), 0.25, 2)
    play(V3, 7.7, 12.2, [[7.7, 0.62], [12.2, 0.58]], until=7.9, over=card_over)
    # C 7.9–11.7: 1º pênalti, Jorginho correndo (0.75x)
    def lab(s):
        return lambda img, t, lt: pop(img, chip(s, 56, WHITE, RED), W / 2, 420, t, 0.0)
    play(V1, 0.9, 3.75, [[0.9, 0.64], [3.3, 0.62]], until=11.7, speed=0.75, over=lab("1º • JORGINHO"))
    # D 11.7–16.4: chute + defesa + replay lento
    def d_over(img, t, lt):
        if lt >= 4.15: SAVES[0] = 1
        saved(4.15)(img, t, lt)
    play(V1, 3.3, 5.0, [[3.3, 0.62], [3.75, 0.30], [5.0, 0.27]], until=13.4, over=d_over)
    def rep(img, t, lt): paste(img, chip("REPLAY", 50, INK, AMB), W / 2, 420, 1)
    play(V1, 11.4, 12.95, [[11.4, 0.45], [12.2, 0.38], [12.95, 0.36]], until=16.4, speed=0.5, over=rep)
    # E 16.4–20.9: Paquetá
    def e_over(img, t, lt):
        lab("2º • PAQUETÁ")(img, t, lt)
        if lt >= 16.1: SAVES[0] = 2
        saved(16.1)(img, t, lt)
    play(V2, 13.6, 17.2, [[13.6, 0.6], [15.45, 0.6], [15.95, 0.3], [17.2, 0.28]], until=20.0, over=e_over)
    play(V2, 18.1, 19.1, [[18.1, 0.45]], until=20.9)
    # F 20.9–25.1(+): Bruno Henrique
    play(V3, 0.9, 2.1, [[0.9, 0.62], [2.1, 0.6]], until=22.1, over=lab("3º • B. HENRIQUE"))
    def f_over(img, t, lt):
        lab("3º • B. HENRIQUE")(img, t, lt)
        if lt >= 5.95: SAVES[0] = 3
        saved(5.95)(img, t, lt)
    play(V3, 3.9, 6.9, [[3.9, 0.6], [5.15, 0.58], [5.65, 0.3], [6.9, 0.3]], until=25.1, over=f_over)
    def conf(img, t, lt): img.alpha_composite(confetti(W, H, t))
    play(V3, 9.8, 11.2, [[9.8, 0.6], [11.2, 0.58]], until=26.5, over=conf)
    play(V3, 12.6, 14.1, [[12.6, 0.5]], until=27.95, over=conf)
    # G 27.95–32.2: gol 2D, mesmo canto
    s0 = T[0]; cuts.append(s0)
    while T[0] < 32.2:
        img = bg(W, H, "night", T[0]); goal2d(img, T[0] - s0); flash(img, s0); paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1); emit(img)
    # H 32.2–36.3: estatística
    s0 = T[0]; cuts.append(s0)
    while T[0] < 36.3:
        t = T[0] - s0; img = blurbg(CEL); img.alpha_composite(rays(W, H, W / 2, 620, T[0], (255, 80, 80), 14, 40))
        pop(img, logo("EST", 260), W / 2, 560, t, 0.0, 0.35)
        pop(img, txt("3 DEFESAS", 150, AMB), W / 2, 830, t, 0.3)
        pop(img, txt("NUMA DISPUTA", 100, WHITE), W / 2, 960, t, 0.5)
        pop(img, stamp("1ª VEZ DESDE 2016", 80, RED), W / 2, 1180, t, wt(6, "dois"), 0.25, -5)
        flash(img, s0); paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1); emit(img)
    # I 36.3–fim: pergunta
    s0 = T[0]; cuts.append(s0)
    while T[0] < TOTAL:
        t = T[0] - s0; img, _, _ = CE.compose(CEL, {"ar": 0.5625, "cx": 0.6, "zoom": 1.0 + 0.03 * t}); img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        hud(img); flash(img, s0)
        pop(img, txt("NA FINAL,", 120, WHITE), W / 2, 470, t, 0.1); pop(img, txt("BATE ONDE?", 140, AMB), W / 2, 620, t, 0.4)
        pop(img, chip("NO CANTO DELE", 70, INK, GREEN), W / 2, 1020, t, 1.2, 0.25, -3)
        pop(img, chip("NO OUTRO CANTO", 70, WHITE, RED), W / 2, 1160, t, 1.5, 0.25, 3)
        if T[0] > TOTAL - 2.5: paste(img, text_el("Música: Volatile Reaction – Kevin MacLeod (incompetech.com) CC BY 4.0", font("sb", 26), (235, 235, 235), 3), W / 2, H - 70, 0.85)
        emit(img)
    enc.stdin.close(); enc.wait()
    json.dump(cuts, open(D + "cuts.json", "w"))

HI = [(11.6, 16.35), (17.8, 25.05)]
def mix():
    SR = 44100; N = int(TOTAL * SR)
    a, sr = sf.read(D + "n/narr.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    vo = np.zeros(N, np.float32)
    for i, (s0, s1) in enumerate(SEGS):
        seg = a[int(s0 * sr): int((s1 + 0.05) * sr)]; k = int(PLACE[i] * SR); vo[k:k + len(seg)] += seg[:max(0, N - k)]
    subprocess.run(f"ffmpeg -loglevel error -y -ss 0 -t {TOTAL + 1} -i /home/claude/ep1/music/Volatile_Reaction.mp3 -ac 1 -ar 44100 {D}mus.wav", shell=True, check=True)
    m, _ = sf.read(D + "mus.wav", dtype="float32"); m = np.pad(m, (0, max(0, N - len(m))))[:N]
    m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.16
    t = np.arange(N) / SR; g = np.full(N, 0.22, np.float32)
    for a0, a1 in HI: g[(t >= a0) & (t < a1)] = 1.0
    g = np.convolve(g, np.ones(8820) / 8820, "same")
    fi = int(0.3 * SR); g[:fi] *= np.linspace(0, 1, fi); fo = int(0.8 * SR); g[-fo:] *= np.linspace(1, 0, fo)
    m = m * g
    sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
    fx = np.zeros(N, np.float32)
    def add(name, at, gn):
        s = sfxlib.load(name) * gn; k = int(max(0, at) * SR); e = min(N, k + len(s)); fx[k:e] += s[:e - k]
    for c in json.load(open(D + "cuts.json"))[1:]: add("whoosh_2", c - 0.1, 0.14)
    add("tambor_impacto", 0.0, 0.4)
    for at in (12.55, 19.15, 23.65): add("tambor_impacto", at, 0.35); add("torcida_aww", at + 0.1, 0.18)
    add("torcida_comemora", 25.1, 0.15); add("tambor_impacto", 32.2 + 2.6, 0.3)
    out = vo + m + fx; out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(D + "mix.wav", out, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {D}mixn.wav", shell=True, check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}v.mp4 -i {D}mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest {D}final.mp4", shell=True, check=True)

if __name__ == "__main__":
    if sys.argv[1] == "render": render(); mix()
    elif sys.argv[1] == "mix": mix()
