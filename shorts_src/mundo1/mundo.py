from extra import *
from art import *
from art import gray as _g
from scripts import MUNDO
sys.path.insert(0, "/home/claude/videos-sylence/toolkit/common"); import emoji
SENTS = [(s, 1.0, 0.0) for s in MUNDO]


def wt(i, w, d=0.5):
    for c in S.caps:
        if S.segs[i][0] - 0.05 <= c["t0"] <= S.segs[i][1] + 0.3 and norm(c["w"]).startswith(norm(w)): return c["t0"] - S.segs[i][0]
    return d


def emo(img, name, x, y, t, t0, sz=170):
    if t >= t0: paste(img, emoji.get(name, sz, t - t0), x, y, 1, 0.3 + 0.7 * back(min(1, (t - t0) / 0.25)))


def put(img, el, x, y, a=1.0, sc=1.0, rot=0.0): paste(img, el, x, y, a, sc, rot)
def full(img, bgim, soft=True):
    if soft and bgim.info.get('stands'): bgim = bgim.filter(ImageFilter.GaussianBlur(5)); bgim.alpha_composite(Image.new('RGBA', bgim.size, (10, 14, 30, 80)))
    img.alpha_composite(bgim)
def tagchip(img, s, y, t, t0=0.0, col=AMB, fg=INK, rot=-2): pop(img, chip(s, 50, fg, col), cx, y, t, t0, 0.25, rot)
def vig(img, a=110):
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(v); d.ellipse((-W * 0.4, -H * 0.15, W * 1.4, H * 1.15), fill=(0, 0, 0, 0))
    m = Image.new("L", (W, H), a); ImageDraw.Draw(m).ellipse((-W * 0.3, -H * 0.05, W * 1.3, H * 1.05), fill=0); m = m.filter(ImageFilter.GaussianBlur(120))
    img.alpha_composite(Image.merge("RGBA", (m.point(lambda _: 0),) * 3 + (m,)))
def bob(t, a=6, f=3): return a * math.sin(t * f)


# 0 — gancho: torcedor perdendo a cor dos pés à cabeça
def s0(img, t, T):
    full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 140)
    c = person("fan", 900, shirt=VERDE, scarf=True, la=150 if t < 1.2 else 20, ra=-150 if t < 1.2 else -20, expr="shout" if t < 1.2 else "sad", seed=2)
    g = person("fan", 900, shirt=VERDE, scarf=True, k=1, la=20, ra=-20, expr="sad", seed=2)
    fr = clamp((t - 1.2) / 1.4)
    put(img, wipe_gray(c, g, fr), cx, 1060 + bob(t, 4))
    put(img, txt("NESSE MUNDO...", 110, WHITE, 12), cx, 330, 1, 1.0 + 0.04 * math.sin(min(t, 0.4) * 8), -2)


# 1 — rua: cinzas e coloridos andando
def s1(img, t, T):
    full(img, bg_street(W, H))
    for j, (x0, k, sp) in enumerate(((120, 0, 60), (420, 1, 35), (700, 0, 70), (960, 1, 30))):
        x = (x0 + sp * t) % (W + 200) - 100
        p = person("fan", 470, k=k, expr="sad" if k else "smile", la=15 + 10 * math.sin(t * 5 + j), ra=-15 - 10 * math.sin(t * 5 + j), ll=10 * math.sin(t * 6 + j), rl=-10 * math.sin(t * 6 + j), seed=10 + j, shirt=VERDE if (j == 2) else None)
        put(img, p, x, 1170 - 240 + abs(bob(t + j, 6, 6)))
    pop(img, chip("REBAIXADO = CINZA", 54, WHITE, (90, 90, 95)), cx, 360, t, wt(1, "rebaixado", 1.8) - 0.2, 0.25, -2)


