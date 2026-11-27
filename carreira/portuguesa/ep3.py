import sys, functools, re; sys.path.insert(0, "/home/claude/por"); sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/carreira")
from com import *
import card as C
sys.path.insert(0, "/home/claude/por/ep3"); from script import S as RAW
TXT = [re.sub(r"\[[a-z ]+\] ?", "", s) for s in RAW]
D = "/home/claude/por/ep3"; IM = "/home/claude/por/img/"
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
def cut(k, h):
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
@functools.lru_cache(256)
def pcard(name, ovr, pos, stats, w=420, prom=False, av="sil"):
    if av == "sil": a = silhouette()
    else:
        a = Image.new("RGBA", (760, 600), (0, 0, 0, 0)); dc = disc(TOK.get(av, ("", "?"))[1], 500); a.alpha_composite(dc, (130, 60))
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

def s0(img, t, T):  # flash-forward
    cam, d = pitch3d(img, T, 30, 5, dist=60, hgt=28, tgt=(25, 0, 0), dim=50)
    paste(img, score("POR", "PAF", 0, 0, 110), cx, 400, 1)
    pop(img, chip("ÚLTIMA RODADA • SÉRIE D", 50, INK, WHITE), cx, 580, t, 0.0)
    if t > wt(0, "minuto") - 0.1: paste(img, clock("90:00", 120), cx, 740, 1, 1 + 0.04 * math.sin(T * 12))
    pop(img, stamp("SE NÃO GANHAR, ACABOU", 84, RED), cx + shake(t, wt(0, "acaba"), 10), 960, t, wt(0, "acaba") - 0.2, 0.25, -5)
    tc = wt(0, "dois") - 0.2
    if t > tc:
        pop(img, cut("benny", 560), 300, 1340, t, tc, 0.3); pop(img, cut("leonardo", 560), 790, 1340, t, tc + 0.15, 0.3)
        pop(img, chip("VIERAM DOS COMENTÁRIOS", 54, WHITE, RED), cx, 1640, t, wt(0, "comentários") - 0.3, 0.25, -2)

def s1(img, t, T):  # volta 2 meses
    img.alpha_composite(speedlines(W, H, T))
    pop(img, txt("2 MESES ANTES", 110, WHITE), cx, 400, t, 0.0)
    pop(img, chip("VOCÊS ESCOLHERAM: B", 64, WHITE, GREEN), cx, 580, t, wt(1, "escolheram") - 0.2, 0.25, -2)
    pop(img, chip("O TIME CONTINUA", 50, INK, WHITE), cx, 720, t, wt(1, "continua") - 0.2)
    tr = wt(1, "romarinho") - 0.2
    if t > tr:
        paste(img, cut("romarinho3d", 760), cx, 1230, 1, 0.85 + 0.15 * back(min(1, (t - tr) / 0.3)))
        pop(img, chip("NO BANCO", 60, WHITE, INK), cx, 900, t, wt(1, "banco") - 0.2, 0.25, 3)
        pop(img, stamp("NÃO GOSTOU NADA", 96, RED), cx, 1600, t, wt(1, "gostou") - 0.2, 0.25, -6)

def s2(img, t, T):  # bordão comentário
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 120), 14, 45))
    pop(img, chip("COMENTÁRIO MAIS CURTIDO", 60, INK, AMB), cx, 420, t, 0.0, 0.25, -2)
    pop(img, cmt("ALL Vs Chelsea • TikTok", "coloca eu na lusa", "4"), cx, 760, t, 0.4)
    pop(img, chip("VIROU PERSONAGEM!", 70, WHITE, RED), cx, 1100, t, 1.2, 0.25, 3)

