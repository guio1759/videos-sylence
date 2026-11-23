from extra import *
from scripts import GAY
def s0(img, t, T):
    rainbow(img, 0, H, 70)
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("O PRIMEIRO", 120, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("A ASSUMIR", 120, WHITE, 12), cx, 520, 1, sc, -3)
    paste(img, txt("QUE ERA GAY", 140, GOLD, 14), cx, 670, 1, sc, -3)
    paste(img, jersey("9", "FASHANU", 400, (40, 40, 44)), cx, 1000, 1, sc)
    pop(img, chip("1º JOGADOR NEGRO DE £1 MILHÃO", 50, INK, WHITE), cx, 1290, t, 0.8, 0.25, 2)
def s1(img, t, T):
    pitch3d(img, T, 0, 6, dist=45, hgt=18, tgt=(0, -20, 0), dim=60)
    pop(img, jersey("9", "FASHANU", 400, (250, 205, 0), (20, 110, 50)), cx, 640, t, 0.0)
    pop(img, chip("JUSTIN FASHANU", 74, INK, WHITE), cx, 920, t, 0.4, 0.25, -2)
    pop(img, chip("1980 • GOL DA TEMPORADA", 60, INK, GOLD), cx, 1080, t, wt(1, "mil"), 0.25, 3)
    pop(img, chip("vs LIVERPOOL", 56, WHITE, RED), cx, 1220, t, wt(1, "liverpool") - 0.2, 0.25, -3)
def s2(img, t, T):
    pop(img, jersey("9", "FASHANU", 380, (200, 20, 30)), cx, 620, t, 0.0)
    pop(img, chip("NOTTINGHAM FOREST", 60, WHITE, RED), cx, 880, t, 0.2)
    pop(img, chip("TÉCNICO: BRIAN CLOUGH", 50, INK, WHITE), cx, 1010, t, wt(2, "técnico") - 0.2)
    pop(img, stamp("AFASTADO DOS TREINOS", 74, RED), cx, 1200, t, wt(2, "afastou") - 0.2, 0.25, -6 + shake(t, wt(2, "afastou"), 8))
def s3(img, t, T):
    paste(img, newspaper(W * 0.88, "OUTUBRO DE 1990", "\"ASTRO DE £1 MILHÃO: SOU GAY\"", "a manchete que parou a Inglaterra", False, "1990"), cx, 760, 1, back(t / 0.4), (1 - ease(t / 0.4)) * 250)
    pop(img, stamp("ATÉ O IRMÃO FICOU CONTRA", 64, RED), cx, 1220, t, wt(3, "irmão") - 0.3, 0.25, -5)
def s4(img, t, T):
    rainbow(img, 0, H, 40)
    pop(img, txt("1961 – 1998", 140, WHITE), cx, 520, t, 0.0)
    pop(img, chip("37 ANOS", 70, INK, WHITE), cx, 700, t, wt(4, "trinta") - 0.2)
    pop(img, candle(360, T), cx, 960, t, 0.3)
    pop(img, chip("HALL DA FAMA • 2020", 70, INK, GOLD), cx, 1250, t, wt(4, "hall") - 0.3, 0.25, -3)
def s5(img, t, T):
    rainbow(img, 0, H, 60)
    pop(img, txt("O FUTEBOL DE HOJE", 100, WHITE), cx, 470, t, 0.0)
    pop(img, txt("RESPEITA MAIS?", 130, GOLD), cx, 620, t, 0.3)
    pop(img, chip("SIM", 100, INK, GREEN), 330, 1000, t, 1.0, 0.25, -3)
    pop(img, chip("NÃO", 100, WHITE, RED), 750, 1000, t, 1.2, 0.25, 3)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
S = Short("/home/claude/qua25/gay", GAY, [s0, s1, s2, s3, s4, s5], "HISTÓRIA REAL", ["night", "dark", "red", "dark", "night", "dark"], "Heartbreaking", 0, sfx_soft=True)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.35), ("torcida_comemora", S.segs[1][0] + 2.0, 0.12), ("tambor_impacto", S.segs[2][0] + wt(2, "afastou"), 0.3), ("camera_click", S.segs[3][0] + 0.3, 0.3)])