# 2 — tríptico: ônibus, trabalho, casamento
def panel_bus(k):
    p = Image.new("RGBA", (960, 380), (250, 214, 160, 255)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((40, 60, 920, 330), 40, fill=_g((240, 190, 60), 0)); d.rectangle((40, 290, 920, 330), fill=(60, 60, 70))
    for j in range(5):
        x = 90 + j * 165; d.rounded_rectangle((x, 100, x + 130, 220), 14, fill=(200, 230, 245))
        if j in (1, 3): p.alpha_composite(person("fan", 210, k=1, expr="sad", seed=30 + j).crop((20, 0, 170, 120)), (x - 10, 110))
        elif j == 2: p.alpha_composite(person("fan", 210, expr="smile", seed=40).crop((20, 0, 170, 120)), (x - 10, 110))
    d.ellipse((150, 290, 250, 370), fill=(40, 40, 45)); d.ellipse((710, 290, 810, 370), fill=(40, 40, 45))
    return p
def panel_office():
    p = Image.new("RGBA", (960, 380), (225, 230, 240, 255)); d = ImageDraw.Draw(p)
    d.rectangle((0, 300, 960, 380), fill=(170, 150, 130)); d.rectangle((180, 230, 780, 260), fill=(150, 110, 80))
    p.alpha_composite(person("fan", 330, k=1, expr="bored", la=70, ra=-70, seed=51).crop((0, 0, 297, 250)), (330, 40))
    d.rectangle((520, 150, 660, 232), fill=(40, 40, 50)); d.rectangle((530, 160, 650, 222), fill=(120, 200, 230))
    return p
def panel_wed():
    p = Image.new("RGBA", (960, 380), (255, 235, 240, 255)); d = ImageDraw.Draw(p)
    for j in range(7): d.ellipse((60 + j * 130, 20, 120 + j * 130, 80), fill=(255, 190, 200))
    p.alpha_composite(person("noivo", 340, k=1, expr="sad", ra=-40, seed=60), (230, 40)); p.alpha_composite(person("noiva", 330, la=40, seed=61), (430, 50))
    return p
def s2(img, t, T):
    full(img, bg_paper(W, H))
    for j, (w, f) in enumerate((("ônibus", lambda: panel_bus(1)), ("trabalho", panel_office), ("casamento", panel_wed))):
        t0 = wt(2, w, 0.3 + 1.3 * j) - 0.25
        el = Image.new("RGBA", (980, 400), (0, 0, 0, 0)); el.alpha_composite(Image.new("RGBA", (980, 400), (40, 32, 28, 255))); el.alpha_composite(f(), (10, 10))
        pop(img, el, cx, 470 + 420 * j, t, t0, 0.3, (-2, 2, -1)[j])


# 3 — os mais velhos: banco da praça e seta pra cima
def s3(img, t, T):
    full(img, bg_street(W, H, sky=(200, 225, 240)))
    d = ImageDraw.Draw(img); d.rounded_rectangle((180, 1000, 900, 1050), 14, fill=(150, 100, 60)); d.rectangle((220, 1050, 250, 1170), fill=(110, 75, 45)); d.rectangle((830, 1050, 860, 1170), fill=(110, 75, 45))
    put(img, person("vo", 520, sit=True, k=1, la=10, ra=-150, expr="o", seed=70, hair=(220, 220, 220)), 380, 900)
    put(img, person("fan", 520, sit=True, k=1, expr="bored", seed=71, hair=(220, 220, 220), skin=2), 700, 900)
    tu = wt(3, "sobe", 2.2) - 0.3
    if t > tu:
        u = ease((t - tu) / 0.7); put(img, crest(220, 1 - u), cx + 180, 520 - 160 * u, 1)
        d = ImageDraw.Draw(img); d.polygon([(cx - 40, 700 - 160 * u), (cx, 620 - 160 * u), (cx + 40, 700 - 160 * u)], fill=GREEN); d.rectangle((cx - 15, 700 - 160 * u, cx + 15, 820), fill=GREEN)
    pop(img, chip("A COR VOLTA SE O TIME SUBIR?", 46, INK, AMB), cx, 330, t, 0.2, 0.25, -2)


# 4 — Caio, cinza, celular no sofá
def sofa(img, x, y):
    d = ImageDraw.Draw(img); d.rounded_rectangle((x - 330, y - 120, x + 330, y + 60), 40, fill=(140, 80, 70)); d.rounded_rectangle((x - 380, y - 40, x + 380, y + 140), 40, fill=(160, 95, 80))
def s4(img, t, T):
    full(img, bg_paper(W, H, 0.3))
    sofa(img, cx, 1080)
    put(img, person("caio", 620, k=1, sit=True, la=40, ra=-40, expr="bored", look=-1), cx, 920)
    d = ImageDraw.Draw(img); d.rounded_rectangle((cx - 50, 880, cx + 50, 960), 10, fill=(30, 30, 35)); d.rectangle((cx - 40, 888, cx + 40, 950), fill=(120, 160, 200))
    pop(img, chip("CAIO, 10 ANOS", 58, WHITE, (90, 90, 95)), cx, 380, t, wt(4, "caio", 1.6) - 0.2, 0.25, -3)
    pop(img, txt("NASCEU CINZA", 90, (200, 200, 200), 10), cx, 520, t, wt(4, "nasceu", 2.6) - 0.2, 0.25, 2)
    emo(img, "sono", 860, 700, t, wt(4, "velho", 4.6), 150)


# 5 — Seu Antônio colorido
def s5(img, t, T):
    full(img, bg_paper(W, H)); img.alpha_composite(rays(W, H, cx, 900, T, (255, 220, 140), 14, 50))
    put(img, person("vo", 900, scarf=True, la=25, ra=-150 + 15 * math.sin(t * 5), expr="smile"), cx - 60, 1010 + bob(t, 4))
    put(img, crest(220), cx + 330, 620, 1, 1.0, 8)
    pop(img, chip("SEU ANTÔNIO, 80", 58, WHITE, VERDE), cx, 330, t, wt(5, "antônio", 2.0) - 0.2, 0.25, -3)
    pop(img, chip("O ÚLTIMO COLORIDO", 50, INK, AMB), cx, 440, t, wt(5, "colorido", 4.0) - 0.2, 0.25, 2)


# 6 — 60 anos sem cair, nunca perdeu um jogo
def s6(img, t, T):
    full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 120)
    put(img, person("vo", 760, scarf=True, la=20, ra=-160, expr="smile"), cx, 1100)
    t6 = wt(6, "sessenta", 0.6) - 0.3
    if t > t6: pop(img, odometer(60, 2, 220, t - t6, 0.8), cx - 120, 450, t, t6)
    pop(img, txt("ANOS", 110, WHITE, 10), cx + 200, 450, t, t6 + 0.2)
    pop(img, chip("SEM CAIR", 70, INK, AMB), cx, 620, t, wt(6, "caído", 2.2) - 0.2, 0.25, -3)


