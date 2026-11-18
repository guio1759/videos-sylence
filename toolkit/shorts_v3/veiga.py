import sys; sys.path.insert(0, "/home/claude/qui")
from engine import *
from scripts import V

cx = W / 2


def locker(w):
    w = int(w); h = int(w * 1.6); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 16, fill=(40, 110, 70), outline=INK, width=8)
    for k in range(4): d.line((w * 0.2, 40 + k * 22, w * 0.8, 40 + k * 22), fill=(20, 60, 40), width=8)
    d.rounded_rectangle((w * 0.78, h * 0.45, w * 0.88, h * 0.58), 6, fill=(200, 200, 200))
    d.text((w / 2, h * 0.3), "23", font=font("blk", w * 0.32), fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=INK)
    return im


def v0(img, t, T):
    paste(img, jersey(23, "VEIGA", 520), cx, 640, 1, 0.92 + 0.08 * back(t / 0.3))
    paste(img, txt("VAI VOLTAR!", 150, AMB, 12), cx, 1080, 1, 0.9 + 0.1 * back(t / 0.25), -3)


def v1(img, t, T):
    pop(img, chip("AMÉRICA-MEX", 70, WHITE, BLUE), cx, 420, t, 0.0)
    pop(img, txt("US$ 6,5 MI", 150), cx, 620, t, 0.4)
    pop(img, stamp("NÃO VAI PAGAR", 90, RED), cx, 800, t, 1.3, 0.3, -6)
    pop(img, txt("VOLTA PRA CASA", 90, WHITE), cx, 1010, t, 3.0)
    pop(img, txt("2027", 220, AMB, 12), cx, 1220, t, 3.6, 0.35, -3)


def v2(img, t, T):
    lines(img, ["VOCÊ CONHECE", "A HISTÓRIA", "DELE?"], 600, t, 0.0, 120, WHITE, cols=[WHITE, WHITE, AMB])


def v3(img, t, T):
    paste(img, logo("PAL", 200), cx, 400, ease(t / 0.4))
    for k, (lab, hh, x, t0) in enumerate((("AVÔ", 430, 260, 0.2), ("PAI", 400, 560, 1.9), ("NETO", 260, 830, 3.3))):
        if t < t0: continue
        fade(img, person(hh, (230, 230, 230) if k < 2 else (255, 205, 80)), x, 1180 - hh / 2, t, t0, 0.4)
        fade(img, chip(lab, 54, INK, AMB if k == 2 else WHITE), x, 1250, t, t0 + 0.1, 0.3)


def v4(img, t, T):
    p = panel(860, 360, (5, 20, 15, 235)); paste(img, p, cx, 620, 1)
    paste(img, heartbeat(800, 240, t), cx, 620, 1)
    paste(img, chip("UTI", 54, WHITE, RED), 260, 470, 1)
    fade(img, txt("ELE SE DESPEDIU…", 76), cx, 950, t, 1.4)
    fade(img, txt("E O AVÔ CHAMOU DE VOLTA", 64, AMB), cx, 1080, t, 3.6)


def v5(img, t, T):
    lines(img, ["“SE TIVER", "OPORTUNIDADE,", "JOGUE NO", "PALMEIRAS.”"], 470, t, 0.0, 112, WHITE, 1.12, 0.35, [WHITE, WHITE, WHITE, AMB])
    fade(img, txt("— O AVÔ", 60, (200, 200, 200)), cx, 1050, t, 1.8)


def v6(img, t, T):
    a = max(0.0, 1 - t / 1.8)
    paste(img, person(500, (200, 200, 200)), cx, 680, 0.25 + 0.6 * a)
    fade(img, txt("FOI A ÚLTIMA VEZ", 100), cx, 1080, t, 0.2)


def v7(img, t, T):
    pop(img, jersey(23, "VEIGA", 460), cx, 640, t, 0.0)
    pop(img, stamp("PROMESSA CUMPRIDA", 76, AMB), cx, 980, t, 0.9, 0.3, -6)
    pop(img, chip("2017", 64, INK, WHITE), cx, 1150, t, 0.3)


def v8(img, t, T):
    if t > 0.1: paste(img, odometer(378, 3, 150, t - 0.1, 0.8, 0), 300, 560)
    pop(img, txt("JOGOS", 60), 300, 750, t, 0.2)
    if t > 1.1: paste(img, odometer(109, 3, 150, t - 1.1, 0.8, 0), 780, 560)
    pop(img, txt("GOLS", 60), 780, 750, t, 1.2)
    pop(img, chip("MAIOR ARTILHEIRO DO PALMEIRAS", 52, INK, AMB), cx, 950, t, 2.4)
    pop(img, txt("NESTE SÉCULO", 90), cx, 1100, t, 2.7)


def v9(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, alpha=50))
    pop(img, trophy(360), 330, 680, t, 0.0); pop(img, trophy(360), 750, 680, t, 0.25)
    pop(img, txt("2 LIBERTADORES", 100, AMB), cx, 980, t, 0.4)
    pop(img, chip("GOL NA FINAL DE 2021", 64, INK, WHITE), cx, 1150, t, 1.4)


def v10(img, t, T):
    pop(img, locker(340), 330, 790, t, 0.0)
    if t > 0.8:
        u = ease((t - 0.8) / 0.6); paste(img, envelope(260), 330 + 400 * u, 790, 1, 1, -8 * u)
    fade(img, txt("UMA CARTA NO ARMÁRIO", 80), cx, 400, t, 0.5)
    fade(img, txt("SÓ ABRE QUANDO", 64, AMB), cx, 1150, t, 2.0)
    fade(img, txt("VOLTAR", 100, AMB), cx, 1260, t, 2.3)


def v11(img, t, T):
    paste(img, envelope(440, min(1, t / 1.2)), cx, 640, 1)
    pop(img, txt("O QUE ESTÁ ESCRITO?", 84, AMB), cx, 980, t, 0.2)
    pop(img, chip("COMENTA AÍ", 66, INK, WHITE), cx, 1150, t, 0.6)


S = Short("/home/claude/qui/veiga", V, [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11], "O CAMISA 23 VOLTA",
          ["green", "blue", "purple", "sepia", "night", "dark", "dark", "green", "dark", "green", "night", "green"], "Dreamer", 0, sfx_soft=True)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.4), ("tambor_impacto", S.segs[7][0] + 0.9, 0.3), ("torcida_comemora", S.segs[9][0], 0.1)])
