"""Cenas do documentário (registradas em SCN). Assinatura: f(img, t, dur, T)."""
from __main__ import *  # noqa
import __main__ as M
cx, cy = W / 2, H / 2


def w(word, nth=0, d=0.4): return M.S.wt(M.S.i, word, nth, d)


# ============ CAPÍTULO 1 — 1968 (sépia) ============
@sc("cap1")
def _(img, t, d, T): chapter_card(img, t, T, 1, "A PRIMEIRA FERIDA", "centst", "sepia")

@sc("map68")
def _(img, t, d, T):
    bgc(img, "sepia", T); dr = ImageDraw.Draw(img)
    pts = {"SÃO PAULO": (1420, 330), "MONTEVIDÉU": (820, 760), "LA PLATA": (560, 690)}
    for k, (nm, (x, y)) in enumerate(pts.items()):
        u = ease((t - 0.3 - 0.35 * k) / 0.4)
        if u <= 0: continue
        r = 18 * u; dr.ellipse((x - r, y - r, x + r, y + r), fill=AMB, outline=INK, width=4)
        paste(img, tx(nm, 50, WHITE), x, y - 55, u)
    if t > 1.2:
        u = ease((t - 1.2) / 1.0); a, b = pts["SÃO PAULO"], pts["MONTEVIDÉU"]
        dr.line((a, (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)), fill=(255, 255, 255), width=6)
    pop(img, datestamp("MAIO • 1968", 56), 360, 170, t, 0.0)
    pop(img, tx("2ª FINAL DO PALMEIRAS", 90, WHITE), 1250, 900, t, w("segunda") - 0.2)

@sc("pal68")
def _(img, t, d, T):
    bgc(img, "sepia", T); pop(img, logo("PAL", 300), 330, 480, t, 0.0, 0.35)
    names = [("ADEMIR DA GUIA", "O DIVINO", "ademir"), ("DUDU", "VOLANTE", "dudu"), ("SERVÍLIO", "ATACANTE", "servílio"), ("TUPÃZINHO", "ARTILHEIRO DA LIBERTADORES", "tupãzinho")]
    for k, (nm, sub, kw) in enumerate(names):
        slide(img, namecard(nm, sub, 880), 1150, 220 + 180 * k, t, w(kw, d=0.6 + 0.8 * k) - 0.2, 600)

@sc("est68")
def _(img, t, d, T):
    kb(img, "laplata", t, d, "sepia", dim=170)
    pop(img, logo("EST", 330), 420, 500, t, 0.1, 0.35)
    pop(img, tx("ESTUDIANTES DE LA PLATA", 96, WHITE), 1180, 420, t, 0.4)
    pop(img, namecard("OSVALDO ZUBELDÍA", "TÉCNICO", 760, (200, 20, 30)), 1180, 620, t, w("zubeldía") - 0.3)

@sc("zubel")
def _(img, t, d, T):
    if t < w("juan") - 0.2:
        bgc(img, "red", T)
        for k, (s, kw) in enumerate((("MARCAÇÃO DURA", "marcação"), ("PROVOCAÇÃO", "provocação"), ("BOLA PARADA", "bola"))):
            pop(img, stamp(s, 100, (240, 230, 220)), cx + (k - 1) * 120, 260 + 210 * k, t, w(kw) - 0.15, 0.25, (-6, 4, -3)[k])
        pop(img, namecard("BILARDO", "MEIO-CAMPO", 560, (200, 20, 30)), 1500, 900, t, w("bilardo") - 0.2)
    else:
        u = t - (w("juan") - 0.2)
        kb(img, "brujas", u, d - w("juan"), "sepia", (1.05, 1.15), dim=140)
        pop(img, namecard("JUAN RAMÓN VERÓN", "ATACANTE • 1968", 860, (200, 20, 30)), 560, 260, u, 0.0)
        pop(img, stamp("LA BRUJA", 170, RED), cx + shake(t, w("bruja") , 14), 640, t, w("bruja") - 0.2, 0.3, -7)