def s3(img, t, T):  # Leonardo
    tt, tl, tp = wt(3, "thiago") - 0.2, wt(3, "lateral") - 0.2, wt(3, "parceiro") - 0.3
    if t < tt:
        pop(img, cmt("ALL Vs Chelsea • TikTok", "nome: Leonardo", "4"), cx, 520, t, 0.0)
        pop(img, cut("leonardo", 800), cx, 1250, t, 0.3, 0.3)
    elif t < tp:
        u = t - tt; paste(img, cut("tee", 600), 300, 1250, 1, 0.9 + 0.1 * back(min(1, u / 0.3)))
        pop(img, txt("O THIAGO", 100, WHITE), cx, 400, u, 0.0); pop(img, txt("CONHECIA!", 120, AMB), cx, 540, u, 0.2, 0.25, -3)
        if t > tl:
            v = t - tl
            pop(img, pcard("LEONARDO", 50, "LE", (70, 40, 56, 55, 52, 58), 380, True, "leonardo"), 780, 1000, v, 0.0, 0.3)
            pop(img, chip("EX-VÁRZEA DO THIAGO", 46, INK, AMB), 760, 1310, v, 0.3, 0.25, 3)
            pop(img, chip("CHUTEIRA EMPRESTADA", 46, WHITE, INK), 760, 1410, t, wt(3, "chuteira") - 0.2, 0.25, -3)
    else:
        u = t - tp; img.alpha_composite(rays(W, H, cx, 1100, T, (255, 200, 140), 12, 30))
        pop(img, chip("ALOJAMENTO DA LUSA", 56, INK, AMB), cx, 420, u, 0.0)
        slide(img, cut("benny", 560), 300, 1000, u, 0.0, -600); slide(img, cut("leonardo", 560), 790, 1000, u, 0.1, 600)
        pop(img, chip("COMENTÁRIO DO EP.2", 36, WHITE, RED), 300, 1340, u, 0.3); pop(img, chip("COMENTÁRIO DO EP.3", 36, WHITE, RED), 790, 1340, u, 0.4)

