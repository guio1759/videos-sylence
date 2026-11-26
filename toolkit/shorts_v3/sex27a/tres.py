from extra import *
from scripts import TRES
EST = lambda h: logo("EST", h)
ESTC = (200, 20, 30)
def wt(i, w):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return 0.5
def minipitch(w, t, t0=0.0, names=("MURILO", "GÓMEZ", "BARBOZA")):
    w = int(w); h = int(w * 0.8); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 26, fill=(30, 120, 60, 240), outline=WHITE, width=6)
    for k in range(6): d.rectangle((0, k * h / 6, w, (k + 0.5) * h / 6), fill=(36, 132, 66, 240))
    d.rounded_rectangle((0, 0, w, h), 26, outline=WHITE, width=6)
    d.line((0, h * 0.12, w, h * 0.12), fill=WHITE, width=4); d.ellipse((w/2 - w*0.13, h*0.12 - w*0.13, w/2 + w*0.13, h*0.12 + w*0.13), outline=WHITE, width=4)
    d.rectangle((w * 0.25, h * 0.8, w * 0.75, h - 3), outline=WHITE, width=4)
    for k, nm in enumerate(names):
        u = ease((t - t0 - k * 0.2) / 0.3)
        if u <= 0: continue
        x = w * (0.22 + 0.28 * k); y = h * 0.52; r = w * 0.075 * (0.6 + 0.4 * back(u))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255), outline=INK, width=6)
        d.text((x, y), "Z", font=font("blk", int(r * 1.1)), fill=(20, 120, 60), anchor="mm")
        d.text((x, y + r + 34), nm, font=font("blk", int(w * 0.05)), fill=WHITE, anchor="mm", stroke_width=5, stroke_fill=INK)
    return im
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 900, T, (150, 255, 170), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("3 ZAGUEIROS", 150, WHITE, 14), cx, 390, 1, sc, -3)
    paste(img, txt("NA FINAL!", 130, AMB, 12), cx, 540, 1, sc, 2)
    paste(img, minipitch(820, t + 0.6, 0.0), cx + shake(t, 0.1, 12), 960, 1, 0.85 + 0.15 * back(t / 0.25))
    pop(img, stamp("A ARMA DO ABEL", 86, GREEN), cx, 1330, t, wt(0, "arma") - 0.15, 0.25, -6 + shake(t, wt(0, "arma"), 8))
def s1(img, t, T):
    pitch3d(img, T, 0, 7, dist=44, hgt=18, tgt=(0, 0, 0), dim=60)
    pop(img, logo("PAL", 170), cx, 420, t, 0.0)
    for k, (nm, w) in enumerate((("GÓMEZ", "gustavo"), ("BARBOZA", "barboza"))):
        x = 320 + 440 * k; t0 = wt(1, w) - 0.25
        pop(img, jersey("", nm, 330, (20, 120, 60)), x, 760, t, t0, 0.25, (-4, 4)[k])
        pop(img, check(120, True), x + 120, 620, t, t0 + 0.2)
    pop(img, stamp("CONFIRMADOS", 100, GREEN), cx, 1080, t, wt(1, "confirmados") - 0.15, 0.25, -5)
def s2(img, t, T):
    pitch3d(img, T, 40, 7, dist=40, hgt=16, tgt=(0, 0, 0), dim=70)
    pop(img, chip("O 3º ZAGUEIRO", 70, INK, WHITE), cx, 400, t, 0.0)
    tb = wt(2, "bruno") - 0.3
    k = min(1.0, max(0.0, (t - tb) / 0.35))
    pop(img, jersey("", "MURILO", 330, (20, 120, 60)), cx - 230 * k, 720, t, wt(2, "murilo") - 0.25, 0.25, -3)
    pop(img, chip("100%?", 80, INK, AMB), cx - 230 * k + 140, 560, t, wt(2, "cem") - 0.2, 0.25, 6)
    if t > tb:
        d = ImageDraw.Draw(img); d.line((cx - 40, 760, cx + 80, 760), fill=WHITE, width=12); d.polygon([(cx + 80, 735), (cx + 120, 760), (cx + 80, 785)], fill=WHITE)
        pop(img, jersey("", "BRUNO FUCHS", 330, (20, 120, 60)), cx + 250, 720, t, tb, 0.25, 4)
        pop(img, chip("PLANO B", 64, WHITE, GREEN), cx + 250, 1000, t, tb + 0.3)
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 150, 150), 14, 35))
    pop(img, stamp("PROBLEMA", 110, RED), cx, 400, t, wt(3, "problema") - 0.15, 0.25, -5)
    for k, (nm, w, inj) in enumerate((("PIQUEREZ", "piquerez", "COXA"), ("PAULINHO", "paulinho", "PANTURRILHA"))):
        x = 300 + 480 * k; t0 = wt(3, w) - 0.25 if k else wt(3, "piq") - 0.25
        if t0 < 0.3: t0 = 0.6 + k * 1.6
        pop(img, jersey("", nm, 330, (20, 120, 60)), x, 760, t, t0, 0.25, (-4, 4)[k])
        pop(img, check(120, False), x + 120, 610, t, t0 + 0.2)
        pop(img, chip(inj, 56, WHITE, RED), x, 1010, t, t0 + 0.35, 0.25, (3, -3)[k])
def s4(img, t, T):
    pop(img, EST(260), cx, 470, t, 0.0)
    pop(img, chip("TAMBÉM DESFALCADO", 66, INK, AMB), cx, 680, t, wt(4, "desfalcado") - 0.2, 0.25, -3)
    tb = wt(4, "baltasar") - 0.25; tg = wt(4, "gabriel") - 0.25
    pop(img, jersey("", "B. RODRÍGUEZ", 300, ESTC), 300, 960, t, tb, 0.25, -4)
    pop(img, redcard(150), 430, 850, t, tb + 0.25, 0.25, 12)
    pop(img, chip("SUSPENSO", 56, WHITE, RED), 300, 1190, t, wt(4, "suspenso") - 0.2)
    pop(img, jersey("", "G. NEVES", 300, ESTC), 780, 960, t, tg, 0.25, 4)
    pop(img, check(120, False), 900, 850, t, tg + 0.2)
    pop(img, chip("PUNHO FRATURADO", 50, WHITE, RED), 780, 1190, t, wt(4, "fraturou") - 0.2)
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (150, 255, 170), 14, 40))
    paste(img, minipitch(640, t + 1, 0.0), cx, 560, 1, 0.8 + 0.2 * back(t / 0.3))
    pop(img, txt("DÁ CERTO?", 130, WHITE), cx, 900, t, wt(5, "certo") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1110, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1110, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("SÁBADO • 17H • CENTENÁRIO", 50, INK, AMB), cx, 1300, t, wt(5, "comenta") - 0.1)
S = Short("/home/claude/sex27a/tres", TRES, [s0, s1, s2, s3, s4, s5], "PALMEIRAS • FINAL", ["green", "dark", "night", "red", "blue", "green"], "Malicious", 20)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "arma"), 0.3), ("camera_click", S.segs[1][0] + wt(1, "confirmados"), 0.25),
                   ("torcida_aww", S.segs[3][0] + 0.3, 0.15), ("apito_juiz", S.segs[4][0] + wt(4, "suspenso"), 0.15), ("torcida_comemora", S.segs[5][0] + 0.2, 0.1)])