@sc("ida")
def _(img, t, d, T):
    bgc(img, "sepia", T)
    pop(img, datestamp("IDA • LA PLATA • 02/05/1968", 44), cx, 120, t, 0.0)
    pop(img, pitch(900, 520, t, [(0.3, 0.6), (0.6, 0.35), (0.85, 0.55), (0.99, 0.5)], w("servílio") - 0.2, 1.0), 560, 560, t, 0.1)
    g = t > w("servílio") + 0.6
    pop(img, scorebox("EST", "PAL", 0, 1 if g else 0, 120), 1440, 460, t, 0.2)
    if g: pop(img, chip("SERVÍLIO ⚽", 50, INK, AMB) if False else chip("GOL: SERVÍLIO", 50, INK, AMB), 1440, 680, t, w("servílio") + 0.6)

@sc("ida2")
def _(img, t, d, T):
    bgc(img, "red", T); tv, tf = w("verón") - 0.2, w("flores") - 0.2
    pop(img, odometer(83 if t < tf else 87, 2, 200, t - (w("trinta") - 0.2), 0.7), 420, 520, t, w("trinta") - 0.2)
    pop(img, tx("MIN", 70, AMB), 420, 700, t, w("trinta"))
    ga = 2 if t > tf else (1 if t > tv else 0)
    pop(img, scorebox("EST", "PAL", ga, 1, 130), 1300 + shake(t, tv, 16) + shake(t, tf, 16), 440, t, 0.0)
    pop(img, chip("83' VERÓN", 54, WHITE, RED), 1150, 680, t, tv)
    pop(img, chip("87' FLORES", 54, WHITE, RED), 1470, 680, t, tf)

@sc("volta")
def _(img, t, d, T):
    bgc(img, "sepia", T)
    pop(img, datestamp("VOLTA • PACAEMBU • 07/05/1968", 44), cx, 120, t, 0.0)
    pop(img, scorebox("PAL", "EST", 3, 1, 140), cx, 420, t, w("responde") - 0.2)
    for k, (s, kw) in enumerate((("TUPÃZINHO 2x", "tupãzinho"), ("RINALDO", "rinaldo"))):
        pop(img, chip(s, 58, INK, AMB), cx - 250 + 500 * k, 700, t, w(kw) - 0.2, 0.3, (-3, 3)[k])

@sc("regra")
def _(img, t, d, T):
    bgc(img, "navy", T)
    pop(img, tx("REGULAMENTO DE 1968", 80, AMB), cx, 220, t, 0.0)
    pop(img, stamp("SEM SALDO DE GOLS", 120, RED), cx, 430, t, w("saldo") - 0.2, 0.3, -4)
    tb = w("terceiro") - 0.3
    pop(img, crest("PAL", 150), 520, 750, t, w("vitória") - 0.2); pop(img, tx("1 VITÓRIA", 60), 520, 880, t, w("vitória"))
    pop(img, crest("EST", 150), 1000, 750, t, w("vitória") + 0.2); pop(img, tx("1 VITÓRIA", 60), 1000, 880, t, w("vitória") + 0.3)
    pop(img, tx("= 3º JOGO", 110, AMB), 1480, 780, t, tb)

@sc("cent68")
def _(img, t, d, T):
    kb(img, "cent30", t, d, "sepia", (1.0, 1.15), (0.5, 0.55), (0.5, 0.45), dim=110)
    pop(img, datestamp("16 DE MAIO DE 1968", 60), cx, 200, t, w("dezesseis") - 0.2)
    pop(img, tx("ESTÁDIO CENTENÁRIO", 140, WHITE, "anton", 8), cx, 820, t, w("centenário") - 0.25)
    pop(img, tx("MONTEVIDÉU", 70, AMB), cx, 940, t, w("montevidéu") - 0.2)

@sc("des")
def _(img, t, d, T):
    kb(img, "centst", t, d, "sepia", dim=180, blur=4); tr, tv = w("ribaudo") - 0.2, w("verón") - 0.2
    ga = 2 if t > tv else (1 if t > tr else 0)
    pop(img, datestamp("JOGO DESEMPATE • CENTENÁRIO", 44), cx, 140, t, 0.0)
    pop(img, scorebox("EST", "PAL", ga, 0, 150), cx + shake(t, tr) + shake(t, tv), 440, t, 0.1)
    pop(img, chip("13' RIBAUDO", 56, WHITE, RED), cx - 260, 720, t, tr)
    pop(img, chip("82' VERÓN", 56, WHITE, RED), cx + 260, 720, t, tv)

