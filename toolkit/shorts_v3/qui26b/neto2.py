from fx2 import *
from scripts import NETO
SANT = (245, 245, 245)
def dur(i): return S.segs[i][1] - S.segs[i][0] + 0.1
def s0(img, t, T):
    img.alpha_composite(blurbg("neymar", t, dur(0), (40, 10, 80, 150), 16))
    img.alpha_composite(rays(W, H, cx, 1000, T, (255, 220, 140), 14, 40))
    sc = 1.0 + 0.04 * math.sin(min(t, 0.4) * 8)
    paste(img, big("O NETO PEDIU", 130, WHITE), cx, 330, 1, sc, -3)
    paste(img, big("DESCULPAS", 190, AMB), cx, 500, 1, sc, 2)
    u = ease(t / 0.35)
    paste(img, FX.polaroid(P["neto1"], 470, 6), 300 - (1 - u) * 500, 980, 1, 1.0)
    paste(img, FX.polaroid(P["neymar"], 360, -6), 790 + (1 - u) * 500, 1000, 1, 1.0)
    pop(img, chip("PRO NEYMAR", 80, INK, WHITE), cx, 1420, t, wt(0, "neymar") - 0.2, 0.25, -3)
    emo(img, "olhos", cx, 760, t, wt(0, "desculpas") - 0.2, 170)
    FX.credit(img, CRJ["neto1"], y=H - 190); FX.credit(img, CRJ["neymar"], y=H - 150)
def s1(img, t, T):
    img.alpha_composite(FX.pop3d(P["neymar"], t, dur(1), (0.5, 0.3), h=1250, y=1260, delay=0.05, dim=130))
    pop(img, chip("QUARTA • 25/11", 56, INK, WHITE), cx, 300, t, 0.0)
    pop(img, big("NEYMAR RECEBEU", 120, WHITE), cx, 430, t, 0.1, 0.3, -2)
    pop(img, logo("SAN", 140), 160, 560, t, 0.3)
    pop(img, chip("INSTITUTO NEYMAR JR.", 58, INK, AMB), cx + 60, 580, t, wt(1, "instituto") - 0.2, 0.25, -2)
    pop(img, chip("PRAIA GRANDE (SP)", 54, WHITE, INK), cx + 60, 690, t, wt(1, "praia") - 0.2, 0.25, 2)
    cr(img, "neymar")
def s2(img, t, T):
    img.alpha_composite(FX.pop3d(P["neto1"], t, dur(2), (0.5, 0.35), h=900, y=1420, delay=0.05, dim=120))
    pop(img, chip("OS DONOS DA BOLA • BAND", 58, INK, (255, 205, 0)), cx, 300, t, 0.0, 0.25, -2)
    pop(img, big("CRAQUE NETO", 130, WHITE), cx, 430, t, 0.1)
    pop(img, stamp("DESCULPA!", 110, RED), cx, 600, t, wt(2, "desculpas") - 0.15, 0.25, -6)
    tf = wt(2, "filho") - 0.25
    pop(img, chip("FILHO DO NETO • 9 ANOS", 54, WHITE, BLUE), cx, 750, t, tf, 0.25, 2)
    emo(img, "chorando", 880, 900, t, wt(2, "emocionou") - 0.3, 210)
    cr(img, "neto1")
def s3(img, t, T):
    img.alpha_composite(blurbg("neymar", t, dur(3), (0, 0, 0, 150), 14, (1.3, 1.4), (0.5, 0.4), (0.5, 0.3)))
    items = [("camisa", jersey("10", "SANTOS", 260, SANT, INK), 260, 560), ("chuteira", chip("CHUTEIRA", 60, INK, AMB), 760, 480), ("bola", chip("BOLA", 60, INK, AMB), 760, 620)]
    for w, el, x, y in items: pop(img, el, x, y, t, wt(3, w) - 0.2, 0.25, (-4 if x < 500 else 4))
    pop(img, chip("AUTOGRAFADAS", 54, WHITE, INK), 760, 740, t, wt(3, "autografadas") - 0.2)
    th = wt(3, "helicóptero") - 0.35
    if t > th:
        u = t - th; x = -300 + (W / 2 + 300) * ease(u / 0.8)
        paste(img, heli(560, T), x, 1060 + 15 * math.sin(T * 5), 1, 1.0, -4)
        pop(img, stamp("EMPRESTOU O HELICÓPTERO", 66, RED), cx, 1330, u, 0.4, 0.25, -4)
    cr(img, "neymar")
def s4(img, t, T):
    img.alpha_composite(blurbg("neto2", t, dur(4), (10, 60, 30, 150), 12))
    pc = FX.polaroid(P["neto2"], 620, -4 + 2 * math.sin(t)); u = ease(t / 0.4)
    paste(img, pc, cx + (1 - u) * 700, 760, 1)
    pop(img, quote("A paz aqui já foi selada.", "Sandra, esposa do Neto"), cx, 1280, t, 0.3)
    emo(img, "coracao_verde", 900, 1060, t, 0.6, 170)
    cr(img, "neto2", y=H - 120)
def s5(img, t, T):
    img.alpha_composite(blurbg("neto1", t, dur(5), (40, 10, 80, 160), 18))
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 35))
    for k, (p, nm) in enumerate((("neto1", "NETO"), ("neymar", "NEYMAR"))):
        tt = 0.1 + k * 0.15
        if t > tt:
            st = FX.sticker(P[p], 520, 8); paste(img, st, 300 + k * 480, 640, 1, back(min(1, (t - tt) / 0.3)) * 0.95, (-5, 5)[k])
    pop(img, big("FOI SINCERO?", 150, AMB), cx, 1000, t, wt(5, "sincero") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1180, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1180, t, wt(5, "não") - 0.2, 0.25, 4)
    FX.credit(img, CRJ["neto1"], y=H - 230); FX.credit(img, CRJ["neymar"], y=H - 190); FX.credit(img, EM.CREDIT, y=H - 150)
S = Short("/home/claude/x26/neto", NETO, [s0, s1, s2, s3, s4, s5], "NETO x NEYMAR", "dark", "Take_a_Chance", 10)
wt = mkwt(S)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "desculpas"), 0.3), ("tambor_impacto", S.segs[2][0] + wt(2, "desculpas"), 0.3),
                   ("torcida_aww", S.segs[2][0] + wt(2, "emocionou"), 0.12), ("whoosh_3", S.segs[3][0] + wt(3, "helicóptero"), 0.25), ("torcida_comemora", S.segs[4][0] + 0.3, 0.1)])
