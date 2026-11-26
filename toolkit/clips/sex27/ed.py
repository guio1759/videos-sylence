import sys, json, math, subprocess, re, difflib
sys.path.insert(0, "/home/claude/ed27"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/clips")
from engine import *
import clipedit as CE
import numpy as np, soundfile as sf
from nscript import GAL
D = "/home/claude/ed27/"
J = json.load(open(D + "n/words.json")); SEGS = J["segs"]
PLACE = [0.0, 3.6, 7.1, 10.4, 15.0, 23.6, 29.8, 36.7]
TOTAL = PLACE[7] + (SEGS[7][1] - SEGS[7][0]) + 0.7
SH = [PLACE[i] - SEGS[i][0] for i in range(len(SEGS))]
MUSIC, MOFF = "Clash_Defiant", 0.0
HI = [(18.7, 23.5)]
def build_caps():
    caps = []
    for i, (s0, s1) in enumerate(SEGS):
        sw = re.findall(r"\S+", GAL[i][0]); wh = [w for w in J["words"] if s0 - 0.15 <= w["t0"] < s1 + 0.05]
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
SKIP = {"o", "a", "e", "de", "da", "do", "no", "na", "os", "as", "em", "se", "um", "uma", "que", "pra", "pro", "com", "aos", "dos", "mesmos"}
def caption(img, T):
    cur = None
    for w in CAPS:
        if w["t0"] - 0.03 <= T < w["t1"] + 0.12 and norm(w["w"]) not in SKIP: cur = w
    if not cur: return
    s = re.sub(r"[.,!?:;…-]+", "", cur["w"]).upper()
    if not s: return
    hot = any(ch.isdigit() for ch in s) or len(s) > 7 or cur["w"].endswith("!")
    paste(img, chip(s, 92, INK, AMB if hot else WHITE, "blk", 0.5, 0.25), W / 2, H * 0.80, 1, 0.8 + 0.2 * back((T - cur["t0"]) / 0.15))
def wt(i, word):
    for w in CAPS:
        if PLACE[i] - 0.05 <= w["t0"] < PLACE[i] + 7 and norm(w["w"]).startswith(norm(word)): return w["t0"] - PLACE[i]
    return 0.5
def frames(src, t0, t1, fps):
    w, h = CE.probe(src)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-to", str(t1), "-i", src, "-r", str(fps), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield Image.frombuffer("RGB", (w, h), b).copy()
def grab(src, t): return next(frames(src, t, t + 0.1, 30))
def redcard(h, rot=0):
    h = int(h); w = int(h * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w, h), 14, fill=RED, outline=INK, width=6); return im
CU, KA, EX = D + "cuello.mp4", D + "kaio.mp4", D + "expulsao.mp4"
TOPIC = "O CORINTHIANS ENTREGOU"
ST = {"g": (0, 0), "men": False}
def hud(img):
    paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1)
    ga, gb = ST["g"]
    paste(img, logo("CAM", 86), W / 2 - 190, 245, 1); paste(img, logo("COR", 86), W / 2 + 190, 245, 1)
    paste(img, chip(f"{ga} x {gb}", 64, INK, WHITE), W / 2, 245, 1)
    if ST["men"]: paste(img, chip("10 x 11", 40, WHITE, RED), W / 2, 330, 1)
FIN = grab(CU, 25.4); CORF = grab(KA, 11.6)
def blurbg(fr, dim=150):
    b = fr.resize((int(fr.width * H / fr.height), H)); x = (b.width - W) // 2
    b = b.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    b.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim))); return b