# 7 — dois ingressos e a cadeira vazia
def s7(img, t, T):
    tc = wt(7, "cadeira", 2.6) - 0.3
    if t < tc:
        full(img, bg_paper(W, H))
        pop(img, ticket(560, n="14"), cx - 60, 760, t, wt(7, "dois", 1.0) - 0.3, 0.3, -6)
        pop(img, ticket(560, n="15"), cx + 60, 1000, t, wt(7, "dois", 1.0) - 0.1, 0.3, 5)
        pop(img, chip("2 INGRESSOS", 60, WHITE, VERDE), cx, 420, t, wt(7, "dois", 1.0) - 0.2, 0.25, -2)
    else:
        full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 160)
        put(img, seat(300), cx - 200, 1120); put(img, seat(300), cx + 200, 1120)
        put(img, person("vo", 640, scarf=True, sit=True, la=10, ra=-10, expr="sad", look=2), cx - 200, 930)
        pop(img, chip("SEMPRE VAZIA", 58, WHITE, (90, 90, 95)), cx + 200, 780, t, wt(7, "vazia", 4.0) - 0.2, 0.25, 4)


def scoreboard(a, b, top="ÚLTIMA RODADA", minute=None, k=0.0):
    w, h = 940, 420; p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, w, h), 34, fill=(20, 22, 30, 245), outline=WHITE, width=6)
    d.text((w / 2, 60), top, font=font("blk", 48), fill=AMB, anchor="mm")
    p.alpha_composite(crest(170, k), (80, 120)); d.text((w / 2, 220), f"{a} x {b}", font=font("blk", 140), fill=WHITE, anchor="mm")
    d.ellipse((w - 240, 130, w - 80, 290), fill=(150, 40, 40), outline=WHITE, width=6); d.text((w - 160, 210), "?", font=font("blk", 90), fill=WHITE, anchor="mm")
    if minute is not None: d.text((w / 2, 360), f"{minute}'", font=font("blk", 56), fill=AMB, anchor="mm")
    return p


# 8 — última rodada, precisa do empate
def s8(img, t, T):
    full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 170)
    pop(img, scoreboard(0, 0), cx, 700, t, 0.0, 0.3, -1)
    pop(img, stamp("PRECISA DO EMPATE", 76, RED), cx + shake(t, wt(8, "empate", 2.4), 10), 1040, t, wt(8, "empate", 2.4) - 0.2, 0.25, -4)


# 9 — Caio foi junto, de braço cruzado
def s9(img, t, T):
    full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 140)
    put(img, seat(300), cx - 200, 1120); put(img, seat(300), cx + 200, 1120)
    put(img, person("vo", 640, scarf=True, sit=True, la=10, ra=-150, expr="smile"), cx - 200, 930)
    tj = wt(9, "sentou", 1.8) - 0.3
    if t > tj: pop(img, person("caio", 600, k=1, sit=True, la=-60, ra=60, expr="angry", look=-2), cx + 200, 950, t, tj)
    pop(img, chip("OBRIGADO", 56, WHITE, (90, 90, 95)), cx + 200, 600, t, wt(9, "obrigado", 1.4) - 0.2, 0.25, 4)