def s4(img, t, T):  # Série D explicada
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 30))
    pop(img, txt("SÉRIE D 2027", 130, WHITE), cx, 380, t, 0.0)
    pop(img, chip("GRUPO A13", 60, INK, AMB), cx, 520, t, 0.3)
    order = ["POR", "MAD", "AME", "PRJ", "AGS", "PAF"]
    ts = wt(4, "seis") - 0.2
    for k, c in enumerate(order):
        x = 230 + (k % 3) * 310; y = 720 + (k // 3) * 300
        pop(img, logo(c, 170), x, y, t, ts + 0.1 * k, 0.3)
        pop(img, text_el(NM[c], font("blk", 34), WHITE, 5), x, y + 125, t, ts + 0.1 * k + 0.1)
    pop(img, chip("10 RODADAS", 50, WHITE, INK), 250, 1350, t, wt(4, "dez") - 0.2, 0.25, -3)
    pop(img, chip("TOP 4 → MATA-MATA", 50, INK, GREEN), 760, 1350, t, wt(4, "quatro") - 0.2, 0.25, 3)
    tm = wt(4, "meta") - 0.2
    if t > tm:
        u = t - tm; paste(img, stamp("META: SÉRIE C", 110, AMB), cx, 1560, 1, 0.6 + 0.4 * back(min(1, u / 0.3)), -4)
        pop(img, chip("D  →  C", 60, WHITE, RED), cx, 1730, u, 0.4)

def s5(img, t, T):  # R1 e R2
    tc = wt(5, "clássico") - 0.3
    if t < tc:
        cover(img, "diadema", t, 110); hud(img, 1, 1)
        pop(img, chip("RODADA 1 • DIADEMA", 56, INK, AMB), cx, 400, t, 0.0)
        pop(img, score("POR", "AGS", 2, 0, 120), cx + shake(t, wt(5, "dois"), 12), 620, t, wt(5, "dois") - 0.3)
        pop(img, pcard("LEVI SANTOS", 64, "MEI", (72, 60, 64, 70, 30, 50), 280, False, "levi3d"), 200, 1060, t, wt(5, "levi") - 0.3)
        pop(img, chip("GOL DO LEVI", 50, INK, AMB), 200, 1310, t, wt(5, "levi"), 0.25, -3)
        if t > wt(5, "levi") + 0.4: paste(img, table(t - wt(5, "levi") - 0.4, 1, 960).resize((600, 465)), 720, 1100, 1)
    else:
        u = t - tc; img.alpha_composite(Image.new("RGBA", (W, H), (12, 60, 30, 120)))
        hud(img, 2, 2)
        pop(img, chip("RODADA 2 • NO RIO", 56, INK, AMB), cx, 400, u, 0.0)
        pop(img, txt("CLÁSSICO DAS", 110, WHITE), cx, 560, u, 0.1); pop(img, txt("PORTUGUESAS", 120, GREEN), cx, 700, u, 0.25)
        pop(img, logo("PRJ", 260), 300, 1030, u, 0.3, 0.3, -5); pop(img, txt("x", 120, AMB), cx, 1030, u, 0.4); pop(img, logo("POR", 260), 780, 1030, u, 0.5, 0.3, 5)
        pop(img, score("PRJ", "POR", 1, 1, 110), cx, 1400, u, 1.3)

def s6(img, t, T):  # R3 derrota, Davi lesão
    img.alpha_composite(Image.new("RGBA", (W, H), (120, 0, 0, 70))); hud(img, 3, 3)
    pop(img, chip("RODADA 3", 56, INK, AMB), cx, 400, t, 0.0)
    pop(img, score("MAD", "POR", 1, 0, 120), cx, 600, t, wt(6, "derrota") - 0.3)
    td = wt(6, "davi") - 0.3
    if t > td:
        u = t - td; paste(img, cut("davi", 700), cx, 1220, 1, 0.85 + 0.15 * back(min(1, u / 0.3)), -8)
        pop(img, stamp("LESÃO NO TORNOZELO", 84, RED), cx, 920, t, wt(6, "tornozelo") - 0.2, 0.25, -5)
        pop(img, chip("3 SEMANAS FORA", 64, WHITE, INK), cx, 1620, t, wt(6, "semanas") - 0.3, 0.25, 3)

def s7(img, t, T):  # Romarinho pede pra sair, treino
    tt = wt(7, "todo") - 0.3
    if t < tt:
        pop(img, mail(900, "Romarinho", "PEDIDO DE SAÍDA"), cx, 650, t, 0.0, 0.3, -2)
        pop(img, stamp("RECUSADO", 120, RED), cx + shake(t, wt(7, "segura"), 10), 930, t, wt(7, "segura") - 0.1, 0.25, -8)
        pop(img, cut("tee", 560), 300, 1350, t, wt(7, "preciso") - 0.3)
        pop(img, chip("\"PRECISO DE VOCÊ COM OS NOVATOS\"", 40, INK, AMB), cx, 1680, t, wt(7, "novatos") - 0.4)
    else:
        u = t - tt; cam, d = pitch3d(img, T, 90, 4, dist=50, hgt=24, dim=60)
        pop(img, chip("TREINO EXTRA • TODO DIA", 56, INK, AMB), cx, 400, u, 0.0)
        pop(img, cut("romarinho3d", 620), cx, 900, u, 0.1, 0.3)
        pop(img, cut("benny", 520), 280, 1380, u, wt(7, "benny") - tt - 0.2, 0.3); pop(img, cut("leonardo", 520), 800, 1380, u, wt(7, "leonardo") - tt - 0.2, 0.3)

def s8(img, t, T):  # tabela antes da última
    hud(img, 9, 5)
    pop(img, chip("FALTA 1 RODADA", 60, INK, AMB), cx, 380, t, 0.0, 0.25, -2)
    paste(img, table(t - 0.2, 9, 960, "red"), cx, 930, 1, 0.9 + 0.1 * back(min(1, t / 0.3)))
    pop(img, chip("1 PONTO ATRÁS DO AMERICA", 48, WHITE, RED), cx, 1430, t, wt(8, "menos") - 0.3, 0.25, -2)
    pop(img, logo("PAF", 140), 250, 1640, t, wt(8, "pouso") - 0.3)
    pop(img, stamp("EMPATE NÃO SERVE", 92, RED), 640, 1640, t, wt(8, "empate") - 0.2, 0.25, -5)

def board(img, X0=90, Y0=430, PW=900, PH=1080):
    d = ImageDraw.Draw(img)
    for k in range(8): d.rectangle((X0, Y0 + k * PH / 8, X0 + PW, Y0 + (k + 1) * PH / 8), fill=(34, 120, 58) if k % 2 else (40, 134, 66))
    L = (235, 245, 235); d.rectangle((X0, Y0, X0 + PW, Y0 + PH), outline=L, width=5)
    d.rectangle((X0 + PW * 0.2, Y0, X0 + PW * 0.8, Y0 + PH * 0.2), outline=L, width=4); d.rectangle((X0 + PW * 0.37, Y0, X0 + PW * 0.63, Y0 + PH * 0.08), outline=L, width=4)
    d.rectangle((X0 + PW * 0.42, Y0 - 26, X0 + PW * 0.58, Y0), outline=WHITE, width=6)
    d.arc((X0 + PW * 0.35, Y0 + PH * 0.12, X0 + PW * 0.65, Y0 + PH * 0.28), 20, 160, fill=L, width=4)
    d.line((X0, Y0 + PH, X0 + PW, Y0 + PH), fill=L, width=4); d.arc((X0 + PW * 0.38, Y0 + PH * 0.88, X0 + PW * 0.62, Y0 + PH * 1.12), 180, 360, fill=L, width=4)
    return X0, Y0, PW, PH
def lerp(a, b, u): u = max(0.0, min(1.0, u)); return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
def qbez(a, c, b, u):
    u = max(0.0, min(1.0, u)); return ((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1])
def tok(img, xy, num, name, d=84, col=LRED, ring=LGRN, lab=True):
    paste(img, disc(num, d, col, ring), xy[0], xy[1], 1)
    if lab: paste(img, chip(name, 26, WHITE, INK if col == LRED else (60, 60, 70)), xy[0], xy[1] + d * 0.75, 1)
def s9(img, t, T):  # o gol: prancheta tática
    tg = wt(9, "goool") - 0.1; tq = wt(9, "quarto") - 0.3
    if t < tg:
        X0, Y0, PW, PH = board(img); P = lambda fx, fy: (X0 + fx * PW, Y0 + fy * PH)
        paste(img, score("POR", "PAF", 0, 0, 90), 330, 300, 1); paste(img, clock("90:00", 80), 780, 300, 1)
        tb, tl, tx, tc = wt(9, "benny") - 0.1, wt(9, "leonardo") - 0.2, wt(9, "cruzamento") - 0.1, wt(9, "cadorini") - 0.1
        opp = [((0.55, 0.62), (0.52, 0.6)), ((0.35, 0.3), (0.42, 0.18)), ((0.6, 0.25), (0.55, 0.16)), ((0.25, 0.5), (0.22, 0.4))]
        for k, (a, b) in enumerate(opp): tok(img, P(*lerp(a, b, (t - tl) / 2.5)), "", "", 70, (150, 150, 160), (60, 60, 70), False)
        benny = P(*lerp((0.55, 0.72), (0.55, 0.64), (t - tb + 0.6) / 0.6)); leo = P(*lerp((0.12, 0.6), (0.1, 0.18), (t - tl - 0.4) / (tx - tl)))
        cado = P(*lerp((0.6, 0.45), (0.44, 0.1), (t - tl) / (tc - tl + 0.2)))
        tok(img, cado, "9", "CADORINI"); tok(img, leo, "6", "LEONARDO"); tok(img, benny, "5", "BENNY")
        tok(img, P(0.5, 0.03), "", "", 64, (240, 200, 40), INK, False)
        # bola
        if t < tb: ball = P(0.55, 0.6)
        elif t < tl: ball = (benny[0], benny[1] - 30)
        elif t < tl + 0.5: ball = lerp(benny, leo, (t - tl) / 0.5)
        elif t < tx: ball = (leo[0] + 30, leo[1] - 30)
        elif t < tc: ball = qbez((leo[0] + 30, leo[1] - 30), P(0.3, -0.05), (cado[0], cado[1] - 20), (t - tx) / (tc - tx))
        else: ball = lerp((cado[0], cado[1] - 20), P(0.47, -0.01), (t - tc) / 0.35)
        d = ImageDraw.Draw(img)
        if t > tl: d.line((benny, leo if t > tl + 0.5 else ball), fill=AMB, width=8)
        if t > tx:
            pts = [qbez((leo[0] + 30, leo[1] - 30), P(0.3, -0.05), (cado[0], cado[1] - 20), u / 20) for u in range(0, 21)]
            d.line(pts, fill=WHITE, width=6)
        d.ellipse((ball[0] - 18, ball[1] - 18, ball[0] + 18, ball[1] + 18), fill=WHITE, outline=INK, width=4)
        pop(img, chip("ROUBA!", 54, WHITE, RED), benny[0], benny[1] - 110, t, tb, 0.25, -4)
        pop(img, chip("CRUZA!", 54, INK, AMB), leo[0] + 120, leo[1] - 90, t, tx, 0.25, 4)
        pop(img, chip("CABEÇADA!", 54, INK, WHITE), cado[0] + 60, cado[1] + 120, t, tc, 0.25, -3)
    elif t < tq:
        u = t - tg; img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 120), 16, 70)); img.alpha_composite(confetti(W, H, u))
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(max(0, 200 * (1 - u / 0.15))))))
        paste(img, txt("GOOOL!", 220, AMB, 16), cx + (10 * math.sin(u * 70) if u < 0.4 else 0), 650, 1, 0.6 + 0.4 * back(min(1, u / 0.25)), -5)
        pop(img, score("POR", "PAF", 1, 0, 110), cx, 980, u, 0.3)
        pop(img, chip("CADORINI • 90'", 64, INK, WHITE), cx, 1180, u, 0.5, 0.25, 3)
    else:
        u = t - tq; hud(img, 10, 4); img.alpha_composite(confetti(W, H, u + 1))
        paste(img, table(u, 10, 960, "green"), cx, 900, 1)
        pop(img, stamp("CLASSIFICADA!", 110, GREEN), cx, 1440, u, 0.6, 0.25, -5)

