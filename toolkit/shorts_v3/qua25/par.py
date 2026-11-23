from extra import *
from scripts import PAR
def wt(i, w, n=1):
    c_ = 0
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)):
            c_ += 1
            if c_ == n: return c["t0"] - S.segs[i][0]
    return 0.5
def penalty2d(img, t, y0=620, kcol=WHITE, gcol=(40, 40, 44), name="PELÉ", gk="ANDRADA", stop=(0.9, 1.9), hop=False):
    d = ImageDraw.Draw(img); X0, X1 = 140, 940
    d.rectangle((X0 - 60, y0, X1 + 60, y0 + 820), fill=(36, 128, 62))
    for k in range(6): d.rectangle((X0 - 60, y0 + k * 140, X1 + 60, y0 + k * 140 + 70), fill=(40, 138, 68))
    L_ = (235, 245, 235); d.line((X0 - 60, y0 + 40, X1 + 60, y0 + 40), fill=L_, width=5)
    d.rectangle((cx - 300, y0 + 40, cx + 300, y0 + 330), outline=L_, width=5)
    d.rectangle((cx - 170, y0 - 10, cx + 170, y0 + 40), outline=WHITE, width=10)
    spot = (cx, y0 + 260); d.ellipse((spot[0] - 8, spot[1] - 8, spot[0] + 8, spot[1] + 8), fill=WHITE)
    a, b = stop; tk = b + 0.35
    if t < a: u = t / a; kx, ky = cx - 140 + 110 * u, y0 + 560 - 230 * u
    elif t < b: kx, ky = cx - 30, y0 + 330 - (18 * abs(math.sin((t - a) * 9)) if hop else 0)
    else: u = min(1, (t - b) / 0.35); kx, ky = cx - 30 + 20 * u, y0 + 330 - 50 * u
    gd = min(1, max(0, (t - (a + 0.3)) / 0.4)); gx = cx - 150 * gd
    d.ellipse((gx - 30, y0 + 30 - 30, gx + 30, y0 + 30 + 30), fill=(250, 210, 40), outline=INK, width=4)
    paste(img, chip(gk, 30, INK, (250, 210, 40)), gx, y0 + 100, 1)
    d.ellipse((kx - 32, ky - 32, kx + 32, ky + 32), fill=kcol, outline=INK, width=5)
    paste(img, chip(name, 32, INK, WHITE), kx, ky + 62, 1)
    if t < tk: bx, by = spot
    else: u = min(1, (t - tk) / 0.4); bx, by = spot[0] + 120 * u, spot[1] - 240 * u
    d.ellipse((bx - 14, by - 14, bx + 14, by + 14), fill=WHITE, outline=INK, width=3)
    if a + 0.1 < t < b: paste(img, chip("PULINHO!" if hop else "PARADINHA!", 50, INK, GOLD), cx + 260, y0 + 420, 1, 1 + 0.05 * math.sin(t * 12), -6)
    return t > tk + 0.4
def s0(img, t, T):
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("PELÉ INVENTOU", 120, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("A FIFA PROIBIU", 120, GOLD, 12), cx, 520, 1, sc, -3)
    paste(img, jersey("10", "PELÉ", 380, WHITE, INK), 320, 900, 1, sc)
    paste(img, txt("→", 140, WHITE), cx, 900, 1)
    pop(img, stamp("PROIBIDO", 90, RED), 780, 900, t, wt(0, "proibiu") - 0.2, 0.25, -8 + shake(t, wt(0, "proibiu"), 8))
    pop(img, chip("1969 → 2010", 70, INK, WHITE), cx, 1230, t, 0.8, 0.25, 3)
def s1(img, t, T):
    paste(img, scorebox("SAN", "VAS", 1, 1, 100), cx, 380, 1)
    pop(img, chip("19/11/1969 • MARACANÃ", 50, INK, WHITE), cx, 520, t, 0.0)
    tp = wt(1, "pênalti") - 0.2
    if t > tp:
        done = penalty2d(img, t - tp, 620, WHITE, (40, 40, 44), "PELÉ", "ANDRADA", (0.9, 2.0))
        if done: pop(img, txt("GOL Nº 1000!", 110, GOLD), cx, 1350, t, tp + 2.8, 0.3, -4)
def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (120, 220, 140), 14, 50))
    pop(img, txt("O TRUQUE", 120, WHITE), cx, 520, t, 0.0); pop(img, txt("VIROU MARCA", 120, GOLD), cx, 660, t, 0.3)
    pop(img, chip("DO FUTEBOL BRASILEIRO", 64, WHITE, GREEN), cx, 820, t, 0.7, 0.25, -3)