@sc("ferida")
def _(img, t, d, T):
    bgc(img, "red", T); pop(img, logo("EST", 220), cx, 240, t, 0.0)
    for k, (y, kw, nth) in enumerate((("1968", "campeão", 0), ("1969", "sessenta", 0), ("1970", "setenta", 0))):
        x = cx + (k - 1) * 380; t0 = w(kw, nth) - 0.2 if k else w("campeão") - 0.2
        pop(img, trophy(240), x, 600, t, t0, 0.3, (-4, 0, 4)[k]); pop(img, chip(y, 56, INK, WHITE), x, 780, t, t0 + 0.1)
    pop(img, stamp("TRI SEGUIDO", 120, AMB), cx, 940, t, w("tricampeão") - 0.2, 0.3, -5)

@sc("ferida2")
def _(img, t, d, T):
    kb(img, "centw", t, d, "gray", dim=150)
    pop(img, tx("GUARDA ESSE NOME:", 80, WHITE), cx, 380, t, w("guarda") - 0.2)
    pop(img, stamp("CENTENÁRIO", 170, AMB), cx + shake(t, w("centenário"), 12), 560, t, w("centenário") - 0.2, 0.3, -5)


# ============ CAPÍTULO 2 ============
@sc("cap2")
def _(img, t, d, T): chapter_card(img, t, T, 2, "O ESTÁDIO MALDITO", "centw2", "gray")

def final_row(img, t, y0, items, t0s):
    for k, ((yr, opp, res, sub, ok), t0) in enumerate(zip(items, t0s)):
        x = 330 + 420 * k
        pop(img, tx(yr, 96, WHITE), x, y0, t, t0)
        pop(img, crest(opp, 150), x, y0 + 170, t, t0 + 0.1)
        pop(img, chip(res, 46, INK, AMB), x, y0 + 300, t, t0 + 0.2)
        pop(img, xmark(90, ok), x + 110, y0 + 110, t, t0 + 0.3)
        if sub: pop(img, tx(sub, 40, (220, 220, 220), "anton", 4), x, y0 + 380, t, t0 + 0.25)

@sc("t61")
def _(img, t, d, T):
    kb(img, "centw", t, d, "gray", dim=170)
    pop(img, tx("1961", 220, WHITE, "anton", 10), 520, 420, t, 0.0)
    pop(img, tx("1ª FINAL DO PALMEIRAS", 60, AMB), 520, 600, t, w("primeira") - 0.2)
    pop(img, scorebox("PEÑ", "PAL", 1, 0, 120, "NO CENTENÁRIO"), 1360, 520, t, w("peñarol") - 0.2)

@sc("tl")
def _(img, t, d, T):
    bgc(img, "gray", T)
    final_row(img, t, 260, [("1961", "PEÑ", "PEÑAROL", "CENTENÁRIO", False), ("1968", "EST", "ESTUDIANTES", "CENTENÁRIO", False)], [0.1, w("derrotas") - 0.2])
    pop(img, stamp("MONTEVIDÉU", 120, RED), 1400, 520, t, w("montevidéu") - 0.2, 0.3, -6)

@sc("t99")
def _(img, t, d, T):
    kb(img, "allianz", t, d, "color", dim=160)
    pop(img, tx("1999", 200, GOLD, "anton", 10), 480, 380, t, w("noventa") - 0.2)
    pop(img, trophy(300), 480, 700, t, w("título") - 0.1 if w("título") < 1 else 0.3)
    pop(img, namecard("FELIPÃO", "TÉCNICO", 600), 1300, 360, t, w("felipão") - 0.2)
    pop(img, chip("PÊNALTIS x DEPORTIVO CALI", 50, INK, AMB), 1300, 560, t, w("pênaltis") - 0.2)
    pop(img, stamp("CAMPEÃO", 120, GREEN), 1300, 760, t, w("cali") + 0.2, 0.3, -5)

@sc("t00")
def _(img, t, d, T):
    bgc(img, "navy", T)
    pop(img, tx("2000", 200, WHITE, "anton", 10), 480, 420, t, w("ano") - 0.2)
    pop(img, crest("BOC", 260), 1300, 400, t, w("boca") - 0.2)
    pop(img, chip("PÊNALTIS • MORUMBI", 56, WHITE, RED), 1300, 640, t, w("pênaltis") - 0.2)
    pop(img, xmark(140), 480, 700, t, w("dor") - 0.1)

