import sys, functools; sys.path.insert(0, "/home/claude/por"); sys.path.insert(0, "/home/claude/sex20"); sys.path.insert(0, "/home/claude/carreira")
from com import *
import card as C
from chars import thiago, kid
sys.path.insert(0, "/home/claude/por/ep1"); from script import S as TXT
D = "/home/claude/por/ep1"
CAN = Image.open("/home/claude/videos-sylence/carreira/portuguesa/assets/caninde.jpg").convert("RGBA")
GOLD = (255, 205, 60)
IM = "/home/claude/por/img/"
@functools.lru_cache(32)
def cut(k, h): im = Image.open(IM + k + "_cut.png").convert("RGBA"); h = int(h); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
@functools.lru_cache(16)
def _cov(k):
    im = Image.open(IM + k + ".jpg").convert("RGBA"); sc = max(W * 1.15 / im.width, H * 1.15 / im.height)
    return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
def cover(img, k, t, dim=90, dx=0.0):
    b = _cov(k); z = 1.0 + 0.035 * t
    bw, bh = int(W * 1.15 / z), int(H * 1.15 / z)
    x0 = int((b.width - bw) / 2 + dx * t * 30); y0 = int((b.height - bh) / 2)
    x0 = max(0, min(b.width - bw, x0))
    img.alpha_composite(b.crop((x0, y0, x0 + bw, y0 + bh)).resize((W, H)))
    if dim: img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim)))

def wt(i, word, n=1):
    s0 = SH.segs[i][0]; c = 0
    for w in SH.caps:
        if SH.segs[i][0] - 0.01 <= w["t0"] <= SH.segs[i][1] + 0.01 and norm(w["w"]).startswith(norm(word)):
            c += 1
            if c == n: return w["t0"] - s0
    return 0.0

@functools.lru_cache(256)
def pcard(name, ovr, pos, stats, w=420, prom=False, av="sil"):
    a = silhouette() if av in ("sil", "levi") else cut(av, 900)
    return C.make_card(a, name, ovr, pos, list(stats), w=w, promessa=prom, crest="POR.png")

@functools.lru_cache(8)
def tee(m, k): return thiago(760, m, k / 10)

def bubble(user, text, likes, w=900):
    h = 260; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), 36, fill=(255, 255, 255, 250), outline=INK, width=5)
    d.ellipse((30, 40, 120, 130), fill=(120, 120, 135)); d.ellipse((58, 55, 92, 89), fill=(200, 200, 210)); d.chord((40, 88, 110, 150), 180, 360, fill=(200, 200, 210))
    d.text((145, 40), user, font=font("bd", 50), fill=(110, 110, 120))
    d.text((145, 115), text, font=font("blk", 66), fill=INK)
    d.text((w - 90, 70), "♥", font=font("blk", 80), fill=RED, anchor="mm"); d.text((w - 90, 150), likes, font=font("bd", 36), fill=(90, 90, 100), anchor="mm")
    return im

def s0(img, t, T):  # Peguei a Portuguesa na Série D... meta Libertadores
    cover(img, "libertadores", t, 150 if t < wt(0, "libertadores") - 0.3 else 70)
    img.alpha_composite(rays(W, H, cx, 640, T, (255, 120, 120), 14, 40))
    if t < wt(0, "libertadores") - 0.3: paste(img, trophy(300), cx, 1360, 0.35)
    paste(img, logo("POR", 330), cx, 520, 1, 1.0 + 0.25 * max(0, 1 - t / 0.18) + 0.03 * math.sin(T * 5))
    paste(img, txt("SÉRIE D", 150, WHITE, 12), cx, 830, 1, 1.0 + 0.08 * max(0, 1 - t / 0.2), -3)
    ta = wt(0, "libertadores") - 0.3
    if t < ta: paste(img, txt("↓", 120, AMB), cx, 980, 1, 1 + 0.1 * math.sin(T * 10))
    paste(img, txt("LIBERTADORES", 120 if t > ta else 95, AMB if t > ta else WHITE, 12), cx, 1130, 1, 1.0 + (0.25 * max(0, 1 - (t - ta) / 0.2) if t > ta else 0), -3)
    if t > ta:
        pop(img, trophy(260), 880, 1330, t, ta, 0.3)
        img.alpha_composite(confetti(W, H, t - ta))

