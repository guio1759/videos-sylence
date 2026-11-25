import sys, json, math, subprocess, re, difflib
sys.path.insert(0, "/home/claude/ed26"); sys.path.insert(0, "/home/claude/videos-sylence/toolkit/clips")
from engine import *
import clipedit as CE
import numpy as np, soundfile as sf
from nscript import NEY
D = "/home/claude/ed26/"
J = json.load(open(D + "n/words.json")); SEGS = J["segs"]
VIC0, VICL = 10.75, 9.8
PLACE = [0.0, 3.62, 20.65, 25.75, 31.85, 34.35]
TOTAL = 38.1
SH = [PLACE[i] - SEGS[i][0] for i in range(len(SEGS))]
MUSIC, MOFF = "Hitman", 50.95
def build_caps():
    caps = []
    for i, (s0, s1) in enumerate(SEGS):
        sw = re.findall(r"\S+", NEY[i][0]); wh = [w for w in J["words"] if s0 - 0.15 <= w["t0"] < s1 + 0.05]
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
class _C: pass
CAPOBJ = Short.__new__(Short); CAPOBJ.caps = CAPS; CAPOBJ._chunks = None
def caption(img, T): Short.caption(CAPOBJ, img, T)
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
LANCE = D + "hq.mp4"; FR0 = grab(LANCE, 0.3); FRE = grab(LANCE, 4.9)
TOPIC = "SANTOS 0 x 2 GRÊMIO"
def hud(img):
    paste(img, tag_box(TOPIC, 44, WHITE, INK), W / 2, 130, 1)
def blurbg(fr, dim=150):
    b = fr.resize((int(fr.width * H / fr.height), H)); x = (b.width - W) // 2
    b = b.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    b.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim))); return b
def shot(path, w, censor=None):
    im = Image.open(path).convert("RGBA")
    if censor:
        d = ImageDraw.Draw(im); d.rounded_rectangle(censor, 10, fill=(232, 58, 58)); d.text(((censor[0] + censor[2]) / 2, (censor[1] + censor[3]) / 2), "#@!", font=font("blk", 40), fill=WHITE, anchor="mm")
    im = im.resize((int(w), int(im.height * w / im.width)), Image.LANCZOS)
    p = Image.new("RGBA", (im.width + 16, im.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(p).rounded_rectangle((0, 0, p.width - 1, p.height - 1), 30, fill=(255, 255, 255, 255))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 24, fill=255)
    p.paste(im, (8, 8), m); return p
C1 = shot(D + "c1.jpg", 980); C2 = shot(D + "c2.jpg", 980, (528, 92, 612, 152))
def scorebox(a, b, ga, gb, sz=150):
    w = int(sz * 5.6); h = int(sz * 1.6); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(15, 18, 26, 240), outline=WHITE, width=5)
    la, lb = logo(a, sz), logo(b, sz)
    im.alpha_composite(la, (int(sz * 0.9 - la.width / 2), int(h / 2 - la.height / 2))); im.alpha_composite(lb, (int(w - sz * 0.9 - lb.width / 2), int(h / 2 - lb.height / 2)))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", sz * 0.85), fill=WHITE, anchor="mm"); return im
def shake(t, t0, amp=18, dur=0.25):
    if t < t0 or t > t0 + dur: return 0
    return amp * (1 - (t - t0) / dur) * math.sin((t - t0) * 90)