# 10 — 0x0, 90', gol do adversário
def s10(img, t, T):
    tg = wt(10, "gol", 2.6) - 0.1
    k = 0.0
    full(img, bg_stands(W, H, 0.0, t=t)); vig(img, 170)
    m = 90 if t > wt(10, "noventa", 1.2) - 0.2 else 88
    if t < tg: put(img, scoreboard(0, 0, minute=m), cx, 760)
    else:
        if t - tg < 0.15: img.alpha_composite(Image.new("RGBA", (W, H), (255, 60, 60, int(200 * (1 - (t - tg) / 0.15)))))
        put(img, scoreboard(0, 1, minute=90), cx + shake(t, tg, 16), 760)
        pop(img, stamp("GOL DELES", 110, RED), cx, 1100, t, tg, 0.25, -6)


# 11 — estádio ficando cinza fileira por fileira
def s11(img, t, T):
    fr = clamp(t / max(1.0, (S.segs[11][1] - S.segs[11][0])))
    full(img, bg_stands(W, H, 0.0, wipe=fr, t=t))
    vig(img, 120)


# 12 — as mãos do seu Antônio perdendo o verde
def s12(img, t, T):
    full(img, bg_stands(W, H, 1.0, people=True)); vig(img, 190)
    c = hand(620); g = hand(620, k=1); fr = clamp((t - 0.8) / 2.2)
    put(img, wipe_gray(c, g, fr, from_bottom=False), cx, 980)
    d = ImageDraw.Draw(img)
    put(img, person("vo", 360, scarf=True, k=fr, sit=True, expr="sad").crop((0, 0, 324, 200)), cx, 420)


# 13 — Caio segura a mão e grita
def s13(img, t, T):
    full(img, bg_stands(W, H, 1.0, people=True, t=t)); vig(img, 150)
    tg = wt(13, "gritou", 3.4) - 0.1; th = wt(13, "segurou", 2.0) - 0.2
    if t < tg:
        put(img, hand(520, k=0.85), cx - 160, 980, 1, 1.0, 20)
        if t > th: pop(img, hand(430, k=1, skin=0, flip=True), cx + 170, 1030, t, th, 0.3, -25)
    else:
        put(img, person("caio", 880, k=1, la=145, ra=-145, expr="shout"), cx + shake(t, tg, 14), 1060)
        pop(img, txt("VAMOS, VILA!", 150, WHITE, 16), cx + shake(t, tg + 0.05, 16), 420, t, tg + 0.05, 0.2, -4)


# 14 — a cor voltou
def s14(img, t, T):
    fr = 1 - clamp(t / 0.9)
    full(img, bg_stands(W, H, fr * 0.7, t=t)); img.alpha_composite(rays(W, H, cx, 900, T, (255, 230, 140), 14, int(80 * (1 - fr))))
    put(img, seat(300, k=fr), cx - 200, 1140); put(img, seat(300, k=fr), cx + 200, 1140)
    put(img, person("vo", 640, scarf=True, sit=True, la=10, ra=-150, expr="smile", k=fr * 0.8), cx - 200, 950)
    tc = wt(14, "dele", 3.2) - 0.4
    kc = 1.0 if t < tc else 1 - clamp((t - tc) / 0.6)
    put(img, person("caio", 600, sit=True, la=150, ra=-150, expr="smile" if kc < 0.5 else "o", shirt=VERDE if kc < 1 else None, scarf=kc < 0.5, k=kc), cx + 200, 970)
    if t > tc and t - tc < 0.8: img.alpha_composite(confetti(W, H, t - tc, seed=4))


# 15 — caiu, mas ninguém naquelas cadeiras ficou cinza
def s15(img, t, T):
    full(img, bg_stands(W, H, 1.0, people=True)); vig(img, 150)
    put(img, seat(300), cx - 200, 1140); put(img, seat(300), cx + 200, 1140)
    put(img, person("vo", 640, scarf=True, sit=True, expr="smile"), cx - 200, 950)
    put(img, person("caio", 600, sit=True, la=30, ra=-30, expr="smile", shirt=VERDE, scarf=True), cx + 200, 970)
    pop(img, stamp("REBAIXADO", 100, RED), cx, 470, t, 0.2, 0.25, -6)
    pop(img, chip("MAS COLORIDOS", 60, INK, AMB), cx, 620, t, wt(15, "ninguém", 1.8) - 0.2, 0.25, 3)