@sc("t00b")
def _(img, t, d, T):
    kb(img, "torcida", t, d, "gray", dim=170)
    if t > w("vinte") - 0.3: pop(img, odometer(20, 2, 230, t - w("vinte") + 0.3, 0.8), cx - 150, 430, t, w("vinte") - 0.3)
    pop(img, tx("ANOS", 140, AMB), cx + 230, 430, t, w("anos") - 0.2)
    pop(img, tx("CHEGANDO PERTO...", 90, WHITE), cx, 700, t, w("perto") - 0.2)


# ============ CAPÍTULO 3 ============
@sc("cap3")
def _(img, t, d, T): chapter_card(img, t, T, 3, "O HOMEM QUE MUDOU TUDO", "abel2")

@sc("abel")
def _(img, t, d, T):
    kb(img, "abel2", t, d, "color", (1.05, 1.15), (0.5, 0.35), (0.48, 0.3), dim=120)
    pop(img, namecard("ABEL FERREIRA", "PORTUGAL • 41 ANOS • 2020", 820), 520, 860, t, w("abel") - 0.3)
    pop(img, chip("QUASE NINGUÉM CONHECIA", 46, INK, AMB), 1450, 200, t, w("ninguém") - 0.2, 0.3, 3)

@sc("t20")
def _(img, t, d, T):
    bgc(img, "green", T); tb = w("breno") - 0.25
    pop(img, datestamp("MARACANÃ • 30/01/2021", 44), cx, 110, t, 0.0)
    pop(img, scorebox("PAL", "SAN", 1 if t > tb else 0, 0, 130), 1300 + shake(t, tb), 400, t, 0.1)
    if t > w("noventa") - 0.3: pop(img, odometer(99, 2, 190, t - w("noventa") + 0.3, 0.6), 420, 420, t, w("noventa") - 0.3)
    pop(img, tx("MIN", 60, AMB), 420, 590, t, w("noventa"))
    pop(img, pitch(760, 420, t, [(0.55, 0.15), (0.86, 0.45), (0.995, 0.5)], tb, 0.8), 1300, 760, t, tb - 0.2)
    pop(img, chip("BRENO LOPES, DE CABEÇA", 46, INK, AMB), 420, 760, t, tb)
    pop(img, stamp("BICAMPEÃO", 110, GREEN), 420, 920, t, w("bicampeão") - 0.2, 0.3, -5)

@sc("t21")
def _(img, t, d, T):
    kb(img, "cent", t, d, "color", (1.0, 1.15), (0.5, 0.6), (0.5, 0.45), dim=110)
    pop(img, tx("ADIVINHA ONDE?", 110, WHITE), cx, 300, t, 0.2)
    pop(img, stamp("CENTENÁRIO", 170, AMB), cx + shake(t, w("centenário"), 14), 620, t, w("centenário") - 0.2, 0.3, -5)

@sc("t21b")
def _(img, t, d, T):
    kb(img, "centst", t, d, "color", dim=190, blur=5); tv, tg = w("raphael") - 0.2, w("gabigol") - 0.2
    pop(img, datestamp("27 DE NOVEMBRO DE 2021", 52), cx, 130, t, 0.0)
    pop(img, scorebox("PAL", "FLA", 1 if t > tv else 0, 1 if t > tg else 0, 140), cx + shake(t, tv) + shake(t, tg), 420, t, w("palmeiras") - 0.2)
    pop(img, chip("5' RAPHAEL VEIGA", 52, INK, AMB), cx - 300, 700, t, tv)
    pop(img, chip("GABIGOL", 52, WHITE, RED), cx + 300, 700, t, tg)

@sc("t21c")
def _(img, t, d, T):
    bgc(img, "green", T); tr = w("rouba") - 0.2; tf = w("faz") - 0.2
    pop(img, stamp("PRORROGAÇÃO", 110, AMB), cx, 150, t, 0.0, 0.3, -3)
    pop(img, pitch(1000, 560, t, [(0.35, 0.45), (0.5, 0.5), (0.75, 0.48), (0.9, 0.5), (0.995, 0.47)], tr, 2.2), 620, 600, t, 0.2)
    pop(img, namecard("DEYVERSON", "ROUBA DO ANDREAS PEREIRA", 640), 1500, 430, t, tr)
    pop(img, scorebox("PAL", "FLA", 2, 1, 110), 1500 + shake(t, tf), 700, t, tf)
    pop(img, stamp("TRI!", 140, GREEN), 1500, 920, t, w("tricampeão") - 0.2, 0.3, -6)
    if t > tf: img.alpha_composite(confetti(W, H, t - tf, seed=5))