HEADS = [(0.335, 0.285), (0.47, 0.28)]
def render():
    out = D + "v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    T = [0.0]; cuts = []
    def emit(img, cap=True):
        if cap: caption(img, T[0])
        if T[0] > TOTAL - 2.5: paste(img, text_el(f"Música: {MUSIC} – Kevin MacLeod (incompetech.com) CC BY 4.0", font("sb", 26), (235, 235, 235), 3), W / 2, H - 70, 0.85)
        enc.stdin.write(img.convert("RGB").tobytes()); T[0] += 1 / 30
    def flash(img, t0):
        if 0 <= T[0] - t0 < 0.12: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (T[0] - t0) / 0.12)))))
    KEYS = [[0.0, 0.42], [1.3, 0.5], [1.8, 0.48], [2.3, 0.36], [2.8, 0.31], [3.3, 0.33], [3.8, 0.3], [4.3, 0.22], [4.8, 0.24], [5.4, 0.3]]
    def play(t0, t1, until, speed=1.0, over=None, zoom=1.0):
        fps = 30 / speed; lt = t0; s0 = T[0]; cuts.append(s0)
        for fr in frames(LANCE, t0, t1, fps):
            if T[0] >= until: break
            img, top, mh = CE.compose(fr, {"ar": 0.5625, "cx_keys": KEYS, "zoom": zoom}, lt=lt); hud(img); flash(img, s0)
            if over: over(img, T[0] - s0, lt)
            emit(img); lt += 1 / fps
        while T[0] < until:
            img, _, _ = CE.compose(fr, {"ar": 0.5625, "cx_keys": KEYS}, lt=lt); hud(img)
            if over: over(img, T[0] - s0, lt)
            emit(img)
    # A gancho: freeze nos platinados
    while T[0] < PLACE[1]:
        t = T[0]; z = 1.25 + 0.012 * t
        img, top, mh = CE.compose(FR0, {"ar": 0.5625, "cx": 0.41, "cy": 0.35, "zoom": z})
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60))); hud(img)
        sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
        paste(img, txt("MARRA DE", 120, WHITE, 12), W / 2, 330, 1, sc, -3)
        paste(img, txt("CAMPEÃO", 150, AMB, 14), W / 2, 470, 1, sc, -3)
        d = ImageDraw.Draw(img)
        if t > 0.5:
            r = 100 * back(min(1, (t - 0.5) / 0.3))
            for hx, hy in ((430, 850), (664, 885)): d.ellipse((hx - r, hy - r, hx + r, hy + r), outline=AMB, width=10)
            pop(img, chip("PLATINADOS", 64, INK, AMB), W / 2, 1140, t, 0.6, 0.25, 3)
        pop(img, stamp("EM 9º LUGAR", 110, RED), W / 2, 1300, t, wt(0, "nono") - 0.15, 0.25, -6 + shake(t, wt(0, "nono"), 8))
        emit(img)
    # B firula em câmera lenta + rápida
    def b_over(img, t, lt):
        pop(img, chip("A FIRULA", 70, INK, AMB), W / 2, 330, t, 0.1, 0.25, -3)
        if lt > 2.3: paste(img, chip("CÂMERA LENTA", 44, WHITE, INK), W / 2, 440, 1)
    play(0.0, 2.6, PLACE[1] + 2.6 / 0.6, 0.6, b_over)
    def b2(img, t, lt): pop(img, chip("E SEGUE O BAILE...", 60, INK, WHITE), W / 2, 330, t, 0.1, 0.25, 2)
    play(2.6, 5.4, VIC0, 1.0, b2)
    # C Vicari (áudio dele)
    s0 = T[0]; cuts.append(s0); VF = list(frames(D + "vic.mp4", 0, VICL + 0.2, 30)); k = 0
    bgv = blurbg(FRE, 170)
    while T[0] < VIC0 + VICL:
        t = T[0] - s0; img = bgv.copy(); fr = VF[min(k, len(VF) - 1)]; k += 1
        card = fr.resize((800, int(fr.height * 860 / fr.width)), Image.LANCZOS).convert("RGBA")
        sc = 0.9 + 0.1 * back(min(1, t / 0.3)) + 0.02 * t / VICL
        paste(img, card, W / 2, 960, 1, sc)
        pop(img, chip("A TV NÃO PERDOOU", 64, INK, AMB), W / 2, 300, t, 0.1, 0.25, -3)
        if t > 3.0: pop(img, stamp("MARRA NO 9º LUGAR?!", 76, RED), W / 2, 1640, t, 3.0, 0.25, -5)
        flash(img, s0); hud(img); emit(img, cap=False)
    # D placar
    s0 = T[0]; cuts.append(s0)
    while T[0] < PLACE[3] - 0.1:
        t = T[0] - s0; img = blurbg(FRE, 120); img.alpha_composite(rays(W, H, W / 2, 800, T[0], (120, 190, 255), 14, 45))
        pop(img, chip("MORUMBIS • 23/11", 58, INK, WHITE), W / 2, 330, t, 0.0)
        paste(img, scorebox("SAN", "GRE", 0, 2, 150), W / 2 + shake(t, wt(2, "dois"), 14), 640, 1, 0.85 + 0.15 * back(t / 0.25))
        pop(img, chip("AMUZU • 1º TEMPO", 52, WHITE, (60, 130, 200)), W / 2, 860, t, wt(2, "dois"), 0.25, -2)
        pop(img, chip("BRAITHWAITE • PÊNALTI", 52, WHITE, (60, 130, 200)), W / 2, 960, t, wt(2, "dois") + 0.3, 0.25, 2)
        pop(img, logo("GRE", 220), W / 2, 1200, t, wt(2, "saiu") - 0.3)
        pop(img, stamp("SAIU DO Z4", 100, GREEN), W / 2, 1400, t, wt(2, "z4") - 0.1, 0.25, -5)
        flash(img, s0); hud(img); emit(img)
    # E comentário 1
    s0 = T[0]; cuts.append(s0)
    while T[0] < PLACE[4] - 0.1:
        t = T[0] - s0; img = bg(W, H, "dark", T[0])
        pop(img, chip("DEPOIS DO JOGO...", 62, INK, WHITE), W / 2, 330, t, 0.0)
        pop(img, logo("SAN", 200), W / 2, 560, t, 0.2)
        pop(img, chip("TORCEDOR CRITICA O TIME", 54, WHITE, RED), W / 2, 760, t, wt(3, "criticou") - 0.2, 0.25, -2)
        tr = wt(3, "neymar") - 0.2
        if t > tr: paste(img, C1, W / 2, 1050, 1, 0.3 + 0.7 * back(min(1, (t - tr) / 0.3)), shake(t, tr + 0.3, 4))
        pop(img, chip("NEYMAR RESPONDE", 60, INK, AMB), W / 2, 1300, t, tr + 0.2, 0.25, 3)
        flash(img, s0); hud(img); emit(img)
    # F comentário 2
    s0 = T[0]; cuts.append(s0)
    while T[0] < PLACE[5] - 0.1:
        t = T[0] - s0; img = bg(W, H, "red", T[0])
        paste(img, C2, W / 2 + shake(t, 0.2, 10), 800, 1, 0.3 + 0.7 * back(min(1, t / 0.3)))
        pop(img, stamp("XINGOU!", 120, AMB), W / 2, 1250, t, wt(4, "xingou") - 0.1, 0.25, -6)
        flash(img, s0); hud(img); emit(img)
    # G CTA
    s0 = T[0]; cuts.append(s0)
    while T[0] < TOTAL:
        t = T[0] - s0; img, _, _ = CE.compose(FR0, {"ar": 0.5625, "cx": 0.41, "cy": 0.35, "zoom": 1.3 + 0.03 * t}); img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120))); hud(img)
        pop(img, txt("O NEYMAR", 120, WHITE), W / 2, 420, t, 0.0); pop(img, txt("ERROU?", 160, AMB), W / 2, 570, t, 0.3)
        pop(img, chip("SIM", 120, WHITE, GREEN), 330, 900, t, wt(5, "sim") - 0.2, 0.25, -4)
        pop(img, chip("NÃO", 120, WHITE, RED), 750, 900, t, wt(5, "não") - 0.2, 0.25, 4)
        pop(img, chip("COMENTA AÍ", 64, INK, WHITE), W / 2, 1110, t, wt(5, "comenta") - 0.1)
        flash(img, s0); emit(img)
    enc.stdin.close(); enc.wait(); json.dump(cuts, open(D + "cuts.json", "w"))
