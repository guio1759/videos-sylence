"""Ep.1 v2 — ritmo rápido, telas de jogo animadas, HUD, legenda palavra a palavra.
Uso: python3 make2.py preview W H t...  |  render i n  |  shots"""
import os, sys, json, math, re, random, subprocess, functools, unicodedata
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from gfx import *
import gfx as G
sys.path.insert(0, "/home/claude/ep1")
import lances as L

D = os.path.dirname(os.path.abspath(__file__))
WJ = json.load(open(os.path.join(D, "words.json")))
WORDS = WJ["words"]; TOTAL = WJ["total"]
FPS = 30


def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())


SHOTS = []
for i, w in enumerate(WORDS):
    if SHOTS and SHOTS[-1]["scene"] == w["scene"]:
        SHOTS[-1]["words"].append(w)
    else:
        SHOTS.append({"scene": w["scene"], "words": [w], "block": w["block"], "music": w["music"]})
for i, s in enumerate(SHOTS):
    s["t0"] = 0.0 if i == 0 else max(SHOTS[i - 1]["words"][-1]["t1"], s["words"][0]["t0"] - 0.12)
for i, s in enumerate(SHOTS):
    s["t1"] = SHOTS[i + 1]["t0"] if i + 1 < len(SHOTS) else TOTAL


def wt(shot, word, nth=0):
    """tempo local (no plano) da n-ésima ocorrência da palavra"""
    k = 0
    for w in shot["words"]:
        if norm(w["w"]) == norm(word):
            if k == nth: return w["t0"] - shot["t0"]
            k += 1
    return 0.0


# ---------- estado do clube (HUD) por cena ----------
POS = {"fixtures_bad": 20, "headline_out": 20, "assist_pre": 20, "assist": 20, "tactics": 20, "kaikai_goal": 14, "fixtures_good": 12, "table_up": 8,
       "base_night": 8, "base_race": 8, "walk_gildo": 8, "gildo_stats": 8, "new_base": 8, "walk_kofi": 8, "walk_ollie": 8, "drama_phone": 8, "drama_bench": 8,
       "boxing": 8, "boxing_sub": 8, "murrey_goal": 8, "murrey_goal_x": 8, "hug": 8, "ovr_up": 7, "contract": 7, "email": 7, "email_x": 7, "ab": 7, "end": 7}
TOPIC = {"crewe": "O MINUTO 93", "crewe_goal": "O MINUTO 93", "crewe_after": "O PIOR DIA", "version": "NOSSA VERSÃO",
         "hist_1912": "1912", "hist_1970": "1970", "hist_1990": "ANOS 90", "hist_1992": "1992", "hist_2005": "2005", "hist_2014": "2014",
         "rick_born": "QUEM É RICK MIGUEL", "rick_kid": "A COZINHA", "rick_2005": "A PROMESSA", "rick_injury": "O JOELHO", "rick_bus": "O CADERNINHO",
         "rick_call": "A LIGAÇÃO", "rick_profile": "O NOVO TÉCNICO", "hub": "CENTRAL DO CLUBE", "hub_budget": "CENTRAL DO CLUBE", "hub_goal": "A META",
         "squad_list": "O ELENCO", "squad_kaikai": "O CRAQUE", "squad_bauer": "O XERIFE", "squad_pelly": "O ÍDOLO", "squad_xi": "O TIME",
         "market": "MERCADO", "walk_tomas": "REFORÇO #1", "walk_theo": "REFORÇO #2", "walk_murrey_pre": "REFORÇO #3", "walk_murrey": "REFORÇO #3",
         "murrey_stats": "REFORÇO #3", "fixtures_bad": "COMEÇO DE TEMPORADA", "headline_out": "PRESSÃO", "assist_pre": "A APOSTA", "assist": "A APOSTA",
         "tactics": "OUTUBRO", "kaikai_goal": "OUTUBRO", "fixtures_good": "A VIRADA", "table_up": "A VIRADA", "base_night": "A APOSTA", "base_race": "A CORRIDA",
         "walk_gildo": "A BASE", "gildo_stats": "A BASE", "new_base": "NOVOS NA BASE", "walk_kofi": "NOVOS NA BASE", "walk_ollie": "NOVOS NA BASE",
         "drama_phone": "O PROBLEMA", "drama_bench": "O PROBLEMA", "boxing": "BOXING DAY", "boxing_sub": "BOXING DAY", "murrey_goal": "BOXING DAY",
         "murrey_goal_x": "BOXING DAY", "hug": "BOXING DAY", "ovr_up": "FIM DE 2026", "contract": "FIM DE 2026", "email": "1º DE JANEIRO",
         "email_x": "1º DE JANEIRO", "ab": "VOCÊ DECIDE", "end": "PRÓXIMO EPISÓDIO"}