@sc("t21d")
def _(img, t, d, T):
    u = min(1, t / 1.2)
    kb(img, "centw", t, d, "gray" if u < 0.5 else "color", dim=110)
    pop(img, tx("A MALDIÇÃO", 140, WHITE, "anton", 8), cx, 380, t, w("maldição") - 0.3)
    pop(img, tx("VIROU CASA", 160, GREEN, "anton", 9), cx, 560, t, w("casa") - 0.3)

@sc("t25")
def _(img, t, d, T):
    bgc(img, "gray", T); tl = w("lima") - 0.2
    pop(img, tx("2025", 180, WHITE), 440, 380, t, w("vinte") - 0.2)
    pop(img, chip("3ª FINAL DO ABEL", 50, INK, AMB), 440, 560, t, w("terceira") - 0.2)
    pop(img, scorebox("PAL", "FLA", 0, 1, 130, "LIMA • GOL DE DANILO", True), 1300, 440, t, tl)
    pop(img, xmark(130), 440, 760, t, w("derrota") - 0.1)

@sc("t25b")
def _(img, t, d, T):
    kb(img, "abel1", t, d, "color", (1.05, 1.12), dim=150)
    pop(img, tx("A PERGUNTA:", 70, AMB), 1350, 300, t, w("pergunta") - 0.2)
    pop(img, tx("ELE APRENDEU", 110, WHITE), 1350, 470, t, w("aprendeu") - 0.3)
    pop(img, tx("A PERDER?", 130, WHITE), 1350, 620, t, w("perder") - 0.3)


# ============ CAPÍTULO 4 ============
@sc("cap4")
def _(img, t, d, T): chapter_card(img, t, T, 4, "O FANTASMA DE LA PLATA", "laplata")

@sc("e09")
def _(img, t, d, T):
    bgc(img, "red", T)
    pop(img, tx("O ESTUDIANTES NUNCA MORREU", 80, WHITE), cx, 170, t, 0.0)
    pop(img, tx("2009", 190, WHITE), 440, 400, t, w("dois") - 0.2)
    pop(img, trophy(220), 440, 680, t, w("quarta") - 0.2)
    pop(img, scorebox("CRU", "EST", 1, 2, 130, "MINEIRÃO • VIRADA"), 1300, 460, t, w("mineirão") - 0.2)
    pop(img, chip("4ª LIBERTADORES", 54, INK, AMB), 1300, 760, t, w("quarta") - 0.1)

@sc("veron")
def _(img, t, d, T):
    bgc(img, "red", T)
    pop(img, polaroid("veron", 520, "color", -4), 520, 540, t, w("juan") - 0.3, 0.35, -4)
    pop(img, namecard("JUAN SEBASTIÁN VERÓN", "CÉREBRO DO TÍTULO DE 2009", 900, (200, 20, 30)), 1350, 340, t, w("juan") - 0.2)
    pop(img, stamp("FILHO DA BRUXA", 110, AMB), 1350, 580, t, w("filho") - 0.2, 0.3, -5)
    pop(img, chip("DEPOIS: PRESIDENTE DO CLUBE", 46, WHITE, INK), 1350, 790, t, w("presidente") - 0.3)

@sc("e26")
def _(img, t, d, T):
    kb(img, "laplata", t, d, "color", dim=160)
    pop(img, logo("EST", 260), 460, 480, t, 0.1)
    pop(img, namecard("ALEXANDER MEDINA", "TÉCNICO URUGUAIO", 820, (200, 20, 30)), 1300, 400, t, w("alexander") - 0.3)
    pop(img, stamp("CASCA-GROSSA", 120, RED), 1300, 650, t, w("casca") - 0.2, 0.3, -5)

