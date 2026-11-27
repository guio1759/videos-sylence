import sys, functools, re; sys.path.insert(0, "/home/claude/por"); sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/carreira")
from com import *
import card as C
sys.path.insert(0, "/home/claude/por/ep3i"); from script import S as RAW
TXT = [re.sub(r"\[[a-z ]+\] ?", "", s) for s in RAW]
D = "/home/claude/por/ep3i"; IM = "/home/claude/por/img/"
GOLD = (255, 205, 60)
TOK = {"benny": ("BENNY", "5"), "leonardo": ("LEONARDO", "6"), "cadorini": ("CADORINI", "9"), "levi3d": ("LEVI", "10"), "romarinho3d": ("ROMARINHO", "11"),
       "davi": ("DAVI", "8"), "tee": ("THIAGO TEH", "T"), "cauari3d": ("CAUARI", "7")}
LRED, LGRN = (196, 28, 40), (22, 140, 70)
@functools.lru_cache(64)
def disc(num, d, col=LRED, ring=LGRN, fg=WHITE, coach=False):
    d = int(d); im = Image.new("RGBA", (d + 24, d + 24), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    dr.ellipse((14, 18, d + 14, d + 18), fill=(0, 0, 0, 110))
    dr.ellipse((4, 4, d + 4, d + 4), fill=(20, 20, 26) if coach else col, outline=ring, width=max(6, d // 11))
    dr.ellipse((d * 0.18 + 4, d * 0.1 + 4, d * 0.82 + 4, d * 0.42 + 4), fill=(255, 255, 255, 40))
    dr.text((d / 2 + 4, d / 2 + 6), num, font=font("blk", int(d * (0.5 if len(num) < 2 else 0.42))), fill=fg, anchor="mm", stroke_width=max(2, d // 40), stroke_fill=INK)
    return im
@functools.lru_cache(64)
def tcut(k, h):
    nm, num = TOK.get(k, (k.upper(), "?")); h = int(h); d = int(h * 0.62); coach = k == "tee"
    im = Image.new("RGBA", (max(d + 24, int(h * 0.95)), h), (0, 0, 0, 0)); dc = disc(num, d, coach=coach)
    im.alpha_composite(dc, ((im.width - dc.width) // 2, int(h * 0.04)))
    lab = chip(nm, int(h * 0.075), WHITE, INK if not coach else (60, 60, 70))
    if lab.width > im.width: lab = lab.resize((im.width, int(lab.height * im.width / lab.width)))
    im.alpha_composite(lab, ((im.width - lab.width) // 2, int(h * 0.04) + d + int(h * 0.04)))
    if coach:
        sub = chip("TÉCNICO", int(h * 0.055), INK, AMB); im.alpha_composite(sub, ((im.width - sub.width) // 2, int(h * 0.04) + d + int(h * 0.15)))
    return im
@functools.lru_cache(16)
def _cov(k):
    im = Image.open(IM + k + ".jpg").convert("RGBA"); sc = max(W * 1.15 / im.width, H * 1.15 / im.height)
    return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
def cover(img, k, t, dim=90, dx=0.0, sepia=False):
    b = _cov(k); z = 1.0 + 0.035 * t
    bw, bh = int(W * 1.15 / z), int(H * 1.15 / z)
    x0 = int((b.width - bw) / 2 + dx * t * 30); y0 = int((b.height - bh) / 2); x0 = max(0, min(b.width - bw, x0))
    im = b.crop((x0, y0, x0 + bw, y0 + bh)).resize((W, H))
    if sepia:
        g = im.convert("L"); im = Image.merge("RGB", [g.point(lambda v: min(255, v * 1.08)), g.point(lambda v: v * 0.9), g.point(lambda v: v * 0.68)]).convert("RGBA")
    img.alpha_composite(im)
    if dim: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim)))
def wt(i, word, n=1):
    s0 = SH.segs[i][0]; c = 0
    for w in SH.caps:
        if SH.segs[i][0] - 0.01 <= w["t0"] <= SH.segs[i][1] + 0.01 and norm(w["w"]).startswith(norm(word)):
            c += 1
            if c == n: return w["t0"] - s0
    return 0.0
REAL = {"benny": "benny_r", "leonardo": "leonardo_r", "davi": "davi_r", "tee": "tee_r",   # criados: estilo base do FIFA
        "romarinho3d": "romarinho", "levi3d": "levi", "cadorini": "cadorini", "cauari3d": "cauari_foto"}  # reais: foto real (enviada pelo usuário)
import os
def portrait_src(k):
    f = IM + REAL.get(k, k) + "_cut.png"
    return f if os.path.exists(f) else None
@functools.lru_cache(64)
def cut(k, h):
    h = int(h); f = portrait_src(k)
    if f is None:
        im = silhouette().convert("RGBA")
    else: im = Image.open(f).convert("RGBA")
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    nm = TOK.get(k, (k.upper(), ""))[0]
    out = Image.new("RGBA", (max(im.width, 10), h + int(h * 0.06)), (0, 0, 0, 0)); out.alpha_composite(im, (0, 0))
    lab = chip(nm, max(30, int(h * 0.07)), WHITE, (20, 20, 26) if k != "tee" else (60, 60, 70))
    out.alpha_composite(lab, ((out.width - lab.width) // 2, out.height - lab.height))
    return out
@functools.lru_cache(256)
def pcard(name, ovr, pos, stats, w=420, prom=False, av="sil"):
    f = None if av == "sil" else portrait_src(av)
    a = silhouette() if f is None else Image.open(f).convert("RGBA")
    return C.make_card(a, name, ovr, pos, list(stats), w=w, promessa=prom, crest="POR.png")
def bubble(user, text, likes, w=900):
    h = 260; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 36, fill=(255, 255, 255, 250), outline=INK, width=5)
    d.ellipse((30, 40, 120, 130), fill=(160, 80, 190)); d.text((75, 85), user[1].upper(), font=font("blk", 56), fill=WHITE, anchor="mm")
    f = font("bd", 44 if len(user) < 22 else 36); d.text((145, 45), user, font=f, fill=(110, 110, 120))
    d.text((145, 120), text, font=font("blk", 66), fill=INK)
    d.text((w - 80, 80), "♥", font=font("blk", 80), fill=RED, anchor="mm"); d.text((w - 80, 160), likes, font=font("bd", 40), fill=(90, 90, 100), anchor="mm")
    return im
def clock(s, sz=120):
    return chip(s, sz, WHITE, (20, 20, 26))
def score(a, b, ga, gb, sz=120): return scorebox(a, b, ga, gb, sz)
def mail(w, frm, subj):
    h = int(w * 0.5); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(250, 250, 252), outline=INK, width=5)
    d.rectangle((0, 0, w, 90), fill=(40, 40, 50)); d.text((30, 45), "NOVO E-MAIL", font=font("blk", 42), fill=WHITE, anchor="lm")
    d.text((30, 150), "De: " + frm, font=font("bd", 40), fill=(90, 90, 100)); d.text((30, 230), subj, font=font("blk", 58), fill=RED)
    d.text((30, h - 60), "Hoje, 07:12", font=font("sb", 34), fill=(130, 130, 140))
    return im
def newspaper2(w, top, head, sub):
    h = int(w * 0.62); im = Image.new("RGBA", (w, h), (238, 226, 200, 255)); d = ImageDraw.Draw(im)
    d.text((w / 2, h * 0.1), top, font=font("blk", w * 0.06), fill=INK, anchor="mm"); d.line((30, h * 0.18, w - 30, h * 0.18), fill=INK, width=4)
    d.text((w / 2, h * 0.42), head, font=font("blk", w * 0.075), fill=INK, anchor="mm"); d.text((w / 2, h * 0.6), sub, font=font("sb", w * 0.042), fill=(70, 70, 70), anchor="mm")
    for k in range(3): d.line((40, h * 0.72 + k * 28, w - 40, h * 0.72 + k * 28), fill=(180, 175, 165), width=10)
    return im

NM = {"POR": "LUSA", "MAD": "MADUREIRA", "AME": "AMERICA-RJ", "PRJ": "PORTUGUESA-RJ", "AGS": "ÁGUA SANTA", "PAF": "POUSO ALEGRE"}
TAB = {
 1: [("POR", 3, 2), ("MAD", 3, 1), ("AME", 1, 0), ("PRJ", 1, 0), ("PAF", 0, -1), ("AGS", 0, -2)],
 3: [("MAD", 7, 3), ("AME", 5, 2), ("POR", 4, 1), ("AGS", 3, 0), ("PRJ", 2, -1), ("PAF", 1, -5)],
 9: [("MAD", 20, 9), ("AGS", 17, 5), ("PRJ", 15, 2), ("AME", 14, 1), ("POR", 13, 1), ("PAF", 5, -18)],
 10: [("MAD", 21, 9), ("PRJ", 18, 3), ("AGS", 17, 4), ("POR", 16, 2), ("AME", 15, 1), ("PAF", 5, -19)]}
def table(t, rnd, w=960, hl=None, col4=True):
    rows = TAB[rnd]; rh = 104; h = 120 + rh * 6; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(14, 16, 22, 240), outline=WHITE, width=4)
    d.text((40, 60), f"GRUPO A13 • RODADA {rnd}/10", font=font("blk", 40), fill=AMB, anchor="lm"); d.text((w - 40, 60), "PTS", font=font("blk", 40), fill=WHITE, anchor="rm")
    for k, (c, p, sg) in enumerate(rows):
        u = ease((t - 0.08 * k) / 0.3)
        if u <= 0: continue
        y = 120 + rh * k
        if c == "POR": d.rounded_rectangle((12, y + 4, w - 12, y + rh - 4), 18, fill=(150, 20, 30, 230) if hl == "red" else (20, 120, 60, 230) if hl == "green" else (70, 70, 80, 230))
        if k == 3 and col4: d.line((24, y + rh, w - 24, y + rh), fill=AMB, width=5)
        d.text((60, y + rh / 2), f"{k + 1}º", font=font("blk", 46), fill=WHITE, anchor="mm")
        im.alpha_composite(logo(c, 74), (110, int(y + rh / 2 - 37)))
        d.text((220, y + rh / 2), NM[c], font=font("blk", 44), fill=WHITE, anchor="lm")
        d.text((w - 40, y + rh / 2), str(p), font=font("blk", 52), fill=WHITE, anchor="rm")
    if col4: d.text((w - 40, h - 14), "TOP 4 → MATA-MATA", font=font("bd", 26), fill=AMB, anchor="rs")
    return im
def hud(img, rnd, pos):
    s = f"SÉRIE D  •  RODADA {rnd}/10  •  LUSA {pos}º  •  META: SÉRIE C"
    paste(img, chip(s, 32, WHITE, (20, 20, 26)), cx, 238, 0.95)
def cmt(user, text, likes, w=940): return bubble(user, text, likes, w)

def cmt(user, text, likes, w=940): return bubble(user, text, likes, w)

def i0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 120), 16, 55))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("VOCÊ PODE", 120, WHITE, 12), cx, 330, 1, sc, -2)
    paste(img, txt("ENTRAR NO TIME!", 112, AMB, 12), cx, 470, 1, sc, 2)
    tj, tc, td = wt(0, "jogador") - 0.3, wt(0, "curtido") - 0.3, wt(0, "decide") - 0.2
    if t < td:
        paste(img, cmt("ALL Vs Chelsea • TikTok", "coloca eu na lusa", "4", 860), cx, 700, 1, 0.85 + 0.15 * back(min(1, t / 0.25)))
        if t > tj:
            u = t - tj; d = ImageDraw.Draw(img); ln = 160 * ease(u / 0.3)
            d.line((cx, 840, 340, 840 + ln), fill=AMB, width=14)
            pop(img, pcard("LEONARDO", 50, "LE", (70, 40, 56, 55, 52, 58), 330, True, "leonardo"), 320, 1180, t, tj + 0.2, 0.3)
        pop(img, chip("O MAIS CURTIDO", 50, WHITE, RED), 770, 1120, t, tc, 0.25, -3)
        pop(img, chip("ENTRA NO TIME", 50, INK, AMB), 770, 1220, t, tc + 0.2, 0.25, 3)
    else:
        u = t - td; img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 180 * (1 - u / 0.15))))))
        pop(img, chip("A", 260, WHITE, RED), 300, 900, u, 0.0, 0.3, -6)
        pop(img, chip("B", 260, WHITE, GREEN), 780, 900, u, 0.12, 0.3, 6)
        pop(img, stamp("VOCÊ DECIDE A HISTÓRIA", 76, AMB), cx, 1240, u, 0.3, 0.25, -4)
SH = Short(D, [(s,) for s in TXT], [i0], "MODO CARREIRA • LUSA • EP.3", ["green"], "Crossing_the_Chasm", 0)
S = SH
SH.CREDIT = False
if __name__ == "__main__":
    main(SH, extra=[("tambor_impacto", 0.0, 0.5), ("whoosh_boom", wt(0, "jogador"), 0.3), ("tambor_impacto", wt(0, "decide"), 0.4)])