def s1(img, t, T):  # você decide, A ou B
    pop(img, txt("QUEM DECIDE", 110), cx, 450, t, 0.0)
    pop(img, txt("É VOCÊ!", 190, AMB, 14), cx, 640, t, wt(1, "você") - 0.1, 0.25)
    te = wt(1, "escolha") - 0.2
    if t > te:
        pop(img, chip("A", 190, WHITE, RED), 330, 1000, t, te, 0.25); pop(img, chip("B", 190, WHITE, GREEN), 750, 1000, t, te + 0.15, 0.25)
        tv = wt(1, "votada") - 0.2
        if t > tv:
            u = ease((t - tv) / 1.0); d = ImageDraw.Draw(img)
            d.rounded_rectangle((140, 1230, 940, 1290), 30, fill=(255, 255, 255, 60))
            d.rounded_rectangle((140, 1230, 140 + 800 * 0.63 * u, 1290), 30, fill=RED)
            paste(img, txt(f"{int(63 * u)}%", 60), 140 + 800 * 0.63 * u, 1190, 1)
            pop(img, stamp("ACONTECE!", 90, AMB), cx, 1400, t, tv + 1.0, 0.25, -5)

def s2(img, t, T):  # comentário mais curtido vira personagem
    pop(img, chip("COMENTÁRIO MAIS CURTIDO", 58, INK, AMB), cx, 380, t, 0.0, 0.25, -2)
    paste(img, bubble("@voce_aqui", "Bota eu na Lusa!", "12,4 mil", 1000), cx, 590, 1 if t > 0.2 else 0, 0.85 + 0.15 * back((t - 0.2) / 0.3) if t > 0.2 else 1)
    tf = wt(2, "fica") - 0.1
    pop(img, stamp("PRA SEMPRE", 90, RED), cx, 790, t, tf, 0.25, -5)
    roles = [("jogador", "JOGADOR DA BASE", 230), ("torcedor", "TORCEDOR", 540), ("técnico", "TÉCNICO RIVAL", 850)]
    for k, (wd, lab, x) in enumerate(roles):
        t0 = wt(2, wd) - 0.15
        if t < t0: continue
        if k == 0: el = pcard("VOCÊ?", 50, "MEI", (60, 50, 55, 58, 30, 45), 230, True)
        elif k == 1: el = cut("fan", 340)
        else: el = cut("rival", 340)
        pop(img, el, x, 1100, t, t0, 0.3); pop(img, chip(lab, 40, INK, WHITE), x, 1330, t, t0 + 0.1)

def s3(img, t, T):  # cartas subindo jogo a jogo
    pop(img, chip("JOGADORES REAIS", 60, INK, WHITE), cx, 380, t, 0.0)
    pop(img, chip("GAROTOS DA BASE", 60, INK, AMB), cx, 480, t, wt(3, "garotos") - 0.1)
    tc = wt(3, "carta") - 0.2
    if t > tc:
        o = int(52 + 38 * ease((t - tc) / 1.8)); o = min(90, o)
        paste(img, pcard("DAVI", o, "MEI", (66, 48, 60, 62, 25, 40), 470, False, "davi"), cx, 1000, 1, 0.9 + 0.1 * back((t - tc) / 0.3))
        if o >= 75: img.alpha_composite(rays(W, H, cx, 1000, T, (255, 220, 120), 14, 50))
        paste(img, chip(f"+{o - 52}", 80, INK, GREEN), 860, 760, 1)

def newspaper2(w, top, head, sub):
    h = int(w * 0.62); im = Image.new("RGBA", (w, h), (238, 226, 200, 255)); d = ImageDraw.Draw(im)
    d.text((w / 2, h * 0.1), top, font=font("blk", w * 0.07), fill=INK, anchor="mm"); d.line((30, h * 0.18, w - 30, h * 0.18), fill=INK, width=4)
    d.text((w / 2, h * 0.42), head, font=font("blk", w * 0.1), fill=INK, anchor="mm"); d.text((w / 2, h * 0.6), sub, font=font("sb", w * 0.045), fill=(70, 70, 70), anchor="mm")
    for k in range(3): d.line((40, h * 0.72 + k * 28, w - 40, h * 0.72 + k * 28), fill=(180, 175, 165), width=10)
    return im