def s3(img, t, T):
    pop(img, chip("A REGRA JÁ MUDOU ANTES", 60, INK, WHITE), cx, 400, t, 0.0)
    for k, (wd, yr, lab, col) in enumerate([("oitenta", "1982", "PARAR = PUNIÇÃO", RED), ("três", "1985", "LIBERADO DE NOVO", GREEN)]):
        t0 = wt(3, wd) - 0.3
        if t > t0:
            y = 700 + k * 360; paste(img, txt(yr, 150, WHITE), cx, y, 1, 0.6 + 0.4 * back((t - t0) / 0.3))
            paste(img, chip(lab, 60, WHITE, col), cx, y + 140, 1, back((t - t0 - 0.2) / 0.3) if t > t0 + 0.2 else 0)
def s4(img, t, T):
    paste(img, scorebox("SAN", "SAO", 0, 0, 100), cx, 380, 1)
    pop(img, chip("FEV/2010 • PAULISTÃO", 50, INK, WHITE), cx, 520, t, 0.0)
    tp = wt(4, "deu") - 0.2
    if t > tp:
        done = penalty2d(img, (t - tp) * 0.9, 620, WHITE, (40, 40, 44), "NEYMAR, 18", "CENI", (0.8, 2.8))
        if t - tp > 1.4: pop(img, chip("O CENI NO CHÃO", 56, WHITE, RED), cx, 1500, t, tp + 1.4, 0.25, -4)
def s5(img, t, T):
    paste(img, quote("Isso não é paradinha, é paradão!", "Rogério Ceni, 2010"), cx, 600, 1, 0.8 + 0.2 * back(t / 0.3))
    pop(img, jersey("01", "CENI", 330, (240, 200, 40), INK), cx, 1000, t, 0.4)
    pop(img, stamp("ELE TAMBÉM JÁ FEZ", 76, RED), cx, 1280, t, wt(5, "só") - 0.2, 0.25, -6)
def s6(img, t, T):
    p = panel(920, 520, (245, 242, 232, 255), 18, (0, 0, 0, 0)); dd = ImageDraw.Draw(p)
    dd.text((40, 40), "REGRA 14 • MAIO DE 2010", font=font("blk", 50), fill=INK)
    dd.text((40, 150), "Parar depois de terminar", font=font("bd", 46), fill=INK); dd.text((40, 215), "a corrida = infração", font=font("bd", 46), fill=INK)
    dd.rounded_rectangle((40, 320, 190, 480), 16, fill=(250, 210, 40), outline=INK, width=5); dd.text((230, 400), "CARTÃO AMARELO", font=font("blk", 54), fill=INK, anchor="lm")
    paste(img, p, cx, 820, 1, back(t / 0.35), -2)
    pop(img, stamp("PROIBIDA", 110, RED), cx, 1250, t, wt(6, "amarelo") - 0.2, 0.25, -8)
def s7(img, t, T):
    pop(img, chip("HOJE: O GOL NÃO VALE", 60, WHITE, RED), cx, 400, t, 0.0)
    tj = wt(7, "jorginho") - 0.2
    if t > tj: penalty2d(img, (t - tj) * 0.8, 560, (40, 90, 200), (40, 40, 44), "JORGINHO", "GOLEIRO", (0.6, 1.5), hop=True)
    pop(img, chip("PULINHO NA CORRIDA = PODE", 52, INK, GREEN), cx, 1460, t, wt(7, "pode") - 0.2, 0.25, 3)
def s8(img, t, T):
    pop(img, txt("A PARADINHA", 120, WHITE), cx, 460, t, 0.0); pop(img, txt("DEVIA VOLTAR?", 120, GOLD), cx, 600, t, 0.3)
    pop(img, chip("SIM", 100, INK, GREEN), 330, 950, t, 0.9, 0.25, -3); pop(img, chip("NÃO", 100, WHITE, RED), 750, 950, t, 1.1, 0.25, 3)
S = Short("/home/claude/qua25/par", PAR, [s0, s1, s2, s3, s4, s5, s6, s7, s8], "A HISTÓRIA DA PARADINHA",
          ["night", "dark", "green", "dark", "dark", "night", "dark", "dark", "night"], "Killers", 0)
if __name__ == "__main__":
    g = S.segs
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("whoosh_boom", wt(0, "proibiu"), 0.3), ("apito_curto", g[1][0] + wt(1, "pênalti"), 0.3),
                   ("chute_bola_1", g[1][0] + wt(1, "pênalti") + 2.3, 0.35), ("torcida_reacao_gol", g[1][0] + wt(1, "pênalti") + 2.7, 0.3),
                   ("chute_bola_1", g[4][0] + wt(4, "deu") + 3.3, 0.35), ("tambor_impacto", g[6][0] + wt(6, "amarelo"), 0.35)])
