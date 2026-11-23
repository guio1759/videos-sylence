import sys, functools, re; sys.path.insert(0, "/home/claude/por"); sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/carreira")
from com import *
import card as C
sys.path.insert(0, "/home/claude/por/ep2"); from script import S as RAW
TXT = [re.sub(r"\[[a-z ]+\] ?", "", s) for s in RAW]
D = "/home/claude/por/ep2"; IM = "/home/claude/por/img/"
GOLD = (255, 205, 60)
@functools.lru_cache(32)
def cut(k, h): im = Image.open(IM + k + "_cut.png").convert("RGBA"); h = int(h); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
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
@functools.lru_cache(256)
def pcard(name, ovr, pos, stats, w=420, prom=False, av="sil"):
    a = silhouette() if av == "sil" else cut(av, 900)
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

def s0(img, t, T):  # hook: última rodada, 93, pênalti
    tp = wt(0, "pênalti") - 0.1
    cover(img, "penalti", t, 110 if t < tp else 60)
    paste(img, score("POR", "SAO", 1, 1, 110), cx, 400, 1)
    pop(img, chip("ÚLTIMA RODADA • PAULISTÃO", 50, INK, WHITE), cx, 580, t, 0.0)
    pop(img, stamp("SE PERDER, CAI", 100, RED), cx, 760, t, wt(0, "perder") - 0.1, 0.25, -6 + shake(t, wt(0, "perder"), 8))
    if t > wt(0, "minuto") - 0.1: paste(img, clock("93:00", 130), cx, 960, 1, 1 + 0.04 * math.sin(T * 12))
    if t > tp:
        u = t - tp; img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 200 * (1 - u / 0.15))))))
        paste(img, txt("PÊNALTI!", 200, AMB, 16), cx + (12 * math.sin(u * 70) if u < 0.4 else 0), 1200, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -5)

def s1(img, t, T):  # volta 3 meses, voto B, Levi
    img.alpha_composite(speedlines(W, H, T))
    pop(img, txt("3 MESES ANTES", 100, WHITE), cx, 400, t, 0.0)
    tb = wt(1, "letra") - 0.2; tl = wt(1, "levi3d") - 0.2
    if t > tb: paste(img, bubble("@beniciorufinodini2186", "Letra b", "1", 960), cx, 620, 1, 0.85 + 0.15 * back((t - tb) / 0.3))
    pop(img, chip("VOCÊS ESCOLHERAM: B", 60, WHITE, GREEN), cx, 820, t, tb + 0.3, 0.25, -2)
    if t > tl:
        pop(img, pcard("LEVI SANTOS", 60, "MEI", (72, 58, 62, 68, 30, 50), 380, False, "levi3d"), cx, 1200, t, tl, 0.3)
        pop(img, stamp("CONTRATADO", 90, GREEN), cx, 1430, t, wt(1, "joia"), 0.25, -6)

def s2(img, t, T):  # Benny
    tth, tpe, tpa = wt(2, "thiago") - 0.2, wt(2, "peneira") - 0.4, wt(2, "passou") - 0.15
    if t < tth:
        pop(img, chip("COMENTÁRIO MAIS CURTIDO", 58, INK, AMB), cx, 400, t, 0.0, 0.25, -2)
        tc = wt(2, "bota") - 0.3
        if t > 0.6: paste(img, bubble("@BennyDouekPikelaizen", "Bota eu no time", "3", 1000), cx, 640, 1, 0.85 + 0.15 * back((t - 0.6) / 0.3))
        pop(img, cut("benny", 560), cx, 1180, t, max(0.8, tc), 0.3)
        pop(img, chip("VIROU PERSONAGEM!", 60, WHITE, RED), cx, 1500, t, 1.4, 0.25, 3)
    elif t < tpe:
        u = t - tth; paste(img, cut("tee", 900), cx, 1050, 1, 0.85 + 0.15 * back(u / 0.35))
        pop(img, txt("E O THIAGO", 110, WHITE), cx, 420, u, 0.0); pop(img, txt("BOTOU!", 160, AMB), cx, 570, u, 0.3, 0.25, -4)
    else:
        u = t - tpe; cover(img, "benny_peneira", u, 40)
        pop(img, chip("PENEIRA • DE CHINELO", 60, INK, AMB), cx, 400, u, 0.1, 0.25, -2)
        if t > tpa:
            v = t - tpa
            pop(img, pcard("BENNY", 47, "VOL", (62, 38, 50, 52, 48, 46), 330, True, "benny"), 780, 1180, v, 0.0, 0.3)
            pop(img, stamp("APROVADO", 100, GREEN), 330, 1250, v, 0.2, 0.25, -8)

