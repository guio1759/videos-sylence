from common2 import *
from scripts import NETO
SANT = (245, 245, 245)
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 880, T, (255, 220, 140), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("O NETO PEDIU", 120, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("DESCULPAS", 150, AMB, 14), cx, 520, 1, sc, 2)
    paste(img, mic(360), 300 + shake(t, 0.1, 10), 900, 1, 0.85 + 0.15 * back(t / 0.25), -8)
    paste(img, jersey("10", "NEYMAR", 340, SANT, INK), 780, 900, 1, 0.85 + 0.15 * back(t / 0.25), 6)
    pop(img, chip("PRO NEYMAR", 80, INK, WHITE), cx, 1180, t, wt(0, "neymar") - 0.2, 0.25, -3)
    emo(img, "olhos", cx, 1360, t, wt(0, "desculpas") - 0.2, 200)
def s1(img, t, T):
    pitch3d(img, T, 0, 6, dist=44, hgt=18, dim=80)
    pop(img, chip("QUARTA • 25/11", 60, INK, WHITE), cx, 400, t, 0.0)
    pop(img, logo("SAN", 230), cx, 640, t, 0.2)
    pop(img, chip("INSTITUTO NEYMAR JR.", 66, INK, AMB), cx, 880, t, wt(1, "instituto") - 0.2, 0.25, -2)
    pop(img, chip("PRAIA GRANDE (SP)", 60, WHITE, INK), cx, 1000, t, wt(1, "praia") - 0.2, 0.25, 2)
    pop(img, chip("+ A FAMÍLIA DO NETO", 56, INK, WHITE), cx, 1120, t, wt(1, "família") - 0.2)
def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (180, 210, 255), 14, 35))
    pop(img, chip("OS DONOS DA BOLA", 70, INK, (255, 205, 0)), cx, 400, t, 0.0, 0.25, -2)
    pop(img, mic(300), 280, 700, t, 0.1, 0.25, -8)
    pop(img, stamp("DESCULPA!", 110, RED), 680, 680, t, wt(2, "desculpas") - 0.15, 0.25, -6)
    tf = wt(2, "filho") - 0.25
    pop(img, chip("FILHO DO NETO • 9 ANOS", 60, WHITE, BLUE), cx, 1000, t, tf, 0.25, 2)
    emo(img, "chorando", cx, 1230, t, wt(2, "emocionou") - 0.3, 260)
def s3(img, t, T):
    pitch3d(img, T, 60, 6, dist=40, hgt=16, dim=90)
    items = [("camisa", jersey("10", "SANTOS", 260, SANT, INK), 260, 640), ("chuteira", chip("CHUTEIRA", 60, INK, AMB), 760, 560), ("bola", chip("BOLA", 60, INK, AMB), 760, 700)]
    for w, el, x, y in items: pop(img, el, x, y, t, wt(3, w) - 0.2, 0.25, (-4 if x < 500 else 4))
    pop(img, chip("AUTOGRAFADAS", 54, WHITE, INK), 760, 820, t, wt(3, "autografadas") - 0.2)
    th = wt(3, "helicóptero") - 0.35
    if t > th:
        u = t - th; x = -300 + 1400 * ease(u / 1.6) if u < 1.6 else 1100 - 0 * u
        x = W / 2 + (x - W / 2) * 0 if u > 0.8 else -300 + (W / 2 + 300) * ease(u / 0.8)
        paste(img, heli(520, T), x, 1060 + 15 * math.sin(T * 5), 1, 1.0, -4)
        pop(img, stamp("EMPRESTOU O HELICÓPTERO", 66, RED), cx, 1320, u, 0.4, 0.25, -4)
def s4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (150, 255, 170), 14, 35))
    pop(img, quote("A paz aqui já foi selada.", "Sandra, esposa do Neto, nas redes"), cx, 720, t, 0.0)
    emo(img, "coracao_verde", cx, 1080, t, 0.5, 220)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 40))
    pop(img, mic(260), 340, 560, t, 0.0, 0.25, -8)
    pop(img, jersey("10", "NEYMAR", 260, SANT, INK), 740, 560, t, 0.1, 0.25, 6)
    pop(img, txt("FOI SINCERO?", 120, WHITE), cx, 880, t, wt(5, "sincero") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1100, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1100, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1290, t, wt(5, "comenta") - 0.1)
S = Short("/home/claude/x26/neto", NETO, [s0, s1, s2, s3, s4, s5], "NETO x NEYMAR", ["purple", "dark", "blue", "night", "green", "purple"], "Take_a_Chance", 10)
wt = mkwt(S)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "desculpas"), 0.3), ("tambor_impacto", S.segs[2][0] + wt(2, "desculpas"), 0.3),
                   ("torcida_aww", S.segs[2][0] + wt(2, "emocionou"), 0.12), ("whoosh_3", S.segs[3][0] + wt(3, "helicóptero"), 0.25), ("torcida_comemora", S.segs[4][0] + 0.3, 0.1)])
