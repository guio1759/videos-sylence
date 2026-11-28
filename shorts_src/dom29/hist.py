from extra import *
from PIL import ImageOps
from scripts import HIST
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
D = "/home/claude/dom29/img/"
def L(f): return Image.open(D + f).convert("RGBA")
SSPI = L("sspi.png"); TACA = L("taca.png"); TIME = L("1.jpg"); PACA = L("5.jpg"); JOGO = L("6.jpg")
def wt(i, w, d=0.5, nth=0):
    k = 0
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] and norm(c["w"]).startswith(norm(w)):
            if k == nth: return c["t0"] - S.segs[i][0]
            k += 1
    return d
def emo(img, name, x, y, t, t0, sz=170):
    if t >= t0: paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))
def fit(im, h): return im.resize((int(im.width * h / im.height), int(h)), Image.LANCZOS)
def sspi(h): return fit(SSPI, h)
def sepia(img, k=1.0):
    if k <= 0: return
    g = ImageOps.grayscale(img.convert("RGB")); s = ImageOps.colorize(g, (30, 20, 10), (245, 225, 185)).convert("RGBA")
    img.paste(Image.blend(img, s, k) if k < 1 else s)
def grain(img, T, a=26):
    rng = np.random.default_rng(int(T * 30)); n = rng.integers(0, a, (H // 4, W // 4), dtype=np.uint8)
    m = Image.fromarray(n, "L").resize((W, H)); img.alpha_composite(Image.merge("RGBA", (m, m, m, m)))
def photo(im, w, cap=None, sep=True):
    w = int(w); p = fit(im, int(im.height * w / im.width)) if False else im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    if sep: g = ImageOps.grayscale(p.convert("RGB")); p = ImageOps.colorize(g, (30, 20, 10), (245, 225, 185)).convert("RGBA")
    b = 18; out = Image.new("RGBA", (w + 2 * b, p.height + 2 * b + (60 if cap else 0)), (245, 240, 228, 255)); out.alpha_composite(p, (b, b))
    if cap: ImageDraw.Draw(out).text((out.width / 2, p.height + b + 32), cap, font=font("bd", 34), fill=INK, anchor="mm")
    return out
def flag(w, t):
    w = int(w); h = int(w * 0.7); f = Image.new("RGBA", (w, h), (0, 156, 59, 255)); d = ImageDraw.Draw(f)
    m = w * 0.085; d.polygon([(m, h / 2), (w / 2, m * 0.7), (w - m, h / 2), (w / 2, h - m * 0.7)], fill=(255, 223, 0))
    r = h * 0.25; d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(0, 39, 118))
    d.arc((w / 2 - r * 1.6, h / 2 - r * 0.55, w / 2 + r * 1.6, h / 2 + r * 2.6), 215, 325, fill=WHITE, width=int(r * 0.16))
    a = np.array(f); out = np.zeros((h + 60, w, 4), np.uint8)
    for x in range(w):
        dy = int(22 * math.sin(x / w * 7 - t * 6) * (x / w)); out[30 + dy:30 + dy + h, x] = a[:, x]
        s = 1 + 0.12 * math.sin(x / w * 7 - t * 6 - 1.2) * (x / w); out[30 + dy:30 + dy + h, x, :3] = np.clip(out[30 + dy:30 + dy + h, x, :3] * s, 0, 255)
    im = Image.fromarray(out, "RGBA"); pole = Image.new("RGBA", (24, h + 400), (220, 220, 220, 255))
    full = Image.new("RGBA", (w + 24, h + 400), (0, 0, 0, 0)); full.alpha_composite(pole); full.alpha_composite(im, (24, 0)); return full
def clock(sz, m):
    sz = int(sz); im = Image.new("RGBA", (int(sz * 2), sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, sz * 2, sz), 26, fill=(15, 18, 26, 240), outline=WHITE, width=6)
    d.text((sz, sz / 2), f"{int(m)}'", font=font("blk", int(sz * 0.62)), fill=AMB, anchor="mm"); return im
# ---------------- cenas ----------------
def s0(img, t, T):
    img.alpha_composite(rays(W, H, cx, 760, T, (150, 255, 170), 14, 50))
    sc = 1.0 + 0.05 * math.sin(min(t, 0.4) * 8)
    paste(img, txt("6 DIAS", 230, WHITE, 16), cx + shake(t, 0.02, 14), 500, 1, sc, -3)
    tn = 2.25
    if t < tn: paste(img, sspi(330), cx - 230, 880, 1, sc, -4)
    else: pop(img, logo("PAL", 330), cx - 230, 880, t, tn, 0.3, -4)
    if tn < t < tn + 0.2: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(190 * (1 - (t - tn) / 0.2)))))
    pop(img, chip("NOME NOVO", 54, INK, AMB), cx - 220, 1100, t, tn, 0.25, -3)
    d = ImageDraw.Draw(img); d.line((cx - 40, 880, cx + 40, 880), fill=WHITE, width=12); d.polygon([(cx + 40, 855), (cx + 80, 880), (cx + 40, 905)], fill=WHITE)
    paste(img, fit(TACA, 560), cx + 250, 850, 1, sc, 4)
    pop(img, stamp("TÍTULO", 96, RED), cx + 230 + shake(t, 3.35, 12), 1100, t, 3.3, 0.25, 6)