def s3(img, t, T):  # sem casa, Diadema, Corinthians
    cover(img, "diadema", t, 80, 0.3)
    pop(img, txt("SEM CASA", 140, WHITE), cx, 420, t, 0.0)
    pop(img, chip("ESTREIA EMPRESTADA EM DIADEMA", 50, INK, AMB), cx, 580, t, wt(3, "diadema") - 0.2)
    tc = wt(3, "corinthians") - 0.2
    if t > tc: paste(img, score("COR", "POR", "", "", 130), cx, 1150, 1, 0.7 + 0.3 * back((t - tc) / 0.3))

def s4(img, t, T):  # Levi acha Davi, GOL, Benny
    tg = wt(4, "gol") - 0.1; tb = wt(4, "benny", 1) - 0.3
    if t < tg:
        cam, d = pitch3d(img, T, 200, 4, dist=55, hgt=26, tgt=(30, 0, 0), dim=30)
        paste(img, score("COR", "POR", 1, 0, 100), cx, 380, 1)
        paste(img, clock("88:00", 100), cx, 560, 1)
        tl = wt(4, "levi3d") - 0.2; td = wt(4, "davi") - 0.2
        if t > tl:
            pop(img, cut("levi3d", 420), 300, 1080, t, tl, 0.3); pop(img, chip("LEVI", 56, WHITE, RED), 300, 1320, t, tl)
        if t > td:
            u = min(1, (t - td) / 0.7); dd = ImageDraw.Draw(img)
            dd.line((380, 900, 380 + (720 - 380) * u, 900 - 150 * u), fill=AMB, width=16)
            pop(img, cut("davi", 420), 780, 1000, t, td + 0.3, 0.3); pop(img, chip("DAVI • 16", 56, INK, AMB), 780, 1240, t, td + 0.3)
    elif t < tb:
        u = t - tg; img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 120), 16, 70)); img.alpha_composite(confetti(W, H, u))
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 200 * (1 - u / 0.15))))))
        paste(img, txt("GOOOL!", 220, AMB, 16), cx + (10 * math.sin(u * 70) if u < 0.4 else 0), 700, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -5)
        pop(img, score("COR", "POR", 1, 1, 110), cx, 1050, u, 0.4)
        pop(img, chip("DAVI, 16 ANOS", 70, INK, WHITE), cx, 1250, u, 0.6, 0.25, 3)
    else:
        u = t - tb; img.alpha_composite(confetti(W, H, u + 2))
        slide(img, cut("benny", 640), 330, 1050, u, 0.0, -600); paste(img, cut("davi", 640), 760, 1050, 1)
        pop(img, chip("O 1º A ABRAÇAR: BENNY", 58, WHITE, RED), cx, 460, u, 0.2, 0.25, -2)
        paste(img, score("COR", "POR", 1, 1, 90), cx, 1500, 1)

LOSS = [("POR", "SAN", 0, 2), ("PAL", "POR", 3, 0), ("POR", "RBB", 1, 2)]
def s5(img, t, T):  # pesadelo
    tf = wt(5, "torcida") - 0.2; ts = wt(5, "saf") - 0.2
    if t < tf:
        pop(img, txt("O PESADELO", 130, RED), cx, 420, t, 0.0)
        for k, (a, b, x, y) in enumerate(LOSS):
            t0 = wt(5, "três") - 0.2 + k * 0.4
            if t > t0:
                paste(img, score(a, b, x, y, 95), cx, 700 + k * 230, 1, 0.8 + 0.2 * back((t - t0) / 0.25), (-3, 2, -2)[k])
                paste(img, chip("DERROTA", 40, WHITE, RED), 900, 640 + k * 230, 1)
    else:
        u = t - tf; cover(img, "faixa", u, 50)
        ban = chip("FORA, THIAGO", 92, RED, (250, 248, 240)); paste(img, ban, 520, 760, 1, 1.0, -6 + 1.5 * math.sin(T * 2))
        if t > ts: paste(img, mail(900, "Diretoria SAF Lusa", "Reunião URGENTE"), cx, 1250, 1, 0.8 + 0.2 * back((t - ts) / 0.3), 2)