EVO = [("benny", "BENNY", "VOL", 47, 53, (64, 40, 54, 54, 56, 50), "benny", True), ("leonardo", "LEONARDO", "LE", 50, 54, (72, 42, 58, 56, 54, 58), "leonardo", True),
       ("levi", "LEVI SANTOS", "MEI", 64, 66, (74, 62, 66, 72, 32, 52), "levi3d", False), ("cadorini", "CADORINI", "ATA", 63, 65, (66, 72, 54, 60, 30, 70), "cadorini", False)]
def s10(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 35))
    pop(img, chip("EVOLUÇÃO DO MÊS", 64, INK, AMB), cx, 380, t, 0.0, 0.25, -2)
    for k, (wd, nm, pos, a, b, st, av, prom) in enumerate(EVO):
        t0 = 0.6 + 0.9 * k
        if t < t0: continue
        x, y = (290 if k % 2 == 0 else 790), (760 if k < 2 else 1290)
        u = t - t0; o = int(a + (b - a) * ease(max(0, u - 0.5) / 0.8))
        paste(img, pcard(nm, o, pos, st, 330, prom, av), x, y, 1, 0.85 + 0.15 * back(min(1, u / 0.3)))
        if u > 1.0: paste(img, chip(f"+{b - a}", 56, INK, GREEN), x + 140, y - 230, 1, 0.8 + 0.2 * back(min(1, (u - 1.0) / 0.2)), 8)
    pop(img, chip("DAVI 58 → 59 (LESIONADO)  •  CAUARI 61 → 62", 34, WHITE, INK), cx, 1640, t, 4.2)