def render():
    out = D + "v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    T = [0.0]; cuts = []
    def emit(img):
        caption(img, T[0])
        if T[0] > TOTAL - 2.5: paste(img, text_el(f"Música: {MUSIC.replace('_', ' ')} – Kevin MacLeod (incompetech.com) CC BY 4.0", font("sb", 26), (235, 235, 235), 3), W / 2, H - 70, 0.85)
        enc.stdin.write(img.convert("RGB").tobytes()); T[0] += 1 / 30
    def flash(img, t0):
        if 0 <= T[0] - t0 < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (T[0] - t0) / 0.12)))))
    def play(src, t0, t1, keys, until=None, speed=1.0, over=None, ar=0.5625, zoom=1.0):
        fps = 30 / speed; lt = t0; s0 = T[0]; cuts.append(s0)
        for fr in frames(src, t0, t1, fps):
            if until and T[0] >= until: break
            img, _, _ = CE.compose(fr, {"ar": ar, "cx_keys": keys, "zoom": zoom}, lt=lt); img = img.convert("RGBA"); hud(img); flash(img, s0)
            if over: over(img, T[0] - s0, lt)
            emit(img); lt += 1 / fps
        last = fr
        while until and T[0] < until:  # segura o último quadro
            img, _, _ = CE.compose(last, {"ar": ar, "cx_keys": keys, "zoom": zoom}, lt=lt); img = img.convert("RGBA"); hud(img)
            if over: over(img, T[0] - s0, lt)
            emit(img)
    def lab(s, col=RED, fg=WHITE): return lambda img, t, lt: pop(img, chip(s, 54, fg, col), W / 2, 420, t, 0.0)
    # A gancho (0–3.6): bola na rede, freeze
    s0 = T[0]; ST["g"] = (1, 1); ST["men"] = True
    while T[0] < PLACE[1]:
        t = T[0]; img, _, _ = CE.compose(FIN, {"ar": 0.5625, "cx": 0.5, "zoom": 1.05 + 0.04 * t}); img = img.convert("RGBA")
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60))); hud(img)
        sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
        paste(img, txt("COM UM", 120, WHITE, 12), W / 2, 500, 1, sc, -3)
        paste(img, txt("A MAIS...", 120, WHITE, 12), W / 2, 630, 1, sc, -3)
        pop(img, stamp("ENTREGOU!", 130, RED), W / 2, 820, t, wt(0, "entregar") - 0.1, 0.25, -6)
        pop(img, chip("47' DO 2º TEMPO", 56, INK, AMB), W / 2, 1240, t, wt(0, "último") - 0.1, 0.25, 3)
        emit(img)
    ST["g"] = (0, 0); ST["men"] = False
    # B entrada dura (3.6–7.1)
    def b_over(img, t, lt):
        lab("2º TEMPO • ATLÉTICO x CORINTHIANS", INK, WHITE)(img, t, lt)
        if lt >= 1.0: pop(img, chip("T. BORBAS", 56, WHITE, (30, 30, 30)), 300, 1120, t, 1.0 / 0.75 - 0.2)
        if lt >= 1.3: pop(img, chip("KAIO CÉSAR", 56, INK, WHITE), 780, 1040, t, 1.3 / 0.75 - 0.2)
    play(EX, 0.0, 2.4, [[0.0, 0.5], [2.4, 0.58]], until=PLACE[2], speed=0.72, over=b_over)
    # C VAR + vermelho (7.1–10.4)
    def var_over(img, t, lt): paste(img, chip("VAR", 70, WHITE, (40, 40, 160)), W / 2, 420, 1)
    play(EX, 5.0, 6.9, [[5.0, 0.72], [6.9, 0.72]], until=PLACE[2] + 1.6, over=var_over)
    def red_over(img, t, lt):
        if lt >= 16.75:
            ST["men"] = True; u = lt - 16.75
            paste(img, redcard(260), W / 2 + 230, 900, 1, 0.5 + 0.5 * back(min(1, u / 0.25)), 12)
            pop(img, stamp("EXPULSO!", 120, RED), W / 2, 620, t, 0.0 if u > 0.25 else 0.0, 0.25, -6)
    play(EX, 16.3, 17.8, [[16.3, 0.55]], until=PLACE[2] + 2.9, over=red_over)
    play(EX, 18.0, 18.5, [[18.0, 0.38]], until=PLACE[3])
    # D gol do Kaio (10.4–15.0)
    def k_over(img, t, lt):
        if lt >= 6.6: ST["g"] = (0, 1); pop(img, stamp("GOL DO CORINTHIANS", 80, WHITE), W / 2, 600, t, 6.6 - 5.0 - 0.0, 0.25, -4)
    play(KA, 5.0, 7.2, [[5.0, 0.4], [7.2, 0.3]], until=PLACE[3] + 2.2, over=k_over, ar=0.8)
    def cel(img, t, lt): pop(img, chip("FESTA NO BANCO", 56, INK, WHITE), W / 2, 420, t, 0.0)
    play(KA, 9.6, 12.0, [[9.6, 0.5], [12.0, 0.55]], until=PLACE[4], over=cel)
    # E o último lance (15.0–23.6): narração, depois música sobe
    def e_over(img, t, lt):
        pop(img, chip("2º TEMPO • 47'", 58, INK, AMB), W / 2, 420, t, 0.0)
        if lt >= 4.75:
            ST["g"] = (1, 1); u = lt - 4.75
            paste(img, txt("GOOOL", 190, AMB, 16), W / 2 + (10 * math.sin(u * 60) if u < 0.3 else 0), 700, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -5)
            pop(img, chip("DO GALO!", 80, WHITE, INK), W / 2, 880, t, 4.75 - 0.0 + 0.2, 0.25, 3)
    play(CU, 0.0, 5.6, [[0.0, 0.56], [3.0, 0.62], [4.5, 0.7], [5.6, 0.7]], until=PLACE[4] + 5.6, over=e_over, ar=0.8)
    def c_over(img, t, lt):
        img.alpha_composite(confetti(W, H, t)); pop(img, chip("CUELLO", 70, INK, AMB), W / 2, 420, t, 0.2)
    play(CU, 7.5, 10.5, [[7.5, 0.55], [8.5, 0.65], [9.5, 0.55], [10.5, 0.55]], until=PLACE[5], over=c_over)
    # F replay (23.6–29.8)
    def r_over(img, t, lt): paste(img, chip("REPLAY", 50, INK, AMB), W / 2, 420, 1)
    play(CU, 20.9, 23.5, [[20.9, 0.6], [22.3, 0.56], [23.5, 0.45]], until=PLACE[5] + 3.4, speed=0.78, over=r_over)
    def d_over(img, t, lt):
        r_over(img, t, lt)
        if lt >= 24.75: pop(img, stamp("DESVIOU!", 120, RED), W / 2, 640, t, (24.75 - 24.2) / 0.5, 0.25, -6)
    play(CU, 24.2, 25.7, [[24.2, 0.42], [25.0, 0.5], [25.7, 0.55]], until=PLACE[6], speed=0.5, over=d_over)
    # G placar e tabela (29.8–36.7)
    s0 = T[0]; cuts.append(s0); BG = blurbg(FIN)
    while T[0] < PLACE[7]:
        t = T[0] - s0; img = BG.copy(); img.alpha_composite(rays(W, H, W / 2, 700, T[0], (255, 220, 140), 14, 35))
        pop(img, logo("CAM", 200), W / 2 - 280, 560, t, 0.0); pop(img, logo("COR", 200), W / 2 + 280, 560, t, 0.1)
        pop(img, txt("1 x 1", 170, WHITE), W / 2, 560, t, 0.2)
        pop(img, chip("COM 10 JOGADORES", 62, WHITE, RED), W / 2, 760, t, wt(6, "dez") - 0.2, 0.25, -3)
        tc = wt(6, "corinthians") - 0.2
        if t > tc:
            pop(img, chip("15º  CORINTHIANS  41 PTS", 56, INK, WHITE), W / 2, 1000, t, tc)
            pop(img, chip("17º  MIRASSOL  41 PTS", 56, WHITE, RED), W / 2, 1110, t, wt(6, "primeiro") - 0.2)
            pop(img, stamp("Z4 COLADO!", 96, RED), W / 2, 1260, t, wt(6, "rebaixamento") - 0.1, 0.25, -5)
        flash(img, s0); paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1); emit(img)
    # H pergunta
    s0 = T[0]; cuts.append(s0)
    while T[0] < TOTAL:
        t = T[0] - s0; img, _, _ = CE.compose(CORF, {"ar": 0.5625, "cx": 0.5, "zoom": 1.0 + 0.03 * t}); img = img.convert("RGBA")
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120))); hud(img); flash(img, s0)
        pop(img, txt("O CORINTHIANS", 110, WHITE), W / 2, 470, t, 0.1); pop(img, txt("ESCAPA?", 150, AMB), W / 2, 620, t, 0.4)
        pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1000, t, wt(7, "sim") - 0.2, 0.25, -4)
        pop(img, chip("NÃO", 110, WHITE, RED), 750, 1000, t, wt(7, "não") - 0.2, 0.25, 4)
        pop(img, chip("COMENTA AÍ", 60, INK, WHITE), W / 2, 1190, t, wt(7, "comenta") - 0.1)
        emit(img)
    enc.stdin.close(); enc.wait()
    json.dump(cuts, open(D + "cuts.json", "w"))
