from extra import *
import os
from scripts import CAMP, VICE
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
MODE = os.environ.get("MODE", "camp")
EST = lambda h: logo("EST", h)
GOLD = (255, 205, 60)
def wt(i, w, d=0.5):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return d
@functools.lru_cache(8)
def taca(h):
    im = Image.open("/home/claude/sab28c/taca_new.png").convert("RGBA"); h = int(h); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    pad = int(h * 0.25); out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    g = Image.new("RGBA", out.size, (255, 210, 90, 0)); a = Image.new("L", out.size, 0); a.paste(im.getchannel("A"), (pad, pad))
    g.putalpha(a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(pad / 2.2)).point(lambda v: int(v * 0.85)))
    out.alpha_composite(g); out.alpha_composite(im, (pad, pad)); return out
def emo(img, name, x, y, t, t0, sz=170):
    if t >= t0: paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def flag_br(w):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 16, fill=(0, 150, 60), outline=INK, width=6)
    d.polygon([(w * 0.08, h / 2), (w / 2, h * 0.09), (w * 0.92, h / 2), (w / 2, h * 0.91)], fill=(255, 215, 0))
    r = h * 0.25; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(20, 40, 130))
    d.arc((w / 2 - r * 1.3, h / 2 - r * 0.6, w / 2 + r * 1.3, h / 2 + r * 2.2), 225, 315, fill=WHITE, width=max(4, int(h * 0.04)))
    return im
def flag_ar(w):
    w = int(w); h = int(w * 0.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 16, fill=WHITE)
    d.rectangle((3, 3, w - 3, h / 3), fill=(116, 172, 223)); d.rectangle((3, h * 2 / 3, w - 3, h - 3), fill=(116, 172, 223))
    r = h * 0.11; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(246, 180, 14), outline=(133, 52, 13), width=3)
    d.rounded_rectangle((0, 0, w, h), 16, outline=INK, width=6)
    return im
def vs_box(la, lb, ga, gb, sz=150, colb=WHITE):
    w = int(sz * 6); h = int(sz * 1.7); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 30, fill=(15, 18, 26, 240), outline=WHITE, width=5)
    im.alpha_composite(la, (int(sz * 1.0 - la.width / 2), int(h / 2 - la.height / 2)))
    im.alpha_composite(lb, (int(w - sz * 1.0 - lb.width / 2), int(h / 2 - lb.height / 2)))
    d.text((w / 2, h / 2), f"{ga} x {gb}", font=font("blk", sz * 0.8), fill=colb, anchor="mm")
    return im
def cups(img, years, y, t, t0s, h=170, col=GOLD):
    n = len(years); gap = min(250, 960 / n)
    for k, (yr, t0) in enumerate(zip(years, t0s)):
        x = cx + (k - (n - 1) / 2) * gap
        pop(img, trophy(h, col), x, y, t, t0, 0.25, (-5, 5)[k % 2])
        pop(img, chip(yr, 46, INK, WHITE), x, y + h * 0.72, t, t0 + 0.1, 0.25)

# ---------- CAMPEÃO ----------
def c0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (255, 220, 120), 16, 60)); img.alpha_composite(confetti(W, H, t + 0.5))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, taca(700), cx, 760, 1, sc)
    k = int((T * 3) % 6); d = ImageDraw.Draw(img)
    for j in range(6):
        a = j * 1.05 + T * 0.8; x, y = cx + 230 * math.cos(a), 700 + 300 * math.sin(a); r = 10 + 8 * abs(math.sin(T * 4 + j))
        d.polygon([(x, y - r * 2), (x + r * 0.5, y), (x, y + r * 2), (x - r * 0.5, y)], fill=(255, 240, 180)); d.polygon([(x - r * 2, y), (x, y + r * 0.5), (x + r * 2, y), (x, y - r * 0.5)], fill=(255, 240, 180))
    paste(img, txt("TETRA", 220, GOLD, 16), cx, 1180, 1, sc, -3)
    paste(img, chip("CAMPEÃO DA LIBERTADORES 2026", 54, INK, WHITE), cx, 1360, 1, sc)
    paste(img, logo("PAL", 140), 160, 330, 1, sc)
