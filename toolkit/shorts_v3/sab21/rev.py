from com import *
from scripts import RV
from PIL import ImageOps
def sep(im):
    a = im.getchannel("A"); g = ImageOps.colorize(ImageOps.grayscale(im.convert("RGB")), (60, 40, 20), (245, 225, 180)).convert("RGBA"); g.putalpha(a); return g
SP = lambda k, h: sep(logo(k, h))

def s0(img, t, T):  # 58 anos depois, revanche
    img.alpha_composite(rays(W, H, cx, 760, T, (255, 220, 140), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("58 ANOS", 220, AMB, 14), cx, 450, 1, sc, -3)
    paste(img, txt("DEPOIS...", 110, WHITE, 10), cx, 620, 1, sc, -3)
    paste(img, logo("PAL", 250), 300, 900, 1, 1.0 + 0.04 * math.sin(T * 6)); paste(img, logo("EST", 250), 780, 900, 1)
    paste(img, txt("X", 100, AMB), cx, 900, 1)
    if t > 0.8: paste(img, stamp("REVANCHE", 120, RED), cx, 1170, 1, 1 + 0.25 * max(0, 1 - (t - 0.8) / 0.15), -6)

def s1(img, t, T):  # 1968 final
    img.alpha_composite(Image.new("RGBA", (W, H), (90, 60, 25, 90)))
    v = 2026 - int(58 * ease(t / 1.4))
    pop(img, txt(str(v), 230, (245, 225, 180), 14), cx, 520, t, 0.0)
    pop(img, chip("FINAL DA LIBERTADORES", 60, INK, (245, 225, 180)), cx, 760, t, 1.6)
    slide(img, SP("PAL", 260), 300, 1040, t, 2.2, -400); slide(img, SP("EST", 260), 780, 1040, t, 2.4, 400)
    pop(img, txt("X", 100, (245, 225, 180)), cx, 1040, t, 2.6)

def s2(img, t, T):  # ida 2x1, volta 3x1
    img.alpha_composite(Image.new("RGBA", (W, H), (90, 60, 25, 70)))
    pop(img, chip("IDA • ARGENTINA", 56, INK, WHITE), cx, 420, t, 0.0)
    pop(img, scorebox(SP("EST", 140), SP("PAL", 140), 2, 1, 140), cx, 620, t, 0.4, 0.3)
    pop(img, chip("VOLTA • PACAEMBU", 56, INK, AMB), cx, 900, t, 2.0)
    pop(img, scorebox(SP("PAL", 140), SP("EST", 140), 3, 1, 140), cx, 1100, t, 2.4, 0.3)

def s3(img, t, T):  # jogo extra no Centenário, 2x0 Estudiantes
    pitch3d(img, T, 120, 8, hgt=36, dim=70)
    img.alpha_composite(Image.new("RGBA", (W, H), (90, 60, 25, 60)))
    pop(img, chip("JOGO EXTRA • CAMPO NEUTRO", 56, INK, WHITE), cx, 420, t, 0.0)
    pop(img, txt("CENTENÁRIO", 140, (245, 225, 180)), cx, 620, t, 1.2)
    pop(img, chip("MONTEVIDÉU", 56, INK, AMB), cx, 770, t, 1.7)
    pop(img, scorebox(SP("PAL", 140), SP("EST", 140), 0, 2, 140), cx, 1030, t, 3.4, 0.3)
    pop(img, chip("16/05/1968", 50, WHITE, INK), cx, 1220, t, 3.8)

def s4(img, t, T):  # mesmo estádio, mesmo rival
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    pop(img, chip("AGORA OLHA ISSO", 64, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    pop(img, chip("MESMO ESTÁDIO", 74, WHITE, GREEN), 470, 640, t, 1.0); pop(img, check(110, True), 900, 640, t, 1.2)
    pop(img, chip("MESMO RIVAL", 74, WHITE, GREEN), 470, 820, t, 2.2); pop(img, check(110, True), 900, 820, t, 2.4)
    pop(img, logo("EST", 250), cx, 1100, t, 2.4)

def s5(img, t, T):  # tetra x quinto
    for k in range(3): pop(img, trophy(140), 200 + k * 110, 620, t, 0.1 + k * 0.12)
    pop(img, logo("PAL", 170), 310, 860, t, 0.0); pop(img, chip("TETRA?", 66, WHITE, GREEN), 310, 1040, t, 0.5)
    for k in range(4): pop(img, trophy(140), 660 + k * 100, 620, t, 0.9 + k * 0.12)
    pop(img, logo("EST", 170), 810, 860, t, 0.8); pop(img, chip("5º TÍTULO?", 60, WHITE, RED), 810, 1040, t, 1.3)

def s6(img, t, T):  # data + CTA
    img.alpha_composite(rays(W, H, cx, 640, T, (255, 220, 140), 14, 40))
    for k, s in enumerate(["SÁBADO • 28/11", "17H • CENTENÁRIO"]):
        pop(img, chip(s, 60, INK, AMB if k == 0 else WHITE), cx, 420 + k * 140, t, 0.0 + k * 0.5)
    pop(img, txt("VAI TER REVANCHE?", 100, AMB), cx, 840, t, 2.0)
    pop(img, chip("SIM", 90, WHITE, GREEN), 330, 1080, t, 2.8, 0.25, -4)
    pop(img, chip("NÃO", 90, WHITE, RED), 750, 1080, t, 3.0, 0.25, 4)

S = Short("/home/claude/sab21/rev", RV, [s0, s1, s2, s3, s4, s5, s6], "A REVANCHE DE 1968",
          ["dark", "night", "night", "dark", "green", "dark", "blue"], "Five_Armies", 0)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_grave", S.segs[1][0], 0.3), ("torcida_comemora", S.segs[2][0] + 2.4, 0.18),
                   ("torcida_aww", S.segs[3][0] + 3.4, 0.22), ("tambor_impacto", S.segs[4][0] + 1.0, 0.3), ("tambor_impacto", S.segs[4][0] + 2.2, 0.3)])
