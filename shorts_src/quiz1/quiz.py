from extra import *
from scripts import QUIZ
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
D = "/home/claude/quiz/img/"
def badge(name, c1, c2, h=150, stripes=False):
    h = int(h); w = int(h * 0.86); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); m = Image.new("L", (w, h), 0); dm = ImageDraw.Draw(m)
    dm.polygon([(4, 4), (w - 4, 4), (w - 4, h * 0.55), (w / 2, h - 4), (4, h * 0.55)], fill=255)
    f = Image.new("RGBA", (w, h), c1); d = ImageDraw.Draw(f)
    if stripes:
        for x in range(0, w, int(w / 5)): d.rectangle((x, 0, x + w / 10, h), fill=c2)
    else: d.rectangle((0, h * 0.62, w, h), fill=c2)
    im.paste(f, (0, 0), m); d = ImageDraw.Draw(im)
    d.polygon([(4, 4), (w - 4, 4), (w - 4, h * 0.55), (w / 2, h - 4), (4, h * 0.55)], outline=WHITE, width=6)
    fs = int(h * 0.2)
    while font("blk", fs).getlength(name) > w * 0.86: fs -= 2
    d.text((w / 2, h * 0.4), name, font=font("blk", fs), fill=WHITE, anchor="mm", stroke_width=4, stroke_fill=INK)
    return im
def crest(k, h=150):
    if k in ("PAL", "CRU", "CAP", "FLU", "CAM", "POR", "GRE", "REM"): return logo(k, h)
    return {"MCI": badge("CITY", (108, 171, 221), (28, 44, 91), h), "ARS": badge("ARSENAL", (219, 0, 7), (255, 255, 255), h),
            "BAR": badge("BARÇA", (165, 0, 68), (0, 77, 152), h, True), "BET": badge("BETIS", (0, 150, 74), (255, 255, 255), h, True),
            "NFO": badge("FOREST", (221, 0, 0), (255, 255, 255), h), "OLY": badge("OLYMPIACOS", (220, 20, 20), (255, 255, 255), h, True),
            "RBR": badge("RB BRASIL", (255, 255, 255), (210, 0, 40), h)}[k]
R = [  # (seg pergunta, nome, nível, cor, carreira, foto)
    (1, "GABRIEL JESUS", "FÁCIL", GREEN, ["PAL", "MCI", "ARS"], "jesus"),
    (3, "VITOR ROQUE", "MÉDIO", AMB, ["CRU", "CAP", "BAR", "BET", "PAL"], "roque"),
    (5, "GUSTAVO SCARPA", "DIFÍCIL", (255, 120, 40), ["FLU", "RBR", "PAL", "NFO", "OLY", "CAM"], "scarpa"),
    (7, "WEVERTON", "SÓ RAIZ", RED, ["POR", "CAP", "PAL", "GRE"], "weverton")]
def wt(i, w, d=0.5):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return d
@functools.lru_cache(8)
def face(k, sz):
    p = D + k + ".jpg"
    if not os.path.exists(p): return None
    im = Image.open(p).convert("RGB"); w, h = im.size; s = min(w, h); im = im.crop(((w - s) // 2, 0 if h > w else (h - s) // 2, (w - s) // 2 + s, (0 if h > w else (h - s) // 2) + s)).resize((sz, sz), Image.LANCZOS)
    m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse((0, 0, sz - 1, sz - 1), fill=255); o = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); o.paste(im, (0, 0), m); return o
def ring(sz, frac, n):
    sz = int(sz); im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((8, 8, sz - 8, sz - 8), fill=(15, 18, 26, 235), outline=(70, 70, 80), width=14)
    col = GREEN if n == 3 else (AMB if n == 2 else RED)
    d.arc((8, 8, sz - 8, sz - 8), -90, -90 + 360 * frac, fill=col, width=14)
    d.text((sz / 2, sz / 2), str(n), font=font("blk", int(sz * 0.5)), fill=WHITE, anchor="mm"); return im
def mystery(sz, t):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, sz - 1, sz - 1), fill=(20, 24, 34, 255), outline=WHITE, width=10)
    p = person(int(sz * 0.8), (60, 66, 80)); im.alpha_composite(p, ((sz - p.width) // 2, int(sz * 0.2)))
    m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse((0, 0, sz - 1, sz - 1), fill=255); o = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); o.paste(im, (0, 0), m)
    ImageDraw.Draw(o).text((sz / 2, sz * 0.48), "?", font=font("blk", int(sz * 0.5)), fill=AMB, anchor="mm", stroke_width=8, stroke_fill=INK); return o
def career(img, ks, y, t, t0, step=0.32):
    n = len(ks); h = 175 if n <= 4 else (150 if n == 5 else 128); gap = min(240, 980 / n); x0 = cx - gap * (n - 1) / 2
    d = ImageDraw.Draw(img)
    for j, k in enumerate(ks):
        x = x0 + gap * j; tj = t0 + step * j
        if j and t > tj - 0.05:
            xa = x - gap / 2; d.polygon([(xa - 14, y - 16), (xa + 12, y), (xa - 14, y + 16)], fill=WHITE)
        pop(img, crest(k, h), x, y, t, tj, 0.25, (-4, 3, -3, 4, -2, 3)[j])
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 820, T, (150, 255, 170), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("SÓ RAIZ ACERTA", 120, WHITE, 14), cx + shake(t, 0.02, 12), 430, 1, sc, -3)
    for j, (_, _, _, _, _, k) in enumerate(R):
        paste(img, mystery(200, t), 170 + 247 * j, 730, 1, sc, (-5, 4, -3, 5)[j])
    pop(img, logo("PAL", 230), cx, 1030, t, wt(0, "palmeiras", 1.2) - 0.2, 0.3, -3)
    tv = wt(0, "valendo", 4.3) - 0.15
    if t < tv: pop(img, chip("PELOS CLUBES", 62, INK, AMB), cx, 1240, t, wt(0, "clubes", 3.0) - 0.2, 0.25, 3)
    pop(img, stamp("VALENDO!", 110, GREEN), cx, 1240, t, wt(0, "valendo", 4.3) - 0.15, 0.25, -5) if t > wt(0, "valendo", 4.3) - 0.15 else None