XI = [("BERTINATO", 60, 0.50, 0.90), ("JOÃO VITOR", 58, 0.86, 0.72), ("BOTTEGHIN", 61, 0.64, 0.76), ("G. HENRIQUE", 58, 0.36, 0.76), ("LEONARDO", 54, 0.14, 0.72),
      ("HUDSON", 58, 0.50, 0.57), ("LEVI", 66, 0.76, 0.48), ("TONTINI", 60, 0.24, 0.48),
      ("TORÓ", 65, 0.84, 0.26), ("CADORINI", 65, 0.50, 0.20), ("CAUARI", 62, 0.16, 0.26)]
def s11(img, t, T):
    X0, Y0, PW, PH = 70, 420, 940, 1130; d = ImageDraw.Draw(img)
    for k in range(8): d.rectangle((X0, Y0 + k * PH / 8, X0 + PW, Y0 + (k + 1) * PH / 8), fill=(34, 120, 58) if k % 2 else (40, 134, 66))
    L = (235, 245, 235); d.rectangle((X0, Y0, X0 + PW, Y0 + PH), outline=L, width=5); d.line((X0, Y0 + PH / 2, X0 + PW, Y0 + PH / 2), fill=L, width=4)
    d.ellipse((W / 2 - 110, Y0 + PH / 2 - 110, W / 2 + 110, Y0 + PH / 2 + 110), outline=L, width=4)
    d.rectangle((W / 2 - 240, Y0 + PH - 190, W / 2 + 240, Y0 + PH), outline=L, width=4); d.rectangle((W / 2 - 240, Y0, W / 2 + 240, Y0 + 190), outline=L, width=4)
    paste(img, txt("TIME TITULAR", 92, WHITE), cx, 300, 1)
    for k, (nm, o, fx, fy) in enumerate(XI):
        t0 = 0.15 + k * 0.15
        if t < t0: continue
        x, y = X0 + fx * PW, Y0 + fy * PH; u = back(min(1, (t - t0) / 0.25))
        col = (205, 127, 50) if o < 65 else (190, 195, 205); new = nm == "LEONARDO"
        r = 46 * u; d.ellipse((x - r, y - r, x + r, y + r), fill=(240, 60, 60) if new else col, outline=INK, width=5)
        paste(img, text_el(str(o), font("blk", 44), INK, 0, shadow=False), x, y, u)
        paste(img, chip(nm, 30, WHITE, RED if new else INK), x, y + 72, u)
    pop(img, chip("4-3-3  •  MÉDIA 60", 54, INK, AMB), cx, 1640, t, 2.0)
    pop(img, chip("BANCO: BENNY 53 • ROMARINHO 64 • DAVI 59", 34, WHITE, (30, 30, 36)), cx, 1740, t, 2.4)

