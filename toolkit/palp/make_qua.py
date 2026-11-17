import os, sys, math, subprocess, importlib
from PIL import Image, ImageDraw
import vlib
from vlib import *
from make_palp import badge, chip, TEAMS, BG, grid_bg, mono, ACC, RED, GREY

HERE = "/home/claude/work/palp"
WMOD = importlib.import_module(os.environ.get("WORDS", "words_qua"))
LEAD = 0.2
WL = WMOD.W
WORDS = []
for i, (w, s) in enumerate(WL):
    e = WL[i + 1][1] if i + 1 < len(WL) else WMOD.END
    WORDS.append([w, s / 1000 + LEAD, min(e, s + 900) / 1000 + LEAD])
TOTAL = WMOD.END / 1000 + LEAD + 1.8
vlib.CF = font(BLK, 60)
def T(word, nth=0):
    c = 0
    for w, a, b in WORDS:
        if w.lower().strip(".,:;!?") == word.lower():
            if c == nth: return a
            c += 1
    raise KeyError(word)

def match_card(img, t, home, away, sh, sa, t_in, t_rev, t_out, info, notes=(), tag=None):
    u = ease((t - t_in) / 0.4); dx = 600 * (1 - u)
    if t > t_out: dx -= 1100 * ease((t - t_out) / 0.35)
    cy = 820
    put(img, card(980, 700, (18, 21, 24, 240), 36, (255, 255, 255, 30), 2), W / 2 + dx, cy, 1, u)
    for k, (code, x) in enumerate(((home, W / 2 - 280), (away, W / 2 + 280))):
        b = badge(code, 220)
        if t > t_rev and ((k == 0 and sh > sa) or (k == 1 and sa > sh)): b = glow(b, ACC, 16, 0.8)
        put(img, b, x + dx, cy - 160, 1, u)
        put(img, txt(TEAMS[code][0], fitf(BLK, TEAMS[code][0], 380, 44), WHITE), x + dx, cy - 10, 1, u)
    put(img, txt("x", font(BD, 64), GREY), W / 2 + dx, cy - 160, 1, u)
    put(img, txt(info, mono(26), GREY), W / 2 + dx, cy - 360 + 0, 1, u)
    for side, text, tn, col in notes:
        if t < tn: continue
        v = ease((t - tn) / 0.3)
        x = W / 2 - 280 if side == 0 else W / 2 + 280
        put(img, chip(text, col, 24, (255, 255, 255) if col == RED else (12, 12, 14)), x + dx, cy + 60 + 20 * (1 - v), 1, v)
    if t > t_rev:
        v = ease((t - t_rev) / 0.3); pop = 1 + 0.35 * (1 - v)
        put(img, chip("PALPITE", ACC, 26), W / 2 + dx, cy + 150, 1, v)
        for k, (n, x) in enumerate(((sh, W / 2 - 120), (sa, W / 2 + 120))):
            col = ACC if (k == 0 and sh > sa) or (k == 1 and sa > sh) else WHITE
            put(img, txt(str(n), font(BLK, 150), col, shadow=10), x + dx, cy + 265, pop, v)
        put(img, txt("x", font(BD, 60), GREY), W / 2 + dx, cy + 265, 1, v)
    if tag and t > tag[1]:
        v = ease((t - tag[1]) / 0.3)
        put(img, chip(tag[0], tag[2], 40, (255, 255, 255) if tag[2] == RED else (12, 12, 14)), W / 2 + dx, cy + 420, 1.3 - 0.3 * v, v)

def small_rows(img, t, title, rows, t_in, t_out):
    u = ease((t - t_in) / 0.4); dx = 600 * (1 - u) - (1100 * ease((t - t_out) / 0.35) if t > t_out else 0)
    put(img, txt(title, fitf(BLK, title, 960, 64), WHITE, shadow=8), W / 2 + dx, 420, 1, u)
    for i, (h_, a_, sh, sa, ta, note) in enumerate(rows):
        if t < ta: continue
        v = ease((t - ta) / 0.3)
        r = card(960, 170, (18, 21, 24, 240), 24, (255, 255, 255, 30), 2)
        r.alpha_composite(badge(h_, 120), (12, 10)); r.alpha_composite(badge(a_, 120), (960 - 172, 10))
        d = ImageDraw.Draw(r)
        d.text((180, 70), TEAMS[h_][0], font=fitf(BLK, TEAMS[h_][0], 230, 36), fill=WHITE, anchor="lm")
        d.text((780, 70), TEAMS[a_][0], font=fitf(BLK, TEAMS[a_][0], 230, 36), fill=WHITE, anchor="rm")
        d.text((480, 70), f"{sh} x {sa}", font=font(BLK, 62), fill=ACC, anchor="mm")
        if note: d.text((480, 135), note, font=mono(22), fill=GREY, anchor="mm")
        put(img, r, W / 2 + dx + 300 * (1 - v), 600 + i * 200, 1, v)

def standings(img, t, t0, rows, extra=None):
    u = ease((t - t0) / 0.4)
    put(img, txt("SE EU ACERTAR...", font(BLK, 72), WHITE, shadow=8), W / 2, 330, 1, u)
    p = ease((t - t0 - 0.6) / 0.8)
    for i, (pos, code, a, b, hl) in enumerate(rows):
        v = ease((t - t0 - 0.2 - i * 0.15) / 0.35)
        r = card(940, 160, (18, 21, 24, 240), 26, (ACC + (200,)) if hl else (255, 255, 255, 30), 3 if hl else 2)
        r.alpha_composite(badge(code, 120), (10, 10)); d = ImageDraw.Draw(r)
        d.text((170, 80), f"{pos}º  {TEAMS[code][0]}", font=font(BLK, 48), fill=WHITE, anchor="lm")
        d.text((900, 80), f"{int(round(a + (b - a) * p))}", font=font(BLK, 76), fill=ACC if hl else WHITE, anchor="rm")
        put(img, r, W / 2, 520 + i * 190, 1, v)
    if extra: extra(img, t)

def cta(img, t, t0):
    v = ease((t - t0) / 0.35)
    put(img, txt("E O SEU", font(BLK, 100), WHITE, shadow=8), W / 2, 720, 1, v)
    put(img, glow(txt("PALPITE?", font(BLK, 150), ACC, shadow=10), ACC, 16, 0.7), W / 2, 870, 1.15 - 0.15 * v, v)
    put(img, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1060 + 10 * math.sin(t * 7), 1, ease((t - t0 - 0.4) / 0.3))