def c1(img, t, T):
    pop(img, chip("58 ANOS DEPOIS", 70, INK, AMB), cx, 400, t, 0.0, 0.25, -3)
    pop(img, logo("PAL", 220), 290, 760, t, wt(1, "mesmo") - 0.2, 0.3, -5); pop(img, txt("x", 110, AMB), cx, 760, t, wt(1, "mesmo"))
    pop(img, EST(220), 790, 760, t, wt(1, "estudiantes") - 0.2, 0.3, 5)
    pop(img, chip("ESTÁDIO CENTENÁRIO", 56, WHITE, INK), cx, 1000, t, wt(1, "centenário") - 0.2)
    pop(img, stamp("REVANCHE!", 130, GREEN), cx, 1250, t, wt(1, "revanche") - 0.2, 0.25, -6)
def c2(img, t, T):
    pop(img, logo("PAL", 200), cx, 380, t, 0.0)
    pop(img, txt("4 TÍTULOS", 120, GOLD), cx, 590, t, wt(2, "quarto") - 0.2)
    ys = ["1999", "2020", "2021", "2026"]; t0s = [wt(2, "noventa") - 0.15, wt(2, "vinte") - 0.3, wt(2, "um") - 0.3, wt(2, "agora") - 0.1]
    for k, (yr, t0) in enumerate(zip(ys, t0s)):
        x = cx + (k - 1.5) * 240
        pop(img, taca(330 if k < 3 else 400), x, 900, t, t0, 0.3, (-4, 4)[k % 2])
        pop(img, chip(yr, 50, INK, GOLD if k == 3 else WHITE), x, 1140, t, t0 + 0.1)
    if t > t0s[3]: img.alpha_composite(confetti(W, H, t - t0s[3]))
def c3(img, t, T):
    tb = wt(3, "brasil") - 0.25
    if t < tb:
        pop(img, chip("ABEL FERREIRA", 70, INK, WHITE), cx, 500, t, 0.0)
        pop(img, txt("TRICAMPEÃO", 140, GOLD), cx, 760, t, wt(3, "tricampeão") - 0.25)
        for k in range(3): pop(img, taca(300), cx + (k - 1) * 260, 1070, t, wt(3, "tricampeão") + 0.1 * k)
    else:
        u = t - tb; pop(img, chip("TÍTULOS DA LIBERTADORES", 56, INK, WHITE), cx, 450, u, 0.0)
        pop(img, vs_box(flag_br(200), flag_ar(200), 26, 25, 140, AMB), cx, 760, u, 0.1)
        pop(img, txt("BRASIL NA FRENTE", 88, GREEN), cx, 1030, u, wt(3, "vinte") - tb - 0.2)
        emo(img, "fogo", 900, 1200, u, 0.6)
def c4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (150, 255, 170), 14, 40))
    pop(img, txt("US$ 25", 190, GOLD), cx, 640, t, wt(4, "vinte") - 0.3)
    pop(img, txt("MILHÕES", 130, WHITE), cx, 830, t, wt(4, "milhões") - 0.2)
    emo(img, "dinheiro", cx, 1110, t, wt(4, "dólares") - 0.2, 220)
def c5(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (255, 220, 120), 14, 45))
    pop(img, taca(470), cx, 620, t, 0.0)
    pop(img, txt("QUEM FOI", 120, WHITE), cx, 990, t, 0.2); pop(img, txt("O HERÓI?", 140, GOLD), cx, 1140, t, 0.4)
    pop(img, chip("COMENTA O NOME", 64, INK, AMB), cx, 1320, t, wt(5, "comenta") - 0.2, 0.25, -3)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 125, 0.85)
# ---------- VICE ----------
def v0(img, t, T):
    sc = 1.0 + 0.04 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("NÃO DEU.", 190, WHITE, 16), cx, 520, 1, sc, -2)
    paste(img, EST(300), cx, 880, 1, sc)
    pop(img, chip("ESTUDIANTES PENTACAMPEÃO", 56, WHITE, RED), cx, 1140, t, wt(0, "estudiantes") - 0.2)
    emo(img, "chorando", 900, 1300, t, 0.6)