def s4(img, t, T):  # história: vice 96, tapetão 2013, queda, eliminada, sem casa
    t1, t2, t3, t4, t5 = wt(4, "caiu") - 0.2, wt(4, "caindo") - 0.3, wt(4, "eliminada") - 0.2, wt(4, "sem") - 0.2, wt(4, "canindé") - 0.3
    if t < t1:
        cover(img, "vice96", t, 110)
        paste(img, newspaper2(860, "DIÁRIO DA LUSA • 1996", "VICE DO BRASIL!", "Portuguesa 2 x 0 Grêmio na ida da final"), cx, 720, 1, 0.9 + 0.1 * ease(t / 0.4), -3 + 2 * ease(t / 0.4))
        pop(img, txt("1996", 150, AMB), cx, 1150, t, 0.4)
    elif t < t2:
        u = t - t1; cover(img, "tapetao", u, 80)
        paste(img, txt("2013", 170, WHITE), cx, 560, 1)
        pop(img, chip("SÉRIE A", 80, INK, WHITE), cx, 780, u, 0.0)
        pop(img, stamp("TAPETÃO", 140, RED), cx, 980, u, 0.5, 0.2, -8)
    elif t < t3:
        u = t - t2
        for k, dv in enumerate("ABCD"):
            x = 230 + k * 210; y = 520 + k * 210
            if u > k * 0.35: pop(img, chip(f"SÉRIE {dv}", 54, WHITE if dv == "D" else INK, RED if dv == "D" else WHITE), x, y, u, k * 0.35, 0.2)
        if u > 0.2: paste(img, logo("POR", 150), 230 + min(3, u / 0.35) * 210, 400 + min(3, u / 0.35) * 210, 1)
    elif t < t4:
        u = t - t3; pop(img, txt("2026", 150, WHITE), cx, 560, u, 0.0)
        pop(img, stamp("ELIMINADA", 130, RED), cx, 800, u, 0.3, 0.2, -6)
    else:
        u = t - t4
        ph = CAN.resize((int(CAN.width * 1250 / CAN.height), 1250))
        z = 1.0 + 0.04 * u; ph2 = ph.resize((int(ph.width * z), int(ph.height * z)))
        paste(img, ph2, cx + 300 - 120 * u, 900, 1)
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(min(150, 60 + 40 * u)))))
        pop(img, txt("SEM CASA", 140, WHITE), cx, 470, u, 0.0)
        if t > t5 + 0.8: cover(img, "obras", t - t5, 70)
        if t > t5:
            v = t - t5
            for k, yy in enumerate((760, 900)):
                paste(img, chip("EM OBRAS  •  EM OBRAS  •  EM OBRAS", 54, INK, AMB), cx, yy, 1, 1.0, (-8 if k else 6) * ease(v / 0.3))

def s5(img, t, T):  # Thiago Teh
    m = "open" if (t % 0.9) < 0.6 else "smile"
    tr = wt(5, "imprensa") - 0.3
    if t > tr: cover(img, "tee_press", t - tr, 40)
    else: paste(img, cut("tee", 900), cx, 1050, 1, 0.85 + 0.15 * back(t / 0.35))
    pop(img, chip("THIAGO TEH", 90, INK, AMB), cx, 380, t, wt(5, "thiago") - 0.1, 0.25, -3)
    for k, (wd, lab, x, y) in enumerate([("careca", "CARECA", 220, 560), ("gordinho", "GORDINHO", 860, 600), ("treinador", "TÉCNICO DE VÁRZEA", cx, 520)]):
        if wd == "treinador":
            pop(img, chip(lab, 52, WHITE, GREEN), cx, 680, t, wt(5, wd) - 0.1, 0.25, 3)
        else: pop(img, chip(lab, 72, WHITE, RED), x, y, t, wt(5, wd) - 0.1, 0.25, -6 if k else 6)
    if t > tr:
        u = t - tr
        if int(u * 8) % 3 == 0: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 70)))
        for k, (x, y, r) in enumerate([(220, 860, -12), (860, 820, 10), (240, 1380, 8), (850, 1420, -8)]):
            pop(img, txt("HAHA", 70, AMB), x, y, u, k * 0.18, 0.2, r)

def s6(img, t, T):  # elenco real
    pop(img, chip("O ELENCO", 70, INK, WHITE), cx, 380, t, 0.0)
    cards = [("jonas", ("JONAS TORÓ", 65, "PE", (80, 62, 66, 72, 30, 58)), 270, 760, "EX-SÃO PAULO"),
             ("cadorini", ("CADORINI", 63, "ATA", (70, 66, 48, 58, 28, 70)), 810, 760, "ARTILHEIRO"),
             ("romarinho", ("ROMARINHO", 64, "ATA", (62, 68, 66, 70, 30, 55)), cx, 1180, "EX-CORINTHIANS")]
    for wd, (n, o, p, st), x, y, lab in cards:
        t0 = wt(6, wd) - 0.25
        slide(img, pcard(n, o, p, st, 330), x, y, t, t0, 500 if x > cx else -500, 0.3)
        pop(img, chip(lab, 38, INK, AMB), x, y + 260, t, t0 + 0.2)