def hook(img, t, t_out, l1, l2, sub):
    a = 1 - ease((t - t_out) / 0.35)
    put(img, txt(l1, fitf(BLK, l1, 960, 92), WHITE, shadow=8), W / 2, 700, 1, a * ease(t / 0.3))
    put(img, glow(txt(l2, fitf(BLK, l2, 960, 140), ACC, shadow=10), ACC, 16, 0.7), W / 2, 850, 1.15 - 0.15 * ease(t / 0.4), a * ease(t / 0.3))
    put(img, txt(sub, mono(34), GREY), W / 2, 970, 1, a * ease((t - 0.3) / 0.3))
    mt = card(700, 110, (18, 21, 24, 230), 55, (255, 255, 255, 40), 2); d = ImageDraw.Draw(mt)
    d.text((350, 55), "1º FLA 76   ·   2º PAL 73", font=font(BLK, 44), fill=WHITE, anchor="mm")
    put(img, mt, W / 2, 1120, 1, a * ease((t - 0.6) / 0.4))

def scene_qua(img, t):
    s_cru, s_fla, s_cor, s_gre, s_oth, s_std, s_cta = T("cruzeiro") - 0.3, T("flamengo") - 0.35, T("corinthians") - 0.35, T("grêmio") - 0.35, T("coritiba") + 0.15, T("se") - 0.3, T("comenta") - 0.25
    if t < s_cru + 0.4: hook(img, t, s_cru, "ANÁLISE DOS", "JOGOS DE QUARTA", "35ª RODADA · BRASILEIRÃO")
    if s_cru < t < s_fla + 0.4:
        match_card(img, t, "CRU", "PAL", 1, 2, s_cru, T("2") - 0.05, s_fla, "QUA 18/11 · 20H30 · MINEIRÃO",
                   [(0, "3º · 60 PTS", T("terceiro"), GREY), (1, "DEFESA MENOS VAZADA", T("defesa"), ACC)])
    if s_fla < t < s_cor + 0.4:
        match_card(img, t, "FLA", "CAP", 1, 1, s_fla, T("1", 1) - 0.05, s_cor, "QUA 18/11 · 20H30 · MARACANÃ",
                   [(0, "5 VITÓRIAS SEGUIDAS", T("cinco"), GREY), (1, "5º · LIBERTADORES", T("briga"), GREY)], ("TROPEÇO DO LÍDER", T("tropeço"), ACC))
    if s_cor < t < s_gre + 0.4:
        match_card(img, t, "COR", "BOT", 0, 1, s_cor, T("1", 3) - 0.05, s_gre, "QUA 18/11 · 21H30 · NEO QUÍMICA ARENA",
                   [(0, "17º · ZONA DE REBAIXAMENTO", T("z4"), RED)], ("PODE SER FATAL", T("fatal"), RED))
    if s_gre < t < s_oth + 0.4:
        match_card(img, t, "GRE", "BAH", 1, 1, s_gre, T("1", 4) - 0.05, s_oth, "QUA 18/11 · 21H30 · ARENA DO GRÊMIO",
                   [(0, "18º · Z4", T("também"), RED), (1, "6º · 53 PTS", T("também") + 0.3, GREY)])
    if s_oth < t < s_std + 0.4:
        small_rows(img, t, "OUTROS JOGOS DE QUARTA",
                   [("CFC", "SAN", 1, 1, T("coritiba") - 0.1, "COUTO PEREIRA · 19H30"), ("REM", "CHA", 2, 1, T("remo") - 0.1, "DUELO DOS LANTERNAS · 20H")], s_oth, s_std)
    if s_std < t < s_cta + 0.2:
        a = 1 - ease((t - s_cta) / 0.25)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        def ex(l, tt):
            if tt > s_std + 1.4:
                v = ease((tt - s_std - 1.4) / 0.3)
                put(l, chip("DIFERENÇA: 1 PONTO", ACC, 40), W / 2, 960, 1.2 - 0.2 * v, v)
        standings(lay, t, s_std, [(1, "FLA", 76, 77, False), (2, "PAL", 73, 76, True)], ex)
        if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)
    if t > s_cta: cta(img, t, s_cta)
    return [T("2") - 0.05, T("1", 1) - 0.05, T("1", 3) - 0.05, T("1", 4) - 0.05]


def scene_qui(img, t):
    s_sao, s_vas, s_vit, s_cta = T("são") - 0.3, T("vasco") - 0.35, T("vitória") - 0.35, T("comenta") - 0.25
    if t < s_sao + 0.4: hook(img, t, s_sao, "ANÁLISE DOS", "JOGOS DE QUINTA", "35ª RODADA · BRASILEIRÃO")
    if s_sao < t < s_vas + 0.4:
        match_card(img, t, "SAO", "FLU", 1, 2, s_sao, T("2") - 0.05, s_vas, "QUI 19/11 · 21H30 · MORUMBIS",
                   [(1, "4º · BRIGA PELO G4", T("quarto"), ACC), (0, "10º · 44 PTS", T("décimo"), GREY)])
    if s_vas < t < s_vit + 0.4:
        match_card(img, t, "VAS", "INT", 2, 1, s_vas, T("2", 1) - 0.05, s_vit, "QUI 19/11 · 19H30 · SÃO JANUÁRIO",
                   [(0, "11º · 44 PTS", T("inter") - 0.2, GREY), (1, "16º · COLADO NO Z4", T("colado"), RED)], ("INTER SE COMPLICA", T("complica"), RED))
    if s_vit < t < s_cta + 0.4:
        match_card(img, t, "VIT", "RBB", 1, 1, s_vit, T("1", 2) - 0.05, s_cta, "QUI 19/11 · 19H30 · BARRADÃO",
                   [(0, "15º · LUTA CONTRA A QUEDA", T("também"), RED), (1, "8º · 47 PTS", T("também") + 0.3, GREY)])
    if t > s_cta: cta(img, t, s_cta)
    return [T("2") - 0.05, T("2", 1) - 0.05, T("1", 2) - 0.05]


def TA(word, after):
    for w, a, b in WORDS:
        if a >= after - 0.01 and w.lower().strip(".,:;!?") == word.lower(): return a
    raise KeyError(word)

import functools
@functools.lru_cache(None)
def mini(code, d=54):
    fp = f"/home/claude/work/logos/{code}.png"
    lg = Image.open(fp).convert("RGBA"); lg.thumbnail((d, d), Image.LANCZOS); return lg

