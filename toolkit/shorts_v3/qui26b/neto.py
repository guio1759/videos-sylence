from fx2 import *
P['nC']=IMG+'nC.jpg'
FOC = {"neto1": (0.42, 0.3, 1.25), "nC": (0.5, 0.42, 1.05)}
def stk(k, h, t=0.0, name=None, col=AMB):
    """Card de foto: retrato recortado no rosto, cantos arredondados, borda branca, sombra e zoom lento."""
    h = int(h); w = int(h * 0.78); fx, fy, z0 = FOC[k]
    im = FX.load(P[k]); iw, ih = im.size; z = z0 + 0.06 * min(1, t / 4)
    ch = ih / z; cw = ch * w / h
    if cw > iw / z: cw = iw / z; ch = cw * h / w
    x0 = min(max(0, fx * iw - cw / 2), iw - cw); y0 = min(max(0, fy * ih - ch / 2), ih - ch)
    ph = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
    b = max(8, h // 45); r = h // 14
    card = Image.new("RGBA", (w + 2 * b, h + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, w + 2 * b - 1, h + 2 * b - 1), r + b, fill=WHITE)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    card.paste(ph, (b, b), m)
    if name:
        nm = chip(name, int(h * 0.085), INK, col); card2 = Image.new("RGBA", (card.width, card.height + nm.height // 2), (0, 0, 0, 0))
        card2.alpha_composite(card); card2.alpha_composite(nm, ((card.width - nm.width) // 2, card.height - nm.height // 2)); card = card2
    sh = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", card.size, (0, 0, 0, 140)), (36, 44), card.getchannel("A")); sh = sh.filter(ImageFilter.GaussianBlur(18))
    sh.alpha_composite(card, (24, 24)); return sh
def credits(img, ks):
    for i,k in enumerate(ks): FX.credit(img, CRJ[k], y=H-140-38*(len(ks)-1-i))
from scripts import NETO
SANT = (245, 245, 245)
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 880, T, (255, 220, 140), 14, 45))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("O NETO PEDIU", 120, WHITE, 12), cx, 380, 1, sc, -3)
    paste(img, txt("DESCULPAS", 150, AMB, 14), cx, 520, 1, sc, 2)
    k = 0.85 + 0.15 * back(t / 0.25)
    paste(img, stk("neto1", 500, t, "NETO"), 290 + shake(t, 0.1, 10), 930, 1, k, -5)
    paste(img, stk("nC", 500, t, "NEYMAR", WHITE), 790, 930, 1, k, 5)
    pop(img, chip("PRO NEYMAR", 80, INK, WHITE), cx, 1290, t, wt(0, "neymar") - 0.2, 0.25, -3)
    emo(img, "olhos", cx, 1420, t, wt(0, "desculpas") - 0.2, 150)
    credits(img, ["neto1", "nC"])
def s1(img, t, T):
    img.alpha_composite(rays(W, H, cx, 700, T, (255, 255, 255), 14, 30))
    pop(img, chip("QUARTA • 25/11", 56, INK, WHITE), cx, 300, t, 0.0)
    pop(img, stk("nC", 600, t, "NEYMAR", WHITE), cx, 720, t, 0.05, 0.3, 3)
    pop(img, logo("SAN", 170), cx + 260, 470, t, 0.3, 0.25, 8)
    pop(img, chip("INSTITUTO NEYMAR JR.", 64, INK, AMB), cx, 1130, t, wt(1, "instituto") - 0.2, 0.25, -2)
    pop(img, chip("PRAIA GRANDE (SP)", 56, WHITE, INK), cx, 1240, t, wt(1, "praia") - 0.2, 0.25, 2)
    pop(img, chip("+ A FAMÍLIA DO NETO", 52, INK, WHITE), cx, 1345, t, wt(1, "família") - 0.2)
    credits(img, ["nC"])
def s2(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (180, 210, 255), 14, 35))
    pop(img, chip("OS DONOS DA BOLA", 70, INK, (255, 205, 0)), cx, 400, t, 0.0, 0.25, -2)
    pop(img, stk("neto1", 560, t, "CRAQUE NETO"), cx, 760, t, 0.05, 0.3, -3)
    pop(img, stamp("DESCULPA!", 120, RED), cx, 1150, t, wt(2, "desculpas") - 0.15, 0.25, -6)
    tf = wt(2, "filho") - 0.25
    pop(img, chip("FILHO DO NETO • 9 ANOS", 52, WHITE, BLUE), cx - 90, 1320, t, tf, 0.25, 2)
    emo(img, "chorando", 920, 1300, t, wt(2, "emocionou") - 0.3, 260)
    credits(img, ["neto1"])
def s3(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 30))
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
    pop(img, stk("neto1", 420, t), 300, 1120, t, 0.3, 0.25, -5); pop(img, stk("nC", 420, t), 780, 1120, t, 0.45, 0.25, 5)
    emo(img, "coracao_verde", cx, 1130, t, 0.7, 170)
    credits(img, ["neto1", "nC"])
def s5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 220, 140), 14, 40))
    pop(img, stk("neto1", 430, t, "NETO"), 310, 540, t, 0.0, 0.25, -5)
    pop(img, stk("nC", 430, t, "NEYMAR", WHITE), 770, 540, t, 0.1, 0.25, 5)
    pop(img, txt("FOI SINCERO?", 120, WHITE), cx, 880, t, wt(5, "sincero") - 0.3)
    pop(img, chip("SIM", 110, WHITE, GREEN), 330, 1100, t, wt(5, "sim") - 0.2, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 750, 1100, t, wt(5, "não") - 0.2, 0.25, 4)
    pop(img, chip("COMENTA AÍ", 60, INK, WHITE), cx, 1290, t, wt(5, "comenta") - 0.1)
    credits(img, ["neto1", "nC"]); FX.credit(img, EM.CREDIT, y=H - 216)
S = Short("/home/claude/x26/neto", NETO, [s0, s1, s2, s3, s4, s5], "NETO x NEYMAR", ["purple", "dark", "blue", "purple", "green", "purple"], "Take_a_Chance", 10)
wt = mkwt(S)
if __name__ == "__main__":
    main(S, extra=[("tambor_impacto", 0.0, 0.45), ("whoosh_boom", wt(0, "desculpas"), 0.3), ("tambor_impacto", S.segs[2][0] + wt(2, "desculpas"), 0.3),
                   ("torcida_aww", S.segs[2][0] + wt(2, "emocionou"), 0.12), ("whoosh_3", S.segs[3][0] + wt(3, "helicóptero"), 0.25), ("torcida_comemora", S.segs[4][0] + 0.3, 0.1)])