def s1(img, t, T):
    pop(img, txt("1942", 200, WHITE, 14), cx, 430, t, 0.0, 0.3, -2)
    tg = wt(1, "guerra", 1.2) - 0.3
    if t > tg: paste(img, newspaper(880, "SETEMBRO DE 1942", "BRASIL ENTRA NA GUERRA", "contra Alemanha e Itália", True, brand="DIÁRIO DA CIDADE"), cx, 800, 1, 0.9 + 0.1 * back(min(1, (t - tg) / 0.3)), -2)
    sepia(img); grain(img, T)
    ts = wt(1, "palestra", 3.0) - 0.2
    if t > ts:
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(185 * min(1, (t - ts) / 0.3)))))
        pop(img, sspi(420), cx, 860, t, ts, 0.3, -3)
        pop(img, chip("PALESTRA ITÁLIA", 56, WHITE, INK), cx, 1130, t, ts + 0.1)
    tu = wt(1, "suspeito", 4.5) - 0.2
    pop(img, stamp("SUSPEITO", 130, RED), cx + shake(t, tu + 0.05, 14), 860, t, tu, 0.25, -12)
def s2(img, t, T):
    pop(img, chip("14 DE SETEMBRO DE 1942", 52, INK, (235, 225, 200)), cx, 400, t, 0.0, 0.25, -2)
    pop(img, txt("PRESSÃO DOS MILITARES", 78, WHITE, 10), cx, 540, t, 0.15)
    tn = wt(2, "nasce", 2.8) - 0.15
    if t < tn:
        u = min(1, t / 0.4); paste(img, sspi(460), cx, 960, 1, 0.9 + 0.1 * u)
        pop(img, txt("MUDAR DE NOME", 96, AMB, 10), cx, 1260, t, wt(2, "obrigado", 1.4) - 0.2, 0.25, 3)
    sepia(img); grain(img, T)
    if t >= tn:
        img.alpha_composite(rays(W, H, cx, 960, T, (150, 255, 170), 14, int(70 * min(1, (t - tn) / 0.3))))
        if t - tn < 0.2: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(230 * (1 - (t - tn) / 0.2)))))
        pop(img, logo("PAL", 470), cx, 960, t, tn, 0.35, -3)
        pop(img, txt("PALMEIRAS", 140, (90, 230, 130), 12), cx, 1290, t, wt(2, "palmeiras", 3.2) - 0.25, 0.3, 2)
def s3(img, t, T):
    paste(img, photo(PACA, 860, "PACAEMBU • 20/09/1942"), cx, 640, 1, 1.0 + 0.03 * t, -2)
    tv = wt(3, "são", 1.4, 0) - 0.2
    pop(img, logo("PAL", 190), cx - 170, 1120, t, tv); pop(img, txt("x", 90, WHITE), cx, 1120, t, tv + 0.05); pop(img, logo("SAO", 190), cx + 170, 1120, t, tv + 0.1)
    sepia(img); grain(img, T)
    tb = wt(3, "bandeira", 3.2) - 0.45
    if t > tb:
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(120 * min(1, (t - tb) / 0.3)))))
        pop(img, flag(620, t), cx + 10, 900, t, tb, 0.35, -3)
def s4(img, t, T):
    paste(img, photo(JOGO, 820, "1942"), cx, 560, 1, 1.0 + 0.03 * t, 2)
    sepia(img, 0.85); grain(img, T)
    pop(img, scorebox("PAL", "SAO", 3, 1, 130), cx + shake(t, 0.1, 10), 960, t, 0.0)
    tp = wt(4, "pênalti", 1.6) - 0.2
    pop(img, stamp("PÊNALTI!", 110, AMB), cx, 1170, t, tp, 0.25, -6)
    ta = wt(4, "abandona", 3.0) - 0.25
    if t > ta:
        u = ease((t - ta) / 0.6); paste(img, logo("SAO", 260), cx + 900 * u, 700, 1 - u, 1.0, 20 * u)
        pop(img, stamp("ABANDONA O CAMPO", 84, RED), cx + shake(t, ta + 0.1, 12), 700, t, ta + 0.1, 0.25, 5)
    emo(img, "congelado", 880, 1320, t, ta + 0.3, 150)