@sc("e26b")
def _(img, t, d, T):
    bgc(img, "navy", T)
    pop(img, scorebox("UC", "EST", 0, 3, 110, "OITAVAS • SANTIAGO"), 520, 330, t, w("atropela") - 0.2)
    pop(img, scorebox("COR", "EST", 0, 1, 110, "QUARTAS • ITAQUERA • 87'"), 1400, 330, t, w("corinthians") - 0.2)
    pop(img, chip("PÊNALTI DO MEMPHIS: PRA FORA", 54, WHITE, RED), 1400, 640, t, w("pênalti") - 0.2, 0.3, -3)
    pop(img, xmark(110), 1400, 790, t, w("isolado") - 0.1)

@sc("e26c")
def _(img, t, d, T):
    bgc(img, "red", T)
    pop(img, tx("SEMIFINAL", 90, AMB), cx, 150, t, 0.0)
    pop(img, scorebox("EST", "FLA", 0, 0, 110, "IDA • LA PLATA"), 520, 420, t, w("dois") - 0.2)
    pop(img, scorebox("FLA", "EST", 0, 0, 110, "VOLTA • MARACANÃ"), 1400, 420, t, w("dois", 1) - 0.2)
    pop(img, stamp("PÊNALTIS NO MARACANÃ", 110, WHITE), cx, 800, t, w("pênaltis") - 0.2, 0.3, -4)

@sc("mus")
def _(img, t, d, T):
    kb(img, "musuy", t, d, "color", (1.05, 1.15), (0.5, 0.3), (0.5, 0.25), dim=130)
    pop(img, namecard("FERNANDO MUSLERA", "GOLEIRO • URUGUAI • GALATASARAY", 900, (200, 20, 30)), 1350, 300, t, w("fernando") - 0.3)
    pop(img, tx("40 ANOS", 160, AMB, "anton", 9), 1350, 560, t, w("quarenta") - 0.3)

@sc("mus2")
def _(img, t, d, T):
    bgc(img, "red", T)
    n = sum(t > w(k) - 0.1 for k in ("jorginho", "paquetá", "bruno"))
    pop(img, pens(["JORGINHO", "PAQUETÁ", "BRUNO HENRIQUE"], [False] * 3, n, 980), 640, 450, t, w("jorginho") - 0.2)
    pop(img, tx("3", 300, AMB, "anton", 12), 1500, 400, t, w("três") - 0.2)
    pop(img, tx("DEFESAS", 90, WHITE), 1500, 600, t, w("defesas") - 0.2)
    pop(img, chip("COM UM A MENOS", 50, WHITE, INK), 1500, 790, t, w("menos") - 0.2)

@sc("mus3")
def _(img, t, d, T):
    kb(img, "cent", t, d, "color", (1.05, 1.2), dim=150)
    pop(img, crest("PAL", 230), 560, 440, t, w("palmeiras") - 0.2, 0.3, -5)
    pop(img, tx("x", 120, AMB), cx, 440, t, w("palmeiras"))
    pop(img, crest("EST", 230), 1360, 440, t, w("palmeiras") + 0.15, 0.3, 5)
    pop(img, stamp("58 ANOS DEPOIS", 140, AMB), cx, 760, t, w("cinquenta") - 0.2, 0.3, -4)


# ============ CAPÍTULO 5 ============
@sc("cap5")
def _(img, t, d, T): chapter_card(img, t, T, 5, "O CAMINHO MAIS SOFRIDO", "torcida")

def leg(img, t, a, b, ga, gb, sub, x, y, t0, sz=110):
    pop(img, scorebox(a, b, ga, gb, sz, sub), x, y, t, t0)

@sc("p1")
def _(img, t, d, T):
    bgc(img, "green", T); pop(img, tx("OITAVAS", 90, AMB), cx, 140, t, 0.0)
    leg(img, t, "PAL", "CER", 1, 1, "IDA • SÃO PAULO", 520, 450, w("cerro") - 0.2)
    leg(img, t, "CER", "PAL", 0, 1, "VOLTA • ASSUNÇÃO", 1400, 450, w("assunção") - 0.3)
    pop(img, chip("GOL: GUSTAVO GÓMEZ", 54, INK, AMB), 1400, 740, t, w("gustavo") - 0.2)