def make_q(r):
    i, name, lvl, col, ks, ph = r
    def sq(img, t, T):
        pop(img, chip(f"{R.index(r) + 1}/4", 60, WHITE, INK), 200, 330, t, 0.0, 0.25, -3)
        pop(img, chip(lvl, 60, INK if col in (GREEN, AMB) else WHITE, col), W - 260, 330, t, 0.05, 0.25, 3)
        sz = 440; paste(img, mystery(sz, t), cx + shake(t, S.segs[i][1] - S.segs[i][0] + 2.0, 10, 1.2), 650, 1)
        career(img, ks, 1010, t, 0.25)
        g0 = S.segs[i][1] - S.segs[i][0]; g1 = S.segs[i + 1][0] - S.segs[i][0]
        if t > g0:
            u = (t - g0) / (g1 - g0); n = 3 - min(2, int(u * 3)); paste(img, ring(230, 1 - u, n), cx, 1250, 1, 1.0 + 0.08 * max(0, 1 - ((u * 3) % 1) * 4))
    def sa(img, t, T):
        img.alpha_composite(rays(W, H, cx, 650, T, (150, 255, 170), 14, 60))
        if t < 0.18: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(220 * (1 - t / 0.18)))))
        pop(img, chip(f"{R.index(r) + 1}/4", 60, WHITE, INK), 200, 330, t, -1)
        f = face(ph, 440); pop(img, f if f else jersey("", name, 380, (20, 120, 60)), cx, 650, t, 0.0, 0.3, -2)
        pop(img, check(120, True), cx + 200, 820, t, 0.1)
        pop(img, txt(name, 96 if len(name) < 13 else 84, WHITE, 12), cx, 920, t, 0.05, 0.25, 2)
        career(img, ks, 1110, 9, 0)
    return sq, sa
SC = [s0]
for r in R: SC += list(make_q(r))
def s9(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 230, 120), 14, 45))
    pop(img, txt("QUANTOS VOCÊ", 110, WHITE, 12), cx, 450, t, 0.0, 0.25, -2); pop(img, txt("ACERTOU?", 140, AMB, 14), cx, 600, t, 0.1, 0.25, 2)
    for j in range(5): pop(img, chip(str(j), 90, INK if j < 4 else WHITE, WHITE if j < 4 else GREEN), 150 + 195 * j, 850, t, 0.3 + 0.12 * j, 0.25, (j % 2) * 6 - 3)
    pop(img, chip("COMENTA AÍ 👇".replace(" 👇", ""), 64, INK, AMB), cx, 1060, t, wt(9, "comenta", 1.2) - 0.2, 0.25, -3)
    emo(img, "olhos", 880, 1220, t, 0.6, 140) if False else None
    if T > S.total - 3.5:
        paste(img, text_el("Fotos (Wikimedia Commons): " + " • ".join(CRED.split(" • ")[:2]), font("sb", 20), (235, 235, 235), 3), W / 2, H - 236, 0.85)
        paste(img, text_el(" • ".join(CRED.split(" • ")[2:]), font("sb", 20), (235, 235, 235), 3), W / 2, H - 208, 0.85)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 170, 0.85)
SC.append(s9)
import json as _j
import re as _re
try: CRED = " • ".join(f"{_re.sub(chr(60)+'[^>]*>?', '', v[2]).strip()[:30]} {v[1]}" for v in _j.load(open(D + "creditos.json")).values())
except Exception: CRED = ""
S = Short("/home/claude/quiz/q", QUIZ, SC, "QUIZ • ADIVINHE O JOGADOR", ["green"] + ["night", "green"] * 4 + ["dark"], "Volatile_Reaction", 0)
if __name__ == "__main__":
    ev = [("whoosh_boom", 0.0, 0.35), ("tambor_impacto", wt(0, "valendo", 4.3), 0.3)]
    for r in R:
        i = r[0]; s0_ = S.segs[i][0]
        for j in range(len(r[4])): ev.append(("whoosh_3", s0_ + 0.25 + 0.32 * j, 0.07))
        g0 = S.segs[i][1]; g1 = S.segs[i + 1][0]
        for k in range(3): ev.append(("tique", g0 + k * (g1 - g0) / 3, 0.35))
        ev += [("riser", g1 - 1.0, 0.12), ("ding", g1, 0.35), ("torcida_comemora", g1 + 0.05, 0.1)]
    main(S, extra=ev)