def s7(img, t, T):  # Davi, base, potencial 90
    tdav, tpot = wt(7, "davi") - 0.2, wt(7, "potencial") - 0.1
    if t < tdav:
        cover(img, "davi_stadium", t, 70)
        pop(img, txt("O SEGREDO", 120, WHITE), cx, 640, t, 0.0); pop(img, txt("TÁ NA BASE", 140, AMB), cx, 820, t, 0.6)
        return
    u = t - tdav
    paste(img, cut("davi", 720), 290, 940, 1, 0.9 + 0.1 * back(u / 0.3))
    pop(img, chip("DAVI • 16 ANOS", 60, INK, AMB), 300, 1260, u, 0.1)
    pop(img, chip("FILHO DO PORTEIRO DO CANINDÉ", 44, INK, WHITE), cx, 420, t, wt(7, "filho") - 0.1)
    paste(img, pcard("DAVI", 52, "MEI", (66, 48, 60, 62, 25, 40), 360, True, "davi"), 800, 860, 1 if t > wt(7, "overall") - 0.2 else 0)
    if t > tpot:
        v = t - tpot; img.alpha_composite(rays(W, H, 800, 1250, T, (255, 220, 120), 16, 70))
        paste(img, chip("POT 90", 110, INK, GOLD), 800, 1250, 1, 0.6 + 0.4 * back(v / 0.3), -4)
        img.alpha_composite(confetti(W, H, v))

def s8(img, t, T):  # A Carlão x B Levi
    ta, tb = wt(8, "carlão") - 0.4, wt(8, "levi") - 0.4
    if t < ta:
        cover(img, "cofre", t, 80)
        pop(img, stamp("1º PROBLEMA", 120, RED), cx, 600, t, 0.0, 0.25, -6)
        pop(img, chip("SAF: SÓ 1 REFORÇO", 70, INK, AMB), cx, 900, t, 1.2)
        return
    pop(img, pcard("CARLÃO", 66, "ATA", (52, 72, 55, 58, 35, 78), 360), 280, 760, t, ta, 0.3)
    pop(img, chip("A", 110, WHITE, RED), 280, 420, t, ta)
    for k, (wd, lab) in enumerate([("trinta", "34 ANOS"), ("artilheiro", "ARTILHEIRO"), ("graça", "DE GRAÇA"), ("salário", "SALÁRIO ALTO")]):
        pop(img, chip(lab, 48, WHITE if lab == "SALÁRIO ALTO" else INK, RED if lab == "SALÁRIO ALTO" else WHITE), 280, 1090 + k * 90, t, wt(8, wd) - 0.1)
    if t > tb:
        pop(img, pcard("LEVI SANTOS", 60, "MEI", (72, 58, 62, 68, 30, 50), 360, False, "levi"), 800, 760, t, tb, 0.3)
        pop(img, chip("B", 110, WHITE, GREEN), 800, 420, t, tb)
        for k, (wd, lab) in enumerate([("dezenove", "19 ANOS"), ("joia", "JOIA DO RIO BRANCO"), ("empréstimo", "EMPRÉSTIMO")]):
            pop(img, chip(lab, 42, INK, AMB if k == 1 else WHITE), 800, 1090 + k * 90, t, wt(8, wd) - 0.1)

def s9(img, t, T):  # CTA
    cover(img, "tee_shout", t, 165)
    pop(img, txt("GOL AGORA", 100, RED), cx, 430, t, 0.0); pop(img, txt("OU FUTURO?", 100, GREEN), cx, 550, t, wt(9, "aposta") - 0.1)
    pop(img, chip("A  CARLÃO", 80, WHITE, RED), cx, 760, t, wt(9, "comenta") - 0.1, 0.25, -3)
    pop(img, chip("B  LEVI", 80, WHITE, GREEN), cx, 890, t, wt(9, "comenta") + 0.15, 0.25, 3)
    tm = wt(9, "mais") - 0.2
    if t > tm:
        paste(img, bubble("@voce_aqui", "Seu comentário aqui", "TOP 1", 1000), cx, 1130, 1, 0.85 + 0.15 * back((t - tm) / 0.3))
        pop(img, chip("ENTRA NO EP.2", 64, INK, AMB), cx, 1330, t, tm + 0.6, 0.25, -3)
    paste(img, logo("POR", 120), 960, 380, 1)

SH = Short(D, [(s,) for s in TXT], [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9], "MODO CARREIRA • LUSA • EP.1",
           ["red", "green", "night", "dark", "sepia", "red", "dark", "night", "dark", "green"], "Five_Armies", 0)
S = SH
if __name__ == "__main__":
    ev = [("tambor_impacto", 0.0, 0.5), ("whoosh_boom", SH.segs[0][0] + 2.5, 0.3), ("torcida_comemora", SH.segs[0][0] + 3.0, 0.15),
          ("tambor_impacto", SH.segs[4][0] + 3.2, 0.3), ("torcida_aww", SH.segs[4][0] + 7.0, 0.2), ("camera_click", SH.segs[5][0] + 4.6, 0.3),
          ("torcida_comemora", SH.segs[7][0] + 6.3, 0.2), ("tambor_impacto", SH.segs[8][0], 0.35)]
    main(SH, extra=ev)
