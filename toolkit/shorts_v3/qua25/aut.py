from extra import *
from scripts import AUT
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def s0(img, t, T):
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("O MESSI É", 130, WHITE, 12), cx, 400, 1, sc, -3)
    paste(img, txt("AUTISTA?", 170, GOLD, 14), cx, 560, 1, sc, -3)
    paste(img, jersey("10", "MESSI", 420, ARG), cx, 920, 1, sc)
    pop(img, stamp("FAKE NEWS", 130, RED), cx, 920, t, wt(0, "fake") - 0.1, 0.25, -10 + shake(t, wt(0, "fake"), 10))
    pop(img, chip("E NASCEU NO BRASIL", 60, INK, GOLD), cx, 1250, t, wt(0, "nasceu") - 0.2, 0.25, 3)
def s1(img, t, T):
    paste(img, newspaper(W * 0.88, "AGOSTO DE 2013 • BLOG", "\"MESSI TEM ASPERGER\"", "texto de um jornalista brasileiro", False, "INTERNET"), cx, 740, 1, back(t / 0.4), (1 - ease(t / 0.4)) * 250)
    pop(img, stamp("SEM NUNCA EXAMINAR", 74, RED), cx, 1200, t, wt(1, "sem") - 0.2, 0.25, -6)
def s2(img, t, T):
    img.alpha_composite(speedlines(W, H, T))
    pop(img, txt("VIRALIZOU", 150, GOLD), cx, 460, t, 0.0, 0.3, -3)
    if t > 0.3: paste(img, odometer(150000, 6, 110, t - 0.3, 1.2), cx, 760, 1)
    pop(img, chip("COMPARTILHAMENTOS", 56, INK, WHITE), cx, 920, t, 0.6)
    pop(img, chip("ATÉ O ROMÁRIO ESPALHOU NO TWITTER", 50, WHITE, RED), cx, 1100, t, wt(2, "romário") - 0.2, 0.25, -2)
def s3(img, t, T):
    pop(img, chip("O PAI DO MESSI NEGOU", 64, WHITE, RED), cx, 400, t, 0.0); pop(img, chip("E AMEAÇOU PROCESSAR", 56, INK, WHITE), cx, 520, t, wt(3, "ameaçou") - 0.2)
    tq = wt(3, "médico") - 0.2
    if t > tq: paste(img, quote("Leo nunca foi diagnosticado com Asperger ou qualquer outra forma de autismo.", "Diego Schwarzstein, médico do Messi na infância"), cx, 860, 1, 0.8 + 0.2 * back((t - tq) / 0.3))
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (150, 220, 255), 14, 40))
    pop(img, txt("O QUE ELE TEVE", 110, WHITE), cx, 420, t, 0.0)
    pop(img, chip("FALTA DE HORMÔNIO", 70, INK, GOLD), cx, 620, t, wt(4, "falta") - 0.2, 0.25, -3)
    pop(img, chip("DO CRESCIMENTO", 70, INK, GOLD), cx, 740, t, wt(4, "crescimento") - 0.3, 0.25, 3)
    pop(img, chip("QUEM PAGOU O TRATAMENTO:", 52, WHITE, INK), cx, 1000, t, wt(4, "pagou") - 0.2)
    pop(img, txt("BARCELONA", 140, (220, 60, 90)), cx, 1150, t, wt(4, "barcelona") - 0.2, 0.3, -3)
def s5(img, t, T):
    pop(img, chip("SER AUTISTA NÃO DIMINUIRIA NADA", 50, INK, WHITE), cx, 420, t, 0.0)
    pop(img, chip("DIAGNÓSTICO DE LONGE = IRRESPONSÁVEL", 46, WHITE, RED), cx, 540, t, wt(5, "diagnóstico") - 0.2)
    pop(img, txt("VOCÊ ACREDITAVA?", 110, GOLD), cx, 780, t, wt(5, "você") - 0.2)
    pop(img, chip("SIM", 100, INK, GREEN), 330, 1050, t, wt(5, "você") + 0.4, 0.25, -3)
    pop(img, chip("NÃO", 100, WHITE, RED), 750, 1050, t, wt(5, "você") + 0.6, 0.25, 3)
S = Short("/home/claude/qua25/aut", AUT, [s0, s1, s2, s3, s4, s5], "MITO OU VERDADE?", ["night", "dark", "red", "dark", "blue", "night"], "Movement_Proposition", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("whoosh_boom", S.segs[0][0] + wt(0, "fake"), 0.3), ("camera_click", S.segs[1][0] + 0.3, 0.3), ("tambor_impacto", S.segs[1][0] + wt(1, "sem"), 0.3)])