def s12(img, t, T):  # proposta Cadorini A/B
    ta, tb = wt(12, "vende") - 0.6, wt(12, "segura") - 0.6
    if t < ta:
        pop(img, mail(900, "Clube da Série B", "R$ 1,5 MILHÃO PELO CADORINI"), cx, 640, t, 0.0, 0.3, 2)
        pop(img, pcard("CADORINI", 65, "ATA", (66, 72, 54, 60, 30, 70), 400, False, "cadorini"), cx, 1250, t, wt(12, "cadorini") - 0.3)
        pop(img, chip("O ARTILHEIRO", 56, INK, AMB), cx, 1600, t, wt(12, "artilheiro") - 0.2)
        return
    pop(img, chip("A", 120, WHITE, RED), 280, 420, t, ta)
    pop(img, polaroid_c(), 280, 760, t, ta + 0.05, 0.3, -4)
    pop(img, chip("VENDE", 70, WHITE, RED), 280, 560, t, ta + 0.1)
    pop(img, chip("+ R$ 1,5 MI", 60, INK, GOLD), 280, 980, t, ta + 0.3)
    pop(img, chip("DINHEIRO PRA REFORÇO", 40, INK, WHITE), 280, 1100, t, wt(12, "reforço") - 0.2)
    if t > tb:
        pop(img, chip("B", 120, WHITE, GREEN), 800, 420, t, tb)
        pop(img, pcard("CADORINI", 65, "ATA", (66, 72, 54, 60, 30, 70), 330, False, "cadorini"), 800, 820, t, tb, 0.3)
        pop(img, chip("SEGURA", 54, INK, WHITE), 800, 1110, t, tb + 0.2)
    paste(img, logo("POR", 120), cx, 1450, 1)

@functools.lru_cache(2)
def polaroid_c():
    im = Image.open(IM + "cofre.jpg").convert("RGBA"); im.thumbnail((360, 360)); b = 14
    c = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (245, 245, 240, 255)); c.paste(im, (b, b)); return c
def s13(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 120), 14, 40))
    pop(img, chip("A", 150, WHITE, RED), 300, 700, t, 0.0, 0.3, -5); pop(img, chip("B", 150, WHITE, GREEN), 780, 700, t, 0.1, 0.3, 5)
    pop(img, txt("COMENTA!", 140, AMB), cx, 1000, t, 0.3)
    pop(img, chip("O MAIS CURTIDO ENTRA NO EP.4", 52, INK, WHITE), cx, 1200, t, wt(13, "curtido") - 0.3)

def s14(img, t, T):
    paste(img, logo("POR", 300), cx, 700, 1, 0.9 + 0.1 * back(min(1, t / 0.3)))
    pop(img, chip("NOVOS EPISÓDIOS", 70, INK, AMB), cx, 1020, t, 0.1)
    pop(img, chip("SEGUNDA, QUARTA E SEXTA • 18H", 50, WHITE, INK), cx, 1160, t, 0.4)

SH = Short(D, [(s,) for s in TXT], [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14], "MODO CARREIRA • LUSA • EP.3",
           ["night", "dark", "green", "dark", "green", "night", "red", "night", "dark", "night", "green", "dark", "red", "green", "dark"], "Crossing_the_Chasm", 0)
S = SH
if __name__ == "__main__":
    g = SH.segs
    ev = [("tambor_impacto", 0.0, 0.5), ("whoosh_boom", g[1][0], 0.3), ("tambor_impacto", g[0][0] + wt(0, "acaba"), 0.3),
          ("torcida_comemora", g[5][0] + wt(5, "levi"), 0.25), ("torcida_aww", g[6][0] + wt(6, "davi"), 0.25), ("tambor_impacto", g[7][0] + wt(7, "segura"), 0.3),
          ("apito_juiz", g[8][0] + wt(8, "empate"), 0.3), ("chute_bola_1", g[9][0] + wt(9, "cadorini"), 0.4), ("torcida_reacao_gol", g[9][0] + wt(9, "cadorini") + 0.6, 0.55),
          ("torcida_comemora", g[9][0] + wt(9, "quarto"), 0.3), ("tambor_impacto", g[12][0], 0.3)]
    main(SH, extra=ev)