@functools.lru_cache(None)
def reason_im(code, text, col):
    f = fitf(BD, text, 800, 36); tw = int(f.getlength(text))
    w = 70 + tw + 40; h = 66
    im = card(w, h, (255, 255, 255, 14), 18, col + (90,), 2); d = ImageDraw.Draw(im)
    lg = mini(code, 48); im.alpha_composite(lg, (14 + (48 - lg.width) // 2, (h - lg.height) // 2))
    d.text((74, h / 2), text, font=f, fill=col, anchor="lm"); return im

def match_card2(img, t, home, away, sh, sa, t_in, t_rev, t_out, info, reasons=(), tag=None):
    u = ease((t - t_in) / 0.4); dx = 600 * (1 - u)
    if t > t_out: dx -= 1100 * ease((t - t_out) / 0.35)
    cy = 860
    put(img, card(1000, 880, (18, 21, 24, 240), 36, (255, 255, 255, 30), 2), W / 2 + dx, cy, 1, u)
    put(img, txt(info, mono(26), GREY), W / 2 + dx, cy - 390, 1, u)
    for k, (code, x) in enumerate(((home, W / 2 - 270), (away, W / 2 + 270))):
        b = badge(code, 210)
        if t > t_rev and ((k == 0 and sh > sa) or (k == 1 and sa > sh)): b = glow(b, ACC, 16, 0.8)
        put(img, b, x + dx, cy - 240, 1, u)
        put(img, txt(TEAMS[code][0], fitf(BLK, TEAMS[code][0], 380, 44), WHITE), x + dx, cy - 90, 1, u)
    put(img, txt("x", font(BD, 64), GREY), W / 2 + dx, cy - 240, 1, u)
    n = len(reasons); step = 74 if n <= 3 else 66
    y0 = cy - 10 if n <= 3 else cy - 20
    for i, (code, text, tn, col) in enumerate(reasons):
        if t < tn: continue
        v = ease((t - tn) / 0.3)
        put(img, reason_im(code, text, col), W / 2 + dx + 60 * (1 - v), y0 + i * step, 1, v)
    if t > t_rev:
        v = ease((t - t_rev) / 0.3); pop = 1 + 0.35 * (1 - v)
        yb = cy + 300
        put(img, chip("PALPITE", ACC, 26), W / 2 + dx - 300, yb, 1, v)
        for k, (nn, x) in enumerate(((sh, W / 2 - 90), (sa, W / 2 + 90))):
            col = ACC if (k == 0 and sh > sa) or (k == 1 and sa > sh) else WHITE
            put(img, txt(str(nn), font(BLK, 120), col, shadow=10), x + dx + 40, yb, pop, v)
        put(img, txt("x", font(BD, 54), GREY), W / 2 + dx + 40, yb, 1, v)
    if tag and t > tag[1]:
        v = ease((t - tag[1]) / 0.3)
        put(img, chip(tag[0], tag[2], 40, (255, 255, 255) if tag[2] == RED else (12, 12, 14)), W / 2 + dx, cy + 480, 1.3 - 0.3 * v, v)

def ycard(rot=0):
    c = Image.new("RGBA", (150, 210), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((5, 5, 145, 205), 14, fill=(250, 210, 40, 255))
    return c

def detail(img, t, t0, t_out):
    a = 1 - ease((t - t_out) / 0.25) if t > t_out else 1
    u = ease((t - t0) / 0.4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    put(lay, txt("O DETALHE", font(BLK, 92), WHITE, shadow=8), W / 2, 360, 1, u)
    put(lay, badge("FLA", 200), W / 2 - 160, 580, 1, u)
    tc = T("oito")
    if t > tc:
        v = ease((t - tc) / 0.3)
        put(lay, txt("8", font(BLK, 200), ACC, shadow=10), W / 2 + 60, 570, 1.3 - 0.3 * v, v)
        put(lay, txt("PENDURADOS", font(BLK, 48), WHITE), W / 2 + 60, 690, 1, v)
    names = ["ARRASCAETA", "PEDRO", "LÉO PEREIRA", "ALEX SANDRO", "PULGAR"]
    ti = T("arrascaeta")
    for i, nm in enumerate(names):
        tn = ti + (0 if i == 0 else 0.6 + i * 0.18)
        if t < tn: continue
        v = ease((t - tn) / 0.25)
        put(lay, chip(nm, (250, 210, 40) if i < 2 else (200, 200, 200), 34), W / 2 + (i % 2 * 2 - 1) * 210 if i < 4 else W / 2, 820 + (i // 2) * 90, 1, v)
    tl = T("levou")
    if t > tl:
        v = ease((t - tl) / 0.3)
        put(lay, ycard(), W / 2 - 330, 1150, 1, v, rot=-12 + 6 * (1 - v))
        put(lay, txt("AMARELO =", font(BLK, 52), WHITE), W / 2 + 80, 1100, 1, v)
        if t > T("fora", 2) - 0.1:
            v2 = ease((t - T("fora", 2) + 0.1) / 0.3)
            put(lay, txt("FORA DE PAL x FLA", font(BLK, 56), RED), W / 2 + 80, 1175, 1, v2)
            put(lay, txt("SÁB 21/11 · 16H30", mono(28), GREY), W / 2 + 80, 1240, 1, v2)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def scene_qua2(img, t):
    P = lambda n: T("palpite", n + 1)
    s_cru, s_fla, s_cor, s_gre, s_oth, s_det, s_cta = T("cruzeiro") - 0.3, T("flamengo") - 0.35, T("corinthians") - 0.35, T("grêmio") - 0.35, T("coritiba") - 0.25, T("agora") - 0.25, T("comenta") - 0.25
    r1, r2, r3, r4 = TA("2", P(0)) - 0.05, TA("2", P(1)) - 0.05, TA("1", P(2)) - 0.05, TA("1", P(3)) - 0.05
    if t < s_cru + 0.4: hook(img, t, s_cru, "PALPITES COM", "O PORQUÊ", "JOGOS DE QUARTA · 35ª RODADA")
    if s_cru < t < s_fla + 0.4:
        match_card2(img, t, "CRU", "PAL", 1, 2, s_cru, r1, s_fla, "QUA 18/11 · 20H30 · MINEIRÃO",
            [("PAL", "SEM GÓMEZ E MAURÍCIO (SELEÇÃO)", T("gómez"), RED), ("PAL", "11 JOGOS SEM PERDER", T("11"), ACC),
             ("PAL", "SÓ 2 DERROTAS FORA NO ANO", T("fora"), ACC), ("CRU", "4 VITÓRIAS SEGUIDAS", T("quatro"), WHITE)])
    if s_fla < t < s_cor + 0.4:
        match_card2(img, t, "FLA", "CAP", 2, 0, s_fla, r2, s_cor, "QUA 18/11 · 20H30 · MARACANÃ",
            [("FLA", "5 VITÓRIAS SEGUIDAS", T("cinco"), ACC), ("FLA", "SÓ 1 DERROTA EM CASA NO ANO", T("uma"), ACC),
             ("CAP", "2 DERROTAS SEGUIDAS", T("duas"), RED)])
    if s_cor < t < s_gre + 0.4:
        match_card2(img, t, "COR", "BOT", 1, 1, s_cor, r3, s_gre, "QUA 18/11 · 21H30 · NEO QUÍMICA ARENA",
            [("COR", "SEM YURI ALBERTO E MATHEUS PEREIRA", T("yuri"), RED), ("COR", "SEM ANDRÉ RAMALHO E ANDRÉ", T("ramalho"), RED),
             ("BOT", "PERDEU 10 DE 17 FORA DE CASA", T("10"), RED)], ("RISCO DE QUEDA: +50%", T("risco"), RED))
    if s_gre < t < s_oth + 0.4:
        match_card2(img, t, "GRE", "BAH", 1, 1, s_gre, r4, s_oth, "QUA 18/11 · 21H30 · ARENA DO GRÊMIO",
            [("BAH", "6º · BRIGA POR LIBERTADORES", T("bahia", 1), WHITE), ("GRE", "18º · JOGA A VIDA EM CASA", T("grêmio", 1), RED)])
    if s_oth < t < s_det + 0.4:
        small_rows(img, t, "OUTROS JOGOS DE QUARTA",
                   [("CFC", "SAN", 2, 1, T("coritiba") - 0.1, "COXA FEZ 3 x 0 NO 1º TURNO"), ("REM", "CHA", 2, 1, T("remo") - 0.1, "19º x 20º · 20H")], s_oth, s_det)
    if s_det < t < s_cta + 0.3: detail(img, t, s_det, s_cta)
    if t > s_cta: cta(img, t, s_cta)
    return [r1, r2, r3, r4]

def scene_qui2(img, t):
    P = lambda n: T("palpite", n + 1)
    s_sao, s_vas, s_vit, s_cta = T("são") - 0.3, T("vasco") - 0.35, T("vitória") - 0.35, T("comenta") - 0.25
    r1, r2, r3 = TA("1", P(0)) - 0.05, TA("2", P(1)) - 0.05, TA("1", P(2)) - 0.05
    if t < s_sao + 0.4: hook(img, t, s_sao, "PALPITES COM", "O PORQUÊ", "JOGOS DE QUINTA · 35ª RODADA")
    if s_sao < t < s_vas + 0.4:
        match_card2(img, t, "SAO", "FLU", 1, 0, s_sao, r1, s_vas, "QUI 19/11 · 21H30 · MORUMBIS",
            [("SAO", "EM CASA: SÓ 3 DERROTAS NO ANO", T("três"), ACC), ("FLU", "FORA: SÓ 4 VITÓRIAS EM 17", T("quatro"), RED)])
    if s_vas < t < s_vit + 0.4:
        match_card2(img, t, "VAS", "INT", 2, 1, s_vas, r2, s_vit, "QUI 19/11 · 19H30 · SÃO JANUÁRIO",
            [("VAS", "VEM DE 3 x 1 NO ATHLETICO", T("3"), ACC), ("INT", "FORA: MENOS DE 1 GOL POR JOGO", T("menos"), RED)],
            ("INTER A UM PASSO DO Z4", T("passo"), RED))
    if s_vit < t < s_cta + 0.4:
        match_card2(img, t, "VIT", "RBB", 1, 1, s_vit, r3, s_cta, "QUI 19/11 · 19H30 · BARRADÃO",
            [("RBB", "8º · JÁ QUASE GARANTIDO NA SULA", T("garantido"), WHITE), ("VIT", "15º · +40% DE RISCO DE QUEDA", T("40%"), RED)])
    if t > s_cta: cta(img, t, s_cta)
    return [r1, r2, r3]

# ---------- simulação ----------
def race(img, t, t0, t_out, keys):
    a = 1 - ease((t - t_out) / 0.3) if t > t_out else 1
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    u = ease((t - t0) / 0.4)
    k = 0
    for i, kf in enumerate(keys):
        if t >= kf[0]: k = i
    tk, label, pts, order, chips = keys[k]
    pv = keys[k - 1] if k > 0 else keys[0]
    p = ease((t - tk) / 0.6) if k > 0 else 1
    put(lay, txt("SIMULAÇÃO", mono(34), ACC), W / 2, 330, 1, u)
    lv = ease((t - tk) / 0.3) if k > 0 else u
    put(lay, txt(label, font(BLK, 96), WHITE, shadow=8), W / 2, 420, 1.15 - 0.15 * lv, lv)
    for code in ("PAL", "FLA"):
        y0 = 620 + pv[3].index(code) * 200; y1 = 620 + order.index(code) * 200
        y = y0 + (y1 - y0) * p
        val = pv[2][code] + (pts[code] - pv[2][code]) * p
        lead = order[0] == code
        r = card(940, 170, (18, 21, 24, 245), 28, (ACC + (220,)) if (lead and code == "PAL") else (255, 255, 255, 40), 3)
        r.alpha_composite(badge(code, 130), (6, 0)); d = ImageDraw.Draw(r)
        d.text((175, 85), f"{order.index(code) + 1}º  {TEAMS[code][0]}", font=font(BLK, 52), fill=WHITE, anchor="lm")
        d.text((905, 85), f"{int(round(val))}", font=font(BLK, 84), fill=ACC if code == "PAL" else WHITE, anchor="rm")
        put(lay, r, W / 2, y, 1, u)
    for j, (text, col, dt) in enumerate(chips):
        if t < tk + dt: continue
        v = ease((t - tk - dt) / 0.3)
        put(lay, chip(text, col, 38, (255, 255, 255) if col == RED else (12, 12, 14)), W / 2, 1030 + j * 95, 1.2 - 0.2 * v, v)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def champion(img, t, t0, t_out):
    a = 1 - ease((t - t_out) / 0.3) if t > t_out else 1
    u = ease((t - t0) / 0.5)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rays(lay, t, W / 2, 700, a=0.6 * u)
    put(lay, glow(badge("PAL", 380), ACC, 22, 0.7), W / 2, 680, 1.2 - 0.2 * u, u)
    put(lay, glow(txt("CAMPEÃO", font(BLK, 150), ACC, shadow=10), ACC, 16, 0.7), W / 2, 960, 1.2 - 0.2 * u, u)
    put(lay, txt("85 PONTOS", font(BLK, 64), WHITE), W / 2, 1090, 1, ease((t - t0 - 0.4) / 0.3))
    confetti(lay, t - t0, u)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def z4(img, t, t0, t_out):
    a = 1 - ease((t - t_out) / 0.3) if t > t_out else 1
    u = ease((t - t0) / 0.4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    put(lay, txt("E LÁ EMBAIXO?", font(BLK, 88), WHITE, shadow=8), W / 2, 340, 1, u)
    tb, tp, tc = T("botafogo"), T("perde"), T("cai")
    cor = 37 + (1 if t > tb else 0)
    rows = [(16, "GRE", 42 if t > tp else 38), (17, "VIT", 40), (18, "COR", cor), (19, "REM", 35), (20, "CHA", 21)]
    fall = ease((t - tc) / 0.4)
    for i, (pos, code, pts) in enumerate(rows):
        v = ease((t - t0 - 0.15 - i * 0.1) / 0.35)
        z = pos >= 17
        oc = (RED + (int(60 + 160 * fall),)) if z else (255, 255, 255, 40)
        r = card(940, 140, (18, 21, 24, 245), 24, oc, 3 if z else 2)
        r.alpha_composite(badge(code, 110), (8, 0)); d = ImageDraw.Draw(r)
        d.text((150, 70), f"{pos}º  {TEAMS[code][0]}", font=font(BLK, 46), fill=WHITE, anchor="lm")
        d.text((905, 70), str(pts), font=font(BLK, 70), fill=RED if (code == "COR" and fall > 0) else WHITE, anchor="rm")
        put(lay, r, W / 2 + (20 if code == "COR" else 0) * math.sin(t * 30) * (1 if tp < t < tp + 0.3 else 0), 520 + i * 160, 1, v)
    if t > tc - 0.1:
        put(lay, chip("ZONA DE REBAIXAMENTO", RED, 34, (255, 255, 255)), W / 2, 1360, 1, fall)
    for j, (text, col, tn) in enumerate([("COR 1 x 1 BOT", GREY, tb), ("COR 0 x 1 GRE · ITAQUERA", RED, tp)]):
        if t < tn: continue
        v = ease((t - tn) / 0.3)
        put(lay, chip(text, col, 32, (255, 255, 255) if col == RED else (12, 12, 14)), W / 2, 1270 - (1 - j) * 0, 1, v * (0 if (j == 0 and t > tp) else 1))
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def verdict(img, t, t0, t_out):
    u = ease((t - t0) / 0.35)
    a = 1 - ease((t - t_out) / 0.3) if t > t_out else 1
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    put(lay, glow(badge("PAL", 300), ACC, 18, 0.6), W / 2 - 240, 700, 1, u)
    put(lay, txt("CAMPEÃO", font(BLK, 70), ACC), W / 2 - 240, 900, 1, u)
    tc = T("corinthians", 1)
    v = ease((t - tc) / 0.35)
    b = badge("COR", 300).convert("LA").convert("RGBA")
    put(lay, b, W / 2 + 240, 700 + 40 * (1 - v), 1, v)
    put(lay, txt("SÉRIE B", font(BLK, 70), RED), W / 2 + 240, 900, 1, v)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def scene_sim(img, t):
    R = [T("rodada", i) - 0.2 for i in range(3)]
    s_last, s_ch, s_z4, s_ver, s_cta = T("na") - 0.2, T("campeão") - 0.3, T("lá") - 0.3, T("palmeiras", 4) - 0.2, T("comenta") - 0.25
    if t < R[0] + 0.4: hook(img, t, R[0], "SIMULEI O FIM DO", "BRASILEIRÃO", "4 ÚLTIMAS RODADAS")
    keys = [
        (R[0], "RODADA 35", {"PAL": 76, "FLA": 79}, ["FLA", "PAL"], [("FLA 2 x 0 CAP", WHITE, 1.4), ("CRU 1 x 2 PAL", ACC, 3.2)]),
        (R[1], "RODADA 36", {"PAL": 79, "FLA": 79}, ["FLA", "PAL"], [("PAL 2 x 1 FLA", ACC, 2.8), ("EMPATADOS EM PONTOS", WHITE, 4.3)]),
        (R[2], "RODADA 37", {"PAL": 82, "FLA": 80}, ["PAL", "FLA"], [("CFC 1 x 1 FLA", WHITE, 2.0), ("CHA 0 x 2 PAL", ACC, 3.5)]),
        (s_last, "RODADA 38", {"PAL": 85, "FLA": 83}, ["PAL", "FLA"], [("PAL 3 x 0 CFC", ACC, 0.5), ("FLA 2 x 0 CHA", WHITE, 0.9)]),
    ]
    if R[0] < t < s_ch + 0.3: race(img, t, R[0], s_ch, keys)
    if s_ch < t < s_z4 + 0.3: champion(img, t, s_ch, s_z4)
    if s_z4 < t < s_ver + 0.3: z4(img, t, s_z4, s_ver)
    if s_ver < t < s_cta + 0.3: verdict(img, t, s_ver, s_cta)
    if t > s_cta: cta(img, t, s_cta)
    return [R[1] + 2.8, s_ch + 0.3, T("cai")]

TAGLINE = {"words_sim": "SIMULAÇÃO · BRASILEIRÃO 2026", "words_sim2": "SIMULAÇÃO · BRASILEIRÃO 2026", "words_hist": "HISTÓRIA · CORINTHIANS 2007"}
def scene_qua3(img, t):
    P = lambda n: T("palpite", n + 1)
    s_cru, s_fla, s_cor, s_gre, s_oth, s_std, s_cta = T("cruzeiro") - 0.3, T("flamengo") - 0.35, T("corinthians") - 0.35, T("grêmio") - 0.35, T("coritiba") - 0.25, T("se") - 0.3, T("comenta") - 0.25
    r1, r2, r3, r4 = TA("2", P(0)) - 0.05, TA("1", P(1)) - 0.05, TA("1", P(2)) - 0.05, TA("1", P(3)) - 0.05
    if t < s_cru + 0.4: hook(img, t, s_cru, "PALPITES COM", "O PORQUÊ", "JOGOS DE QUARTA · 35ª RODADA")
    if s_cru < t < s_fla + 0.4:
        match_card2(img, t, "CRU", "PAL", 1, 2, s_cru, r1, s_fla, "QUA 18/11 · 20H30 · MINEIRÃO",
            [("CRU", "NÃO BRIGA POR MAIS NADA", T("nada"), WHITE), ("CRU", "99,8% DE CHANCE DE LIBERTADORES", T("garantido"), WHITE),
             ("PAL", "PRECISA VENCER · 11 JOGOS SEM PERDER", T("precisa"), ACC), ("PAL", "SEM GÓMEZ E MAURÍCIO (SELEÇÃO)", T("gómez"), RED)])
    if s_fla < t < s_cor + 0.4:
        match_card2(img, t, "FLA", "CAP", 1, 1, s_fla, r2, s_cor, "QUA 18/11 · 20H30 · MARACANÃ",
            [("FLA", "5 VITÓRIAS SEGUIDAS", T("cinco"), WHITE), ("FLA", "8 PENDURADOS · PEGA O PALMEIRAS SÁBADO", T("oito"), RED),
             ("CAP", "5º · BRIGA POR LIBERTADORES", T("briga", 1), ACC)], ("TROPEÇO DO LÍDER", T("tropeço"), ACC))
    if s_cor < t < s_gre + 0.4:
        match_card2(img, t, "COR", "BOT", 1, 1, s_cor, r3, s_gre, "QUA 18/11 · 21H30 · NEO QUÍMICA ARENA",
            [("COR", "SEM YURI ALBERTO E MATHEUS PEREIRA", T("yuri"), RED), ("COR", "SEM ANDRÉ RAMALHO E ANDRÉ", T("ramalho"), RED),
             ("BOT", "PERDEU 10 DE 17 FORA DE CASA", T("10"), RED)], ("RISCO DE QUEDA: +50%", T("risco"), RED))
    if s_gre < t < s_oth + 0.4:
        match_card2(img, t, "GRE", "BAH", 1, 1, s_gre, r4, s_oth, "QUA 18/11 · 21H30 · ARENA DO GRÊMIO",
            [("BAH", "6º · BRIGA POR LIBERTADORES", T("bahia", 1), WHITE), ("GRE", "18º · JOGA A VIDA EM CASA", T("grêmio", 1), RED)])
    if s_oth < t < s_std + 0.4:
        small_rows(img, t, "OUTROS JOGOS DE QUARTA",
                   [("CFC", "SAN", 2, 1, T("coritiba") - 0.1, "COXA FEZ 3 x 0 NO 1º TURNO"), ("REM", "CHA", 2, 1, T("remo") - 0.1, "19º x 20º · 20H")], s_oth, s_std)
    if s_std < t < s_cta + 0.2:
        a = 1 - ease((t - s_cta) / 0.25)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        def ex(l, tt):
            if tt > s_std + 1.4:
                v = ease((tt - s_std - 1.4) / 0.3)
                put(l, chip("DIFERENÇA: 1 PONTO", ACC, 40), W / 2, 960, 1.2 - 0.2 * v, v)
                put(l, txt("PAL x FLA · SÁB 21/11 · 16H30", mono(32), WHITE), W / 2, 1060, 1, v)
        standings(lay, t, s_std, [(1, "FLA", 76, 77, False), (2, "PAL", 73, 76, True)], ex)
        if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)
    if t > s_cta: cta(img, t, s_cta)
    return [r1, r2, r3, r4]

def scene_sim2(img, t):
    R = [T("rodada", i) - 0.2 for i in range(3)]
    s_last, s_ch, s_z4, s_ver, s_cta = T("na") - 0.2, T("campeão") - 0.3, T("lá") - 0.3, T("palmeiras", 4) - 0.2, T("comenta") - 0.25
    if t < R[0] + 0.4: hook(img, t, R[0], "SIMULEI O FIM DO", "BRASILEIRÃO", "4 ÚLTIMAS RODADAS")
    keys = [
        (R[0], "RODADA 35", {"PAL": 76, "FLA": 77}, ["FLA", "PAL"], [("FLA 1 x 1 CAP", WHITE, 2.0), ("CRU 1 x 2 PAL", ACC, 4.4)]),
        (R[1], "RODADA 36", {"PAL": 79, "FLA": 77}, ["PAL", "FLA"], [("PAL 2 x 1 FLA", ACC, 3.0), ("PALMEIRAS NA LIDERANÇA", ACC, 3.9)]),
        (R[2], "RODADA 37", {"PAL": 82, "FLA": 78}, ["PAL", "FLA"], [("CFC 1 x 1 FLA", WHITE, 1.7), ("CHA 0 x 2 PAL", ACC, 4.0)]),
        (s_last, "RODADA 38", {"PAL": 85, "FLA": 81}, ["PAL", "FLA"], [("PAL 3 x 0 CFC", ACC, 0.5), ("FLA 2 x 0 CHA", WHITE, 0.9)]),
    ]
    if R[0] < t < s_ch + 0.3: race(img, t, R[0], s_ch, keys)
    if s_ch < t < s_z4 + 0.3: champion(img, t, s_ch, s_z4)
    if s_z4 < t < s_ver + 0.3: z4(img, t, s_z4, s_ver)
    if s_ver < t < s_cta + 0.3: verdict(img, t, s_ver, s_cta)
    if t > s_cta: cta(img, t, s_cta)
    return [R[1] + 3.0, s_ch + 0.3, T("cai")]

def fade_layer(img, lay, t, t0, t1):
    a = min(ease((t - t0) / 0.35), 1 - ease((t - t1) / 0.3) if t > t1 else 1)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda q: int(q * a)))
    img.alpha_composite(lay)

def gray(code, d):
    b = badge(code, d); g = b.convert("LA").convert("RGBA"); g.putalpha(b.split()[3]); return g

def stamp(lay, text, x, y, t, t0, size=110, rot=-8):
    if t < t0: return
    v = ease((t - t0) / 0.25)
    im = txt(text, font(BLK, size), RED); bx = Image.new("RGBA", (im.width + 60, im.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(bx).rounded_rectangle((4, 4, bx.width - 5, bx.height - 5), 16, outline=RED + (255,), width=8)
    bx.alpha_composite(im, (30, 20)); put(lay, bx, x, y, 1.6 - 0.6 * v, v, rot=rot)

def mcard(lay, t, t0, home, away, sh, sa, info, sub=None, t_score=None, hl=None):
    u = ease((t - t0) / 0.35)
    c = card(980, 470, (18, 21, 24, 245), 34, (255, 255, 255, 30), 2)
    put(lay, c, W / 2, 800, 1, u)
    put(lay, txt(info, mono(28), GREY), W / 2, 610, 1, u)
    for code, x in ((home, W / 2 - 290), (away, W / 2 + 290)):
        put(lay, badge(code, 200), x, 770, 1, u)
        put(lay, txt(TEAMS[code][0], fitf(BLK, TEAMS[code][0], 340, 42), WHITE), x, 905, 1, u)
    ts = t_score if t_score is not None else t0
    if t > ts:
        v = ease((t - ts) / 0.3)
        put(lay, txt(f"{sh} x {sa}", font(BLK, 130), hl or WHITE, shadow=10), W / 2, 770, 1.3 - 0.3 * v, v)
    if sub: put(lay, txt(sub, font(BD, 36), WHITE), W / 2, 1000, 1, u)

def scene_hist(img, t):
    S = {k: T(*k) if isinstance(k, tuple) else T(k) for k in []}
    sA, sB, sC, sD, sE, sF, sG, sH, sCTA = 0, T("e") - 0.2, T("em", 1) - 0.15, T("na", 1) - 0.2, T("na", 2) - 0.1, T("corinthians", 2) - 0.2, T("agora") - 0.2, T("e", 2) - 0.1, T("a", 4) - 0.1
    lay = None
    if t < sB + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u = ease(t / 0.4)
        put(lay, txt("02/12/2007", font(BLK, 150), WHITE, shadow=10), W / 2, 560, 1.1 - 0.1 * u, u)
        tc = T("corinthians")
        if t > tc - 0.2: put(lay, gray("COR", 300), W / 2, 880, 1, ease((t - tc + 0.2) / 0.3))
        stamp(lay, "SÉRIE B", W / 2, 1060, t, T("série"))
        fade_layer(img, lay, t, sA, sB)
    if sB < t < sC + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u = ease((t - sB) / 0.35)
        put(lay, txt("2007 · QUEDA DO CORINTHIANS", mono(34), GREY), W / 2, 470, 1, u)
        put(lay, txt("02/12", font(BLK, 160), (150, 150, 150)), W / 2, 590, 1, u)
        put(lay, txt("2026 · ÚLTIMA RODADA", mono(34), ACC), W / 2, 790, 1, ease((t - T("última") + 0.1) / 0.3))
        t2 = T("2", 1)
        if t > t2 - 0.1:
            v = ease((t - t2 + 0.1) / 0.3)
            put(lay, glow(txt("02/12", font(BLK, 200), ACC, shadow=10), ACC, 16, 0.7), W / 2, 930, 1.3 - 0.3 * v, v)
            put(lay, chip("MESMA DATA", RED, 40, (255, 255, 255)), W / 2, 1110, 1, ease((t - t2 - 0.3) / 0.3))
        fade_layer(img, lay, t, sB, sC)
    if sC < t < sD + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u = ease((t - sC) / 0.35)
        put(lay, txt("BRASILEIRÃO 2007", font(BLK, 80), WHITE, shadow=8), W / 2, 400, 1, u)
        tl = T("liderou")
        if t > tl:
            v = ease((t - tl) / 0.3)
            put(lay, badge("COR", 170), W / 2 - 300, 600, 1, v)
            put(lay, txt("1º NAS 6 PRIMEIRAS", font(BLK, 52), WHITE), W / 2 + 90, 600, 1, v)
        tp = T("palmeiras")
        if t > tp - 0.2:
            v = ease((t - tp + 0.2) / 0.3)
            put(lay, glow(badge("PAL", 170), ACC, 12, 0.6), W / 2 - 300, 820, 1, v)
            put(lay, txt("1ª DERROTA: 8ª RODADA", font(BLK, 48), ACC), W / 2 + 90, 820, 1, v)
        td = T("desabou")
        if t > td - 0.2:
            v = ease((t - td + 0.2) / 0.4)
            put(lay, txt("1º", font(BLK, 120), WHITE), W / 2 - 220, 1080, 1, v)
            d = ImageDraw.Draw(lay); x0, x1 = W / 2 - 120, W / 2 - 120 + 240 * v
            d.line((x0, 1060, x1, 1060 + 50 * v), fill=RED + (255,), width=12)
            if v > 0.9: d.polygon([(x1 + 30, 1060 + 50 * v + 6), (x1 - 12, 1060 + 50 * v - 22), (x1 - 4, 1060 + 50 * v + 30)], fill=RED + (255,))
            put(lay, txt("17º", font(BLK, 120), RED), W / 2 + 250, 1110, 1, ease((t - td) / 0.3))
        fade_layer(img, lay, t, sC, sD)
    if sD < t < sE + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(lay, txt("PENÚLTIMA RODADA", font(BLK, 76), WHITE, shadow=8), W / 2, 420, 1, ease((t - sD) / 0.35))
        mcard(lay, t, sD + 0.2, "COR", "VAS", 0, 1, "28/11/2007 · PACAEMBU", "DERROTA EM CASA", T("1"), RED)
        fade_layer(img, lay, t, sD, sE)
    if sE < t < sF + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(lay, txt("ÚLTIMA RODADA", font(BLK, 76), WHITE, shadow=8), W / 2, 420, 1, ease((t - sE) / 0.35))
        tg, te = T("2", 2), T("empatou")
        sc = (1, 1) if t > te else (1, 0)
        mcard(lay, t, sE + 0.2, "GRE", "COR", sc[0], sc[1], "02/12/2007 · OLÍMPICO", None, tg)
        if t > tg: put(lay, chip("2' JONAS", (0, 140, 210), 34, (255, 255, 255)), W / 2 - 290, 1000, 1, ease((t - tg) / 0.3))
        if t > te: put(lay, chip("CLODOALDO", WHITE, 34), W / 2 + 290, 1000, 1, ease((t - te) / 0.3))
        tgo = T("goiás")
        if t > tgo - 0.1:
            v = ease((t - tgo + 0.1) / 0.3)
            r = card(900, 150, (18, 21, 24, 245), 24, RED + (180,), 3); r.alpha_composite(badge("GOI", 110), (10, 0)); r.alpha_composite(badge("INT", 110), (900 - 150, 0))
            ImageDraw.Draw(r).text((450, 75), "GOIÁS VENCE O INTER", font=font(BLK, 44), fill=WHITE, anchor="mm")
            put(lay, r, W / 2, 1200, 1, v)
        fade_layer(img, lay, t, sE, sF)
    if sF < t < sG + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u = ease((t - sF) / 0.35)
        put(lay, txt("TABELA FINAL · 2007", font(BLK, 70), WHITE, shadow=8), W / 2, 420, 1, u)
        for i, (pos, code, pts, z) in enumerate([(16, "GOI", 45, False), (17, "COR", 44, True)]):
            v = ease((t - sF - 0.2 - i * 0.2) / 0.35)
            r = card(940, 160, (18, 21, 24, 245), 26, (RED + (230,)) if z else (255, 255, 255, 40), 4 if z else 2)
            r.alpha_composite(badge(code, 120), (8, 0)); d = ImageDraw.Draw(r)
            d.text((160, 80), f"{pos}º  {TEAMS[code][0]}", font=font(BLK, 50), fill=WHITE, anchor="lm")
            d.text((905, 80), str(pts), font=font(BLK, 80), fill=RED if z else WHITE, anchor="rm")
            put(lay, r, W / 2, 620 + i * 190, 1, v)
        tu = T("um")
        if t > tu: put(lay, chip("1 PONTO DE DIFERENÇA", ACC, 40), W / 2, 1000, 1, ease((t - tu) / 0.3))
        stamp(lay, "SÉRIE B", W / 2, 1170, t, T("série", 1) - 0.1)
        fade_layer(img, lay, t, sF, sG)
    if sG < t < sH + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); u = ease((t - sG) / 0.35)
        put(lay, txt("O DETALHE", font(BLK, 80), WHITE, shadow=8), W / 2, 380, 1, u)
        put(lay, txt("PONTOS APÓS 32 RODADAS", mono(34), GREY), W / 2, 470, 1, ease((t - T("32")) / 0.3))
        base = 1130
        for k, (yr, pts, tn, col, lab) in enumerate([("2007", 38, T("38"), (150, 150, 150), "CAIU"), ("2026", 33, T("33"), RED, "AGORA")]):
            if t < tn - 0.3: continue
            v = ease((t - tn + 0.3) / 0.5); x = W / 2 - 200 + k * 400; h = pts * 12 * v
            ImageDraw.Draw(lay).rounded_rectangle((x - 110, base - h, x + 110, base), 18, fill=col + (255,))
            put(lay, txt(str(int(round(pts * v))), font(BLK, 110), WHITE, shadow=8), x, base - h - 80, 1, v)
            put(lay, txt(yr, font(BLK, 60), WHITE), x, base + 60, 1, v)
            put(lay, chip(lab, col, 30, (255, 255, 255)), x, base + 135, 1, v)
        tp = T("pior")
        if t > tp: put(lay, chip("PIOR QUE O TIME QUE CAIU", RED, 44, (255, 255, 255)), W / 2, 1400, 1.2 - 0.2 * ease((t - tp) / 0.3), ease((t - tp) / 0.3))
        fade_layer(img, lay, t, sG, sH)
    if sH < t < sCTA + 0.3:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(lay, txt("PENÚLTIMA RODADA · 2026", font(BLK, 64), WHITE, shadow=8), W / 2, 420, 1, ease((t - sH) / 0.35))
        tg = T("grêmio", 2)
        if t > tg - 0.3: mcard(lay, t, tg - 0.3, "COR", "GRE", "?", "?", "29/11/2026 · NEO QUÍMICA ARENA", "DE NOVO ELE", tg, ACC)
        fade_layer(img, lay, t, sH, sCTA)
    if t > sCTA:
        v = ease((t - sCTA) / 0.35)
        put(img, txt("A HISTÓRIA VAI", font(BLK, 92), WHITE, shadow=8), W / 2, 720, 1, v)
        put(img, glow(txt("SE REPETIR?", font(BLK, 130), ACC, shadow=10), ACC, 16, 0.7), W / 2, 860, 1.15 - 0.15 * v, v)
        put(img, txt("COMENTA ↓", font(BLK, 76), WHITE, 4, (0, 0, 0), 6), W / 2, 1050 + 10 * math.sin(t * 7), 1, ease((t - sCTA - 0.4) / 0.3))
    return [T("série") , T("2", 1), T("1"), T("série", 1)]

SCENE = {"words_qua": scene_qua, "words_qui": scene_qui, "words_qua2": scene_qua2, "words_qui2": scene_qui2, "words_sim": scene_sim, "words_qua3": scene_qua3, "words_sim2": scene_sim2, "words_hist": scene_hist}
def frame(Tm):
    img = BG.copy(); dust(img, Tm, (255, 230, 170))
    reveals = SCENE[WMOD.__name__](img, Tm)
    fl = 0
    for tr in reveals:
        if 0 <= Tm - tr < 0.12: fl = 0.22 * (1 - (Tm - tr) / 0.12)
    d = ImageDraw.Draw(img); d.rectangle((60, 196, 76, 212), fill=ACC); d.text((92, 204), TAGLINE.get(WMOD.__name__, "35ª RODADA · ANÁLISE"), font=mono(30), fill=ACC, anchor="lm")
    caption(img, WORDS, Tm, y=1500)
    progress(img, Tm, TOTAL)
    dark = max(1 - Tm / 0.2 if Tm < 0.2 else 0, (Tm - (TOTAL - 0.5)) / 0.5)
    return post(img, int(Tm * FPS), fl, dark)

def render(a, b, name):
    od = f"{HERE}/chunks_{WMOD.__name__}"; os.makedirs(od, exist_ok=True); tmp = f"{od}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: os.replace(tmp, f"{od}/{name}.mp4")
    print("done", name, flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for s in sys.argv[2:]: frame(float(s)).save(f"{HERE}/pv_{float(s):05.1f}.jpg", quality=85)
    else:
        NF = int(round(TOTAL * FPS)); parts = int(sys.argv[2]); i = int(sys.argv[1])
        bd = [NF * j // parts for j in range(parts + 1)]; render(bd[i], bd[i + 1], f"c{i:02d}")