# 16 — a verdade da regra
def s16(img, t, T):
    full(img, bg_paper(W, H, 0.6)); vig(img, 120)
    pop(img, txt("NINGUÉM PERDE A COR", 84, WHITE, 10), cx, 500, t, 0.1, 0.25, -2)
    pop(img, txt("QUANDO O TIME CAI", 84, (200, 200, 200), 10), cx, 620, t, 0.4, 0.25, 2)
    tp = wt(16, "perde", 2.6, ) if False else wt(16, "quando", 3.0) + 0.6
    pop(img, txt("PERDE QUANDO", 96, AMB, 12), cx, 860, t, tp, 0.25, -2)
    pop(img, txt("TORCE SOZINHO", 110, AMB, 12), cx, 990, t, wt(16, "torcer", 4.6) - 0.3, 0.25, 2)


# 17 — a cadeira vazia era do pai
def s17(img, t, T):
    full(img, Image.new("RGBA", (W, H), (30, 34, 60, 255)))
    d = ImageDraw.Draw(img); d.rounded_rectangle((140, 360, 940, 1180), 30, fill=(60, 66, 100)); d.rectangle((180, 400, 900, 1140), fill=(90, 96, 140))
    d.rectangle((520, 400, 540, 1140), fill=(60, 66, 100)); d.rectangle((180, 760, 900, 780), fill=(60, 66, 100))
    tp = wt(17, "pai", 2.4) - 0.3
    put(img, person("pai", 620, k=1, sit=True, expr="sad", la=10, ra=-10), cx, 1000)
    pop(img, chip("O PAI DO CAIO", 56, WHITE, (90, 90, 95)), cx, 300, t, tp, 0.25, -3)


# 18 — três ingressos
def s18(img, t, T):
    full(img, bg_stands(W, H, 0.0, t=t)); img.alpha_composite(rays(W, H, cx, 1000, T, (255, 230, 140), 14, 60))
    for j, x in enumerate((cx - 330, cx, cx + 330)): put(img, seat(260), x, 1180)
    put(img, person("pai", 560, sit=True, la=10, ra=-150, expr="smile", shirt=VERDE, scarf=True), cx - 330, 1010)
    put(img, person("vo", 560, scarf=True, sit=True, la=150, ra=-150, expr="smile"), cx, 1010)
    put(img, person("caio", 520, sit=True, la=150, ra=-30, expr="shout", shirt=VERDE, scarf=True), cx + 330, 1030)
    tt = wt(18, "três", 2.2) - 0.3
    for j in range(3): pop(img, ticket(380, n=str(14 + j)), cx - 230 + 230 * j, 520 + 20 * (j % 2), t, tt + 0.12 * j, 0.25, (-8, 0, 8)[j])
    if T > S.total - 3.0:
        pop(img, chip("MARCA QUEM TE LEVOU NO 1º JOGO", 44, INK, AMB), cx, 800, t, S.total - 3.0 - S.segs[18][0], 0.25, -2)
    if T > S.total - 2.5: paste(img, text_el(emoji.CREDIT, font("sb", 24), (235, 235, 235), 3), W / 2, H - 170, 0.85)


S = Short("/home/claude/mundo/m", SENTS, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18], "NESSE MUNDO…", "dark", "Heartbreaking", 0)
S.MUSG = 0.085; S.DUCK = 0.6
S.total = S.total + 2.5
if __name__ == "__main__":
    sg = S.segs
    S.SWELL = [(sg[13][0] + wt(13, "gritou", 3.4), S.total, 1.7)]
    ev = [("whoosh_grave", 0.0, 0.3), ("torcida_aww", 1.3, 0.15), ("estadio_ambiente", sg[6][0], 0.1), ("camera_click", sg[7][0] + wt(7, "dois", 1.0), 0.2),
          ("estadio_ambiente", sg[8][0], 0.14), ("apito_curto", sg[10][0] + wt(10, "noventa", 1.2), 0.15), ("torcida_reacao_gol", sg[10][0] + wt(10, "gol", 2.6), 0.2),
          ("torcida_aww", sg[11][0] + 0.3, 0.2), ("riser", sg[13][0] + wt(13, "gritou", 3.4) - 1.0, 0.15), ("tambor_impacto", sg[13][0] + wt(13, "gritou", 3.4), 0.35),
          ("torcida_comemora", sg[14][0] + 0.1, 0.2), ("ding", sg[18][0] + wt(18, "três", 2.2), 0.25), ("torcida_comemora", sg[18][0] + wt(18, "três", 2.2), 0.15)]
    main(S, extra=ev)