@sc("p2")
def _(img, t, d, T):
    bgc(img, "navy", T); pop(img, tx("QUARTAS", 90, AMB), cx, 140, t, 0.0)
    leg(img, t, "PAL", "LDU", 1, 0, "IDA • SÃO PAULO", 520, 450, w("ldu") - 0.2)
    leg(img, t, "LDU", "PAL", 3, 2, "VOLTA • QUITO (ALTITUDE)", 1400, 450, w("quito") - 0.2)
    pop(img, stamp("PÊNALTIS", 120, RED), cx, 820, t, w("pênaltis") - 0.2, 0.3, -4)

@sc("p3")
def _(img, t, d, T):
    bgc(img, "green", T)
    from gfx import INK as _I  # noqa
    pop(img, namecard("CARLOS MIGUEL", "GOLEIRO DO PALMEIRAS", 820), 560, 300, t, w("carlos") - 0.3)
    if t > w("dois") - 0.3:
        u = t - w("dois") + 0.3; dr = ImageDraw.Draw(img); hh = 520 * ease(u / 0.8)
        dr.line((260, 980, 260, 980 - hh), fill=WHITE, width=10)
        for k in range(0, int(hh), 52): dr.line((260, 980 - k, 300, 980 - k), fill=WHITE, width=5)
        pop(img, tx("2,04 m", 150, GREEN), 560, 760, t, w("dois") - 0.3)
    pop(img, pens(["DEFESA 1", "DEFESA 2"], [True, True], 2, 640), 1450, 520, t, w("duas") - 0.2)
    pop(img, chip("4 x 3 NOS PÊNALTIS", 54, INK, AMB), 1450, 820, t, w("quatro") - 0.2)

@sc("p4")
def _(img, t, d, T):
    bgc(img, "red", T); pop(img, tx("SEMIFINAL", 90, AMB), cx, 140, t, 0.0)
    leg(img, t, "FLU", "PAL", 1, 2, "IDA • MARACANÃ", 520, 450, w("dois") - 0.2)
    leg(img, t, "PAL", "FLU", 0, 1, "VOLTA • EM CASA", 1400, 450, w("volta") - 0.2)
    pop(img, chip("81' HÉRCULES", 56, WHITE, RED), 1400, 740, t, w("hércules") - 0.2)
    pop(img, stamp("PÊNALTIS DE NOVO", 110, AMB), cx, 900, t, w("pênaltis") - 0.2, 0.3, -4)

@sc("p5")
def _(img, t, d, T):
    bgc(img, "green", T)
    pop(img, pens(["NONATO (FLU)", "MARLON FREITAS (PAL)"], [False, True], 1 + (t > w("marlon") - 0.1), 980), 640, 430, t, w("nonato") - 0.3)
    pop(img, tx("5 x 3", 200, WHITE, "anton", 10), 1500, 430, t, w("cinco") - 0.2)
    pop(img, stamp("FINAL!", 160, GREEN), 1500 + shake(t, w("final")), 700, t, w("final") - 0.2, 0.3, -6)
    if t > w("final"): img.alpha_composite(confetti(W, H, t - w("final"), seed=2))

@sc("p6")
def _(img, t, d, T):
    bgc(img, "navy", T); tb = w("boca") - 0.3
    pop(img, tx("FINAIS DE LIBERTADORES", 70, AMB), cx, 150, t, 0.0)
    bars(img, [("PALMEIRAS", 8, (30, 160, 80)), ("PEÑAROL", 10, (230, 190, 20)), ("BOCA", 12, (30, 60, 160))], t, min(tb, w("oitava") - 0.2), 560, 360, 12, 980)
    pop(img, namecard("ABEL: 4ª FINAL", "11 TÍTULOS • O MAIOR DA HISTÓRIA DO CLUBE", 1000), cx, 920, t, w("quarta") - 0.3)

@sc("p7")
def _(img, t, d, T):
    kb(img, "cent", t, d, "color", (1.1, 1.25), (0.5, 0.55), (0.5, 0.45), dim=140)
    pop(img, polaroid("musgol", 380, "color", 4), 1500, 520, t, w("goleiros") - 0.3, 0.3, 5)
    pop(img, tx("DOIS GOLEIROS HERÓIS", 70, WHITE), 600, 300, t, w("goleiros") - 0.3)
    pop(img, tx("UM ESTÁDIO COM MEMÓRIA", 70, AMB), 600, 450, t, w("estádio") - 0.3)
    pop(img, stamp("TAVA TUDO PRONTO", 120, WHITE), 650, 750, t, w("pronto") - 0.4, 0.3, -4)
