"""Episódio 1 — Modo Carreira Cambridge United (1920x1080, 30 fps).
Uso: python3 make_ep1.py preview t1 t2 ...   |   python3 make_ep1.py render i n"""
import os, sys, json, math, random, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
sys.path.insert(0, "/home/claude/carreira")
import card as C
import lances as L

W, H, FPS = 1920, 1080, 30
D = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(D, "img")
A = "/home/claude/carreira/assets"
FD = "/usr/share/fonts/opentype/inter/"
AMB = (246, 178, 40); WHITE = (255, 255, 255); BG = (14, 14, 16); RED = (230, 60, 60); GREEN = (70, 200, 110)
CUES = json.load(open(os.path.join(D, "cues.json")))
TOTAL = CUES["total"]


@functools.lru_cache(None)
def font(name, size):
    return ImageFont.truetype(FD + {"blk": "InterDisplay-Black.otf", "xb": "InterDisplay-ExtraBold.otf", "bd": "InterDisplay-Bold.otf",
                                   "sb": "Inter-SemiBold.otf", "md": "InterDisplay-Medium.otf"}[name], size)


def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def clamp(u, a=0, b=1): return max(a, min(b, u))


# ---------- shots: cenas consecutivas iguais viram um plano ----------
SHOTS = []
for c in CUES["cues"]:
    if SHOTS and SHOTS[-1]["scene"] == c["scene"]:
        SHOTS[-1]["cues"].append(c)
    else:
        SHOTS.append({"scene": c["scene"], "cues": [c]})
for i, s in enumerate(SHOTS):
    s["t0"] = 0 if i == 0 else s["cues"][0]["t0"] - 0.35
    s["t1"] = SHOTS[i + 1]["cues"][0]["t0"] - 0.35 if i + 1 < len(SHOTS) else TOTAL


# ---------- utilidades visuais ----------
@functools.lru_cache(None)
def load(name, flash=False):
    p = os.path.join(IMG, name + ".jpg")
    im = Image.open(p).convert("RGB")
    if flash:
        g = ImageOps.grayscale(im); im = ImageOps.colorize(g, (40, 26, 14), (250, 226, 180))
    return im


def kenburns(im, t, dur, z0=1.0, z1=1.12, dx=0.0, dy=-0.04):
    """quadrado 1024 -> 16:9 com zoom lento"""
    u = clamp(t / max(dur, 0.1)); z = z0 + (z1 - z0) * u
    sw = im.width / z; sh = sw * 9 / 16
    cx = im.width / 2 + dx * im.width * u; cy = im.height / 2 + dy * im.height * u
    box = (cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2)
    return im.resize((W, H), Image.BICUBIC, box=box).convert("RGBA")


@functools.lru_cache(None)
def vignette():
    v = Image.new("L", (W, H), 0); d = ImageDraw.Draw(v)
    d.ellipse((-W * 0.15, -H * 0.25, W * 1.15, H * 1.25), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255)); out.putalpha(ImageOps.invert(v).point(lambda a: int(a * 0.85)))
    return out