def s6(img, t, T):  # última rodada, Cauari
    tm = wt(6, "mesmo") - 0.2; tc = wt(6, "cauari") - 0.2
    if t < tm:
        cover(img, "penalti", t, 90)
        paste(img, score("POR", "SAO", 1, 1, 110), cx, 400, 1)
        pop(img, clock("93:00", 110), cx, 580, t, wt(6, "minuto") - 0.2)
        pop(img, chip("PÊNALTI PRA LUSA", 70, INK, AMB), cx, 760, t, wt(6, "pênalti") - 0.2, 0.25, -3)
        if t > tc: paste(img, pcard("CAUARI", 58, "PE", (78, 60, 58, 66, 30, 55), 380, False, "cauari3d"), cx, 1200, 1, 0.8 + 0.2 * back((t - tc) / 0.3))
    else:
        u = t - tm; cover(img, "penalti", u, 40, sepia=True)
        paste(img, newspaper2(900, "PAULISTÃO 2026 • QUARTAS", "CAUARI PERDE O PÊNALTI", "Corinthians passa nas cobranças"), cx, 820, 1, 0.9 + 0.1 * ease(u / 0.4), -3)
        pop(img, chip("ANO PASSADO", 60, WHITE, INK), cx, 1250, u, 0.4)

def s7(img, t, T):  # fecha o olho... GOL
    tg = wt(7, "gol") - 0.1
    if t < tg:
        cover(img, "penalti", t, 170 - int(40 * min(1, t)))
        pop(img, txt("ELE FECHA", 120, WHITE), cx, 700, t, 0.0); pop(img, txt("O OLHO...", 120, WHITE), cx, 860, t, 0.4)
    else:
        u = t - tg; cover(img, "festa", u, 30); img.alpha_composite(confetti(W, H, u))
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 220 * (1 - u / 0.15))))))
        paste(img, txt("GOOOL!", 220, AMB, 16), cx + (10 * math.sin(u * 70) if u < 0.4 else 0), 560, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -5)
        pop(img, score("POR", "SAO", 2, 1, 100), cx, 820, u, 0.3)
        pop(img, stamp("A LUSA FICA NA A1!", 84, GREEN), cx, 1150, u, wt(7, "fica") - tg, 0.25, -5)

EVO = [("davi", "DAVI", "MEI", 52, 58, (66, 52, 62, 64, 28, 42), "davi", True), ("levi", "LEVI SANTOS", "MEI", 60, 63, (72, 60, 64, 70, 30, 50), "levi3d", False),
       ("cauari", "CAUARI", "PE", 58, 61, (78, 60, 58, 66, 30, 55), "cauari3d", False), ("benny", "BENNY", "VOL", 47, 47, (62, 38, 50, 52, 48, 46), "benny", True)]
def s8(img, t, T):  # bloco único de evolução
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 35))
    pop(img, chip("EVOLUÇÃO DO TRIMESTRE", 64, INK, AMB), cx, 380, t, 0.0, 0.25, -2)
    for k, (wd, nm, pos, a, b, st, av, prom) in enumerate(EVO):
        t0 = wt(8, wd) - 0.2
        if t < t0: continue
        x, y = (290 if k % 2 == 0 else 790), (760 if k < 2 else 1290)
        u = t - t0; o = int(a + (b - a) * ease(max(0, u - 0.6) / 1.0))
        paste(img, pcard(nm, o, pos, st, 330, prom, av), x, y, 1, 0.85 + 0.15 * back(min(1, u / 0.3)))
        lab = f"+{b - a}" if b > a else "ESTREOU"
        if u > 0.9: paste(img, chip(lab, 56 if b > a else 44, INK, GREEN if b > a else WHITE), x + 140, y - 230, 1, 0.8 + 0.2 * back(min(1, (u - 0.9) / 0.2)), 8)

XI = [("BERTINATO", 60, 0.50, 0.90), ("JOÃO VITOR", 58, 0.86, 0.72), ("BOTTEGHIN", 61, 0.64, 0.76), ("G. HENRIQUE", 58, 0.36, 0.76), ("HIPÓLITO", 57, 0.14, 0.72),
      ("HUDSON", 58, 0.50, 0.57), ("LEVI", 63, 0.76, 0.48), ("DAVI", 58, 0.24, 0.48),
      ("TORÓ", 65, 0.84, 0.26), ("CADORINI", 63, 0.50, 0.20), ("CAUARI", 61, 0.16, 0.26)]
