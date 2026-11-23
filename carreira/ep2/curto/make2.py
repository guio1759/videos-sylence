"""Ep.2 — ritmo rápido, telas de jogo animadas, HUD, legenda palavra a palavra.
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



# ---------- Ep.2: estado do clube (HUD) por cena ----------
ORDER = [s["scene"] for s in SHOTS]
def _first(sc): return next((i for i, s in enumerate(SHOTS) if s["scene"] == sc), 10 ** 6)
POS_STEPS = [("recap", 7), ("lg_run", 4), ("cr_run", 9), ("fs_run", 8), ("fs_ollie_x", 7), ("wb_whistle", 0)]
def pos_of(i):
    p = None
    for sc, v in POS_STEPS:
        if i >= _first(sc): p = v
    return p
UP = _first("wb_whistle")

TOPIC = {"recap": "ATÉ AQUI", "recap_base": "ATÉ AQUI", "recap_hud": "ATÉ AQUI", "vote_card": "VOCÊS ESCOLHERAM", "vote_comment": "OS MAIS CURTIDOS",
         "vote_reply": "A RESPOSTA", "vote_murrey": "EFEITO MURREY", "vote_kaikai": "EFEITO MURREY", "vote_cost": "O PREÇO",
         "jan_hub": "JANELA DE JANEIRO", "jan_need": "JANELA DE JANEIRO", "jan_arlo": "REFORÇO", "jan_theo": "JANELA DE JANEIRO", "jan_out": "JANELA DE JANEIRO",
         "jan_gildo_pre": "A CONTRATAÇÃO", "jan_gildo": "A CONTRATAÇÃO", "jan_contract": "A CONTRATAÇÃO", "jan_bike": "A ÚLTIMA ENTREGA",
         "fa_draw": "COPA DA INGLATERRA", "fa_draw_x": "COPA DA INGLATERRA", "fa_twist": "COPA DA INGLATERRA", "fa_stadium": "TOTTENHAM x CAMBRIDGE",
         "fa_speech": "O TÚNEL", "fa_goal1": "TOTTENHAM x CAMBRIDGE", "fa_sub": "INTERVALO", "fa_gildo_run": "61 MINUTOS", "fa_murrey_goal": "61 MINUTOS",
         "fa_murrey_cele": "O RECADO", "fa_equal": "89 MINUTOS", "fa_pens": "PÊNALTIS", "fa_miss": "PÊNALTIS", "fa_hug": "PÊNALTIS", "fa_viral": "OS ENTREGADORES",
         "lg_back": "FEVEREIRO", "lg_run": "FEVEREIRO", "lg_gildo_goal": "1º GOL DO GILDO", "lg_kofi": "A VOLTA DO KOFI", "lg_kofi2": "A VOLTA DO KOFI",
         "lg_ollie": "SUB-18", "lg_table": "A CIDADE ACREDITA", "cr_march": "MARÇO", "cr_injury": "LESÃO", "cr_run": "MARÇO", "cr_paper": "CRISE",
         "cr_meeting": "ULTIMATO", "cr_depot": "A GARAGEM", "cr_pelly": "O VESTIÁRIO", "cr_pelly_x": "O VESTIÁRIO", "ev_title": "EVOLUÇÃO DA BASE",
         "ev_murrey": "EVOLUÇÃO DA BASE", "ev_gildo": "EVOLUÇÃO DA BASE", "ev_kofi": "EVOLUÇÃO DA BASE", "ev_ollie": "EVOLUÇÃO DA BASE",
         "gh_dinner": "JANTAR", "gh_mum": "JANTAR", "gh_dad": "A PERGUNTA", "gh_rick": "A PERGUNTA", "fs_return": "ABRIL", "fs_run": "ABRIL",
         "fs_race": "ÚLTIMA RODADA", "fs_tense": "ÚLTIMA RODADA", "fs_ollie": "ÚLTIMA RODADA", "fs_ollie_x": "PLAY-OFF!", "fs_table": "PLAY-OFF!",
         "sf_draw": "SEMIFINAL", "sf_flash": "A VINGANÇA", "sf_leg1": "SEMIFINAL", "sf_leg1b": "ABBEY STADIUM", "sf_leg2": "SEMIFINAL", "sf_93": "MINUTO 93",
         "sf_murrey_pen": "MINUTO 93", "sf_goal": "WEMBLEY!", "wb_arrive": "FINAL EM WEMBLEY", "wb_mum": "FINAL EM WEMBLEY", "wb_tunnel": "O TÚNEL",
         "wb_tunnel2": "O TÚNEL", "wb_goal_w": "FINAL EM WEMBLEY", "wb_et": "PRORROGAÇÃO", "wb_ball": "MINUTO 118", "wb_choice": "MINUTO 118",
         "wb_pass": "MINUTO 118", "wb_goal": "MINUTO 118", "wb_whistle": "ACESSO!", "wb_hist": "37 ANOS", "wb_players": "ACESSO!", "wb_rick": "A PRIMEIRA LINHA",
         "dl_bus": "A LIGAÇÃO", "dl_hud": "LEAGUE ONE", "dl_call": "A LIGAÇÃO", "dl_family": "A FAMÍLIA", "dl_ab": "A PROPOSTA", "dl_vote": "VOCÊ DECIDE",
         "end": "PRÓXIMO EPISÓDIO"}

NOHUD = ("ff_wembley", "ff_rick", "ff_cut", "end")


def hud(img, scene, t):
    W, H = img.size; vert = H > W
    if scene in NOHUD: return
    i = ORDER.index(scene) if scene in ORDER else 0
    up = i >= UP; pos = pos_of(i); budget = "£600K" if i >= _first("dl_hud") else "£180K"
    league = "LEAGUE ONE" if up else "LEAGUE TWO"
    if vert:
        y = 70; h = 86
        p = panel(W - 60, h, (12, 12, 16, 220), 24); img.alpha_composite(p, (30, y))
        paste(img, crest(64), 80, y + h / 2)
        ImageDraw.Draw(img).text((125, y + h / 2), "CAMBRIDGE", font=font("blk", 30), fill=WHITE, anchor="lm")
        paste(img, chip("SUBIU!" if up else (f"{pos}º" if pos else "-"), 30, INK, GREEN if up else AMB), W - 250, y + h / 2)
        paste(img, chip(budget, 30, WHITE, (60, 60, 70)), W - 110, y + h / 2)
        return
    h = 64; p = panel(W - 40, h, (12, 12, 16, 215), 22); img.alpha_composite(p, (20, 16))
    paste(img, crest(52), 58, 16 + h / 2)
    d = ImageDraw.Draw(img)
    d.text((96, 16 + h / 2), "CAMBRIDGE UNITED", font=font("blk", 28), fill=WHITE, anchor="lm")
    x = 420
    for s, bgc, fg in ((league, (60, 60, 70), WHITE), (("ACESSO ✓" if up else f"POSIÇÃO {pos}º"), GREEN if up else AMB, INK), (f"ORÇAMENTO {budget}", (60, 60, 70), WHITE)):
        c = chip(s, 24, fg, bgc); img.alpha_composite(c, (x, 16 + h // 2 - c.height // 2)); x += c.width + 10
    steps = ["4ª", "3ª", "2ª", "PREMIER", "CHAMPIONS"]; cur = 1 if up else 0
    x0 = W - 640
    d.text((x0, 16 + h / 2), "RUMO À", font=font("bd", 20), fill=(190, 190, 190), anchor="lm")
    for k, s in enumerate(steps):
        on = k == cur; done = k < cur
        c = chip(s + (" ✓" if done else ""), 20, INK if on else (200, 200, 200), AMB if on else GREEN if done else (50, 50, 58)); img.alpha_composite(c, (x0 + 90 + k * 104, 16 + h // 2 - c.height // 2))


def topic(img, scene, t):
    W, H = img.size; vert = H > W
    s = TOPIC.get(scene)
    if not s: return
    el = tag_box(s, 50 if vert else 40)
    paste(img, el, W / 2, (250 if vert else 140), 1, 0.6 + 0.4 * back(t / 0.35), rot=-2)


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


# ---------- adversários e lances ----------
for k, kit in {"TOT": ((245, 245, 245), (20, 30, 70)), "WAL": ((210, 30, 40), (245, 245, 245)), "SAL": ((235, 235, 235), (200, 30, 40)),
               "BRO": ((245, 245, 245), (20, 20, 22)), "BAR": ((240, 240, 240), (30, 60, 160))}.items():
    L.SPR[k] = L.make_player(kit[0], kit[1], kit[1])


def opp_fn(fn, opp):
    def f(t, D):
        teams, ball, cam, labels, rings = fn(t, D)
        teams = [((opp if tm not in ("CAM",) else tm), dd, g) for tm, dd, g in teams]
        return teams, ball, cam, labels, rings
    return f


def amb(opp): return functools.partial(L.ambient, opp=opp)
def goal_for(opp, name):
    def f(t, D):
        teams, ball, cam, labels, rings = opp_fn(L.golaco, opp)(t, D)
        return teams, ball, cam, [(name, p, a, b, c) for _, p, a, b, c in labels], rings
    return f
def goal_against(opp):
    def f(t, D):
        teams, ball, cam, labels, rings = opp_fn(L.crewe, opp)(t, D)
        return teams, ball, cam, [], []
    return f
def assist_play(opp):
    def f(t, D):
        teams, ball, cam, labels, rings = opp_fn(L.assist, opp)(t, D)
        return teams, ball, cam, [], rings
    return f
TSH = min(1.6, 6 * 0.25) + 1.2 + 0.6   # instante do chute no golaco (D=6)


def gol_screen(img, t, txt, score, col="amber"):
    W, H = img.size; vert = H > W; cx, cy = W / 2, H / 2
    img.alpha_composite(bg(W, H, col, t)); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 16, 90)); img.alpha_composite(confetti(W, H, t))
    img = flash(img, t, 0, 0.3)
    sz = 200 if not vert else 150
    while font("blk", sz).getlength(txt) > W * 0.9: sz -= 6
    pop_text(img, txt, cx, cy - 60, t, 0, sz, WHITE, 14, -4)
    if score: paste(img, chip(score, 54, WHITE, INK), cx, cy + 140, 1, back((t - 0.3) / 0.3))
    return shake(img, t, 0, 26, 0.6)


def fixtures(img, sh, t, res, opp, scr, first_word, step=0.45):
    W, H = img.size; vert = H > W; cx = W / 2
    first = wt(sh, first_word)
    for i, r in enumerate(res):
        u = (t - first - i * step) / 0.25
        if u <= 0: continue
        col = {"V": GREEN, "E": (150, 150, 160), "D": RED}[r]
        p = panel(W * (0.86 if vert else 0.42), 96, (14, 14, 18, 235), 18); pd = ImageDraw.Draw(p)
        pd.rounded_rectangle((14, 14, 82, 82), 14, fill=col); pd.text((48, 48), r, font=font("blk", 46), fill=WHITE, anchor="mm")
        pd.text((110, 48), f"Cambridge {scr[i]} {opp[i]}", font=font("bd", 38), fill=WHITE, anchor="lm")
        x = cx if vert else (W * 0.27 if i < 3 else W * 0.73); y = (H * 0.3 + i * 115) if vert else (290 + (i % 3) * 120)
        paste(img, p, x, y, 1, back(u))


def evo(img, t, key, a, b, why, col):
    W, H = img.size; vert = H > W; cx, cy = W / 2, H / 2
    img.alpha_composite(bg(W, H, col, t)); img.alpha_composite(rays(W, H, cx, cy, t, AMB, 12, 60))
    tu = 0.9; o = a if t < tu else b
    card_in(img, key, cx if vert else W * 0.3, cy - (200 if vert else -20), 440, t, 0, o, spin=False)
    if t > tu:
        img = flash(img, t, tu)
        pop_text(img, f"{a} → {b}", cx if vert else W * 0.7, H * 0.6 if vert else cy - 120, t, tu, 120, GREEN, 8)
        pop_text(img, f"+{b - a}", cx if vert else W * 0.7, H * 0.68 if vert else cy + 40, t, tu + 0.2, 110, AMB, 8)
        paste(img, chip(why, 40, INK, WHITE), cx if vert else W * 0.7, H * 0.76 if vert else cy + 190, 1, back((t - tu - 0.4) / 0.3))
    return img


def two_av(img, k1, k2, t, txt=None):
    W, H = img.size; vert = H > W; cx = W / 2
    a = avatar(k1, H * (0.42 if vert else 0.7)); b = avatar(k2, H * (0.38 if vert else 0.64))
    paste(img, a, cx - (200 if vert else 300), H - a.height / 2 - (H * 0.12 if vert else 0), ease(t / 0.3))
    paste(img, b, cx + (200 if vert else 300), H - b.height / 2 - (H * 0.12 if vert else 0), ease((t - 0.15) / 0.3))
    if txt: paste(img, chip(txt, 40 if vert else 44, INK, WHITE), cx, H * (0.3 if vert else 0.2), 1, back((t - 0.4) / 0.3), rot=-2)


def notebook(w, h, lines, n_show, strike=0.0):
    p = panel(w, h, (250, 246, 225, 250), 12, (0, 0, 0, 0)); dd = ImageDraw.Draw(p); U = h / 520
    dd.text((40, 30), "O CADERNINHO", font=font("blk", 44 * U), fill=INK)
    for i, n in enumerate(lines[:n_show]):
        y = 110 * U + i * 70 * U
        dd.text((40, y), n, font=font("bd", 38 * U), fill=(30, 40, 120))
        dd.line((40, y + 52 * U, w - 40, y + 52 * U), fill=(160, 180, 220), width=2)
        if i == 0 and strike > 0: dd.line((30, y + 24 * U, 30 + (w - 60) * strike, y + 24 * U), fill=RED, width=10)
    return p


GOALS = ["1. Sair da 4ª divisão", "2. Subir pra 2ª", "3. Premier League", "4. CHAMPIONS LEAGUE"]


def phone_call(w, name, sub, t, col=(20, 110, 60)):
    w = int(w); h = int(w * 2.0); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, h), int(w * 0.14), fill=INK, outline=(90, 90, 100), width=8)
    d.rounded_rectangle((18, 18, w - 18, h - 18), int(w * 0.11), fill=(28, 30, 40))
    d.text((w / 2, h * 0.16), "chamada recebida", font=font("md", w * 0.07), fill=(190, 190, 200), anchor="mm")
    r = w * 0.2; d.ellipse((w / 2 - r, h * 0.36 - r, w / 2 + r, h * 0.36 + r), fill=col)
    d.text((w / 2, h * 0.36), "+55", font=font("blk", w * 0.13), fill=WHITE, anchor="mm")
    d.text((w / 2, h * 0.55), name, font=font("blk", w * 0.1), fill=WHITE, anchor="mm")
    d.text((w / 2, h * 0.62), sub, font=font("md", w * 0.065), fill=(190, 190, 200), anchor="mm")
    for x, c in ((0.27, RED), (0.73, GREEN)):
        rr = w * 0.11 * (1 + 0.08 * math.sin(t * 10)); cxx, cyy = w * x, h * 0.84
        d.ellipse((cxx - rr, cyy - rr, cxx + rr, cyy + rr), fill=c)
    return im


def comment_card(w, net, user, text, likes, col):
    p = panel(int(w), 230, (250, 250, 252, 255), 26, (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((26, 26, 150, 70), 16, fill=col); d.text((88, 48), net, font=font("blk", 26), fill=WHITE, anchor="mm")
    d.ellipse((30, 96, 110, 176), fill=(200, 200, 210)); d.text((70, 136), user[0].upper(), font=font("blk", 44), fill=INK, anchor="mm")
    d.text((135, 100), user, font=font("bd", 36), fill=(90, 90, 100)); d.text((135, 145), text, font=font("blk", 64), fill=INK)
    d.text((p.width - 40, 160), f"{likes} curtida", font=font("blk", 40), fill=RED, anchor="ra")
    return p


def pens_board(w, ours, theirs, n_show):
    p = panel(int(w), 330, (12, 12, 18, 240)); d = ImageDraw.Draw(p)
    for row, (nm, seq) in enumerate((("TOTTENHAM", theirs), ("CAMBRIDGE", ours))):
        y = 80 + row * 150
        d.text((40, y), nm, font=font("blk", 46), fill=WHITE, anchor="lm")
        for k, v in enumerate(seq[:n_show]):
            x = w * 0.5 + k * 90; c = GREEN if v else RED
            d.ellipse((x - 32, y - 32, x + 32, y + 32), fill=c); d.text((x, y), "✓" if v else "✗", font=font("blk", 36), fill=WHITE, anchor="mm")
    return p


def wembley_bg(img, t):
    W, H = img.size; d = ImageDraw.Draw(img)
    img.alpha_composite(bg(W, H, "night", t))
    cx = W / 2; base = H * 0.72; r = min(W, H) * 0.55
    d.rectangle((0, base, W, H), fill=(26, 80, 46))
    d.arc((cx - r, base - r * 1.2, cx + r, base + r * 1.2), 180, 360, fill=WHITE, width=14)
    for k in range(9):
        x = cx - r + k * r / 4; d.line((x, base, cx, base - r * 1.2), fill=(255, 255, 255, 60), width=2)
    d.rectangle((0, base - 60, W, base), fill=(20, 20, 30))
    for i in range(0, W, 18): d.ellipse((i, base - 50 + (i * 7) % 20, i + 10, base - 40 + (i * 7) % 20), fill=AMB if (i // 18) % 3 else (230, 60, 60))


def trophy(w):
    w = int(w); im = Image.new("RGBA", (w, int(w * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g = (240, 196, 60); dk = (190, 140, 30)
    d.pieslice((w * 0.15, -w * 0.2, w * 0.85, w * 0.7), 0, 180, fill=g)
    d.arc((0, w * 0.05, w * 0.35, w * 0.45), 90, 270, fill=dk, width=int(w * 0.06)); d.arc((w * 0.65, w * 0.05, w, w * 0.45), 270, 90, fill=dk, width=int(w * 0.06))
    d.rectangle((w * 0.45, w * 0.68, w * 0.55, w * 0.95), fill=dk); d.rounded_rectangle((w * 0.25, w * 0.95, w * 0.75, w * 1.15), 10, fill=INK)
    return im


def clockchip(img, s, y=None):
    W, H = img.size; vert = H > W
    paste(img, chip(s, 48, WHITE, RED), W / 2, y or (H * 0.27 if vert else 290), 1, 1 + 0.05 * math.sin(time_ph[0] * 8))
time_ph = [0.0]


# ---------- cenas ----------
def scene(img, sh, t):
    W, H = img.size; vert = H > W; cx, cy = W / 2, H / 2
    sc = sh["scene"]; d = sh["t1"] - sh["t0"]; time_ph[0] = t
    U = min(W, H) / 1080
    def B(key): img.alpha_composite(bg(W, H, key, t))
    X = lambda v, h_: v if vert else h_
    # ---- abertura / flash-forward ----
    if sc == "ff_wembley":
        lance(img, amb("WAL"), t + 40, d, "CAMBRIDGE 1 x 1 WALSALL")
        clockchip(img, "118'"); pop_text(img, "A BOLA DO ACESSO", cx, cy - X(120, 40), t, 0, X(84, 130), AMB, 12, -3); paste(img, chip("WEMBLEY • PRORROGAÇÃO", 40, INK, AMB), cx, X(H * 0.68, H - 280), 1, back(t / 0.3))
    elif sc == "ff_rick":
        B("dark"); av = avatar("murrey", H * X(0.45, 0.8)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.15, 0))
        for i, (s_, c_, w_) in enumerate((("ENTRA: SOBE", GREEN, "entra"), ("NÃO ENTRA: VOLTA PRO ZERO", RED, "nao"))):
            t0 = wt(sh, w_)
            if t > t0: paste(img, chip(s_, X(54, 60), WHITE, c_), X(cx, W * 0.68), X(H * 0.2, 380) + i * 140, 1, back((t - t0) / 0.3), rot=-3 + 6 * i)
    elif sc == "ff_cut":
        B("purple"); img.alpha_composite(speedlines(W, H, -t * 3, 30))
        months = ["MAIO", "ABRIL", "MARÇO", "FEVEREIRO", "JANEIRO"]; k = min(4, int(t / max(0.3, d * 0.8 / 5)))
        pop_text(img, "<< " + months[k] + " 2027", cx, cy, t, 0, X(90, 130) * 1.0, WHITE, 10)
        pop_text(img, "5 MESES ANTES", cx, cy + 150, t, 0.4, 70, AMB, 8)
    # ---- recap ----
    elif sc == "recap":
        B("amber"); paste(img, icon_bus(W * X(0.6, 0.32)), X(cx, W * 0.28) + 8 * math.sin(t * 20), X(H * 0.62, cy + 120))
        av = avatar("rick", H * X(0.36, 0.7)); paste(img, av, X(cx, W * 0.72), X(H * 0.38, H - av.height / 2), ease(t / 0.3))
        pop_text(img, "ÔNIBUS → TÉCNICO", cx, X(H * 0.86, 250), t, 0.3, X(70, 90), WHITE, 8)
    elif sc == "recap_base":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t))
        card_in(img, "murrey", X(cx - 230, W * 0.33), X(cy - 100, cy + 30), X(400, 380), t, wt(sh, "murrey") - 0.1, 57)
        card_in(img, "gildo", X(cx + 230, W * 0.67), X(cy + 260, cy + 30), X(400, 380), t, wt(sh, "gildo") - 0.1)
    elif sc == "recap_hud":
        B("night"); pop_text(img, "2026: 7º LUGAR", cx, X(H * 0.25, 280), t, 0, X(90, 110), WHITE, 8)
        tp = wt(sh, "proposta")
        if t > tp:
            p = panel(W * X(0.9, 0.56), 300, (250, 250, 252, 255), 22, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
            pd.text((40, 30), "Proposta por MURREY", font=font("blk", 46), fill=INK); pd.text((40, 120), "£1.200.000", font=font("blk", 110), fill=(20, 130, 60))
            paste(img, p, cx, cy + 60, 1, back((t - tp) / 0.35), rot=-2)
        tv = wt(sh, "decidiram")
        if t > tv: paste(img, chip("VOCÊS DECIDIRAM", 60, INK, AMB), cx, X(H * 0.75, H - 180), 1, back((t - tv) / 0.3), rot=3)
    # ---- votação ----
    elif sc == "vote_card":
        dd = ImageDraw.Draw(img)
        if vert: dd.rectangle((0, 0, W, H / 2), fill=(60, 60, 64)); dd.rectangle((0, H / 2, W, H), fill=(150, 30, 30)); pa, pb = (cx, H * 0.27), (cx, H * 0.67)
        else: dd.rectangle((0, 0, W / 2, H), fill=(60, 60, 64)); dd.rectangle((W / 2, 0, W, H), fill=(150, 30, 30)); pa, pb = (W * 0.25, cy), (W * 0.75, cy)
        paste(img, text_el("A", font("blk", 200), (150, 150, 150), 8), pa[0], pa[1] - 80, 0.6)
        paste(img, text_el("VENDER", font("blk", 60), (170, 170, 170), 6), pa[0], pa[1] + 80, 0.6)
        u = (t - wt(sh, "b")) / 0.3
        paste(img, text_el("B", font("blk", 260), WHITE, 10), pb[0], pb[1] - 90, 1, 0.6 + 0.4 * back(u) if u > 0 else 0.6)
        paste(img, text_el("SEGURAR O MURREY", font("blk", 62), WHITE, 6), pb[0], pb[1] + 90)
        if u > 0: paste(img, stamp("VENCEU", 90, GREEN), pb[0], pb[1] + 220, 1, back(u), rot=-8); img = flash(img, t, wt(sh, "b"), 0.2)
    elif sc == "vote_comment":
        B("dark")
        c1 = comment_card(W * X(0.86, 0.42), "YOUTUBE", "Gabriel M", "B", 1, (220, 30, 30))
        c2 = comment_card(W * X(0.86, 0.42), "TIKTOK", "@vayard23", "B", 1, (20, 20, 22))
        paste(img, c1, X(cx, W * 0.27), X(H * 0.36, cy), 1, back((t - wt(sh, "gabriel")) / 0.35), rot=-2)
        paste(img, c2, X(cx, W * 0.73), X(H * 0.56, cy), 1, back((t - wt(sh, "vayard")) / 0.35), rot=2)
        pop_text(img, "EMPATE: 1 CURTIDA CADA", cx, X(H * 0.2, 250), t, 0, X(56, 70), AMB, 6)
    elif sc == "vote_reply":
        B("night"); p = panel(W * X(0.9, 0.56), 430, (250, 250, 252, 255), 22, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((40, 30), "Responder • proposta por MURREY", font=font("bd", 32), fill=(110, 110, 120))
        msg = "O garoto não tá à venda."; tf = wt(sh, "frase"); n = int(len(msg) * clamp((t - tf) / 1.2))
        pd.text((40, 150), msg[:n] + ("|" if int(t * 3) % 2 else ""), font=font("blk", 58), fill=INK)
        pd.text((40, 330), "— Rick Miguel", font=font("sb", 36), fill=(90, 90, 100))
        paste(img, p, cx, cy + 20, 1, back(t / 0.35))
        if t > tf + 1.3: paste(img, stamp("ENVIADO", 80, GREEN), cx + X(0, 380), X(H * 0.75, cy + 230), 1, back((t - tf - 1.3) / 0.25), rot=-8)
    elif sc == "vote_murrey":
        B("purple"); av = avatar("murrey", H * X(0.45, 0.78)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        pop_text(img, "06:00 • 1H ANTES", X(cx, W * 0.68), X(H * 0.2, 360), t, 0.2, X(70, 80), WHITE, 8)
        if t > wt(sh, "primeira"): paste(img, chip("1ª VEZ NA VIDA", 64, INK, AMB), X(cx, W * 0.68), X(H * 0.3, 520), 1, back((t - wt(sh, "primeira")) / 0.3), rot=-4)
    elif sc == "vote_kaikai":
        B("amber"); img.alpha_composite(rays(W, H, cx, cy, t))
        card_in(img, "kaikai", X(cx, W * 0.3), X(cy - 150, cy + 20), X(440, 420), t)
        if t > wt(sh, "proposta"): paste(img, chip("PROPOSTA DA 3ª DIVISÃO", 40, WHITE, RED), X(cx, W * 0.68), X(H * 0.72, 340), 1, back((t - wt(sh, "proposta")) / 0.3))
        tq = wt(sh, "moleque")
        if t > tq: paste(img, chip("\"SE O MOLEQUE FICA, EU FICO\"", X(40, 46), INK, WHITE), X(cx, W * 0.68), X(H * 0.82, 500), 1, back((t - tq) / 0.3), rot=-2)
    elif sc == "vote_cost":
        B("red"); od = odometer(180, 3, 160 * U, t, 0.8, 1200)
        paste(img, od, cx, X(H * 0.42, cy - 40), 1); pop_text(img, "MIL LIBRAS", cx, X(H * 0.53, cy + 110), t, 0.5, 70, WHITE, 6)
        if t > wt(sh, "milhao"): paste(img, stamp("SEM O MILHÃO", 80), cx, X(H * 0.25, 260), 1, back((t - wt(sh, "milhao")) / 0.3), rot=-8)
        if t > wt(sh, "curto"): paste(img, chip("ELENCO CURTO", 56, WHITE, INK), cx, X(H * 0.7, H - 230), 1, back((t - wt(sh, "curto")) / 0.3))
    # ---- janeiro ----
    elif sc == "jan_hub":
        B("teal"); p = panel(W * X(0.9, 0.6), 420, (12, 30, 34, 240)); dd = ImageDraw.Draw(p)
        dd.text((40, 30), "JANELA DE JANEIRO", font=font("blk", 46), fill=WHITE)
        for i, (a, b) in enumerate([("DINHEIRO", "QUASE NADA"), ("FERRAMENTA", "O CADERNINHO"), ("PRAZO", "31 DE JANEIRO")]):
            if t > 0.3 + i * 0.4:
                dd.rounded_rectangle((40, 120 + i * 92, p.width - 40, 190 + i * 92), 16, fill=(24, 60, 66))
                dd.text((70, 155 + i * 92), a, font=font("bd", 32), fill=(160, 220, 220), anchor="lm"); dd.text((p.width - 70, 155 + i * 92), b, font=font("blk", 36), fill=AMB, anchor="rm")
        paste(img, p, cx, cy + 20, 1, back(t / 0.35))
    elif sc == "jan_need":
        img.alpha_composite(Image.new("RGBA", (W, H), (24, 92, 52, 255))); dd = ImageDraw.Draw(img)
        for i in range(0, W, 160): dd.rectangle((i, 0, i + 80, H), fill=(28, 100, 58))
        pos = [(0.5, 0.85), (0.85, 0.7), (0.38, 0.73), (0.62, 0.73), (0.15, 0.7), (0.3, 0.55), (0.7, 0.55), (0.5, 0.47), (0.82, 0.36), (0.5, 0.3), (0.18, 0.36)] if vert else \
              [(0.08, 0.55), (0.25, 0.2), (0.22, 0.42), (0.22, 0.68), (0.25, 0.88), (0.42, 0.38), (0.42, 0.72), (0.55, 0.55), (0.75, 0.22), (0.8, 0.55), (0.75, 0.86)]
        for i, (px, py) in enumerate(pos):
            x, y = W * px, H * py; r = 34
            if i == 4:
                rr = r * (1 + 0.15 * math.sin(t * 10)); dd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=RED, outline=WHITE, width=5)
                paste(img, chip("LATERAL ESQ.?", 32, WHITE, RED), x + X(80, 0), y - 75)
            else: dd.ellipse((x - r, y - r, x + r, y + r), fill=AMB, outline=INK, width=5)
        if t > wt(sh, "trinta"): paste(img, chip("VERBA: £30.000", 60, INK, WHITE), cx, X(H * 0.18, 250), 1, back((t - wt(sh, "trinta")) / 0.3), rot=-3)
    elif sc == "jan_arlo":
        img.alpha_composite(Image.new("RGBA", (W, H), (8, 8, 12, 255))); sp = 0.6
        if t < sp * 3:
            k = int(t / sp); u = (t - k * sp) / sp
            img.alpha_composite(rays(W, H, cx, cy, t, AMB, 10, 40))
            el = [chip("ING", 120, INK, WHITE), chip("LE", 120, INK, AMB), chip("ACADEMIA → CAMBRIDGE", 60, WHITE, (60, 60, 70))][k]
            paste(img, el, cx, cy, 1 - clamp((u - 0.75) / 0.25), 0.6 + 0.4 * back(u / 0.5))
        else:
            u = t - sp * 3; img.alpha_composite(rays(W, H, cx, cy, t, AMB, 16, 90)); img = flash(img, u, 0, 0.3)
            card_in(img, "f_arlo", cx, cy + X(-60, 0), X(520, 440), u, 0, spin=False)
            paste(img, chip("GRÁTIS", 60, INK, GREEN), cx + X(0, 380), cy + X(450, -200), 1, back((u - 0.4) / 0.3), rot=8)
            img.alpha_composite(confetti(W, H, u, seed=11))
    elif sc == "jan_theo":
        B("blue"); card_in(img, "f_theo", X(cx, W * 0.33), X(cy - 120, cy + 20), X(440, 420), t)
        paste(img, stamp("RENOVADO", 90, GREEN), X(cx, W * 0.68), X(H * 0.78, cy), 1, back((t - 0.6) / 0.3), rot=-8)
    elif sc == "jan_out":
        B("dark")
        for i in range(2):
            u = (t - 0.2 - i * 0.3) / 0.6; x = X(cx - 200 + i * 400, W * 0.3 + i * 250) + W * 0.6 * ease(u)
            paste(img, silhouette().resize((300, 300)), x, X(H * 0.4, cy - 40), 1 - clamp(u - 0.6))
        paste(img, chip("2 EMPRESTADOS → 5ª DIVISÃO", 46, WHITE, (60, 60, 70)), cx, X(H * 0.25, 230), 1, back(t / 0.3))
        tc = wt(sh, "chuveiro")
        if t > tc: paste(img, chip("CHUVEIRO CONSERTADO ✓", 60, INK, GREEN), cx, X(H * 0.7, H - 250), 1, back((t - tc) / 0.3), rot=-3)
    elif sc == "jan_gildo_pre":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t))
        pop_text(img, "A CONTRATAÇÃO MAIS IMPORTANTE", cx, cy - 80, t, 0, X(60, 90), WHITE, 8)
        if t > wt(sh, "nao"): pop_text(img, "NÃO É UM JOGADOR", cx, cy + 80, t, wt(sh, "nao"), X(80, 100), AMB, 8)
    elif sc == "jan_gildo":
        B("night"); img.alpha_composite(speedlines(W, H, t, 15))
        av = avatar("gildo", H * X(0.42, 0.72)); paste(img, av, X(cx, W * 0.32), H - av.height / 2 - X(H * 0.15, 0))
        paste(img, icon_pizza(W * X(0.3, 0.14)), X(cx + 250, W * 0.48), X(H * 0.45, cy), 1, 1, -8)
        pop_text(img, "23:59", X(cx, W * 0.72), X(H * 0.17, 330), t, 0, 140, AMB, 10)
        if t > wt(sh, "dormindo"): paste(img, chip("Zzz • TREINO ÀS 8H", 50, WHITE, (60, 60, 70)), X(cx, W * 0.72), X(H * 0.27, 520), 1, back((t - wt(sh, "dormindo")) / 0.3))
    elif sc == "jan_contract":
        B("dark"); p = panel(W * X(0.86, 0.5), 520, (245, 242, 232, 255), 14, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((50, 50), "CONTRATO PROFISSIONAL", font=font("blk", 52), fill=INK); pd.text((50, 150), "Gildo • 15 anos", font=font("bd", 46), fill=INK)
        ts = wt(sh, "salario")
        if t > ts: pd.text((50, 270), "Salário: paga as contas", font=font("blk", 48), fill=(20, 130, 60)); pd.text((50, 350), "de casa ✓", font=font("blk", 48), fill=(20, 130, 60))
        u = clamp((t - ts - 0.8) / 0.8); pd.line((50, 470, 50 + 400 * u, 470 - 30 * math.sin(u * 12)), fill=(30, 40, 120), width=6)
        paste(img, p, cx, cy, 1, back(t / 0.3), rot=-2)
    elif sc == "jan_bike":
        B("amber"); d_ = ImageDraw.Draw(img); d_.line((cx, X(H * 0.25, 160), cx, X(H * 0.33, 260)), fill=INK, width=10)
        paste(img, icon_pizza(W * X(0.5, 0.25)), cx, X(H * 0.45, cy) + 10 * math.sin(t * 2), 1, 1, 4 * math.sin(t * 2))
        pop_text(img, "A MOCHILA TÁ LÁ ATÉ HOJE", cx, X(H * 0.75, H - 200), t, wt(sh, "ela"), X(64, 80), WHITE, 8)
        if t < wt(sh, "ela"): pop_text(img, "ÚLTIMA ENTREGA", cx, X(H * 0.75, H - 200), t, 0.2, X(70, 90), WHITE, 8)
    # ---- FA Cup ----
    elif sc == "fa_draw":
        B("blue"); img.alpha_composite(rays(W, H, cx, cy, t))
        for i in range(2):
            u = (t - 0.3 - i * 0.6) / 0.5; ang = t * 6 * (1 - ease(u))
            ball = Image.new("RGBA", (260, 260), (0, 0, 0, 0)); bd = ImageDraw.Draw(ball); bd.ellipse((0, 0, 259, 259), fill=WHITE, outline=INK, width=6)
            bd.text((130, 130), "?" if u < 1 else ("TOT" if i == 0 else "CAM"), font=font("blk", 80), fill=INK, anchor="mm")
            paste(img, ball, X(cx, W * (0.35 + i * 0.3)), X(H * (0.35 + i * 0.25), cy), 1 if u > 0 else 0.3, 1, ang * 20)
        pop_text(img, "SORTEIO • FA CUP", cx, X(H * 0.17, 240), t, 0, X(70, 90), WHITE, 8)
    elif sc == "fa_draw_x":
        B("dark"); p = panel(W * X(0.9, 0.62), 420, (14, 16, 30, 245)); pd = ImageDraw.Draw(p)
        pd.text((p.width / 2, 60), "3ª FASE • FA CUP", font=font("bd", 40), fill=AMB, anchor="mm")
        pd.text((p.width / 2, 190), "TOTTENHAM", font=font("blk", 86), fill=WHITE, anchor="mm"); pd.text((p.width / 2, 270), "x", font=font("bd", 50), fill=(180, 180, 190), anchor="mm")
        pd.text((p.width / 2, 350), "CAMBRIDGE", font=font("blk", 86), fill=AMB, anchor="mm")
        paste(img, p, cx, cy + 20, 1, back(t / 0.35)); img = shake(img, t, 0.1, 12)
        if t > wt(sh, "fora"): paste(img, chip("FORA DE CASA", 50, WHITE, RED), cx, X(H * 0.75, H - 140), 1, back((t - wt(sh, "fora")) / 0.3), rot=-4)
    elif sc == "fa_twist":
        B("night"); p = panel(W * X(0.9, 0.56), 360, (250, 250, 252, 255), 22, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((40, 30), "1º de janeiro", font=font("bd", 32), fill=(110, 110, 120)); pd.text((40, 100), "Proposta por MURREY", font=font("blk", 46), fill=INK)
        pd.text((40, 190), "£1.200.000", font=font("blk", 100), fill=(20, 130, 60))
        paste(img, p, cx, cy, 1, back(t / 0.35), rot=-3)
        tt = wt(sh, "tottenham")
        if t > tt: paste(img, stamp("ERA O TOTTENHAM", 80), cx, X(H * 0.72, cy + 200), 1, back((t - tt) / 0.3), rot=-10)
    elif sc == "fa_stadium":
        lance(img, amb("TOT"), t + 5, d, "TOTTENHAM 0 x 0 CAMBRIDGE")
        if t > wt(sh, "sessenta"): paste(img, chip("60.000 NO ESTÁDIO", 46, WHITE, INK), cx, X(H * 0.62, H - 330), 1, back((t - wt(sh, "sessenta")) / 0.3))
        if t > wt(sh, "quatro"): paste(img, chip("4.000 DO CAMBRIDGE", 46, INK, AMB), cx, X(H * 0.7, H - 250), 1, back((t - wt(sh, "quatro")) / 0.3), rot=-2)
    elif sc == "fa_speech":
        B("dark"); two_av(img, "rick", "murrey", t, None)
        tq = wt(sh, "hoje")
        if t > tq: paste(img, chip("\"MOSTRA PRA ELES O QUE ELES NÃO COMPRARAM\"", X(30, 40), INK, WHITE), cx, X(H * 0.3, 220), 1, back((t - tq) / 0.3), rot=-2)
    elif sc == "fa_goal1":
        t2 = wt(sh, "quarenta"); first = t < t2
        tt = t if first else t - t2; D_ = t2 if first else d - t2
        tg = min(4.2, D_ * 0.55)
        lance(img, goal_against("TOT"), tt, D_, ("TOTTENHAM 0 x 0 CAMBRIDGE" if first else "TOTTENHAM 1 x 0 CAMBRIDGE") if tt < tg + 0.35 else ("TOTTENHAM 1 x 0 CAMBRIDGE" if first else "TOTTENHAM 2 x 0 CAMBRIDGE"),
              tg + 0.35, "1 x 0" if first else "2 x 0", RED)
        clockchip(img, "20'" if first else "40'")
    elif sc == "fa_sub":
        B("dark"); p = panel(W * X(0.86, 0.42), 330, (10, 10, 12, 245)); pd = ImageDraw.Draw(p)
        pd.text((40, 40), "SUBSTITUIÇÃO • INTERVALO", font=font("bd", 34), fill=(160, 160, 160)); pd.text((40, 100), "ENTRA", font=font("blk", 40), fill=GREEN)
        pd.text((40, 150), "GILDO", font=font("blk", 110), fill=(255, 210, 60))
        paste(img, p, X(cx, W * 0.68), X(H * 0.3, cy), 1, back(t / 0.3))
        av = avatar("gildo", H * X(0.4, 0.75)); paste(img, av, X(cx, W * 0.27), H - av.height / 2 - X(H * 0.1, 0), ease((t - 0.3) / 0.3))
        if t > wt(sh, "primeiro"): paste(img, chip("1º JOGO PROFISSIONAL", 46, INK, AMB), X(cx, W * 0.68), X(H * 0.45, cy + 230), 1, back((t - wt(sh, "primeiro")) / 0.3), rot=-3)
    elif sc == "fa_gildo_run":
        lance(img, assist_play("TOT"), t * (5.0 / max(d, 1)) + 0.3, 8, "TOTTENHAM 2 x 0 CAMBRIDGE")
        img.alpha_composite(speedlines(W, H, t, 18)); clockchip(img, "61'")
        if t > wt(sh, "tres"): paste(img, chip("GILDO: 3 METROS NA FRENTE", 44, INK, AMB), cx, X(H * 0.7, H - 280), 1, back((t - wt(sh, "tres")) / 0.3))
    elif sc == "fa_murrey_goal":
        img = gol_screen(img, t, "MURREY!", "TOTTENHAM 2 x 1 CAMBRIDGE")
    elif sc == "fa_murrey_cele":
        B("amber"); img.alpha_composite(confetti(W, H, t + 1))
        av = avatar("murrey", H * X(0.45, 0.8)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        if t > wt(sh, "tribuna"): paste(img, chip("PRA TRIBUNA", 54, WHITE, INK), X(cx, W * 0.68), X(H * 0.22, 380), 1, back((t - wt(sh, "tribuna")) / 0.3), rot=-4)
        if t > wt(sh, "diretor"): paste(img, chip("DIRETOR DO TOTTENHAM", 44, INK, WHITE), X(cx, W * 0.68), X(H * 0.3, 520), 1, back((t - wt(sh, "diretor")) / 0.3), rot=3)
    elif sc == "fa_equal":
        te = wt(sh, "dois") - TSH - 0.4
        tt = max(0.0, t - te)
        lance(img, goal_for("TOT", "BAUER"), tt, 6, "TOTTENHAM 2 x 1 CAMBRIDGE" if t < wt(sh, "dois") else "TOTTENHAM 2 x 2 CAMBRIDGE", wt(sh, "dois") - te, "2 x 2!", AMB)
        clockchip(img, "89'")
    elif sc == "fa_pens":
        B("dark"); n = min(5, 1 + int(t / 0.45))
        paste(img, pens_board(W * X(0.92, 0.6), [1, 1, 1, 1], [1, 1, 1, 1, 1], n), cx, cy, 1, back(t / 0.3))
        if t > wt(sh, "kofi"): paste(img, chip("ÚLTIMA COBRANÇA: KOFI", 52, INK, AMB), cx, X(H * 0.72, H - 200), 1, back((t - wt(sh, "kofi")) / 0.3), rot=-3)
        pop_text(img, "4 x 4", cx, X(H * 0.25, 230), t, wt(sh, "quatro"), 110, WHITE, 8)
    elif sc == "fa_miss":
        B("dark"); paste(img, pens_board(W * X(0.92, 0.6), [1, 1, 1, 1, 0], [1, 1, 1, 1, 1], 5), cx, X(H * 0.35, cy - 140), 1)
        g = gray("f_kofi", H * X(0.35, 0.5)); paste(img, g, cx, H - g.height / 2)
        tt = wt(sh, "trave")
        if t > tt: img = flash(img, t, tt, 0.2, (255, 60, 60)); paste(img, stamp("NA TRAVE", 110), cx, X(H * 0.55, cy + 40), 1, back((t - tt) / 0.25), rot=-10); img = shake(img, t, tt, 20)
        if t > wt(sh, "fora"): paste(img, chip("CAMBRIDGE ELIMINADO", 50, WHITE, RED), cx, X(H * 0.15, 200), 1, back((t - wt(sh, "fora")) / 0.3))
    elif sc == "fa_hug":
        B("blue"); two_av(img, "f_kofi", "murrey", t)
        tq = wt(sh, "proxima")
        if t > tq: paste(img, chip("\"A PRÓXIMA VOCÊ FAZ\"", 56, INK, WHITE), cx, X(H * 0.3, 230), 1, back((t - tq) / 0.3), rot=-3)
    elif sc == "fa_viral":
        B("purple"); ph = Image.new("RGBA", (int(W * X(0.6, 0.26)), int(W * X(1.15, 0.5))), (0, 0, 0, 0)); pd = ImageDraw.Draw(ph)
        pd.rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), 50, fill=INK, outline=(90, 90, 100), width=8)
        pd.rounded_rectangle((20, 20, ph.width - 20, ph.height * 0.6), 30, fill=(20, 90, 50)); ph.alpha_composite(speedlines(ph.width, int(ph.height * 0.6), t, 12), (0, 0))
        paste(ph, avatar("gildo", ph.height * 0.5), ph.width / 2, ph.height * 0.33)
        views = int(10_000_000 * ease(t / 1.6)); pd.text((ph.width / 2, ph.height * 0.72), f"{views:,}".replace(",", "."), font=font("blk", ph.width * 0.11), fill=WHITE, anchor="mm")
        pd.text((ph.width / 2, ph.height * 0.8), "visualizações", font=font("sb", ph.width * 0.06), fill=(200, 200, 210), anchor="mm")
        paste(img, ph, X(cx, W * 0.3), X(H * 0.42, cy + 20), 1, back(t / 0.35), rot=-3)
        tn = wt(sh, "apelido")
        if t > tn: paste(img, newspaper(W * X(0.8, 0.4), "JANEIRO 2027", "OS ENTREGADORES", "o Cambridge do pique do Gildo"), X(cx, W * 0.7), X(H * 0.78, cy + 20), 1, back((t - tn) / 0.4), rot=(1 - ease((t - tn) / 0.4)) * 200)
    # ---- fevereiro ----
    elif sc == "lg_back":
        B("green"); k = int(t * 6) % 28 + 1
        p = panel(420, 420, (250, 250, 252, 255), 30, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.rounded_rectangle((0, 0, 420, 110), 30, fill=RED); pd.text((210, 55), "FEVEREIRO", font=font("blk", 52), fill=WHITE, anchor="mm")
        pd.text((210, 260), str(k), font=font("blk", 200), fill=INK, anchor="mm")
        paste(img, p, cx, cy, 1, back(t / 0.3), rot=3 * math.sin(t * 6)); img.alpha_composite(speedlines(W, H, t, 20))
    elif sc == "lg_run":
        B("green"); fixtures(img, sh, t, ["V", "V", "E", "V", "V"], ["Harrogate", "Newport", "Chesterfield", "Tranmere", "Notts Co."], ["2-0", "3-1", "1-1", "1-0", "2-1"], "vitoria", 0.42)
        if t > wt(sh, "quarto"): paste(img, chip("7º → 4º", 90, INK, AMB), cx, X(H * 0.88, H - 140), 1, back((t - wt(sh, "quarto")) / 0.3), rot=-4)
    elif sc == "lg_gildo_goal":
        tg = wt(sh, "puxa")
        if t < tg:
            lance(img, goal_for("BAR", "GILDO"), t * (TSH + 0.8) / max(tg, 0.5), 6, "CAMBRIDGE 0 x 0 BARROW", TSH + 0.4, "GOL DO GILDO!", AMB)
        else:
            B("amber"); img.alpha_composite(rays(W, H, cx, cy, t))
            av = avatar("gildo", H * X(0.45, 0.78)); paste(img, av, X(cx, W * 0.32), H - av.height / 2 - X(H * 0.12, 0))
            paste(img, chip("OBRIGADO, MÃE", X(70, 80), INK, WHITE), X(cx, W * 0.32), X(H * 0.8, H * 0.82), 1, back((t - wt(sh, "obrigado")) / 0.3), rot=-3)
            pop_text(img, "1º GOL PROFISSIONAL", X(cx, W * 0.7), X(H * 0.2, 300), t, tg, X(66, 80), WHITE, 8)
    elif sc == "lg_kofi":
        B("blue"); card_in(img, "f_kofi", X(cx, W * 0.3), X(cy - 150, cy + 20), X(440, 420), t)
        if t > wt(sh, "titular"): paste(img, chip("TITULAR DO MEIO", 54, INK, AMB), X(cx, W * 0.68), X(H * 0.72, 380), 1, back((t - wt(sh, "titular")) / 0.3), rot=-3)
        tq = wt(sh, "penalti", 1)
        if t > tq: paste(img, chip("\"PÊNALTI PERDIDO NÃO DEFINE JOGADOR\"", X(34, 40), INK, WHITE), X(cx, W * 0.68), X(H * 0.82, 540), 1, back((t - tq) / 0.3), rot=2)
    elif sc == "lg_kofi2":
        ta = wt(sh, "assistencia")
        lance(img, goal_for("BRO", "KOFI → GOL"), clamp(t / max(ta + 0.6, 0.5)) * (TSH + 0.6), 6, "CAMBRIDGE 0 x 0 BROMLEY" if t < ta + 0.6 else "CAMBRIDGE 1 x 0 BROMLEY")
        if t > wt(sh, "rouba"): paste(img, chip("3 DESARMES", 46, INK, AMB), cx, X(H * 0.62, H - 330), 1, back((t - wt(sh, "rouba")) / 0.3))
        if t > ta: paste(img, chip("ASSISTÊNCIA: KOFI", 50, WHITE, GREEN), cx, X(H * 0.7, H - 240), 1, back((t - ta) / 0.3), rot=-3)
        if t > wt(sh, "canta"): pop_text(img, "KOFI! KOFI!", cx, X(H * 0.45, cy - 60), t, wt(sh, "canta"), 120, AMB, 10, -4)
    elif sc == "lg_ollie":
        B("teal"); card_in(img, "f_ollie", X(cx, W * 0.3), X(cy - 160, cy + 20), X(420, 400), t)
        if t > wt(sh, "quatro"): pop_text(img, "4 GOLS", X(cx, W * 0.68), X(H * 0.72, 340), t, wt(sh, "quatro"), 130, AMB, 10, -3)
        if t > wt(sh, "anota"): paste(img, notebook(W * X(0.7, 0.3), 300, ["Ollie — 9, 15 ✓✓"], 1), X(cx, W * 0.68), X(H * 0.86, 640), 1, back((t - wt(sh, "anota")) / 0.3), rot=3)
    elif sc == "lg_table":
        B("green"); p = panel(W * X(0.86, 0.44), 520, (12, 30, 18, 235)); pd = ImageDraw.Draw(p)
        rows = [("1º", "Líder", "70"), ("2º", "Vice", "68"), ("3º", "3º colocado", "67"), ("4º", "CAMBRIDGE", "63"), ("5º", "5º colocado", "61")]
        for r, (a, b, c) in enumerate(rows):
            y = 40 + r * 92; me = b == "CAMBRIDGE"
            if me: pd.rounded_rectangle((20, y - 10, p.width - 20, y + 62), 16, fill=AMB)
            if r == 2: pd.line((20, y + 74, p.width - 20, y + 74), fill=GREEN, width=6)
            pd.text((40, y), a, font=font("blk", 40), fill=INK if me else WHITE); pd.text((140, y), b, font=font("blk" if me else "bd", 40), fill=INK if me else WHITE)
            pd.text((p.width - 40, y), c, font=font("blk", 40), fill=INK if me else WHITE, anchor="ra")
        paste(img, p, X(cx, W * 0.3), X(H * 0.45, cy + 30), 1, back(t / 0.3))
        pop_text(img, "ACESSO DIRETO: -4 PTS", X(cx, W * 0.72), X(H * 0.15, 380), t, 0.3, X(64, 70), WHITE, 8)
        if t > wt(sh, "cidade"): paste(img, chip("A CIDADE ACREDITA", 56, INK, AMB), X(cx, W * 0.72), X(H * 0.82, 560), 1, back((t - wt(sh, "cidade")) / 0.3), rot=-3)
    # ---- crise ----
    elif sc == "cr_march":
        B("red"); p = panel(420, 420, (250, 250, 252, 255), 30, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.rounded_rectangle((0, 0, 420, 110), 30, fill=INK); pd.text((210, 55), "MARÇO", font=font("blk", 60), fill=WHITE, anchor="mm")
        pd.text((210, 260), "!", font=font("blk", 220), fill=RED, anchor="mm")
        paste(img, p, cx, cy, 1, back(t / 0.3), rot=-4); img = shake(img, t, wt(sh, "quase"), 16)
    elif sc == "cr_injury":
        B("dark"); g = (avatar if t < wt(sh, "coxa") else gray)("murrey", H * X(0.45, 0.8))
        paste(img, g, X(cx, W * 0.3), H - g.height / 2 - X(H * 0.12, 0))
        pop_text(img, "11 JOGOS SEGUIDOS", X(cx, W * 0.7), X(H * 0.18, 300), t, 0, X(66, 80), WHITE, 8)
        tc = wt(sh, "coxa")
        if t > tc:
            img = flash(img, t, tc, 0.2, (255, 60, 60)); img = shake(img, t, tc, 22)
            paste(img, chip("LESÃO NA COXA", 54, WHITE, RED), X(cx, W * 0.7), X(H * 0.28, 450), 1, back((t - tc) / 0.3))
        if t > wt(sh, "semanas"): paste(img, stamp("4 SEMANAS FORA", 74), X(cx, W * 0.7), X(H * 0.78, 640), 1, back((t - wt(sh, "semanas")) / 0.3), rot=-8)
    elif sc == "cr_run":
        B("red"); fixtures(img, sh, t, ["D", "D", "E", "D"], ["Grimsby", "Walsall", "Crawley", "MK Dons"], ["0-1", "1-2", "0-0", "0-2"], "derrota", 0.45)
        if t > wt(sh, "nono"): paste(img, chip("4º → 9º", 90, WHITE, RED), cx, X(H * 0.86, H - 140), 1, back((t - wt(sh, "nono")) / 0.3), rot=-4); img = shake(img, t, wt(sh, "nono"), 16)
    elif sc == "cr_paper":
        B("night"); tj = 0.1
        paste(img, newspaper(W * X(0.88, 0.55), "MARÇO 2027", "O MOTORISTA PERDEU O CAMINHO", "Cambridge cai para 9º"), cx, cy + 30, 1, back((t - tj) / 0.4), rot=(1 - ease((t - tj) / 0.4)) * 300)
    elif sc == "cr_meeting":
        B("dark"); p = panel(W * X(0.88, 0.56), 470, (245, 242, 232, 255), 14, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((50, 40), "DIRETORIA • REUNIÃO", font=font("bd", 40), fill=(90, 90, 100)); pd.text((50, 120), "Assunto: Rick Miguel", font=font("blk", 46), fill=INK)
        if t > wt(sh, "simples"): pd.text((50, 230), "PLAY-OFF", font=font("blk", 90), fill=(20, 130, 60)); pd.text((50, 340), "OU FIM DO CONTRATO", font=font("blk", 60), fill=RED)
        paste(img, p, cx, cy + 20, 1, back(t / 0.3), rot=-2)
    elif sc == "cr_depot":
        B("night"); paste(img, icon_bus(W * X(0.7, 0.4)), X(cx, W * 0.3), X(H * 0.35, cy + 60))
        paste(img, notebook(W * X(0.8, 0.36), 420, GOALS, 4), X(cx, W * 0.72), X(H * 0.7, cy + 20), 1, back((t - wt(sh, "caderninho")) / 0.35), rot=3)
        pop_text(img, "03:00 • GARAGEM", cx, X(H * 0.15, 240), t, 0.2, X(70, 80), (180, 190, 255), 8)
    elif sc == "cr_pelly":
        B("dark"); card_in(img, "pelly", X(cx, W * 0.3), X(cy - 150, cy + 20), X(440, 420), t)
        if t > wt(sh, "sem"): paste(img, chip("SEM O TÉCNICO", 56, WHITE, INK), X(cx, W * 0.68), X(H * 0.72, 380), 1, back((t - wt(sh, "sem")) / 0.3), rot=-3)
        if t > wt(sh, "ninguem"): paste(img, chip("PORTA FECHADA", 50, INK, WHITE), X(cx, W * 0.68), X(H * 0.82, 540), 1, back((t - wt(sh, "ninguem")) / 0.3), rot=3)
    elif sc == "cr_pelly_x":
        lance(img, amb("SAL"), t + 60, d, "CAMBRIDGE x ADVERSÁRIO")
        band = panel(W * X(0.7, 0.36), 140, (240, 240, 240, 255), 60, (0, 0, 0, 0)); ImageDraw.Draw(band).text((band.width / 2, 70), "RICK", font=font("blk", 80), fill=INK, anchor="mm")
        paste(img, band, cx, cy, 1, back((t - wt(sh, "munhequeira") + 0.2) / 0.35), rot=-6)
    # ---- evolução ----
    elif sc == "ev_title":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t, AMB, 14, 70))
        for i, k in enumerate(["murrey", "gildo", "f_kofi", "f_ollie"]):
            ang = t * 1.2 + i * math.pi / 2; r = W * X(0.32, 0.34)
            card_in(img, k, cx + r * math.cos(ang), cy + r * 0.45 * math.sin(ang) + 40, 220 * U * X(1.3, 1), t, i * 0.12, {"murrey": 57}.get(k))
        pop_text(img, "EVOLUÇÃO DA BASE", cx, cy - X(0, 40), t, 0.2, X(80, 110), WHITE, 10)
    elif sc == "ev_murrey": img = evo(img, t, "murrey", 57, 66, "VIROU O CAMISA 10", "purple")
    elif sc == "ev_gildo": img = evo(img, t, "gildo", 48, 58, "VELOCIDADE 99 • DORME 8H", "teal")
    elif sc == "ev_kofi": img = evo(img, t, "f_kofi", 50, 56, "GANHOU A POSIÇÃO", "blue")
    elif sc == "ev_ollie": img = evo(img, t, "f_ollie", 46, 53, "9 GOLS NO SUB-18", "green")
    # ---- casa do Gildo ----
    elif sc == "gh_dinner":
        B("amber"); two_av(img, "rick", "gildo", t)
        for i, (s_, w_) in enumerate((("ARROZ", "arroz"), ("FEIJÃO", "feijao"), ("FAROFA", "farofa"))):
            if t > wt(sh, w_): paste(img, chip(s_, 56, INK, WHITE), cx + (i - 1) * X(300, 330), X(H * 0.28, 260), 1, back((t - wt(sh, w_)) / 0.3), rot=(i - 1) * 5)
    elif sc == "gh_mum":
        B("green"); p = panel(W * X(0.9, 0.62), 300, (14, 30, 20, 240)); pd = ImageDraw.Draw(p)
        u = ease((t - 0.4) / 1.4)
        pd.text((60, 60), "MINAS GERAIS", font=font("blk", 46), fill=AMB); pd.text((p.width - 60, 60), "CAMBRIDGE", font=font("blk", 46), fill=WHITE, anchor="ra")
        pd.line((90, 190, 90 + (p.width - 180) * u, 190 - 60 * math.sin(u * math.pi)), fill=WHITE, width=8); pd.ellipse((80 + (p.width - 180) * u, 180 - 60 * math.sin(u * math.pi), 100 + (p.width - 180) * u, 200 - 60 * math.sin(u * math.pi)), fill=AMB)
        paste(img, p, cx, X(H * 0.35, cy - 60), 1, back(t / 0.3))
        if t > wt(sh, "feliz"): pop_text(img, "\"NUNCA TÃO FELIZ\"", cx, X(H * 0.65, cy + 230), t, wt(sh, "feliz"), X(70, 90), WHITE, 8)
    elif sc == "gh_dad":
        B("night"); av = avatar("f_pai_gildo", H * X(0.45, 0.8)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        tq = wt(sh, "se")
        if t > tq:
            p = panel(W * X(0.88, 0.5), 300, (250, 250, 252, 255), 30, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
            for i, l in enumerate(["Se aparecer uma chance", "no Brasil, o senhor", "deixa ele ir?"]): pd.text((40, 40 + i * 80), l, font=font("blk", 52), fill=INK)
            paste(img, p, X(cx, W * 0.7), X(H * 0.25, cy - 40), 1, back((t - tq) / 0.35), rot=-2)
    elif sc == "gh_rick":
        B("dark"); av = avatar("rick", H * X(0.45, 0.8)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        pop_text(img, "?", X(cx + 250, W * 0.68), X(H * 0.25, cy), t, wt(sh, "guarda"), 300, AMB, 12, 8)
    # ---- reta final ----
    elif sc == "fs_return":
        B("purple"); img.alpha_composite(rays(W, H, cx, cy, t)); card_in(img, "murrey", X(cx, W * 0.33), X(cy - 100, cy + 20), X(460, 420), t, 0, 66)
        paste(img, stamp("VOLTOU", 100, GREEN), X(cx, W * 0.68), X(H * 0.8, cy), 1, back((t - wt(sh, "volta")) / 0.3), rot=-8)
    elif sc == "fs_run":
        B("green"); fixtures(img, sh, t, ["V", "V", "V", "V"], ["Bromley", "Barrow", "Cheltenham", "Fleetwood"], ["2-0", "1-0", "3-2", "2-1"], "quatro", 0.35)
        if t > wt(sh, "salford"): paste(img, chip("ÚLTIMA RODADA: SÓ A VITÓRIA", 50, INK, AMB), cx, X(H * 0.86, H - 140), 1, back((t - wt(sh, "salford")) / 0.3), rot=-3)
    elif sc == "fs_race":
        B("dark"); p = panel(W * X(0.86, 0.5), 360, (14, 16, 24, 240)); pd = ImageDraw.Draw(p)
        for r, (a, b, c) in enumerate([("6º", "Concorrente", "71"), ("7º", "CAMBRIDGE", "71"), ("8º", "Concorrente", "70")]):
            y = 50 + r * 100; me = b == "CAMBRIDGE"
            if me: pd.rounded_rectangle((20, y - 14, p.width - 20, y + 66), 16, fill=AMB)
            pd.text((40, y), a, font=font("blk", 46), fill=INK if me else WHITE); pd.text((150, y), b, font=font("blk", 46), fill=INK if me else WHITE); pd.text((p.width - 40, y), c, font=font("blk", 46), fill=INK if me else WHITE, anchor="ra")
        paste(img, p, cx, cy + 20, 1, back(t / 0.3))
        pop_text(img, "3 TIMES, 1 VAGA", cx, X(H * 0.2, 230), t, 0.1, X(80, 90), WHITE, 8)
    elif sc == "fs_tense":
        lance(img, amb("SAL"), t + 20, d, "CAMBRIDGE 1 x 1 SALFORD"); clockchip(img, "87'")
        tb = wt(sh, "chama")
        if t > tb:
            p = panel(W * X(0.86, 0.42), 280, (10, 10, 12, 245)); pd = ImageDraw.Draw(p)
            pd.text((40, 40), "ENTRA", font=font("blk", 40), fill=GREEN); pd.text((40, 100), "OLLIE • 15", font=font("blk", 90), fill=(255, 210, 60))
            paste(img, p, cx, X(H * 0.62, cy + 120), 1, back((t - tb) / 0.3))
    elif sc == "fs_ollie":
        lance(img, goal_for("SAL", "OLLIE"), t * (TSH + 0.5) / max(d, 0.5), 6, "CAMBRIDGE 1 x 1 SALFORD"); clockchip(img, "89'")
    elif sc == "fs_ollie_x":
        img = gol_screen(img, t, "GOL!", "CAMBRIDGE 2 x 1 SALFORD")
        if t > wt(sh, "play-off"): paste(img, chip("PLAY-OFF!", 80, INK, WHITE), cx, X(H * 0.72, H - 200), 1, back((t - wt(sh, "play-off")) / 0.3), rot=4)
    elif sc == "fs_table":
        B("green"); pop_text(img, "7º LUGAR", cx, cy - 60, t, 0, 160 * U, WHITE, 10)
        if t > wt(sh, "elenco"): paste(img, chip("UM ELENCO QUE ACREDITA", 56, INK, AMB), cx, cy + 120, 1, back((t - wt(sh, "elenco")) / 0.3), rot=-3)
    # ---- semifinal ----
    elif sc == "sf_draw":
        B("red"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 40))
        paste(img, crest(260 * U), X(cx, W * 0.3), X(H * 0.3, cy), 1, back(t / 0.3))
        pop_text(img, "VS", cx, cy if not vert else H * 0.47, t, 0.3, 140, WHITE, 10)
        pop_text(img, "CREWE", X(cx, W * 0.7), X(H * 0.65, cy), t, wt(sh, "crewe"), 140, (255, 120, 120), 10)
    elif sc == "sf_flash":
        tg = min(4.2, d * 0.55)
        lance(img, L.crewe, t, d, "MAIO DE 2026 • 93'", tg + 0.35, "LEMBRA?", RED)
        im2 = img.convert("L").convert("RGBA"); im2.putalpha(150); img.alpha_composite(im2)
    elif sc == "sf_leg1":
        B("dark"); p = panel(W * X(0.86, 0.5), 260, (14, 14, 18, 240)); pd = ImageDraw.Draw(p)
        pd.text((p.width / 2, 60), "JOGO DE IDA", font=font("bd", 40), fill=(170, 170, 190), anchor="mm"); pd.text((p.width / 2, 160), "CREWE 1 x 0 CAMBRIDGE", font=font("blk", 60), fill=WHITE, anchor="mm")
        paste(img, p, cx, cy - 60, 1, back(t / 0.3))
        if t > wt(sh, "volta"): paste(img, chip("VOLTA: ABBEY STADIUM", 56, INK, AMB), cx, cy + 180, 1, back((t - wt(sh, "volta")) / 0.3), rot=-3)
    elif sc == "sf_leg1b":
        lance(img, amb("CRE"), t + 12, d, "CAMBRIDGE 0 x 0 CREWE • AGREGADO 0-1")
        if t > wt(sh, "oito"): pop_text(img, "8.000", cx, X(H * 0.55, cy), t, wt(sh, "oito"), 160, AMB, 10)
        if t > wt(sh, "telhado"): paste(img, chip("TEM GENTE NO TELHADO", 46, INK, WHITE), cx, X(H * 0.68, H - 260), 1, back((t - wt(sh, "telhado")) / 0.3), rot=-3)
    elif sc == "sf_leg2":
        lance(img, goal_for("CRE", "LAVERY"), clamp(t / 3.5) * (TSH + 0.6), 6, "CAMBRIDGE 0 x 0 CREWE" if t < 3.2 else "CAMBRIDGE 1 x 0 CREWE", TSH + 0.4, "LAVERY!", AMB)
        if t > wt(sh, "agregado"): paste(img, chip("AGREGADO 1-1", 56, INK, WHITE), cx, X(H * 0.7, H - 250), 1, back((t - wt(sh, "agregado")) / 0.3))
    elif sc == "sf_93":
        lance(img, assist_play("CRE"), t * (5.0 / max(d, 1)) + 0.3, 8, "CAMBRIDGE 1 x 0 CREWE • AGREGADO 1-1"); clockchip(img, "93'")
        tp = wt(sh, "penalti")
        if t > tp: img = flash(img, t, tp); pop_text(img, "PÊNALTI!", cx, cy, t, tp, 170, RED, 12, -4); img = shake(img, t, tp, 24)
    elif sc == "sf_murrey_pen":
        B("dark"); av = avatar("murrey", H * X(0.5, 0.85)); paste(img, av, cx, H - av.height / 2 - X(H * 0.1, 0))
        dd = ImageDraw.Draw(img); r = 120 * U; dd.ellipse((cx - r, X(H * 0.2, 150) - r * 0.3, cx + r, X(H * 0.2, 150) + r * 0.3), outline=(255, 255, 255, 120), width=4)
        if t > wt(sh, "silencio"): pop_text(img, "SILÊNCIO", cx, X(H * 0.18, 200), t, wt(sh, "silencio"), 90, WHITE, 8)
    elif sc == "sf_goal":
        img = gol_screen(img, t, "GOL!", "AGREGADO 2-1 • CAMBRIDGE NA FINAL")
        if t > wt(sh, "wembley"): paste(img, chip("RUMO A WEMBLEY", 70, INK, WHITE), cx, X(H * 0.72, H - 200), 1, back((t - wt(sh, "wembley")) / 0.3), rot=4)
    # ---- Wembley ----
    elif sc == "wb_arrive":
        wembley_bg(img, t); pop_text(img, "FINAL DO PLAY-OFF", cx, X(H * 0.2, 250), t, 0, X(70, 90), WHITE, 8)
        pop_text(img, "CAMBRIDGE x WALSALL", cx, X(H * 0.3, 370), t, wt(sh, "cambridge"), X(64, 100), AMB, 8)
        if t > wt(sh, "trinta"): paste(img, chip("35.000 TORCEDORES AMARELOS", 46, INK, AMB), cx, X(H * 0.5, 500), 1, back((t - wt(sh, "trinta")) / 0.3), rot=-3)
    elif sc == "wb_mum":
        wembley_bg(img, t); av = avatar("f_mae_rick", H * X(0.42, 0.75)); paste(img, av, X(cx, W * 0.32), H - av.height / 2 - X(H * 0.15, 0))
        if t > wt(sh, "camisa"): paste(img, chip("CAMISA DO CAMBRIDGE", 46, INK, AMB), X(cx, W * 0.7), X(H * 0.2, 380), 1, back((t - wt(sh, "camisa")) / 0.3), rot=-3)
        if t > wt(sh, "terco"): paste(img, chip("TERÇO DO PALMEIRAS", 46, WHITE, (20, 110, 60)), X(cx, W * 0.7), X(H * 0.28, 520), 1, back((t - wt(sh, "terco")) / 0.3), rot=3)
    elif sc == "wb_tunnel":
        B("dark"); tw = wt(sh, "devolver"); n = int(len("DEVOLVER O CAMBRIDGE PRO LUGAR DELE") * clamp((t - tw) / 1.4))
        p = panel(W * X(0.86, 0.5), 460, (240, 232, 200, 255), 12, (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        pd.text((40, 30), "Página 1 • Rick, 13 anos", font=font("bd", 36), fill=(110, 90, 60))
        for i, l in enumerate(wrap("DEVOLVER O CAMBRIDGE PRO LUGAR DELE"[:n], font("blk", 56), p.width - 80)): pd.text((40, 130 + i * 76), l, font=font("blk", 56), fill=(30, 40, 120))
        paste(img, p, cx, cy + 20, 1, back(t / 0.35), rot=-2)
    elif sc == "wb_tunnel2":
        B("amber"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 50))
        paste(img, notebook(W * X(0.8, 0.42), 420, GOALS, 4), cx, cy + X(80, 40), 1, back(t / 0.3), rot=2)
        pop_text(img, "BORA RISCAR A 1ª LINHA", cx, X(H * 0.2, 200), t, wt(sh, "bora"), X(66, 90), WHITE, 8)
    elif sc == "wb_goal_w":
        tk = wt(sh, "kaikai")
        if t < tk:
            tg = min(4.2, tk * 0.55)
            lance(img, goal_against("WAL"), t, tk, "CAMBRIDGE 0 x 0 WALSALL" if t < tg + 0.35 else "CAMBRIDGE 0 x 1 WALSALL", tg + 0.35, "0 x 1", RED)
        else:
            lance(img, goal_for("WAL", "KAIKAI"), clamp((t - tk) / 2.5) * (TSH + 0.8), 6, "CAMBRIDGE 0 x 1 WALSALL" if t < tk + 2.2 else "CAMBRIDGE 1 x 1 WALSALL", TSH + 0.4, "KAIKAI!", AMB)
    elif sc == "wb_et":
        B("dark"); m = int(90 + 30 * clamp(t / max(d * 0.9, 0.5)))
        pop_text(img, f"{m}'", cx, cy - 40, t, 0, 220 * U, WHITE, 12); pop_text(img, "1 x 1", cx, X(H * 0.25, 220), t, 0, 100, AMB, 8)
        if t > wt(sh, "prorrogacao"): paste(img, chip("PRORROGAÇÃO", 70, WHITE, RED), cx, cy + 180, 1, back((t - wt(sh, "prorrogacao")) / 0.3), rot=-3)
    elif sc == "wb_ball":
        lance(img, amb("WAL"), t + 41, d, "CAMBRIDGE 1 x 1 WALSALL"); clockchip(img, "118'")
        if t > wt(sh, "gildo"): paste(img, chip("GILDO DISPARANDO →", 54, INK, AMB), cx, X(H * 0.68, H - 260), 1, back((t - wt(sh, "gildo")) / 0.3))
    elif sc == "wb_choice":
        B("dark"); av = avatar("murrey", H * X(0.45, 0.8)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        paste(img, chip("CHUTAR?", 60, WHITE, RED), X(cx - 200, W * 0.62), X(H * 0.2, 320), 1, back(t / 0.3), rot=-5)
        tq = wt(sh, "aqui")
        if t > tq: paste(img, chip("\"AQUI NINGUÉM É MAIOR QUE O CLUBE\"", X(34, 40), INK, WHITE), X(cx, W * 0.68), X(H * 0.3, 520), 1, back((t - tq) / 0.3), rot=2)
    elif sc == "wb_pass":
        lance(img, assist_play("WAL"), 1.0 + t * (5.0 / max(d, 1)), 8, "CAMBRIDGE 1 x 1 WALSALL"); clockchip(img, "118'")
        if t > wt(sh, "vazio"): pop_text(img, "GILDO!", cx, cy, t, wt(sh, "vazio"), 170, AMB, 12, -4)
    elif sc == "wb_goal":
        img = gol_screen(img, t, "GOL DOS ENTREGADORES!" if t > wt(sh, "entregadores") else "GOL!", "CAMBRIDGE 2 x 1 WALSALL")
    elif sc == "wb_whistle":
        img = gol_screen(img, t, "ACESSO!", None, "green")
        if t > wt(sh, "terceira"): paste(img, chip("LEAGUE TWO → LEAGUE ONE", X(56, 70), INK, WHITE), cx, cy + 150, 1, back((t - wt(sh, "terceira")) / 0.3), rot=-3)
    elif sc == "wb_hist":
        B("blue"); paste(img, odometer(2027, 4, 150 * U, t, 1.2, 1990), cx, X(H * 0.35, cy - 120), 1)
        pop_text(img, "37 ANOS DEPOIS", cx, X(H * 0.55, cy + 60), t, 0.8, X(90, 110), AMB, 10)
        pop_text(img, "WEMBLEY É AMARELO DE NOVO", cx, X(H * 0.68, cy + 200), t, wt(sh, "torcida"), X(56, 70), WHITE, 8)
    elif sc == "wb_players":
        wembley_bg(img, t); img.alpha_composite(confetti(W, H, t, 5))
        paste(img, trophy(W * X(0.4, 0.16) * (1 + 0.04 * math.sin(t * 4))), cx, X(H * 0.4, cy - 60), 1, back(t / 0.3))
        for k, (key, w_) in enumerate((("pelly", "pelly"), ("kaikai", "kaikai"), ("gildo", "gildo"))):
            tw_ = wt(sh, w_)
            if t > tw_: card_in(img, key, X(cx + (k - 1) * 330, W * (0.2 + k * 0.3)), X(H * 0.72, cy + 260), X(300, 260), t, tw_, 58 if key == "gildo" else None)
    elif sc == "wb_rick":
        B("dark"); av = avatar("rick", H * X(0.42, 0.78)); paste(img, av, X(cx, W * 0.28), H - av.height / 2 - X(H * 0.12, 0))
        tr_ = wt(sh, "risca"); paste(img, notebook(W * X(0.82, 0.44), 420, GOALS, 4, clamp((t - tr_) / 0.8)), X(cx, W * 0.7), X(H * 0.3, cy), 1, back(t / 0.3), rot=2)
    # ---- dilema ----
    elif sc == "dl_bus":
        B("night"); paste(img, icon_bus(W * X(0.6, 0.34)), X(cx, W * 0.28) + 6 * math.sin(t * 20), X(H * 0.72, cy + 120))
        tp = wt(sh, "toca")
        if t > tp: paste(img, phone_call(W * X(0.45, 0.2), "NÚMERO DO BRASIL", "chamada internacional", t), X(cx, W * 0.7) + 8 * math.sin(t * 40), X(H * 0.33, cy), 1, back((t - tp) / 0.3))
    elif sc == "dl_hud":
        B("green"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 40))
        for i, (a, b, w_) in enumerate((("DIVISÃO", "LEAGUE ONE", "terceira"), ("ORÇAMENTO", "£600.000", "orcamento"), ("CADERNINHO", "1 LINHA RISCADA", "caderninho"))):
            t0 = wt(sh, w_); u = (t - t0) / 0.35
            if u <= 0: continue
            p = panel(W * X(0.86, 0.28), 240, (14, 40, 24, 235)); pd = ImageDraw.Draw(p)
            pd.text((36, 34), a, font=font("bd", 32), fill=(190, 230, 200)); f = font("blk", 56)
            while f.getlength(b) > p.width - 60: f = font("blk", f.size - 4)
            pd.text((36, 110), b, font=f, fill=AMB)
            paste(img, p, X(cx, W * (0.2 + i * 0.3)), X(H * (0.32 + i * 0.17), cy + 20), ease(u), 0.7 + 0.3 * back(u))
    elif sc == "dl_call":
        B("dark"); paste(img, phone_call(W * X(0.5, 0.22), "PALMEIRAS", "São Paulo, Brasil", t), X(cx, W * 0.3), X(H * 0.45, cy + 20), 1, back(t / 0.3))
        if t > wt(sh, "base"): paste(img, chip("QUER O GILDO NA BASE", X(50, 56), WHITE, (20, 110, 60)), X(cx, W * 0.7), X(H * 0.85, cy), 1, back((t - wt(sh, "base")) / 0.3), rot=-3)
    elif sc == "dl_family":
        B("green"); av = avatar("f_pai_gildo", H * X(0.42, 0.78)); paste(img, av, X(cx, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
        if t > wt(sh, "voltar"): paste(img, chip("SONHO: VOLTAR PRO BRASIL", 46, INK, WHITE), X(cx, W * 0.7), X(H * 0.2, 380), 1, back((t - wt(sh, "voltar")) / 0.3), rot=-3)
        if t > wt(sh, "emprego"): paste(img, chip("EMPREGO EM SÃO PAULO", 46, WHITE, (20, 110, 60)), X(cx, W * 0.7), X(H * 0.28, 520), 1, back((t - wt(sh, "emprego")) / 0.3), rot=3)
    elif sc == "dl_ab":
        B("dark"); tm = wt(sh, "mas")
        if t < tm:
            p = panel(W * X(0.9, 0.56), 420, (14, 40, 24, 245)); pd = ImageDraw.Draw(p)
            pd.text((40, 30), "PROPOSTA DO PALMEIRAS", font=font("bd", 38), fill=(190, 230, 200)); pd.text((40, 110), "£800.000", font=font("blk", 120), fill=AMB)
            pd.text((40, 270), "+ 20% DE UMA VENDA FUTURA", font=font("blk", 46), fill=WHITE)
            paste(img, p, cx, cy + 20, 1, back(t / 0.35), rot=-2)
        else:
            u = t - tm; av = avatar("f_pai_gildo", H * X(0.36, 0.6)); paste(img, av, X(cx - 200, W * 0.3), H - av.height / 2 - X(H * 0.12, 0))
            av2 = avatar("gildo", H * X(0.34, 0.56)); paste(img, av2, X(cx + 200, W * 0.5), H - av2.height / 2 - X(H * 0.12, 0))
            paste(img, chip("PAI DO GILDO NO CLUBE?", 54, INK, AMB), X(cx, W * 0.75), X(H * 0.25, 360), 1, back(u / 0.3), rot=-3)
            if t > wt(sh, "ficar"): paste(img, chip("A FAMÍLIA FICA", 54, WHITE, RED), X(cx, W * 0.75), X(H * 0.34, 520), 1, back((t - wt(sh, "ficar")) / 0.3), rot=3)
    elif sc == "dl_vote":
        dd = ImageDraw.Draw(img)
        if vert: dd.rectangle((0, 0, W, H / 2), fill=(20, 110, 60)); dd.rectangle((0, H / 2, W, H), fill=(190, 130, 20)); pa, pb = (cx, H * 0.31), (cx, H * 0.64)
        else: dd.rectangle((0, 0, W / 2, H), fill=(20, 110, 60)); dd.rectangle((W / 2, 0, W, H), fill=(190, 130, 20)); pa, pb = (W * 0.25, cy), (W * 0.75, cy)
        ta, tb = wt(sh, "comenta"), wt(sh, "comenta", 1)
        for (x, y), L_, s1, s2 in ((pa, "A", "GILDO VAI PRO PALMEIRAS", "£800 MIL + 20%"), (pb, "B", "GILDO FICA EM CAMBRIDGE", "PAI CONTRATADO PELO CLUBE")):
            paste(img, text_el(L_, font("blk", 240), WHITE, 10), x, y - 170, 1, 1 + 0.05 * math.sin(t * 4))
            paste(img, text_el(s1, font("blk", X(58, 56)), WHITE, 6), x, y + 20)
            paste(img, text_el(s2, font("bd", 40), (240, 240, 240), 4), x, y + 95)
        hl = 0 if ta <= t < tb else 1 if tb <= t else None
        if hl is not None:
            x, y = (pa, pb)[hl]; paste(img, chip("COMENTE " + "AB"[hl], 60, INK, WHITE), x, y + 190, 1, back(((t - (ta, tb)[hl])) / 0.3))
        if not vert: paste(img, card("gildo", 200, 58), cx, 330, 1, 1 + 0.04 * math.sin(t * 3))
    elif sc == "end":
        B("amber"); img.alpha_composite(rays(W, H, cx, cy, t, WHITE, 12, 60))
        paste(img, crest(260 * U), cx, cy - 200 * U, 1, back(t / 0.4))
        pop_text(img, "INSCREVA-SE", cx, cy + 40 * U, t, 0.3, 120 * U, WHITE, 10)
        paste(img, chip("EPISÓDIO COMPLETO NO CANAL", 50, WHITE, RED), cx, cy + 200 * U, 1, back((t - 0.5) / 0.3), rot=-3); paste(img, chip("SEGUE PRO EP.3", 50, INK, WHITE), cx, cy + 330 * U, 1, back((t - 1.0) / 0.3))
        if t > 0.5:
            f = font("md", 22); dd = ImageDraw.Draw(img)
            for i, l in enumerate(wrap(" ".join(CREDITS), f, W - 80)): dd.text((cx, 40 + i * 30), l, font=f, fill=(60, 40, 0), anchor="mm")
    else:
        B("dark"); pop_text(img, sc, cx, cy, t, 0, 80)
    return img


CREDITS = ["Músicas: Kevin MacLeod (incompetech.com) — Night of Chaos, Clash Defiant, Ouroboros,",
           "Lasting Hope, Heartbreaking. Licença Creative Commons: By Attribution 4.0"]


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