GRAIN = [Image.fromarray((np.random.RandomState(i).rand(H // 2, W // 2) * 60).astype(np.uint8)).resize((W, H)) for i in range(6)]


def film(img, t):
    g = GRAIN[int(t * 12) % 6]
    layer = Image.new("RGBA", (W, H), (255, 240, 220, 0)); layer.putalpha(g.point(lambda a: a // 3))
    img.alpha_composite(layer); img.alpha_composite(vignette())
    return img


def txt(img, xy, s, f, fill=WHITE, anchor="la", shadow=True, alpha=1.0):
    d = ImageDraw.Draw(img)
    a = int(255 * alpha)
    if shadow:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text((xy[0] + 3, xy[1] + 4), s, font=f, fill=(0, 0, 0, int(170 * alpha)), anchor=anchor)
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
    d.text(xy, s, font=f, fill=fill + (a,) if len(fill) == 3 else fill, anchor=anchor)


def panel(w, h, col=(18, 18, 20, 225), r=26, border=(255, 255, 255, 38)):
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(p).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=col, outline=border, width=2)
    return p


def paste(img, el, x, y, alpha=1.0, scale=1.0, center=True):
    if scale != 1.0:
        el = el.resize((max(1, int(el.width * scale)), max(1, int(el.height * scale))), Image.LANCZOS)
    if alpha < 1:
        el = el.copy(); el.putalpha(el.getchannel("A").point(lambda a: int(a * alpha)))
    if center: x, y = x - el.width / 2, y - el.height / 2
    img.alpha_composite(el, (int(x), int(y)))


def chip(s, f, fg=BG, bg=AMB, pad=(26, 12)):
    tw = f.getbbox(s)
    w, h = tw[2] - tw[0] + pad[0] * 2, tw[3] - tw[1] + pad[1] * 2
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=bg)
    d.text((pad[0] - tw[0], pad[1] - tw[1]), s, font=f, fill=fg)
    return c


def year_tag(img, t, s, sub=None):
    a = ease(t / 0.5)
    c = chip(s, font("blk", 46))
    paste(img, c, 90 + c.width / 2 - 40 * (1 - a), 110, a)
    if sub: txt(img, (90, 160), sub, font("sb", 34), (235, 235, 235), alpha=a)


# ---------- cartas ----------
SIL = None
def silhouette():
    global SIL
    if SIL is None:
        im = Image.new("RGBA", (600, 600), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((210, 90, 390, 290), fill=(30, 30, 34, 255)); d.rounded_rectangle((110, 300, 490, 640), 120, fill=(30, 30, 34, 255))
        SIL = im
    return SIL


REAL = [("Jake Eastwood", "GOL", 64, [65, 60, 62, 66, 45, 63]), ("Liam Bennett", "LD", 63, [72, 45, 60, 62, 62, 66]),
        ("Patrick Bauer", "ZAG", 66, [48, 38, 52, 46, 68, 78]), ("Kelland Watts", "ZAG", 65, [60, 35, 55, 52, 66, 72]),
        ("Pelly R. Mpanzu", "VOL", 64, [62, 52, 63, 64, 62, 70]), ("Dominic Ball", "VOL", 63, [58, 45, 64, 60, 63, 66]),
        ("Ben Knight", "MEI", 65, [70, 62, 66, 70, 35, 55]), ("Sullay Kaikai", "PD", 66, [80, 64, 63, 72, 30, 60]),
        ("Shayne Lavery", "ATA", 64, [72, 66, 52, 63, 30, 66]), ("Louis Appéré", "ATA", 63, [66, 64, 55, 62, 32, 68])]


@functools.lru_cache(None)
def real_card(i, w=300):
    n, p, o, s = REAL[i]
    return C.make_card(silhouette(), n, o, p, s, w=w)


@functools.lru_cache(None)
def face_card(key, name, ovr, pos, stats, w=420, promessa=False):
    src = os.path.join(A, key + "_ai.png") if os.path.exists(os.path.join(A, key + "_ai.png")) else os.path.join(IMG, key + ".png")
    av = C.clean_avatar(src) if src.endswith("_ai.png") else Image.open(src).convert("RGBA").crop(Image.open(src).getchannel("A").getbbox())
    return C.make_card(av, name, ovr, pos, list(stats), w=w, promessa=promessa)


@functools.lru_cache(None)
def avatar(key, h=760):
    im = C.clean_avatar(os.path.join(A, key + "_ai.png"))
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def bg_dark(t, glow=AMB):
    img = Image.new("RGBA", (W, H), BG + (255,))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((W * 0.2, -H * 0.5, W * 0.8, H * 0.7), fill=glow + (60,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(180)))
    crest = Image.open(os.path.join(A, "cambridge_united.png")).convert("RGBA").resize((900, 900))
    crest.putalpha(crest.getchannel("A").point(lambda a: a // 22))
    img.alpha_composite(crest, (W - 760, 200 + int(10 * math.sin(t * 0.4))))
    return img


@functools.lru_cache(None)
def bg_dark_c():
    return bg_dark(0)


# ---------- tabela ----------
TEAMS = ["Accrington", "Barnet", "Bristol Rovers", "Bromley", "Chesterfield", "Colchester", "Crawley", "Crewe", "Exeter", "Fleetwood",
         "Gillingham", "Grimsby", "Newport", "Northampton", "Oldham", "Port Vale", "Rochdale", "Rotherham", "Salford", "Shrewsbury",
         "Swindon", "Tranmere", "Walsall"]


def table(img, t, pos_from, pos_to, title, x=980, y=110):
    rows = 11
    u = ease((t - 0.8) / 2.5)
    pos = pos_from + (pos_to - pos_from) * u
    rng = random.Random(7); others = TEAMS[:]; rng.shuffle(others)
    off = max(1.0, min(24 - rows + 1.0, pos - rows // 2))
    p = panel(820, 70 + rows * 58); d = ImageDraw.Draw(p)
    body = Image.new("RGBA", (820, rows * 58), (0, 0, 0, 0)); bd = ImageDraw.Draw(body)
    for place in range(int(off), int(off) + rows + 2):
        if place > 24: break
        yy = (place - off) * 58
        if abs(place - pos) < 0.5: continue
        bd.text((30, yy + 12), f"{place}", font=font("bd", 30), fill=(170, 170, 170))
        bd.text((100, yy + 12), others[(place * 3) % 23], font=font("sb", 30), fill=(225, 225, 225))
    cy = (pos - off) * 58
    bd.rounded_rectangle((14, cy + 4, 806, cy + 54), 14, fill=AMB)
    bd.text((30, cy + 12), f"{round(pos)}", font=font("blk", 30), fill=BG)
    bd.text((100, cy + 12), "Cambridge United", font=font("blk", 30), fill=BG)
    p.alpha_composite(body, (0, 70))
    d.text((30, 22), title, font=font("blk", 32), fill=AMB)
    paste(img, p, x, y, ease(t / 0.4), center=False)


# ---------- legendas ----------
def caption(img, t):
    for c in CUES["cues"]:
        if c["t0"] - 0.05 <= t <= c["t1"] + 0.25:
            s = c["text"]; f = font("sb", 40)
            words = s.split(); lines = [""]
            for w_ in words:
                if f.getlength(lines[-1] + " " + w_) > 1500: lines.append(w_)
                else: lines[-1] = (lines[-1] + " " + w_).strip()
            if len(lines) > 2:  # mostra a metade certa da frase
                half = (c["t0"] + c["t1"]) / 2; n = len(lines)
                lines = lines[:2] if t < half else lines[2:4] if n > 2 else lines
            hgt = 58 * len(lines) + 28
            bw = max(f.getlength(l) for l in lines) + 70
            p = panel(int(bw), hgt, (10, 10, 12, 190), 18, (0, 0, 0, 0))
            for i, l in enumerate(lines):
                ImageDraw.Draw(p).text((bw / 2, 14 + i * 58), l, font=f, fill=WHITE, anchor="ma")
            paste(img, p, W / 2, H - 70 - hgt / 2)
            return


# ---------- lances com sobreposições ----------
def lance(fn, t, dur, bug=None, flash_at=None, flash_txt=None, flash_col=AMB, sub=None):
    im, labs = L.render(fn, t, dur)
    d = ImageDraw.Draw(im)
    for s, pr, a, b, col in labs:
        if pr and a < t < b:
            v = ease((t - a) / 0.25) * (1 - ease((t - b + 0.25) / 0.25))
            c = chip(s, font("blk", 30), BG if col != WHITE else BG, col)
            paste(im, c, pr[0], pr[1] - 50, v)
            d.line((pr[0], pr[1] - 30, pr[0], pr[1] + 4), fill=(255, 255, 255, int(170 * v)), width=3)
    if bug:
        p = panel(760, 96, (12, 12, 14, 230), 48)
        ImageDraw.Draw(p).text((380, 48), bug, font=font("blk", 40), fill=WHITE, anchor="mm")
        paste(im, p, W / 2, 90)
    if sub:
        paste(im, chip(sub, font("bd", 30), WHITE, (40, 40, 44)), W / 2, 165)
    if flash_at is not None and t > flash_at:
        u = t - flash_at
        if u < 0.25:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(160 * (1 - u / 0.25)))); im.alpha_composite(fl)
        f = font("blk", 150); a = ease(u / 0.35)
        txt(im, (W / 2, H / 2 - 60), flash_txt, f, flash_col, "mm", alpha=a)
    return im


# ---------- cenas ----------
def scene(sc, t, dur, shot):
    if sc == "crewe":
        im = lance(L.ambient, t + 3, dur, "CREWE  0  x  0  CAMBRIDGE")
        clock = 92 + min(0.99, t / dur)
        m = 92; s_ = int((t / dur) * 59)
        paste(im, chip(f"{m}:{s_:02d}", font("blk", 38), WHITE, RED), W / 2, 168)
        paste(im, chip("ÚLTIMA RODADA • 2/5/2026", font("bd", 28), BG, AMB), W / 2, 230)
        return im
    if sc == "crewe_goal":
        tg = min(4.2, dur * 0.55)
        im = lance(L.crewe, t, dur, "CREWE  0  x  0  CAMBRIDGE" if t < tg + 0.35 else "CREWE  1  x  0  CAMBRIDGE", tg + 0.35, "GOL DO CREWE • 93'", RED)
        return im
    if sc == "fall":
        im = kenburns(load("fall"), t, dur)
        paste(im, chip("PLAY-OFF: ELIMINADO", font("blk", 46), WHITE, RED), W / 2, 130, ease(t / 0.5))
        return im
    if sc == "ourversion":
        im = bg_dark(t)
        a = ease(t / 0.6)
        txt(im, (W / 2, 330), "NA VIDA REAL", font("bd", 48), (190, 190, 190), "mm", alpha=a)
        txt(im, (W / 2, 410), "o Cambridge subiu para a 3ª divisão", font("md", 44), WHITE, "mm", alpha=a)
        b = ease((t - 1.6) / 0.6)
        txt(im, (W / 2, 590), "NA NOSSA VERSÃO", font("blk", 64), AMB, "mm", alpha=b)
        txt(im, (W / 2, 680), "ele ficou na 4ª divisão", font("bd", 52), WHITE, "mm", alpha=b)
        return im
    if sc == "bus":
        im = kenburns(load("bus"), t, dur, 1.05, 1.15, 0.03, 0)
        if shot["cues"][0]["i"] > 20: year_tag(im, t, "2015 – 2026", "motorista de dia, técnico do sub-16 à noite")
        return im
    if sc == "title":
        im = bg_dark(t)
        cr = Image.open(os.path.join(A, "cambridge_united.png")).convert("RGBA")
        paste(im, cr, W / 2, 330, ease(t / 0.6), 0.55 + 0.05 * ease(t / 0.6))
        txt(im, (W / 2, 610), "MODO CARREIRA", font("blk", 120), WHITE, "mm", alpha=ease((t - 0.4) / 0.5))
        txt(im, (W / 2, 720), "DA 4ª DIVISÃO À CHAMPIONS LEAGUE", font("xb", 54), AMB, "mm", alpha=ease((t - 0.9) / 0.5))
        paste(im, chip("EPISÓDIO 1 • O MOTORISTA DE ÔNIBUS", font("bd", 34), BG, WHITE), W / 2, 830, ease((t - 1.4) / 0.5))
        return im
    if sc in ("h1912", "h1990", "h1992", "h2005"):
        key = {"h1992": "h1990"}.get(sc, sc)
        im = kenburns(load(key, sc == "h1912"), t, dur, 1.0, 1.1)
        if sc == "h1912": im = film(im, t)
        # linha do tempo
        years = ["1912", "1970", "1990", "1992", "2005", "2014"]
        cur = {"h1912": [0, 1], "h1990": [2], "h1992": [3], "h2005": [4, 5]}[sc]
        bar = panel(1500, 90, (12, 12, 14, 215), 45)
        dd = ImageDraw.Draw(bar)
        for i, y in enumerate(years):
            x = 125 + i * 250
            on = i in cur and (i == cur[0] or t > dur * 0.5)
            dd.ellipse((x - 12, 33, x + 12, 57), fill=AMB if on else (90, 90, 90))
            dd.text((x + 22, 45), y, font=font("blk" if on else "bd", 32), fill=AMB if on else (170, 170, 170), anchor="lm")
        paste(im, bar, W / 2, 95)
        big = {"h1912": ("ABBEY UNITED", "fundado em 1912 • profissional em 1970"),
               "h1990": ("A ERA DE OURO", "acesso em Wembley • 2x quartas da FA Cup • campeão da 3ª"),
               "h1992": ("A UM PLAY-OFF DA PREMIER LEAGUE", "1992 • o quase que nunca saiu da cidade"),
               "h2005": ("FORA DA LIGA", "administração • estádio vendido • 9 anos para voltar")}[sc]
        a = ease((t - 0.5) / 0.5)
        txt(im, (W / 2, 700), big[0], font("blk", 82), WHITE, "mm", alpha=a)
        txt(im, (W / 2, 780), big[1], font("sb", 38), AMB, "mm", alpha=a)
        return im
    if sc in ("kitchen", "kitman", "promise", "injury"):
        flash = sc != "injury"
        im = kenburns(load(sc, flash), t, dur, 1.0, 1.1)
        im = film(im, t) if flash else im
        tag = {"kitchen": ("FLASHBACK • 2000", "Rick, 8 anos"), "kitman": ("FLASHBACK • 1992", "o pai, roupeiro do Abbey Stadium"),
               "promise": ("FLASHBACK • 2005", "Rick, 13 anos"), "injury": ("2011", "Rick, 19 anos • a estreia que virou fim")}[sc]
        if shot["cues"][0]["i"] == 18: tag = ("FLASHBACK • 1992", "nasce Rick Miguel")
        year_tag(im, t, *tag)
        return im
    if sc in ("notebook", "phone", "banner", "bike", "race", "gaming", "bench", "hug", "offer", "whiteboard"):
        im = kenburns(load(sc), t, dur, 1.0, 1.1)
        if sc == "phone": year_tag(im, t, "JULHO • 2026", "a ligação da diretoria")
        if sc == "whiteboard":
            # escrita na lousa
            s = "CHAMPIONS LEAGUE"; n = int(len(s) * clamp((t - 1.0) / 1.8))
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((W * 0.5 + 40, H * 0.43), s[:n], font=font("blk", 92), fill=(20, 40, 160, 235), anchor="mm")
            im.alpha_composite(lay.rotate(-2, center=(W / 2, H / 2)))
            paste(im, chip("A META DO RICK", font("blk", 40)), W / 2, 110, ease(t / 0.5))
        if sc == "banner":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((W * 0.5 + 20, H * 0.43), "WE WANT A REAL MANAGER", font=font("blk", 62), fill=(20, 20, 20, 230), anchor="mm")
            im.alpha_composite(lay.rotate(3, center=(W / 2, H / 2)))
            paste(im, chip("\"QUEREMOS UM TÉCNICO DE VERDADE\"", font("bd", 34), WHITE, RED), W / 2, 110, ease(t / 0.5))
        if sc == "race": paste(im, chip("VENCEU POR 5 METROS • DE CHINELO", font("blk", 40)), W / 2, 110, ease((t - 2) / 0.5))
        if sc == "gaming": paste(im, chip("FALTOU AO TREINO", font("blk", 40), WHITE, RED), W / 2, 110, ease(t / 0.5))
        if sc == "bench": paste(im, chip("NO BANCO", font("blk", 40), WHITE, RED), W / 2, 110, ease(t / 0.5))
        if sc == "hug": paste(im, chip("PRIMEIRO GOL PROFISSIONAL", font("blk", 44)), W / 2, 110, ease(t / 0.5))
        if sc == "offer":
            if t > 2.0:
                a = ease((t - 2.0) / 0.5)
                p = panel(860, 300, (250, 250, 250, 245), 24, (0, 0, 0, 0)); dd = ImageDraw.Draw(p)
                dd.text((40, 34), "De: clube da Premier League", font=font("sb", 30), fill=(90, 90, 90))
                dd.text((40, 84), "Assunto: proposta por Murrey", font=font("bd", 36), fill=(20, 20, 20))
                dd.text((40, 160), "£1.200.000", font=font("blk", 84), fill=(20, 120, 60))
                paste(im, p, W / 2, H / 2 + 20 * (1 - a), a)
            if t > 7.5: paste(im, chip("≈ 7x O ORÇAMENTO DO CLUBE", font("blk", 40), WHITE, RED), W / 2, 110, ease((t - 7.5) / 0.5))
        return im
    if sc == "rickcard":
        im = bg_dark(t)
        av = avatar("rick", 820)
        paste(im, av, 560, H - av.height / 2 + 30 * (1 - ease(t / 0.6)), ease(t / 0.5))
        a = ease((t - 0.5) / 0.5)
        txt(im, (1040, 380), "RICK MIGUEL", font("blk", 110), WHITE, alpha=a)
        txt(im, (1046, 520), "TÉCNICO INTERINO • 34 ANOS", font("bd", 44), AMB, alpha=a)
        txt(im, (1046, 590), "ex-motorista da linha 3", font("md", 40), (210, 210, 210), alpha=a)
        paste(im, chip("+ O CADERNO", font("blk", 40)), 1180, 700, ease((t - 1.5) / 0.5))
        return im
    if sc == "budget":
        im = bg_dark(t)
        txt(im, (120, 110), "SITUAÇÃO DO CLUBE • JULHO 2026", font("blk", 56), WHITE, alpha=ease(t / 0.4))
        items = [("ORÇAMENTO PARA CONTRATAR", "£180.000", AMB), ("FOLHA SALARIAL", "3ª MENOR DA LIGA", WHITE),
                 ("META DA DIRETORIA", "MEIO DA TABELA", WHITE), ("MORAL", "BAIXA", RED)]
        for i, (k, v, col) in enumerate(items):
            a = ease((t - 0.6 - i * 0.9) / 0.5)
            p = panel(800, 200); dd = ImageDraw.Draw(p)
            dd.text((40, 36), k, font=font("bd", 32), fill=(180, 180, 180)); dd.text((40, 92), v, font=font("blk", 66), fill=col)
            paste(im, p, 120 + (i % 2) * 860, 260 + (i // 2) * 260 + 30 * (1 - a), a, center=False)
        return im
    if sc.startswith("squad"):
        im = bg_dark(t)
        txt(im, (W / 2, 80), "ELENCO • CAMBRIDGE UNITED", font("blk", 52), WHITE, "mm")
        focus = {"squad_kaikai": 7, "squad_bauer": 2, "squad_pelly": 4}.get(sc)
        for i in range(len(REAL)):
            a = ease((t - i * 0.12) / 0.4) if sc == "squad" and shot["cues"][0]["i"] == 32 else 1
            c = real_card(i, 260)
            x = 140 + (i % 5) * 330 + 130; y = 340 + (i // 5) * 400
            dim = focus is not None and i != focus
            if dim:
                c = c.copy(); c.putalpha(c.getchannel("A").point(lambda v: v // 4))
            paste(im, c, x, y, a)
        if focus is not None:
            c = real_card(focus, 420)
            paste(im, c, W / 2, H / 2 + 40, ease(t / 0.4), 0.9 + 0.1 * ease(t / 0.4))
        if sc == "squad" and shot["cues"][0]["i"] == 36:
            paste(im, chip("ELENCO CURTO", font("blk", 44), WHITE, RED), W / 2, 160, ease(t / 0.4))
        return im
    if sc in ("transfer", "tr_tomas", "tr_theo"):
        im = bg_dark(t)
        txt(im, (W / 2, 90), "MERCADO • JANELA DE VERÃO", font("blk", 56), WHITE, "mm")
        paste(im, chip("ORÇAMENTO: £180.000", font("bd", 34)), W / 2, 160)
        if sc == "transfer":
            txt(im, (W / 2, H / 2), "quem ninguém quer" if shot["cues"][0]["i"] == 37 else "a 3ª contratação: £0", font("blk", 90), AMB, "mm", alpha=ease(t / 0.5))
        else:
            k, n, o, p, s, tag, col = (("f_tomas", "Tomás Ferreira", 68, "ZAG", (52, 40, 58, 50, 70, 74), "GRÁTIS", GREEN) if sc == "tr_tomas"
                                       else ("f_theo", "Theo Okafor", 63, "ATA", (78, 63, 55, 66, 30, 64), "EMPRÉSTIMO", AMB))
            c = face_card(k, n, o, p, s, 420)
            paste(im, c, W / 2, H / 2 + 60, ease(t / 0.4), 0.85 + 0.15 * ease(t / 0.4))
            st = chip(tag, font("blk", 52), BG if col != GREEN else WHITE, col)
            paste(im, st.rotate(12, expand=True), W / 2 + 280, H / 2 - 80, ease((t - 0.7) / 0.3))
        return im
    if sc in ("murrey_in", "murrey_card", "gildo", "gildo_card", "kofi", "ollie", "newbase"):
        im = bg_dark(t)
        if sc == "murrey_in":
            av = avatar("murrey", 760)
            sil = Image.new("RGBA", av.size, (0, 0, 0, 255)); sil.putalpha(av.getchannel("A"))
            reveal = clamp((t - dur + 1.2) / 1.0)
            el = Image.blend(sil, av, reveal) if reveal > 0 else sil
            paste(im, el, W / 2, H - av.height / 2, 1)
            txt(im, (W / 2, 120), "PROMOVIDO DO SUB-18", font("blk", 60), AMB, "mm", alpha=ease(t / 0.4))
            return im
        if sc == "newbase":
            txt(im, (W / 2, H / 2 - 40), "BASE", font("blk", 140), AMB, "mm", alpha=ease(t / 0.4))
            txt(im, (W / 2, H / 2 + 80), "2 garotos novos", font("bd", 56), WHITE, "mm", alpha=ease((t - 0.3) / 0.4))
            return im
        if sc == "gildo":
            av = avatar("gildo", 780); paste(im, av, 620, H - av.height / 2, ease(t / 0.5))
            a = ease((t - 0.4) / 0.5)
            txt(im, (1080, 380), "GILDO", font("blk", 130), WHITE, alpha=a)
            for i, l in enumerate(["15 ANOS • PONTA-ESQUERDA", "filho de imigrantes brasileiros", "o mais rápido da cidade"]):
                txt(im, (1086, 540 + i * 70), l, font("bd" if i == 0 else "md", 44), AMB if i == 0 else (220, 220, 220), alpha=ease((t - 0.8 - i * 0.4) / 0.4))
            return im
        key, name, o, p, s, pot, prom = {
            "murrey_card": ("murrey", "Murrey", 52, "MEI", (66, 50, 60, 62, 25, 40), 91, True),
            "gildo_card": ("gildo", "Gildo", 48, "PE", (84, 40, 42, 58, 20, 38), 89, True),
            "kofi": ("f_kofi", "Kofi Mensah-Hart", 50, "VOL", (55, 30, 48, 46, 52, 56), 79, True),
            "ollie": ("f_ollie", "Ollie Fenwick", 46, "ATA", (58, 50, 35, 44, 18, 45), 77, True)}[sc]
        c = face_card(key, name, o, p, s, 460, prom)
        paste(im, c, 700, H / 2 + 20, ease(t / 0.4), 0.85 + 0.15 * ease(t / 0.4))
        a = ease((t - 0.6) / 0.5)
        txt(im, (1100, 360), "OVERALL", font("bd", 40), (180, 180, 180), alpha=a)
        txt(im, (1100, 400), f"{o}", font("blk", 150), WHITE, alpha=a)
        txt(im, (1100, 600), "POTENCIAL", font("bd", 40), (180, 180, 180), alpha=ease((t - 1.0) / 0.5))
        pv = int(o + (pot - o) * ease((t - 1.1) / 1.2))
        txt(im, (1100, 640), f"{pv}", font("blk", 150), AMB, alpha=ease((t - 1.0) / 0.5))
        paste(im, chip("PROMESSA DA BASE", font("blk", 34)), W / 2, 90, ease(t / 0.4))
        return im
    if sc == "table_bad":
        im = bg_dark(t, RED)
        txt(im, (140, 300), "5 RODADAS", font("blk", 110), WHITE, alpha=ease(t / 0.4))
        txt(im, (146, 430), "1 vitória", font("bd", 64), RED, alpha=ease((t - 0.4) / 0.4))
        table(im, t, 12, 20, "LEAGUE TWO • SETEMBRO")
        return im
    if sc == "table_up":
        im = bg_dark(t, GREEN)
        txt(im, (140, 300), "6 VITÓRIAS", font("blk", 110), WHITE, alpha=ease(t / 0.4))
        txt(im, (146, 430), "seguidas", font("bd", 64), GREEN, alpha=ease((t - 0.4) / 0.4))
        paste(im, chip("KAIKAI: 3 GOLS vs BRISTOL ROVERS", font("blk", 34)), 140 + 330, 560, ease((t - 1.5) / 0.5))
        table(im, t, 20, 8, "LEAGUE TWO • OUTUBRO")
        return im
    if sc == "ovr_up":
        im = bg_dark(t)
        table(im, t, 8, 7, "LEAGUE TWO • 31 DE DEZEMBRO", 980, 110)
        c = face_card("murrey", "Murrey", 57 if t > 2.6 else 52, "MEI", (70, 56, 62, 66, 26, 42), 380, True)
        paste(im, c, 470, H / 2 + 20, 1)
        if t > 2.4: paste(im, chip("52 → 57", font("blk", 56), BG, GREEN), 470, 140, ease((t - 2.4) / 0.4))
        paste(im, chip("ZONA DE PLAY-OFF", font("blk", 34), BG, GREEN), 1390, 120, ease((t - 2) / 0.4))
        return im
    if sc == "murrey_assist":
        if shot["cues"][0]["i"] == 45 and t < (shot["cues"][0]["t1"] - shot["t0"]):
            im = lance(L.ambient, t, dur, "CAMBRIDGE  0  x  0  ACCRINGTON", sub="EFL TROPHY • ESTREIA DE MURREY")
            return im
        t2 = t - (shot["cues"][1]["t0"] - shot["t0"]) + 0.4
        tl = min(2.2, dur * 0.3) + 1.3 + 1.1 + 0.4
        return lance(L.assist, max(0, t2), dur, "CAMBRIDGE  0  x  0  ACCRINGTON" if t2 < tl else "CAMBRIDGE  1  x  0  ACCRINGTON",
                     tl, "ASSISTÊNCIA DE LETRA", AMB, sub="EFL TROPHY")
    if sc == "tactics":
        im = Image.new("RGBA", (W, H), (22, 80, 44, 255)); d = ImageDraw.Draw(im)
        for i in range(10): d.rectangle((i * 192, 0, i * 192 + 96, H), fill=(26, 88, 48))
        lw = (235, 245, 235, 200)
        d.rectangle((100, 80, W - 100, H - 80), outline=lw, width=5); d.line((W / 2, 80, W / 2, H - 80), fill=lw, width=5)
        d.ellipse((W / 2 - 120, H / 2 - 120, W / 2 + 120, H / 2 + 120), outline=lw, width=5)
        d.rectangle((100, H / 2 - 220, 380, H / 2 + 220), outline=lw, width=5); d.rectangle((W - 380, H / 2 - 220, W - 100, H / 2 + 220), outline=lw, width=5)
        pos = [(220, 540), (450, 300), (430, 470), (430, 620), (450, 790), (720, 420), (700, 660), (900, 540), (1150, 300), (1200, 540), (1150, 800)]
        pre = [(220, 540), (420, 300), (400, 470), (400, 620), (420, 790), (640, 420), (620, 660), (780, 540), (950, 360), (1000, 540), (950, 760)]
        u = ease((t - 2.5) / 1.5)
        for i, (p0, p1) in enumerate(zip(pre, pos)):
            x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u
            if i == 10: y += (880 - p1[1]) * ease((t - 4.5) / 1.0); x += (1250 - p1[0]) * ease((t - 4.5) / 1.0)
            d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=AMB, outline=(20, 20, 20), width=4)
        if t > 4.5:
            paste(im, chip("KAIKAI ABERTO NA DIREITA", font("blk", 34)), 1560, 770, ease((t - 4.8) / 0.4))
        if t > 6:
            a = ease((t - 6) / 0.6)
            for y in (300, 540, 800):
                d.line((1230, y, 1230 + 300 * a, y), fill=(255, 255, 255, 230), width=10)
                d.polygon([(1230 + 300 * a + 30, y), (1230 + 300 * a, y - 20), (1230 + 300 * a, y + 20)], fill=(255, 255, 255, 230))
            paste(im, chip("PRESSÃO DESDE A SAÍDA DE BOLA", font("blk", 40), WHITE, RED), W / 2, 130, a)
        else:
            paste(im, chip("OUTUBRO • RICK MUDA TUDO", font("blk", 44)), W / 2, 130, ease(t / 0.4))
        return im
    if sc == "facup":
        im = bg_dark(t)
        txt(im, (W / 2, 260), "COPA DA INGLATERRA", font("blk", 96), WHITE, "mm", alpha=ease(t / 0.4))
        steps = [("1ª FASE", "✓"), ("2ª FASE", "→"), ("3ª FASE", ""), ("...", "")]
        for i, (s, m) in enumerate(steps):
            a = ease((t - 0.5 - i * 0.4) / 0.4)
            col = GREEN if i == 0 else AMB if i == 1 else (90, 90, 90)
            p = panel(330, 160, col + (230,) if i < 2 else (40, 40, 44, 230)); dd = ImageDraw.Draw(p)
            dd.text((165, 60), s, font=font("blk", 46), fill=BG if i < 2 else (200, 200, 200), anchor="mm")
            dd.text((165, 118), m, font=font("blk", 40), fill=BG, anchor="mm")
            paste(im, p, 280 + i * 450, 560, a)
        txt(im, (W / 2, 780), "vitória sobre um time da 5ª divisão", font("md", 46), (220, 220, 220), "mm", alpha=ease((t - 1.5) / 0.5))
        return im
    if sc == "boxing":
        return lance(L.ambient, t + 20, dur, "CAMBRIDGE  0  x  1  COLCHESTER", sub="BOXING DAY • ABBEY STADIUM • 70'")
    if sc == "boxing_sub":
        im = lance(L.ambient, t + 30, dur, "CAMBRIDGE  0  x  1  COLCHESTER", sub="SUBSTITUIÇÃO • 70'")
        p = panel(560, 260, (16, 16, 18, 235)); dd = ImageDraw.Draw(p)
        dd.text((40, 40), "ENTRA", font=font("bd", 34), fill=GREEN); dd.text((40, 86), "MURREY", font=font("blk", 80), fill=WHITE)
        dd.text((40, 190), "\"aqui ninguém é maior que o clube\"", font=font("md", 26), fill=AMB)
        paste(im, p, W / 2, H / 2 + 40, ease(t / 0.4), 0.9 + 0.1 * ease(t / 0.4))
        return im
    if sc == "murrey_goal":
        tsh = min(1.6, dur * 0.25) + 1.2 + 0.6
        return lance(L.golaco, t, dur, "CAMBRIDGE  0  x  1  COLCHESTER" if t < tsh + 0.6 else "CAMBRIDGE  1  x  1  COLCHESTER",
                     tsh + 0.6, "GOL DE MURREY! 88'", AMB, sub="BOXING DAY")
    if sc == "contract":
        im = bg_dark(t)
        p = panel(900, 640, (245, 242, 232, 250), 16, (0, 0, 0, 0)); dd = ImageDraw.Draw(p)
        dd.text((60, 60), "CONTRATO DE TRABALHO", font=font("blk", 46), fill=(30, 30, 30))
        dd.text((60, 160), "Rick Miguel", font=font("bd", 44), fill=(30, 30, 30))
        dd.text((60, 250), "Cargo:", font=font("md", 38), fill=(80, 80, 80))
        dd.text((60, 310), "TÉCNICO INTERINO", font=font("blk", 60), fill=(30, 30, 30))
        u = ease((t - 1.2) / 0.6)
        if u > 0:
            dd.line((50, 350, 50 + 620 * u, 350), fill=(200, 30, 30), width=10)
        if t > 2.2:
            dd.text((60, 420), "TÉCNICO PRINCIPAL", font=font("blk", 60), fill=(20, 120, 60))
        paste(im, p, W / 2, H / 2 + 30, ease(t / 0.4))
        return im
    if sc == "ab":
        im = Image.new("RGBA", (W, H), BG + (255,))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W / 2, H), fill=(28, 52, 34)); d.rectangle((W / 2, 0, W, H), fill=(52, 30, 28))
        txt(im, (W / 4, 150), "A", font("blk", 200), GREEN, "mm"); txt(im, (3 * W / 4, 150), "B", font("blk", 200), RED, "mm")
        txt(im, (W / 4, 330), "VENDER O MURREY", font("blk", 64), WHITE, "mm")
        txt(im, (W / 4, 410), "£1,2 milhão • 3 reforços prontos", font("md", 40), (220, 220, 220), "mm")
        txt(im, (3 * W / 4, 330), "SEGURAR O MURREY", font("blk", 64), WHITE, "mm")
        txt(im, (3 * W / 4, 410), "elenco curto • o talento fica em casa", font("md", 40), (220, 220, 220), "mm")
        c = face_card("murrey", "Murrey", 57, "MEI", (70, 56, 62, 66, 26, 42), 340, True)
        paste(im, c, W / 2, 200, 1, 0.6 + 0.02 * math.sin(t * 2))
        paste(im, chip("COMENTE A OU B", font("blk", 56), BG, WHITE), W / 2, 640, ease((t - 6) / 0.5))
        return im
    if sc == "end":
        im = bg_dark(t)
        cr = Image.open(os.path.join(A, "cambridge_united.png")).convert("RGBA")
        paste(im, cr, W / 2, 380, 1, 0.5)
        txt(im, (W / 2, 690), "PRÓXIMO EPISÓDIO: JAN – JUN 2027", font("blk", 64), WHITE, "mm")
        paste(im, chip("INSCREVA-SE", font("blk", 52), WHITE, RED), W / 2, 820, ease(t / 0.5))
        return im
    im = bg_dark(t)
    txt(im, (W / 2, H / 2), sc, font("blk", 80), WHITE, "mm")
    return im


def frame(T):
    for i, s in enumerate(SHOTS):
        if s["t0"] <= T < s["t1"] or i == len(SHOTS) - 1:
            break
    dur = s["t1"] - s["t0"]
    im = scene(s["scene"], T - s["t0"], dur, s)
    # crossfade de 0.35 s com o plano anterior
    if i > 0 and T - s["t0"] < 0.35:
        p = SHOTS[i - 1]
        prev = scene(p["scene"], T - p["t0"], p["t1"] - p["t0"], p)
        im = Image.blend(prev.convert("RGB"), im.convert("RGB"), (T - s["t0"]) / 0.35).convert("RGBA")
    caption(im, T)
    return im.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for x in sys.argv[2:]:
            frame(float(x)).save(f"/tmp/pv_{float(x):06.1f}.jpg", quality=88)
    elif sys.argv[1] == "shots":
        for s in SHOTS: print(f"{s['t0']:7.2f} {s['t1']:7.2f} {s['scene']}")
    else:
        i, n = int(sys.argv[2]), int(sys.argv[3])
        nf = int(TOTAL * FPS); a, b = nf * i // n, nf * (i + 1) // n
        out = f"{D}/chunk_{i}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b):
            p.stdin.write(frame(f / FPS).tobytes())
        p.stdin.close(); p.wait()
        if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