def v1(img, t, T):
    pop(img, chip("CENTENÁRIO", 70, INK, WHITE), cx, 420, t, 0.0)
    pop(img, txt("1968", 170, (200, 200, 200)), 300, 760, t, wt(1, "mil") - 0.2, 0.3, -4)
    pop(img, txt("2026", 170, WHITE), 780, 760, t, wt(1, "história") - 0.4, 0.3, 4)
    pop(img, stamp("A HISTÓRIA SE REPETIU", 84, RED), cx, 1040, t, wt(1, "repetiu") - 0.3, 0.25, -5)
def v2(img, t, T):
    pop(img, txt("2ª FINAL SEGUIDA", 110, WHITE), cx, 420, t, 0.0)
    pop(img, scorebox("PAL", "FLA", "", "", 120), cx, 680, t, wt(2, "flamengo") - 0.2)
    pop(img, chip("2025 • LIMA", 50, INK, WHITE), cx, 860, t, wt(2, "flamengo"))
    pop(img, scorebox("PAL", "EST", "", "", 120), cx, 1080, t, wt(2, "agora") - 0.1)
    pop(img, chip("2026 • MONTEVIDÉU", 50, INK, WHITE), cx, 1260, t, wt(2, "agora") + 0.1)
def v3(img, t, T):
    pop(img, chip("TÍTULOS DA LIBERTADORES", 56, INK, WHITE), cx, 450, t, 0.0)
    pop(img, vs_box(flag_ar(200), flag_br(200), 26, 25, 140, AMB), cx, 760, t, wt(3, "argentina") - 0.2)
    pop(img, txt("ARGENTINA NA FRENTE", 70, (116, 172, 223)), cx, 1030, t, wt(3, "frente") - 0.2)
def v4(img, t, T):
    img.alpha_composite(rays(W, H, cx, 850, T, (150, 255, 170), 14, 35))
    pop(img, chip("ABEL FERREIRA", 70, INK, WHITE), cx, 520, t, 0.0)
    pop(img, txt("O MAIS VENCEDOR", 92, GREEN), cx, 780, t, wt(4, "vencedor") - 0.3)
    pop(img, txt("DA HISTÓRIA", 92, WHITE), cx, 920, t, wt(4, "história") - 0.3)
    pop(img, logo("PAL", 200), cx, 1170, t, wt(4, "palmeiras") - 0.3)
def v5(img, t, T):
    pop(img, txt("O QUE", 140, WHITE), cx, 640, t, 0.0); pop(img, txt("FALTOU?", 160, AMB), cx, 820, t, 0.2)
    pop(img, chip("COMENTA AÍ", 70, INK, AMB), cx, 1060, t, wt(5, "comenta") - 0.2, 0.25, -3)
    emo(img, "pensando", cx, 1280, t, 0.4)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 125, 0.85)
if MODE == "camp":
    S = Short("/home/claude/sab28c/camp", CAMP, [c0, c1, c2, c3, c4, c5], "FINAL DA LIBERTADORES", ["green", "night", "green", "dark", "green", "night"], "Lasting_Hope", 0)
    EV = [("torcida_grita_gol", 0.0, 0.5), ("torcida_comemora", 0.3, 0.35), ("tambor_impacto", S.segs[1][0] + wt(1, "revanche"), 0.35), ("torcida_comemora", S.segs[2][0] + wt(2, "agora"), 0.3), ("camera_click", S.segs[4][0], 0.2)]
else:
    S = Short("/home/claude/sab28c/vice", VICE, [v0, v1, v2, v3, v4, v5], "FINAL DA LIBERTADORES", ["dark", "night", "dark", "night", "green", "dark"], "Heartbreaking", 0)
    EV = [("torcida_aww", 0.0, 0.35), ("tambor_impacto", S.segs[1][0] + wt(1, "repetiu"), 0.3)]
if __name__ == "__main__":
    main(S, extra=EV)