def s5(img, t, T):
    tc = wt(5, "campeão", 1.8) - 0.3
    k = 1.0 - ease((t - tc) / 0.6) if t > tc else 1.0
    if t < tc:
        m = 64 + (90 - 64) * ease(t / max(0.5, tc - 0.2)); paste(img, clock(200, m), cx, 760, 1)
        pop(img, txt("O JUIZ ESPERA...", 90, WHITE, 10), cx, 1060, t, 0.1)
    else:
        img.alpha_composite(rays(W, H, cx, 800, T, (150, 255, 170), 14, 55))
        pop(img, photo(TIME, 940, None, sep=False), cx, 690, t, tc, 0.35, -2)
        pop(img, txt("CAMPEÃO PAULISTA", 90, WHITE, 12), cx, 1080, t, tc + 0.1, 0.3, 2)
        pop(img, chip("1º JOGO COMO PALMEIRAS", 54, INK, AMB), cx, 1240, t, wt(5, "primeiro", 3.6) - 0.2, 0.25, -3)
        if t - tc < 1.4: img.alpha_composite(confetti(W, H, t - tc, seed=5))
    sepia(img, k); grain(img, T, int(26 * k) + 1)
def s6(img, t, T):
    img.alpha_composite(rays(W, H, cx, 800, T, (255, 230, 120), 14, 40))
    l = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); paste(l, sspi(190), 160, 150, 1); paste(l, txt("MORRE LÍDER", 96, (200, 190, 170), 10), 620, 150, 1)
    g = ImageOps.grayscale(l.convert("RGB")).convert("RGBA"); g.putalpha(l.split()[3]); pop(img, g, cx, 470, t, 0.0, 0.3, -2)
    tn = wt(6, "nasce", 1.0) - 0.2
    r = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); paste(r, logo("PAL", 200), 160, 150, 1); paste(r, txt("NASCE CAMPEÃO", 84, (90, 230, 130), 10), 620, 150, 1)
    pop(img, r, cx, 760, t, tn, 0.3, 2)
    pop(img, chip("SIM", 110, WHITE, GREEN), 320, 1060, t, wt(6, "comenta", 2.6) - 0.1, 0.25, -4)
    pop(img, chip("NÃO", 110, WHITE, RED), 760, 1060, t, wt(6, "comenta", 2.6) + 0.15, 0.25, 4)
    pop(img, txt("VOCÊ SABIA?", 96, AMB), cx, 1280, t, wt(6, "conhecia", 2.0) - 0.2)
    if T > S.total - 3.5: paste(img, text_el("Fotos: Wikimedia Commons (domínio público)", font("sb", 22), (235, 235, 235), 3), W / 2, H - 240, 0.85); paste(img, text_el("Troféu: Paulo_hv • Escudo 1942: Danilo13cruz (CC BY-SA 4.0)", font("sb", 22), (235, 235, 235), 3), W / 2, H - 208, 0.85)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 170, 0.85)
S = Short("/home/claude/dom29/hist", HIST, [s0, s1, s2, s3, s4, s5, s6], "HISTÓRIA • 1942", ["green", "dark", "dark", "dark", "dark", "dark", "green"], "Interloper", 0)
if __name__ == "__main__":
    ev = [("whoosh_boom", 0.0, 0.35), ("tambor_impacto", 3.3, 0.3), ("whoosh_1", 2.25, 0.25), ("whoosh_grave", S.segs[1][0], 0.3),
          ("tambor_impacto", S.segs[1][0] + wt(1, "suspeito", 4.5), 0.4), ("whoosh_boom", S.segs[2][0] + wt(2, "nasce", 2.8), 0.35),
          ("torcida_comemora", S.segs[2][0] + wt(2, "palmeiras", 3.2), 0.18), ("estadio_ambiente", S.segs[3][0], 0.12),
          ("apito_juiz", S.segs[4][0] + wt(4, "pênalti", 1.6), 0.25), ("torcida_aww", S.segs[4][0] + wt(4, "abandona", 3.0), 0.2),
          ("apito_juiz", S.segs[5][0] + wt(5, "campeão", 1.8) - 0.3, 0.3), ("torcida_grita_gol", S.segs[5][0] + wt(5, "campeão", 1.8), 0.22)]
    main(S, extra=ev)