def mix():
    SR = 44100; N = int(TOTAL * SR)
    a, sr = sf.read(D + "n/narr.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    vo = np.zeros(N, np.float32)
    for i, (s0, s1) in enumerate(SEGS):
        seg = a[int(s0 * sr): int((s1 + 0.05) * sr)]; k = int(PLACE[i] * SR); vo[k:k + len(seg)] += seg[:max(0, N - k)]
    subprocess.run(f"ffmpeg -loglevel error -y -ss {MOFF} -t {TOTAL + 1} -i /home/claude/ep1/music/{MUSIC}.mp3 -ac 1 -ar 44100 {D}mus.wav", shell=True, check=True)
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
    for c in json.load(open(D + "cuts.json"))[1:]: add("whoosh_2", c - 0.1, 0.12)
    add("tambor_impacto", 0.0, 0.4); add("whoosh_boom", wt(0, "entregar"), 0.3)
    add("apito_juiz", PLACE[2] + 1.6 + 0.45, 0.25); add("tambor_impacto", PLACE[2] + 1.6 + 0.45, 0.3)
    add("torcida_grita_gol", PLACE[3] + 1.6, 0.2)
    add("torcida_reacao_gol", PLACE[4] + 4.75, 0.35); add("tambor_impacto", PLACE[4] + 4.75, 0.35)
    add("tambor_impacto", PLACE[5] + 3.4 + 1.1, 0.3); add("tambor_impacto", PLACE[6] + wt(6, "rebaixamento"), 0.3)
    out = vo + m + fx; out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(D + "mix.wav", out, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {D}mixn.wav", shell=True, check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}v.mp4 -i {D}mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest {D}final.mp4", shell=True, check=True)
if __name__ == "__main__":
    if sys.argv[1] == "render": render(); mix()
    elif sys.argv[1] == "mix": mix()