def hud(img, scene, t):
    W, H = img.size; vert = H > W
    if scene.startswith("tz_") or scene in ("end",): return
    pos = POS.get(scene); budget = "£180K"
    if vert:
        y = 70; h = 86
        p = panel(W - 60, h, (12, 12, 16, 220), 24); img.alpha_composite(p, (30, y))
        paste(img, crest(64), 80, y + h / 2)
        d = ImageDraw.Draw(img)
        d.text((125, y + h / 2), "CAMBRIDGE UNITED", font=font("blk", 30), fill=WHITE, anchor="lm")
        if pos: paste(img, chip(f"{pos}º", 30, INK, AMB), W - 230, y + h / 2)
        paste(img, chip(budget, 30, WHITE, (60, 60, 70)), W - 110, y + h / 2)
        return
    h = 64; p = panel(W - 40, h, (12, 12, 16, 215), 22); img.alpha_composite(p, (20, 16))
    paste(img, crest(52), 58, 16 + h / 2)
    d = ImageDraw.Draw(img)
    d.text((96, 16 + h / 2), "CAMBRIDGE UNITED", font=font("blk", 28), fill=WHITE, anchor="lm")
    x = 420
    for s, bgc, fg in ((("LEAGUE TWO", (60, 60, 70), WHITE)), ((f"POSIÇÃO {pos}º" if pos else "PRÉ-TEMPORADA"), AMB, INK), (f"ORÇAMENTO {budget}", (60, 60, 70), WHITE)):
        c = chip(s, 24, fg, bgc); img.alpha_composite(c, (x, 16 + h // 2 - c.height // 2)); x += c.width + 10
    # rumo à champions
    steps = ["4ª", "3ª", "2ª", "PREMIER", "CHAMPIONS"]
    x0 = W - 640
    d.text((x0, 16 + h / 2), "RUMO À", font=font("bd", 20), fill=(190, 190, 190), anchor="lm")
    for i, s in enumerate(steps):
        c = chip(s, 20, INK if i == 0 else (200, 200, 200), AMB if i == 0 else (50, 50, 58)); img.alpha_composite(c, (x0 + 90 + i * 104, 16 + h // 2 - c.height // 2))


def topic(img, scene, t):
    W, H = img.size; vert = H > W
    s = TOPIC.get(scene)
    if not s: return
    el = tag_box(s, 50 if vert else 40)
    a = back(t / 0.35)
    paste(img, el, W / 2, (250 if vert else 140), 1, 0.6 + 0.4 * a, rot=-2)


SKIPN = None
SKIP = {"o", "a", "e", "de", "da", "do", "pra", "pro", "um", "uma", "no", "na", "que", "com", "os", "as", "em", "se", "ele", "eu", "é", "ja", "ta"}


SKIPN = {norm(x) for x in SKIP}

def caption(img, T):
    W, H = img.size; vert = H > W
    cur = None
    for w in WORDS:
        if w["t0"] - 0.03 <= T < w["t1"] + 0.12: cur = w
        if w["t0"] > T: break
    if not cur: return
    # palavras curtas/vazias: segura a última palavra forte por até 0.7 s
    def strong(w): return len(norm(w["w"])) > 2 and norm(w["w"]) not in SKIPN
    if not strong(cur):
        idx = WORDS.index(cur); prev = next((WORDS[k] for k in range(idx - 1, max(-1, idx - 4), -1) if strong(WORDS[k])), None)
        if not prev or T - prev["t1"] > 0.7: return
        cur = prev
    s = re.sub(r"[.,!?:;]", "", cur["w"]).upper()
    if not s: return
    age = T - cur["t0"]
    sc = 0.75 + 0.25 * back(age / 0.18)
    size = 92 if vert else 76
    el = chip(s, size, INK, AMB if cur["w"].endswith(("!",)) or len(s) > 7 else WHITE, "blk", 0.5, 0.25)
    paste(img, el, W / 2, H * (0.85 if vert else 0.86), 1, sc, rot=-2 if (hash(s) % 2) else 2)


# ---------- helpers de cena ----------
def shake(img, t, t0, amp=18, dur=0.4):
    u = t - t0
    if 0 <= u < dur:
        a = amp * (1 - u / dur); dx = int(a * math.sin(u * 90)); dy = int(a * math.cos(u * 70))
        im2 = Image.new("RGBA", img.size, (0, 0, 0, 255)); im2.alpha_composite(img, (dx, dy)); return im2
    return img


def flash(img, t, t0, dur=0.25, col=(255, 255, 255)):
    u = t - t0
    if 0 <= u < dur:
        img.alpha_composite(Image.new("RGBA", img.size, col + (int(200 * (1 - u / dur)),)))
    return img


def pop_text(img, s, x, y, t, t0, size=120, col=WHITE, stroke=8, rot=0):
    if t < t0: return
    a = back((t - t0) / 0.3)
    paste(img, text_el(s, font("blk", size), col, stroke), x, y, 1, 0.3 + 0.7 * a, rot)


def big_lines(img, lines, x, y, t, t0=0.0, size=80, gap=1.15, cols=None, anchor="c"):
    for i, l in enumerate(lines):
        u = (t - t0 - i * 0.2) / 0.35
        if u <= 0: continue
        col = (cols or [WHITE] * len(lines))[i]
        el = text_el(l, font("blk", size), col, 6)
        xx = x if anchor == "c" else x + el.width / 2
        paste(img, el, xx - 60 * (1 - ease(u)), y + i * size * gap, ease(u))


def card_in(img, key, x, y, w, t, t0=0.0, ovr=None, spin=True):
    u = (t - t0) / 0.45
    if u <= 0: return
    c = card(key, w, ovr)
    paste(img, c, x, y, ease(u), 0.5 + 0.5 * back(u), rot=(1 - ease(u)) * 25 if spin else 0)


def lance(img, fn, t, dur, bug=None, flash_at=None, flash_txt=None, flash_col=AMB):
    W, H = img.size
    L.W, L.H = W, H
    im, labs = L.render(fn, t, dur)
    for s, pr, a, b, col in labs:
        if pr and a < t < b:
            v = ease((t - a) / 0.25) * (1 - ease((t - b + 0.25) / 0.25))
            paste(im, chip(s, 30, INK, col), pr[0], pr[1] - 50, v)
    if bug:
        p = panel(640, 80, (12, 12, 16, 235), 40); ImageDraw.Draw(p).text((320, 40), bug, font=font("blk", 36), fill=WHITE, anchor="mm")
        paste(im, p, W / 2, (360 if H > W else 210))
    if flash_at is not None and t > flash_at:
        im = flash(im, t, flash_at)
        pop_text(im, flash_txt, W / 2, H * 0.45, t, flash_at, 150 if W > H else 120, flash_col, 10, -3)
        im = shake(im, t, flash_at)
    img.alpha_composite(im)


# ---------- cenas ----------
def scene(img, sh, t):
    W, H = img.size; vert = H > W; cx, cy = W / 2, H / 2
    sc = sh["scene"]; d = sh["t1"] - sh["t0"]
    U = min(W, H) / 1080
    def B(key): img.alpha_composite(bg(W, H, key, t))
    if sc == "tz_bus":
        B("amber"); paste(img, icon_bus(W * (0.7 if vert else 0.42)), cx + (1 - ease(t / 0.4)) * W * 0.6 - 20 * math.sin(t * 20), cy + 40, 1)
        img.alpha_composite(speedlines(W, H, t)); pop_text(img, "UM MOTORISTA DE ÔNIBUS", cx, H * 0.22, t, 0, 70 if vert else 90, WHITE, 8)
    elif sc == "tz_broke":
        B("red"); paste(img, newspaper(W * (0.85 if vert else 0.5), "2005", "CLUBE FALIDO: ESTÁDIO VENDIDO"), cx, cy, 1, 0.3 + 0.7 * back(t / 0.35), rot=(1 - ease(t / 0.35)) * 200)
    elif sc == "tz_gamer":
        B("purple"); paste(img, avatar("murrey", H * 0.55 if not vert else W * 0.9), cx - (0 if vert else 260), H - (H * 0.55 if not vert else W * 0.9) / 2, ease(t / 0.3))
        paste(img, icon_pad(W * (0.45 if vert else 0.25)), cx + (0 if vert else 330), cy - (300 if vert else 40) + 15 * math.sin(t * 12), 1, back(t / 0.3), rot=10 * math.sin(t * 8))
        paste(img, stamp("FALTOU AO TREINO", 70 if vert else 64), cx + (0 if vert else 300), H * (0.25 if vert else 0.75), 1, back((t - 0.6) / 0.25), rot=-8)
    elif sc == "tz_pizza":
        B("teal"); img.alpha_composite(speedlines(W, H, t))
        av = avatar("gildo", H * 0.6 if not vert else W * 0.95); x = -W * 0.3 + (W * 0.75) * ease(t / 0.6)
        paste(img, av, x if not vert else cx, H - av.height / 2)
        paste(img, icon_pizza(W * (0.35 if vert else 0.2)), (x + 260 if not vert else cx + 260), H * 0.42 + 10 * math.sin(t * 15), 1, 1, rot=-10)
        pop_text(img, "MAIS RÁPIDO QUE PROFISSIONAL", cx, H * 0.22, t, 0.3, 64 if vert else 84, WHITE, 8)
    elif sc == "tz_goal":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t))
        keys = ["murrey", "gildo", "f_kofi", "f_ollie"]
        for i, k in enumerate(keys):
            ang = t * 1.2 + i * math.pi / 2; r = (W * 0.36 if not vert else W * 0.32)
            card_in(img, k, cx + r * math.cos(ang), cy + r * 0.45 * math.sin(ang) + 40, 230 * U * (1.3 if vert else 1), t, i * 0.12)
        paste(img, text_el("4ª DIVISÃO", font("blk", 110 * U), WHITE, 8), cx, cy - 80 * U, ease((t - wt(sh, "quarta")) / 0.3))
        paste(img, text_el("→ CHAMPIONS", font("blk", 120 * U), AMB, 8), cx, cy + 60 * U, 1, back((t - wt(sh, "champions")) / 0.3))
    elif sc == "tz_title":
        B("dark"); img.alpha_composite(rays(W, H, cx, cy - 120, t, AMB, 12, 50))
        paste(img, crest(300 * U), cx, cy - 200 * U, 1, back(t / 0.4))
        pop_text(img, "MODO CARREIRA", cx, cy + 40 * U, t, 0.3, 130 * U, WHITE, 8)
        pop_text(img, "EP. 1 • O MOTORISTA DE ÔNIBUS", cx, cy + 170 * U, t, 0.8, 56 * U, AMB, 6)
    elif sc in ("crewe", "crewe_goal"):
        if sc == "crewe":
            lance(img, L.ambient, t + 3, d, "CREWE 0 x 0 CAMBRIDGE")
            clk = f"93:{int(clamp(t / d) * 59):02d}"
            paste(img, chip(clk, 44, WHITE, RED), cx, (450 if vert else 290), 1, 1 + 0.06 * math.sin(t * 8))
            if t > wt(sh, "torcida"): paste(img, chip("A CIDADE INTEIRA NO RÁDIO", 34, INK, AMB), cx, (540 if vert else 360), ease((t - wt(sh, "torcida")) / 0.3))
        else:
            tg = min(4.2, d * 0.55)
            lance(img, L.crewe, t, d, "CREWE 0 x 0 CAMBRIDGE" if t < tg + 0.35 else "CREWE 1 x 0 CAMBRIDGE", tg + 0.35, "GOL DO CREWE", RED)
    elif sc == "crewe_after":
        B("red")
        steps = [("PLAY-OFF", "eliminado na semi"), ("TÉCNICO", "foi embora"), ("EMPRESTADOS", "voltaram"), ("COFRE", "vazio")]
        anchors = [0, wt(sh, "tecnico"), wt(sh, "emprestados"), wt(sh, "cofre")]
        for i, (a, b) in enumerate(steps):
            u = (t - anchors[i]) / 0.3
            if u <= 0: continue
            y = (H * 0.38 + i * 200) if vert else (300 + i * 150)
            p = panel(W * (0.86 if vert else 0.5), 120, (20, 10, 12, 230)); dd = ImageDraw.Draw(p)
            dd.text((40, 60), a, font=font("blk", 54), fill=WHITE, anchor="lm"); dd.text((p.width - 40, 60), b, font=font("bd", 40), fill=(255, 150, 150), anchor="rm")
            paste(img, p, cx, y, ease(u), 0.8 + 0.2 * back(u))
        paste(img, stamp("ELIMINADO", 90), cx + (0 if vert else 520), (H * 0.25 if vert else 520), 1, back(t / 0.3), rot=-10)
        img = shake(img, t, 0.0, 14)
    elif sc == "version":
        B("dark")
        if vert:
            boxes = [(cx, H * 0.38, "VIDA REAL", "SUBIU ✓", GREEN, 0), (cx, H * 0.6, "NOSSA VERSÃO", "FICOU NA 4ª ✗", RED, wt(sh, "nossa"))]
        else:
            boxes = [(W * 0.3, cy, "VIDA REAL", "SUBIU ✓", GREEN, 0), (W * 0.7, cy, "NOSSA VERSÃO", "FICOU NA 4ª ✗", RED, wt(sh, "nossa"))]
        for x, y, a, b, col, t0 in boxes:
            u = (t - t0) / 0.35
            if u <= 0: continue
            p = panel(720, 300, col + (235,)); dd = ImageDraw.Draw(p)
            dd.text((360, 95), a, font=font("bd", 52), fill=WHITE, anchor="mm"); dd.text((360, 200), b, font=font("blk", 78), fill=WHITE, anchor="mm")
            paste(img, p, x, y, ease(u), 0.7 + 0.3 * back(u), rot=-3 if col == RED else 3)
    elif sc.startswith("hist_"):
        y = sc[5:]
        B("sepia" if y in ("1912", "1970") else "blue" if y in ("1990", "1992") else "red" if y == "2005" else "green")
        heads = {"1912": ("NASCE O ABBEY UNITED", "o clube do bairro operário"), "1970": ("NA LIGA PROFISSIONAL!", "depois de 58 anos no amador"),
                 "1990": ("CAMBRIDGE EM WEMBLEY!", "acesso, FA Cup e título da 3ª"), "1992": ("A UM JOGO DA PREMIER LEAGUE", "o play-off que nunca saiu da cidade"),
                 "2005": ("FALÊNCIA: CLUBE VENDE O ESTÁDIO", "fora da liga após 35 anos"), "2014": ("DE VOLTA À LIGA!", "nove anos depois")}[y]
        od = odometer(int(y), 4, 120 * U, t, 0.8, int(y) - 40 if y != "1912" else 1880)
        paste(img, od, cx, (H * 0.25 if vert else 185), 1)
        npw = W * (0.88 if vert else 0.46)
        u = (t - 0.5) / 0.45
        if u > 0: paste(img, newspaper(npw, y, heads[0], heads[1], y in ("1912", "1970")), cx, (H * 0.52 if vert else cy + 120), 1, 0.2 + 0.8 * back(u), rot=(1 - ease(u)) * 360)
        if y == "1992" and t > wt(sh, "nao"): paste(img, stamp("NÃO DEU", 100), cx, (H * 0.52 if vert else cy + 90), 1, back((t - wt(sh, "nao")) / 0.25), rot=-12)
    elif sc == "rick_born":
        B("blue"); av = avatar("rick", H * (0.42 if vert else 0.78))
        paste(img, av, (cx if vert else W * 0.3), H - av.height / 2 - (H * 0.18 if vert else 0), ease(t / 0.3))
        x0 = cx if vert else W * 0.68; y0 = H * 0.2 if vert else 300
        pop_text(img, "RICK MIGUEL", x0, y0, t, 0.1, 110 * U, WHITE, 8)
        for i, (s, t0) in enumerate([("NASCEU EM 1992", wt(sh, "nasceu")), ("PAI: ROUPEIRO DO ESTÁDIO", wt(sh, "pai")), ("MÃE: PAULISTANA E PALMEIRENSE", wt(sh, "mae"))]):
            if t > t0: paste(img, chip(s, 40 * U * (1.1 if vert else 1), INK if i != 2 else WHITE, AMB if i != 2 else (20, 120, 60)), x0, y0 + 140 * U + i * 90 * U, 1, back((t - t0) / 0.3))
    elif sc == "rick_kid":
        B("sepia")
        paste(img, icon_radio(W * (0.45 if vert else 0.26), t), cx - (0 if vert else 380), cy + (120 if vert else 60))
        b1 = chip("GOL DO CAMBRIDGE!", 48, INK, AMB); b2 = chip("GOL DO PALMEIRAS!", 48, WHITE, (20, 120, 60))
        paste(img, b1, cx + (0 if vert else 300), (H * 0.25 if vert else 330), 1, back(t / 0.3), rot=-4 + 3 * math.sin(t * 6))
        paste(img, b2, cx + (0 if vert else 330), (H * 0.33 if vert else 470), 1, back((t - wt(sh, "mae")) / 0.3), rot=4 + 3 * math.sin(t * 6))
        pop_text(img, "FLASHBACK • 2000", cx, (H * 0.16 if vert else 270), t, 0, 50 * U, WHITE, 6)
    elif sc == "rick_2005":
        B("night"); paste(img, newspaper(W * (0.85 if vert else 0.42), "2005", "CLUBE CAI E DEMITE FUNCIONÁRIOS"), cx - (0 if vert else 380), (H * 0.38 if vert else cy + 40), 1, back(t / 0.4), rot=-4)
        u = t - wt(sh, "prometeu")
        if u > 0:
            s = "VOU DEVOLVER O CAMBRIDGE PRO LUGAR DELE"; n = int(len(s) * clamp(u / 1.6))
            f = font("blk", 46 * U); lines = wrap(s[:n], f, W * (0.8 if vert else 0.4))
            for i, l in enumerate(lines):
                ImageDraw.Draw(img).text((cx if vert else W * 0.73, (H * 0.68 if vert else 380) + i * 64 * U), l, font=f, fill=AMB, anchor="mm")
            paste(img, chip("A PROMESSA", 40), cx if vert else W * 0.73, (H * 0.62 if vert else 300), 1)
    elif sc == "rick_injury":
        B("dark"); tb = wt(sh, "terceiro")
        key = "rick"
        av = (avatar if t < tb else gray)(key, H * (0.45 if vert else 0.8))
        paste(img, av, cx if vert else W * 0.35, H - av.height / 2 - (H * 0.15 if vert else 0))
        pop_text(img, "ESTREIA AOS 19", cx if vert else W * 0.7, H * 0.2 if vert else 330, t, 0, 70 * U, WHITE, 6)
        if t > tb:
            img = flash(img, t, tb, 0.2, (255, 60, 60))
            paste(img, stamp("CARREIRA ENCERRADA", 64), cx if vert else W * 0.7, H * 0.32 if vert else 520, 1, back((t - tb) / 0.3), rot=-8)
            img = shake(img, t, tb, 22)
    elif sc == "rick_bus":
        B("amber"); img.alpha_composite(speedlines(W, H, t, 20))
        paste(img, icon_bus(W * (0.7 if vert else 0.4)), cx - (0 if vert else 380) + 10 * math.sin(t * 25), (H * 0.35 if vert else cy + 30))
        tn = wt(sh, "anotava")
        if t > tn:
            p = panel(W * (0.8 if vert else 0.36), 520 * U, (250, 246, 225, 250), 12, (0, 0, 0, 0)); dd = ImageDraw.Draw(p)
            dd.text((40, 40), "O CADERNINHO", font=font("blk", 46 * U), fill=INK)
            names = ["Murrey — meia, 16", "Gildo — ponta, 15 ?", "Kofi — volante, 16", "Ollie — 9, 15", "Victor — goleiro, 16", "Matic — zagueiro, 17"]
            for i, n in enumerate(names[: int(1 + (t - tn) * 3)]):
                dd.text((40, 120 * U + i * 62 * U), n, font=font("bd", 38 * U), fill=(30, 40, 120))
                dd.line((40, 168 * U + i * 62 * U, p.width - 40, 168 * U + i * 62 * U), fill=(160, 180, 220), width=2)
            paste(img, p, cx if vert else W * 0.72, H * 0.68 if vert else cy + 30, 1, back((t - tn) / 0.35), rot=3)
        pop_text(img, "10 ANOS: ÔNIBUS DE DIA, SUB-16 À NOITE", cx, H * 0.15 if vert else 270, t, 0.1, 44 * U if vert else 58, WHITE, 6)
    elif sc == "rick_call":
        B("night"); ph = icon_phone(W * 0.5 if vert else H * 0.36, "DIRETORIA\nCAMBRIDGE UNITED", t)
        paste(img, ph, cx + 8 * math.sin(t * 40) * (t < 2.5), cy + (80 if vert else 30), 1, back(t / 0.35))
        pop_text(img, "JULHO 2026", cx, H * 0.17 if vert else 270, t, 0.1, 70 * U, AMB, 6)
        if t > wt(sh, "interino"): paste(img, chip("CARGO: TÉCNICO INTERINO", 46, INK, AMB), cx, H * 0.86 if vert else H - 260, 1, back((t - wt(sh, "interino")) / 0.3))
    elif sc == "rick_profile":
        B("blue"); av = avatar("rick", H * (0.4 if vert else 0.75))
        paste(img, av, cx if vert else W * 0.28, H - av.height / 2 - (H * 0.17 if vert else 0))
        p = panel(W * (0.88 if vert else 0.48), 470, (12, 14, 24, 235)); dd = ImageDraw.Draw(p)
        dd.text((40, 30), "PERFIL DO TÉCNICO", font=font("bd", 32), fill=AMB); dd.text((40, 80), "RICK MIGUEL", font=font("blk", 70), fill=WHITE)
        rows = [("IDADE", "34"), ("NACIONALIDADE", "ING / BRA"), ("REPUTAÇÃO", "DESCONHECIDO"), ("ESTILO", "PRESSÃO ALTA"), ("ITEM ESPECIAL", "CADERNINHO")]
        for i, (a, b) in enumerate(rows):
            if t > 0.2 + i * 0.25:
                dd.text((40, 190 + i * 54), a, font=font("bd", 32), fill=(170, 170, 190)); dd.text((p.width - 40, 190 + i * 54), b, font=font("blk", 34), fill=WHITE, anchor="ra")
        paste(img, p, cx if vert else W * 0.7, H * 0.3 if vert else cy + 20, 1, back(t / 0.35))
    elif sc in ("hub", "hub_budget"):
        B("purple")
        tiles = [("ORÇAMENTO", "£180.000", AMB, "cento"), ("FOLHA SALARIAL", "3ª MENOR", WHITE, "terceira"), ("META DA DIRETORIA", "MEIO DA TABELA", WHITE, "diretoria")]
        for i, (a, b, col, wk) in enumerate(tiles):
            t0 = 0.2 + i * 0.3 if sc == "hub" else wt(sh, wk)
            u = (t - t0) / 0.35
            if u <= 0: continue
            p = panel(W * (0.86 if vert else 0.28), 260, (18, 14, 40, 235)); dd = ImageDraw.Draw(p)
            dd.text((36, 34), a, font=font("bd", 32), fill=(190, 180, 230))
            val = b
            if i == 0 and sc == "hub_budget": val = f"£{int(180000 * ease((t - t0) / 0.8)):,}".replace(",", ".")
            f = font("blk", 64);
            while f.getlength(val) > p.width - 60: f = font("blk", f.size - 4)
            dd.text((36, 110), val, font=f, fill=col)
            x = cx if vert else W * (0.2 + i * 0.3); y = H * (0.32 + i * 0.17) if vert else cy + 20
            paste(img, p, x, y, ease(u), 0.7 + 0.3 * back(u))
        if sc == "hub": pop_text(img, "CENTRAL DO CLUBE", cx, H * 0.16 if vert else 250, t, 0, 70 * U, WHITE, 6)
    elif sc == "hub_goal":
        B("dark"); p = panel(W * (0.9 if vert else 0.62), 460, (245, 245, 245, 255), 18, (180, 180, 180, 255))
        paste(img, p, cx, cy, 1)
        tl = wt(sh, "lousa") + 0.2; s = "CHAMPIONS LEAGUE"; n = int(len(s) * clamp((t - tl) / 1.2))
        ImageDraw.Draw(img).text((cx, cy), s[:n], font=font("blk", 104 * U if not vert else 86), fill=(30, 50, 170), anchor="mm")
        if t > wt(sh, "pouquinho") and t < tl: pop_text(img, "HAHA", cx + 420, cy + 260, t, wt(sh, "pouquinho"), 90, AMB, 6, 12)
        paste(img, chip("META DA DIRETORIA: MEIO DA TABELA", 34, WHITE, (90, 90, 100)), cx, cy - 300 * U, 1)
    elif sc == "squad_list":
        B("dark")
        p = panel(W * (0.92 if vert else 0.74), H * (0.62 if vert else 0.7), (14, 16, 24, 240)); dd = ImageDraw.Draw(p)
        cols = [40, int(p.width * 0.5), int(p.width * 0.64), int(p.width * 0.76), int(p.width * 0.88)]
        for c, h_ in zip(cols, ["JOGADOR", "POS", "IDADE", "OVR", "VALOR"]): dd.text((c, 30), h_, font=font("bd", 28), fill=(160, 160, 180))
        off = t * 160
        for i, (n, ps, ag, o, v) in enumerate(SQUAD):
            y = 90 + i * 72 - off
            if y < 80 or y > p.height - 60: continue
            dd.rounded_rectangle((20, y - 8, p.width - 20, y + 56), 14, fill=(30, 32, 44))
            for c, val in zip(cols, [n, ps, str(ag), str(o), v]): dd.text((c, y + 6), val, font=font("blk" if c == cols[3] else "sb", 34), fill=AMB if c == cols[3] else WHITE)
        paste(img, p, cx, cy + 40, 1, back(t / 0.3))
    elif sc in ("squad_kaikai", "squad_bauer", "squad_pelly"):
        k = sc[6:]; B({"kaikai": "amber", "bauer": "blue", "pelly": "green"}[k]); img.alpha_composite(rays(W, H, cx, cy, t))
        card_in(img, k, cx if vert else W * 0.32, cy + (-120 if vert else 20), 470 if vert else 420, t)
        info = {"kaikai": ["O CRAQUE", "66 OVR • 80 RIT"], "bauer": ["O XERIFE", "78 FÍS • 68 DEF"], "pelly": ["O ÍDOLO", "BRAÇO DIREITO DO RICK"]}[k]
        big_lines(img, info, cx if vert else W * 0.68, H * 0.7 if vert else cy - 60, t, 0.3, 84 * U, 1.3, [WHITE, AMB])
    elif sc == "squad_xi":
        img.alpha_composite(Image.new("RGBA", (W, H), (24, 92, 52, 255))); dd = ImageDraw.Draw(img)
        for i in range(0, W, 160): dd.rectangle((i, 0, i + 80, H), fill=(28, 100, 58))
        m = 60; dd.rectangle((m, 120 if not vert else 380, W - m, H - m - (0 if not vert else 300)), outline=(230, 240, 230), width=6)
        names = [("EASTWOOD", 64), ("BENNETT", 63), ("BAUER", 66), ("WATTS", 65), ("McLOUGHLIN", 62), ("PELLY", 64), ("BALL", 63), ("KNIGHT", 65), ("KAIKAI", 66), ("LAVERY", 64), ("APPÉRÉ", 63)]
        if vert: pos = [(0.5, 0.85), (0.15, 0.7), (0.38, 0.73), (0.62, 0.73), (0.85, 0.7), (0.3, 0.55), (0.7, 0.55), (0.5, 0.47), (0.82, 0.36), (0.5, 0.3), (0.18, 0.36)]
        else: pos = [(0.08, 0.55), (0.25, 0.2), (0.22, 0.42), (0.22, 0.68), (0.25, 0.88), (0.42, 0.38), (0.42, 0.72), (0.55, 0.55), (0.75, 0.22), (0.8, 0.55), (0.75, 0.86)]
        for i, ((n, o), (px, py)) in enumerate(zip(names, pos)):
            u = (t - i * 0.08) / 0.3
            if u <= 0: continue
            p = panel(190, 92, (14, 14, 18, 235), 16); pd = ImageDraw.Draw(p)
            pd.text((95, 30), n, font=font("blk", 22), fill=WHITE, anchor="mm"); pd.text((95, 66), str(o), font=font("blk", 30), fill=AMB, anchor="mm")
            paste(img, p, W * px, H * py, ease(u), back(u))
        tb = wt(sh, "banco")
        if t > tb:
            p = panel(W * (0.9 if vert else 0.5), 110, (180, 30, 30, 240)); pd = ImageDraw.Draw(p)
            pd.text((p.width / 2, 55), "BANCO: 3 JOGADORES", font=font("blk", 48), fill=WHITE, anchor="mm")
            paste(img, p, cx, H - (200 if vert else 70), 1, back((t - tb) / 0.3))
        pop_text(img, "4-3-3", cx, H * 0.2 if vert else 270, t, 0, 70, WHITE, 6)
    elif sc == "market":
        B("teal")
        p = panel(W * (0.9 if vert else 0.6), 420, (12, 30, 34, 240)); dd = ImageDraw.Draw(p)
        dd.text((40, 30), "MERCADO • BUSCA", font=font("blk", 46), fill=WHITE)
        for i, (a, b) in enumerate([("PREÇO MÁX.", "£180K"), ("SITUAÇÃO", "SEM CLUBE / EMPRÉSTIMO"), ("PERFIL", "NINGUÉM QUER")]):
            if t > 0.3 + i * 0.4:
                dd.rounded_rectangle((40, 120 + i * 92, p.width - 40, 190 + i * 92), 16, fill=(24, 60, 66))
                dd.text((70, 155 + i * 92), a, font=font("bd", 32), fill=(160, 220, 220), anchor="lm"); dd.text((p.width - 70, 155 + i * 92), b, font=font("blk", 36), fill=AMB, anchor="rm")
        paste(img, p, cx, cy + 20, 1, back(t / 0.35))
    elif sc in ("walk_tomas", "walk_theo", "walk_murrey", "walk_gildo", "walk_kofi", "walk_ollie"):
        key = {"walk_tomas": "f_tomas", "walk_theo": "f_theo", "walk_murrey": "murrey", "walk_gildo": "gildo", "walk_kofi": "f_kofi", "walk_ollie": "f_ollie"}[sc]
        info = {"f_tomas": ("POR", "ZAG", "GRÁTIS"), "f_theo": ("ING", "ATA", "EMPRÉSTIMO"), "murrey": ("ING", "MEI", "DA BASE"), "gildo": ("BRA", "PE", "DA BASE"),
                "f_kofi": ("ING", "VOL", "BASE"), "f_ollie": ("ING", "ATA", "BASE")}[key]
        fast = sc in ("walk_kofi", "walk_ollie")
        img.alpha_composite(Image.new("RGBA", (W, H), (8, 8, 12, 255)))
        sp = 0.45 if fast else 0.8
        # sequência: bandeira -> posição -> clube -> carta
        if t < sp * 3:
            k = int(t / sp); u = (t - k * sp) / sp
            img.alpha_composite(rays(W, H, cx, cy, t, AMB, 10, 40))
            el = [chip(info[0], 120, INK, WHITE), chip(info[1], 120, INK, AMB), crest(320)][k]
            paste(img, el, cx, cy, 1 - clamp((u - 0.75) / 0.25), 0.6 + 0.4 * back(u / 0.5))
        else:
            u = t - sp * 3
            img.alpha_composite(rays(W, H, cx, cy, t, AMB, 16, 90))
            img = flash(img, u, 0, 0.3)
            card_in(img, key, cx, cy + (0 if not vert else -60), 520 if vert else 440, u, 0, spin=False)
            paste(img, chip(info[2], 50, WHITE if info[2] != "GRÁTIS" else INK, RED if "BASE" in info[2] else GREEN), cx + (0 if vert else 380), cy + (450 if vert else -200), 1, back((u - 0.4) / 0.3), rot=8)
            img.alpha_composite(confetti(W, H, u, seed=len(sc)))
    elif sc == "walk_murrey_pre":
        B("purple"); pop_text(img, "REFORÇO #3", cx, cy - 80, t, 0, 120 * U, WHITE, 8); pop_text(img, "CUSTO: £0", cx, cy + 80, t, 0.6, 100 * U, AMB, 8)
    elif sc in ("murrey_stats", "gildo_stats"):
        key = "murrey" if sc == "murrey_stats" else "gildo"; B("purple" if key == "murrey" else "teal")
        card_in(img, key, cx if vert else W * 0.3, cy - (230 if vert else -10), 420 if vert else 400, t, 0, spin=False)
        rows = [("OVERALL", 52, 52), ("POTENCIAL", 91, 91)] if key == "murrey" else [("OVERALL", 48, 48), ("VELOCIDADE", 98, 98), ("POTENCIAL", 89, 89)]
        for i, (a, v, mx) in enumerate(rows):
            t0 = 0.3 + i * 0.6
            u = (t - t0) / 1.0
            if u <= 0: continue
            x = cx - (W * 0.4 if vert else 0) if vert else W * 0.55; y = (H * 0.62 + i * 150) if vert else (300 + i * 170)
            xx = (W * 0.08) if vert else W * 0.55
            ImageDraw.Draw(img).text((xx, y), a, font=font("bd", 40), fill=WHITE)
            paste(img, bar(W * (0.66 if vert else 0.38), 40, v / 100 * ease(u), AMB if a != "OVERALL" else WHITE), xx, y + 60, 1, center=False)
            ImageDraw.Draw(img).text((xx + W * (0.66 if vert else 0.38) + 20, y + 40), str(int(v * ease(u))), font=font("blk", 70), fill=AMB)
    elif sc in ("fixtures_bad", "fixtures_good"):
        good = sc == "fixtures_good"; B("green" if good else "red")
        res = ["V"] * 6 if good else ["D", "E", "D", "V", "D"]
        opp = ["Exeter", "Grimsby", "Oldham", "Swindon", "Bristol R.", "Walsall"] if good else ["Newport", "Rochdale", "Port Vale", "Tranmere", "Barnet"]
        sc_ = ["2-0", "1-0", "3-1", "2-1", "4-1", "1-0"] if good else ["0-2", "1-1", "0-1", "2-0", "1-3"]
        first = wt(sh, "vitoria") if good else wt(sh, "derrota")
        for i, r in enumerate(res):
            t0 = first + i * (0.42 if good else 0.55)
            u = (t - t0) / 0.25
            if u <= 0: continue
            col = {"V": GREEN, "E": (150, 150, 160), "D": RED}[r]
            p = panel(W * (0.86 if vert else 0.42), 96, (14, 14, 18, 235), 18); pd = ImageDraw.Draw(p)
            pd.rounded_rectangle((14, 14, 82, 82), 14, fill=col); pd.text((48, 48), r, font=font("blk", 46), fill=WHITE, anchor="mm")
            pd.text((110, 48), f"Cambridge {sc_[i]} {opp[i]}", font=font("bd", 38), fill=WHITE, anchor="lm")
            x = cx if vert else (W * 0.27 if i < 3 else W * 0.73); y = (H * 0.3 + i * 115) if vert else (290 + (i % 3) * 120)
            paste(img, p, x, y, 1, back(u))
        if not good and t > wt(sh, "vigesimo"):
            paste(img, chip("20º LUGAR", 80, WHITE, RED), cx, H * 0.88 if vert else H - 300, 1, back((t - wt(sh, "vigesimo")) / 0.3), rot=-4)
            img = shake(img, t, wt(sh, "vigesimo"), 16)
        if good and t > wt(sh, "seis"): paste(img, chip("6 SEGUIDAS!", 90, INK, AMB), cx, H * 0.86 if vert else H - 300, 1, back((t - wt(sh, "seis")) / 0.3), rot=-4)
    elif sc == "headline_out":
        B("night")
        paste(img, newspaper(W * (0.88 if vert else 0.5), "SETEMBRO 2026", "O MOTORISTA DURA ATÉ O NATAL?", "Cambridge em 20º"), cx + (0 if vert else 330), H * 0.58 if vert else cy + 40, 1, back((t - wt(sh, "jornal")) / 0.4), rot=(1 - ease((t - wt(sh, "jornal")) / 0.4)) * 300)
        b = panel(W * (0.9 if vert else 0.42), 150, (250, 250, 250, 255), 6, (0, 0, 0, 0)); ImageDraw.Draw(b).text((b.width / 2, 75), "WE WANT A REAL MANAGER", font=font("blk", 46), fill=INK, anchor="mm")
        paste(img, b, cx - (0 if vert else 470), H * 0.26 if vert else 330, 1, back(t / 0.35), rot=-4 + 2 * math.sin(t * 3))
    elif sc in ("assist_pre", "assist"):
        if sc == "assist_pre":
            lance(img, L.ambient, t + 10, d, "CAMBRIDGE 0 x 0 ACCRINGTON")
            if t > wt(sh, "murrey"): paste(img, chip("ENTRA MURREY • 16 ANOS", 48, INK, AMB), cx, H * 0.7 if vert else H - 300, 1, back((t - wt(sh, "murrey")) / 0.3))
        else:
            tl = min(2.2, 8 * 0.3) + 1.3 + 1.1 + 0.4
            lance(img, L.assist, t + 0.8, 8, "CAMBRIDGE 0 x 0 ACCRINGTON" if t + 0.8 < tl else "CAMBRIDGE 1 x 0 ACCRINGTON")
            if t > wt(sh, "letra") - 0.2: pop_text(img, "DE LETRA!", cx, H * 0.42, t, wt(sh, "letra") - 0.2, 140 if not vert else 120, AMB, 10, -4)
    elif sc == "tactics":
        img.alpha_composite(Image.new("RGBA", (W, H), (24, 92, 52, 255))); dd = ImageDraw.Draw(img)
        for i in range(0, W, 160): dd.rectangle((i, 0, i + 80, H), fill=(28, 100, 58))
        u = ease((t - wt(sh, "marcacao")) / 0.8); k = ease((t - wt(sh, "kaikai")) / 0.8)
        if vert: base = [(0.5, 0.86), (0.18, 0.72), (0.4, 0.74), (0.6, 0.74), (0.82, 0.72), (0.35, 0.56), (0.65, 0.56), (0.5, 0.5), (0.8, 0.36), (0.5, 0.32), (0.2, 0.36)]
        else: base = [(0.08, 0.55), (0.25, 0.2), (0.22, 0.42), (0.22, 0.68), (0.25, 0.88), (0.4, 0.38), (0.4, 0.72), (0.5, 0.55), (0.66, 0.25), (0.7, 0.55), (0.66, 0.85)]
        for i, (px, py) in enumerate(base):
            if i:
                if vert: py -= 0.08 * u
                else: px += 0.12 * u
            if i == 8:
                if vert: px += 0.1 * k; py -= 0.05 * k
                else: py -= 0.04 * k; px += 0.1 * k
            x, y = W * px, H * py; r = 34
            dd.ellipse((x - r, y - r, x + r, y + r), fill=AMB if i != 8 else WHITE, outline=INK, width=5)
            if i == 8 and t > wt(sh, "kaikai"): paste(img, chip("KAIKAI", 30, INK, WHITE), x, y - 70)
        if t > wt(sh, "pressionando"):
            a = ease((t - wt(sh, "pressionando")) / 0.5)
            for j in range(3):
                if vert: x0, y0 = W * (0.25 + j * 0.25), H * 0.28; dd.line((x0, y0, x0, y0 - 180 * a), fill=WHITE, width=12)
                else: x0, y0 = W * 0.8, H * (0.25 + j * 0.3); dd.line((x0, y0, x0 + 260 * a, y0), fill=WHITE, width=12)
            pop_text(img, "PRESSÃO!", cx, H * 0.15 if vert else 270, t, wt(sh, "pressionando"), 110, RED, 8, -3)
        else:
            pop_text(img, "OUTUBRO: RICK MUDA TUDO", cx, H * 0.15 if vert else 270, t, 0, 60 if vert else 80, WHITE, 8)
    elif sc == "kaikai_goal":
        tsh = min(1.6, 6 * 0.25) + 1.2 + 0.6
        tt = t + 1.0
        lance(img, L.golaco, tt, 6, "CAMBRIDGE 2 x 0 BRISTOL ROVERS", tsh + 0.4, "HAT-TRICK!", AMB)
        paste(img, chip("KAIKAI: 3 GOLS", 50, INK, AMB), cx, H * 0.75 if vert else H - 300, 1, back((t - 0.3) / 0.3))
    elif sc == "table_up":
        B("green"); u = ease((t - 0.2) / 1.6); pos = 20 - 12 * u
        p = panel(W * (0.86 if vert else 0.44), 640, (12, 30, 18, 235)); pd = ImageDraw.Draw(p)
        for r in range(9):
            place = int(pos) - 4 + r; yy = 40 + r * 64 + (pos - int(pos)) * -64
            if place < 1 or place > 24: continue
            pd.text((40, yy), f"{place}º", font=font("bd", 34), fill=(180, 220, 190))
        yy = 40 + 4 * 64
        pd.rounded_rectangle((20, yy - 8, p.width - 20, yy + 52), 16, fill=AMB); pd.text((40, yy), f"{round(pos)}º  CAMBRIDGE UNITED", font=font("blk", 36), fill=INK)
        paste(img, p, cx if vert else W * 0.3, H * 0.45 if vert else cy + 30, 1, back(t / 0.3))
        pop_text(img, "20º → 8º", cx if vert else W * 0.72, H * 0.15 if vert else 400, t, 0.2, 120, WHITE, 8)
        if t > wt(sh, "copa"): paste(img, chip("FA CUP: PASSOU DE FASE ✓", 50, INK, AMB), cx if vert else W * 0.72, H * 0.86 if vert else 580, 1, back((t - wt(sh, "copa")) / 0.3))
    elif sc in ("base_night", "base_race"):
        B("night"); dd = ImageDraw.Draw(img)
        dd.rectangle((0, H * 0.62, W, H), fill=(26, 80, 46)); [dd.line((x, H * 0.62, x, H), fill=(80, 80, 90), width=4) for x in range(0, W, 60)]
        dd.line((0, H * 0.62, W, H * 0.62), fill=(140, 140, 150), width=8)
        for x in (W * 0.15, W * 0.85): dd.rectangle((x - 8, H * 0.15, x + 8, H * 0.62), fill=(70, 70, 80)); img.alpha_composite(rays(W, H, x, H * 0.15, 0.3, (255, 255, 230), 1, 0))
        if sc == "base_night":
            x = -300 + (cx + 300) * ease(t / 1.2)
            paste(img, gray("gildo", H * 0.3) if False else avatar("gildo", H * 0.42), x, H * 0.62 - H * 0.21 + 30)
            paste(img, icon_pizza(240), x + 230, H * 0.5, 1, 1, -8)
            pop_text(img, "A MAIOR APOSTA DO RICK VEIO DE BIKE", cx, H * 0.15 if vert else 270, t, 0, 56 if vert else 72, WHITE, 8)
        else:
            tr = wt(sh, "corrida"); u = clamp((t - tr) / 2.2)
            img.alpha_composite(speedlines(W, H, t, 25) if u > 0 else Image.new("RGBA", (W, H)))
            ys = H * 0.55
            paste(img, chip("PONTA DO SUB-18", 36, WHITE, (60, 60, 70)), W * 0.1 + W * 0.7 * ease(u) * 0.86, ys - 200)
            paste(img, avatar("gildo", H * 0.3), W * 0.1 + W * 0.7 * ease(u), ys - 40)
            if t > wt(sh, "chinelo") - 0.3: pop_text(img, "DE CHINELO!", cx, H * 0.2 if vert else 270, t, wt(sh, "chinelo") - 0.3, 130, AMB, 10, -5)
            elif t > wt(sh, "cinco"): pop_text(img, "+5 METROS", cx, H * 0.2 if vert else 270, t, wt(sh, "cinco"), 120, WHITE, 10, -3)
    elif sc == "new_base":
        B("teal"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 40))
        pop_text(img, "NOVOS NA BASE", cx, cy - 60, t, 0, 120 * U, WHITE, 8); pop_text(img, "+2", cx, cy + 100, t, 0.4, 160, AMB, 10)
    elif sc == "drama_phone":
        B("purple")
        ph = Image.new("RGBA", (int(W * (0.62 if vert else 0.3)), int(W * (1.2 if vert else 0.58))), (0, 0, 0, 0)); pd = ImageDraw.Draw(ph)
        pd.rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), 50, fill=INK, outline=(90, 90, 100), width=8)
        pd.rounded_rectangle((20, 20, ph.width - 20, ph.height * 0.6), 30, fill=(40, 30, 70))
        pd.text((40, 40), "AO VIVO", font=font("blk", 34), fill=RED)
        pd.text((ph.width / 2, ph.height * 0.66), "murrey_10", font=font("blk", 44), fill=WHITE, anchor="mm")
        pd.text((ph.width / 2, ph.height * 0.74), "Torneio • prêmio £1.000", font=font("sb", 34), fill=(200, 200, 210), anchor="mm")
        paste(ph, icon_pad(ph.width * 0.6), ph.width / 2, ph.height * 0.33)
        paste(img, ph, cx - (0 if vert else 330), cy + (60 if vert else 30), 1, back(t / 0.35), rot=-4)
        if t > wt(sh, "descobre"): paste(img, stamp("FALTOU AO TREINO", 70), cx + (0 if vert else 380), H * 0.18 if vert else cy, 1, back((t - wt(sh, "descobre")) / 0.3), rot=-10)
    elif sc == "drama_bench":
        B("dark"); paste(img, gray("murrey", H * (0.5 if vert else 0.8)), cx, H - H * (0.25 if vert else 0.4))
        paste(img, chip("NO BANCO", 90, WHITE, RED), cx, H * 0.2 if vert else 270, 1, back(t / 0.3), rot=-5)
    elif sc in ("boxing", "boxing_sub"):
        lance(img, L.ambient, t + 30, d, "CAMBRIDGE 0 x 1 COLCHESTER")
        paste(img, chip("70'", 48, WHITE, RED), cx, H * 0.27 if vert else 290)
        if sc == "boxing": paste(img, chip("BOXING DAY • ABBEY STADIUM LOTADO", 40, INK, AMB), cx, H * 0.64 if vert else H - 300, 1, back(t / 0.3))
        else:
            p = panel(W * (0.86 if vert else 0.42), 330, (10, 10, 12, 245)); pd = ImageDraw.Draw(p)
            pd.text((40, 40), "SUBSTITUIÇÃO", font=font("bd", 36), fill=(160, 160, 160)); pd.text((40, 100), "ENTRA", font=font("blk", 40), fill=GREEN)
            pd.text((40, 150), "MURREY", font=font("blk", 100), fill=(255, 210, 60))
            paste(img, p, cx, cy + 40, 1, back(t / 0.3))
            tf = wt(sh, "ninguem")
            if t > tf: paste(img, chip("\"AQUI NINGUÉM É MAIOR QUE O CLUBE\"", 40, INK, WHITE), cx, H * 0.78 if vert else H - 250, 1, back((t - tf) / 0.3))
    elif sc in ("murrey_goal", "murrey_goal_x"):
        if sc == "murrey_goal":
            tsh = min(1.6, 6 * 0.25) + 1.2 + 0.6
            lance(img, L.golaco, t * (tsh / max(d, 1)) * 1.0 + 0.0, 6, "CAMBRIDGE 0 x 1 COLCHESTER")
            paste(img, chip("88'", 48, WHITE, RED), cx, H * 0.27 if vert else 290)
        else:
            B("amber"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 16, 90)); img.alpha_composite(confetti(W, H, t))
            img = flash(img, t, 0, 0.3)
            pop_text(img, "GOLAÇO!", cx, cy - 60, t, 0, 220 if not vert else 170, WHITE, 14, -4)
            paste(img, chip("CAMBRIDGE 1 x 1 COLCHESTER", 54, WHITE, INK), cx, cy + 140, 1, back((t - 0.3) / 0.3))
            img = shake(img, t, 0, 26, 0.6)
    elif sc == "hug":
        B("amber"); img.alpha_composite(confetti(W, H, t + 2))
        r = avatar("rick", H * (0.42 if vert else 0.7)); m = avatar("murrey", H * (0.38 if vert else 0.64))
        paste(img, r, cx - (180 if vert else 260), H - r.height / 2 - (H * 0.12 if vert else 0)); paste(img, m, cx + (180 if vert else 260), H - m.height / 2 - (H * 0.12 if vert else 0))
        pop_text(img, "1º GOL PROFISSIONAL", cx, H * 0.2 if vert else 270, t, 0, 70 if vert else 90, WHITE, 8)
    elif sc == "ovr_up":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t, AMB, 12, 60))
        tu = wt(sh, "cinquenta", 1)
        card_in(img, "murrey", cx if vert else W * 0.3, cy - (200 if vert else -20), 440, t, 0, 57 if t > tu else 52, spin=False)
        if t > tu: img = flash(img, t, tu); pop_text(img, "52 → 57", cx if vert else W * 0.3, H * 0.15 if vert else 270, t, tu, 100, GREEN, 8)
        tp = wt(sh, "setimo")
        if t > tp: paste(img, chip("7º • ZONA DE PLAY-OFF", 56, INK, GREEN), cx if vert else W * 0.7, H * 0.82 if vert else cy, 1, back((t - tp) / 0.3))
    elif sc == "contract":
        B("dark"); p = panel(W * (0.86 if vert else 0.5), 520, (245, 242, 232, 255), 14, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((50, 50), "CONTRATO", font=font("blk", 56), fill=INK); pd.text((50, 150), "Rick Miguel", font=font("bd", 46), fill=INK)
        pd.text((50, 260), "TÉCNICO INTERINO", font=font("blk", 60), fill=INK)
        u = ease((t - wt(sh, "interino")) / 0.4); pd.line((40, 300, 40 + 660 * u, 300), fill=RED, width=12)
        if t > wt(sh, "interino") + 0.5: pd.text((50, 360), "TÉCNICO PRINCIPAL", font=font("blk", 60), fill=(20, 130, 60))
        paste(img, p, cx, cy, 1, back(t / 0.3), rot=-2)
    elif sc in ("email", "email_x"):
        B("night")
        p = panel(W * (0.9 if vert else 0.56), 470, (250, 250, 252, 255), 22, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((40, 30), "Caixa de entrada • 1 nova", font=font("bd", 32), fill=(110, 110, 120))
        pd.text((40, 100), "De: clube da Premier League", font=font("sb", 36), fill=(60, 60, 70)); pd.text((40, 160), "Assunto: proposta por MURREY", font=font("blk", 42), fill=INK)
        if sc == "email_x" or t > wt(sh, "oferece"):
            pd.text((40, 260), "£1.200.000", font=font("blk", 120), fill=(20, 130, 60))
        paste(img, p, cx, cy + (0 if vert else 20), 1, back(t / 0.35) if sc == "email" else 1)
        if sc == "email_x": pop_text(img, "≈ 7x O ORÇAMENTO", cx, H * 0.2 if vert else 270, t, 0, 90, AMB, 8, -3); img = shake(img, t, 0, 14)
    elif sc == "ab":
        dd = ImageDraw.Draw(img)
        if vert:
            dd.rectangle((0, 0, W, H / 2), fill=(26, 110, 60)); dd.rectangle((0, H / 2, W, H), fill=(150, 30, 30))
            pa, pb = (cx, H * 0.24), (cx, H * 0.6)
        else:
            dd.rectangle((0, 0, W / 2, H), fill=(26, 110, 60)); dd.rectangle((W / 2, 0, W, H), fill=(150, 30, 30))
            pa, pb = (W * 0.25, cy), (W * 0.75, cy)
        ta, tb = wt(sh, "comenta"), wt(sh, "comenta", 1)
        for (x, y), L_, s1, s2, t0 in ((pa, "A", "VENDER O MURREY", "£1,2 MI • 3 REFORÇOS", 0), (pb, "B", "SEGURAR O MURREY", "ELENCO CURTO • TALENTO FICA", 0)):
            paste(img, text_el(L_, font("blk", 240), WHITE, 10), x, y - 170, 1, 1 + 0.05 * math.sin(t * 4))
            paste(img, text_el(s1, font("blk", 66), WHITE, 6), x, y + 20)
            paste(img, text_el(s2, font("bd", 40), (240, 240, 240), 4), x, y + 95)
        hl = 0 if ta <= t < tb else 1 if tb <= t < tb + 2.5 else None
        if hl is not None:
            x, y = (pa, pb)[hl]; paste(img, chip("COMENTE " + "AB"[hl], 60, INK, WHITE), x, y + 190, 1, back(((t - (ta, tb)[hl])) / 0.3))
        if not vert: paste(img, card("murrey", 200, 57), cx, 330, 1, 1 + 0.04 * math.sin(t * 3))
    elif sc == "end":
        B("amber"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 60))
        paste(img, crest(300 * U), cx, cy - 160 * U, 1, back(t / 0.4))
        pop_text(img, "INSCREVA-SE", cx, cy + 90 * U, t, 0.3, 120 * U, WHITE, 10)
        paste(img, chip("PRÓXIMO: EPISÓDIO 2", 50, WHITE, INK), cx, cy + 230 * U, 1, back((t - 0.8) / 0.3))
    else:
        B("dark"); pop_text(img, sc, cx, cy, t, 0, 80)
    return img


def frame(T, W=1920, H=1080):
    s = SHOTS[-1]; i = len(SHOTS) - 1
    for k, sh in enumerate(SHOTS):
        if sh["t0"] <= T < sh["t1"]: s, i = sh, k; break
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img = scene(img, s, T - s["t0"])
    if i > 0 and T - s["t0"] < 0.18:  # transição curta: zoom/whip
        u = (T - s["t0"]) / 0.18
        prev = scene(Image.new("RGBA", (W, H), (0, 0, 0, 255)), SHOTS[i - 1], T - SHOTS[i - 1]["t0"])
        dx = int(W * u)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255)); canvas.alpha_composite(prev, (-dx, 0)); canvas.alpha_composite(img, (W - dx, 0)); img = canvas
    hud(img, s["scene"], T - s["t0"])
    topic(img, s["scene"], T - s["t0"])
    caption(img, T)
    return img.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "shots":
        for s in SHOTS: print(f"{s['t0']:7.2f} {s['t1']:7.2f} {s['scene']}")
    elif sys.argv[1] == "preview":
        W, H = int(sys.argv[2]), int(sys.argv[3])
        for x in sys.argv[4:]:
            frame(float(x), W, H).save(f"/tmp/p2_{W}_{float(x):06.1f}.jpg", quality=85)
    elif sys.argv[1] == "render":
        i, n = int(sys.argv[2]), int(sys.argv[3]); W, H = 1920, 1080
        nf = int(TOTAL * FPS); a, b = nf * i // n, nf * (i + 1) // n
        out = f"{D}/c2_{i}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", out + ".tmp.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame(f / FPS, W, H).tobytes())
        p.stdin.close(); p.wait()
        if p.returncode == 0: os.replace(out + ".tmp.mp4", out)