HI = [(PLACE[1] + 2.0, VIC0 - 0.1)]
def mix():
    SR = 44100; N = int(TOTAL * SR)
    a, sr = sf.read(D + "n/narr.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    vo = np.zeros(N, np.float32)
    for i, (s0, s1) in enumerate(SEGS):
        seg = a[int(s0 * sr): int((s1 + 0.05) * sr)]; k = int(PLACE[i] * SR); vo[k:k + len(seg)] += seg[:max(0, N - k)]
    v, _ = sf.read(D + "vic.wav", dtype="float32"); v = v / (np.abs(v).max() + 1e-9) * 0.8
    k = int(VIC0 * SR); vo[k:k + len(v)] += v[:N - k]
    subprocess.run(f"ffmpeg -loglevel error -y -ss {MOFF} -t {TOTAL + 1} -i /home/claude/ep1/music/{MUSIC}.mp3 -ac 1 -ar 44100 {D}mus.wav", shell=True, check=True)
    m, _ = sf.read(D + "mus.wav", dtype="float32"); m = np.pad(m, (0, max(0, N - len(m))))[:N]
    m = m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.16
    t = np.arange(N) / SR; g = np.full(N, 0.22, np.float32)
    for a0, a1 in HI: g[(t >= a0) & (t < a1)] = 1.0
    g[(t >= VIC0) & (t < VIC0 + VICL)] = 0.15
    g = np.convolve(g, np.ones(8820) / 8820, "same")
    fi = int(0.3 * SR); g[:fi] *= np.linspace(0, 1, fi); fo = int(0.8 * SR); g[-fo:] *= np.linspace(1, 0, fo)
    m = m * g
    sys.path.insert(0, "/home/claude/work/sfx"); import sfxlib
    fx = np.zeros(N, np.float32)
    def add(name, at, gn):
        s = sfxlib.load(name) * gn; k = int(max(0, at) * SR); e = min(N, k + len(s)); fx[k:e] += s[:e - k]
    for c in json.load(open(D + "cuts.json"))[1:]: add("whoosh_2", c - 0.1, 0.14)
    add("tambor_impacto", 0.0, 0.4); add("whoosh_boom", wt(0, "nono"), 0.3)
    add("tambor_impacto", PLACE[2] + wt(2, "dois"), 0.35); add("torcida_comemora", PLACE[2] + wt(2, "saiu"), 0.12)
    add("camera_click", PLACE[3] + wt(3, "neymar"), 0.3); add("tambor_impacto", PLACE[4] + 0.2, 0.3); add("torcida_aww", PLACE[4] + wt(4, "xingou"), 0.15)
    out = vo + m + fx; out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(D + "mix.wav", out, SR)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}mix.wav -af loudnorm=I=-14:TP=-1.5 -ar 44100 {D}mixn.wav", shell=True, check=True)
    subprocess.run(f"ffmpeg -loglevel error -y -i {D}v.mp4 -i {D}mixn.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest {D}final.mp4", shell=True, check=True)
if __name__ == "__main__":
    if sys.argv[1] == "render": render(); mix()
    elif sys.argv[1] == "mix": mix()