def s9(img, t, T):  # escalação titular
    X0, Y0, PW, PH = 70, 420, 940, 1130; d = ImageDraw.Draw(img)
    for k in range(8): d.rectangle((X0, Y0 + k * PH / 8, X0 + PW, Y0 + (k + 1) * PH / 8), fill=(34, 120, 58) if k % 2 else (40, 134, 66))
    L = (235, 245, 235); d.rectangle((X0, Y0, X0 + PW, Y0 + PH), outline=L, width=5); d.line((X0, Y0 + PH / 2, X0 + PW, Y0 + PH / 2), fill=L, width=4)
    d.ellipse((W / 2 - 110, Y0 + PH / 2 - 110, W / 2 + 110, Y0 + PH / 2 + 110), outline=L, width=4)
    d.rectangle((W / 2 - 240, Y0 + PH - 190, W / 2 + 240, Y0 + PH), outline=L, width=4); d.rectangle((W / 2 - 240, Y0, W / 2 + 240, Y0 + 190), outline=L, width=4)
    paste(img, txt("TIME TITULAR", 92, WHITE), cx, 300, 1)
    for k, (nm, o, fx, fy) in enumerate(XI):
        t0 = 0.15 + k * 0.12
        if t < t0: continue
        x, y = X0 + fx * PW, Y0 + fy * PH; u = back(min(1, (t - t0) / 0.25))
        col = (205, 127, 50) if o < 65 else (190, 195, 205)
        r = 46 * u; d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INK, width=5)
        paste(img, text_el(str(o), font("blk", 44), INK, 0, shadow=False), x, y, u)
        paste(img, chip(nm, 30, WHITE, INK), x, y + 72, u)
    pop(img, chip("4-3-3  •  MÉDIA 60", 54, INK, AMB), cx, 1640, t, 1.7)
    pop(img, chip("BANCO: ROMARINHO 64 • BENNY 47", 36, WHITE, (30, 30, 36)), cx, 1740, t, 2.0)

def s10(img, t, T):  # Romarinho perdeu a vaga, A/B
    ta = wt(10, "a", 1) if False else wt(10, "romarinho", 2) - 0.6; tb = wt(10, "continua") - 0.8
    if t < ta:
        img.alpha_composite(Image.new("RGBA", (W, H), (120, 0, 0, 60)))
        paste(img, cut("romarinho3d", 900), cx, 1060, 1, 0.9 + 0.1 * back(min(1, t / 0.35)))
        pop(img, chip("ROMARINHO • ÍDOLO", 64, INK, WHITE), cx, 420, t, 0.0)
        pop(img, stamp("PERDEU A VAGA", 96, RED), cx, 600, t, wt(10, "perdeu") - 0.1, 0.25, -6)
        pop(img, chip("E NÃO GOSTOU...", 60, WHITE, INK), cx, 1500, t, wt(10, "gostou") - 0.2, 0.25, 3)
        return
    pop(img, chip("A", 120, WHITE, RED), 280, 420, t, ta)
    pop(img, pcard("ROMARINHO", 64, "ATA", (62, 68, 66, 70, 30, 55), 360, False, "romarinho3d"), 280, 780, t, ta, 0.3)
    pop(img, chip("VOLTA PRO TIME", 44, INK, WHITE), 280, 1090, t, ta + 0.2)
    if t > tb:
        pop(img, chip("B", 120, WHITE, GREEN), 800, 420, t, tb)
        pop(img, pcard("DAVI", 58, "MEI", (66, 52, 62, 64, 28, 42), 360, True, "davi"), 800, 780, t, tb, 0.3)
        pop(img, chip("TIME COMO ESTÁ", 44, INK, WHITE), 800, 1090, t, tb + 0.2)
    tc = wt(10, "comenta") - 0.2
    pop(img, chip("COMENTA A OU B", 70, INK, AMB), cx, 1270, t, tc, 0.25, -2)
    pop(img, chip("EP.3 • QUARTA 18H", 56, WHITE, INK), cx, 1400, t, tc + 0.8)
    paste(img, logo("POR", 110), 960, 1520, 1)

SH = Short(D, [(s,) for s in TXT], [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10], "MODO CARREIRA • LUSA • EP.2",
           ["night", "dark", "green", "dark", "night", "red", "night", "night", "green", "dark", "red"], "Impact_Prelude", 0)
S = SH
if __name__ == "__main__":
    g = SH.segs
    ev = [("tambor_impacto", 0.0, 0.5), ("apito_juiz", g[0][0] + wt(0, "pênalti"), 0.4), ("whoosh_boom", g[1][0], 0.3),
          ("torcida_reacao_gol", g[4][0] + wt(4, "gol"), 0.45), ("torcida_aww", g[5][0] + 0.8, 0.2), ("tambor_impacto", g[5][0] + wt(5, "saf"), 0.3),
          ("apito_curto", g[6][0] + wt(6, "pênalti"), 0.3), ("chute_bola_1", g[7][0] + wt(7, "gol") - 0.25, 0.4), ("torcida_reacao_gol", g[7][0] + wt(7, "gol"), 0.5),
          ("tambor_impacto", g[9][0], 0.3), ("tambor_impacto", g[10][0] + wt(10, "perdeu"), 0.3)]
    main(SH, extra=ev)
