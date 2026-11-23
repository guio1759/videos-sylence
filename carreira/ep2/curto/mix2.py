import sys, numpy as np, subprocess, json
sys.path.insert(0, "/home/claude/work/sfx")
from scipy.io import wavfile
import sfxlib
sys.argv = ["x", "shots"]
import make2 as M
SR = 44100
def mp3(path):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
sr, v = wavfile.read("narr.wav"); v = v.astype(np.float32) / 32768
N = int(M.TOTAL * SR) + SR; voice = np.zeros(N, np.float32); voice[:len(v)] = v[:N]
voice = voice / np.abs(voice).max() * 0.92
# trilha por bloco
blocks = []
for s in M.SHOTS:
    if not blocks or blocks[-1][0] != s["block"]: blocks.append([s["block"], s["music"], s["t0"], s["t1"]])
    else: blocks[-1][3] = s["t1"]
music = np.zeros(N, np.float32); cache = {}
OFF = {"Night_of_Chaos": 0, "Take_a_Chance": 0, "Movement_Proposition": 0, "Clash_Defiant": 30, "Exhilarate": 0, "Ouroboros": 10, "Rising_Game": 4, "Dreamer": 8, "Killers": 15, "Malicious": 10, "Lasting_Hope": 0, "Heartbreaking": 0}
for k, (bid, mus, t0, t1) in enumerate(blocks):
    if mus not in cache: cache[mus] = mp3(f"/home/claude/ep1/music/{mus}.mp3")
    tr = cache[mus]; start = int(OFF.get(mus, 0) * SR)
    a = int(max(0, t0 - 0.6) * SR); b = int(min(M.TOTAL + 1, t1 + 0.6) * SR); L = b - a
    seg = np.tile(tr[start:], int(np.ceil(L / max(1, len(tr) - start))) + 1)[:L].copy()
    f = int(0.6 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    music[a:b] += seg
music /= max(1e-6, np.abs(music).max())
env = np.convolve(np.abs(voice), np.ones(4410) / 4410, "same")
duck = 0.26 - 0.15 * np.clip(env / 0.08, 0, 1)
music *= duck
# efeitos
fx = np.zeros(N, np.float32)
def put(t, name, g):
    s = sfxlib.load(name); i = int(max(0, t) * SR); s = s[: max(0, N - i)]; fx[i:i + len(s)] += s * g
ws = ["whoosh_1", "whoosh_2", "whoosh_3"]
for i, s in enumerate(M.SHOTS):
    sc, t0 = s["scene"], s["t0"]; wt = lambda w, n=0: t0 + M.wt(s, w, n)
    if i: put(t0, ws[i % 3], 0.16)
    if sc in ("ff_wembley", "fa_stadium", "sf_leg1b", "wb_arrive", "fs_tense", "wb_ball"): put(t0, "estadio_ambiente", 0.14)
    if sc in ("vote_card",): put(t0 + M.wt(s, "b"), "tambor_impacto", 0.4)
    if sc in ("ff_cut",): put(t0, "whoosh_grave", 0.3)
    if sc in ("fa_draw_x", "sf_draw", "cr_march", "cr_paper", "dl_bus", "fa_twist"): put(t0 + 0.15, "tambor_impacto", 0.32)
    if sc == "jan_arlo":
        for k in range(3): put(t0 + k * 0.6, "whoosh_grave", 0.2)
        put(t0 + 1.8, "whoosh_boom", 0.35); put(t0 + 1.9, "torcida_comemora", 0.12)
    if sc == "fa_goal1":
        t2 = M.wt(s, "quarenta")
        for a_, D_ in ((0, t2), (t2, s["t1"] - t0 - t2)):
            tg = min(4.2, D_ * 0.55); put(t0 + a_ + tg - 0.15, "chute_bola_2", 0.3); put(t0 + a_ + tg + 0.4, "torcida_aww", 0.3)
    if sc in ("fa_gildo_run", "sf_93", "wb_pass"): put(t0 + 0.3, "whoosh_3", 0.3); put(t0 + 0.5, "estadio_ambiente", 0.12)
    if sc in ("fa_murrey_goal", "fs_ollie_x", "sf_goal", "wb_goal"): put(t0, "torcida_grita_gol", 0.45); put(t0 + 0.4, "torcida_comemora", 0.3); put(t0, "whoosh_boom", 0.3)
    if sc == "wb_whistle": put(t0, "apito_juiz", 0.4); put(t0 + 0.3, "torcida_comemora", 0.35)
    if sc in ("fa_equal",): put(t0 + M.wt(s, "dois") - 0.5, "chute_bola_2", 0.35); put(t0 + M.wt(s, "dois"), "torcida_grita_gol", 0.4)
    if sc in ("lg_kofi2", "sf_leg2"): put(t0 + 3.0, "torcida_reacao_gol", 0.3)
    if sc == "fs_ollie": put(t0 + s["t1"] - t0 - 0.4, "chute_bola_1", 0.35)
    if sc == "wb_goal_w": put(t0 + 2.5, "torcida_aww", 0.25); put(t0 + M.wt(s, "kaikai") + 2.2, "torcida_reacao_gol", 0.35)
    if sc == "fa_miss": put(t0 + M.wt(s, "trave") - 0.3, "chute_bola_2", 0.35); put(t0 + M.wt(s, "trave"), "torcida_aww", 0.4)
    if sc == "fa_pens": put(t0, "apito_curto", 0.3)
    if sc == "cr_injury": put(t0 + M.wt(s, "coxa"), "whoosh_boom", 0.3)
    if sc in ("ev_murrey", "ev_gildo", "ev_kofi", "ev_ollie"): put(t0 + 0.9, "camera_click", 0.35); put(t0 + 0.9, "whoosh_boom", 0.2)
    if sc == "lg_kofi2": put(t0 + M.wt(s, "canta"), "torcida_grito_homens", 0.25)
    if sc == "dl_vote": put(t0, "tambor_impacto", 0.35)
    if sc == "fa_viral": put(t0 + M.wt(s, "apelido"), "camera_click", 0.3)
envf = 1 - 0.4 * np.clip(env / 0.12, 0, 1)
mix = voice + music + fx * envf
fo = int(0.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write("bed.wav", SR, (np.clip(music + fx * 0.6, -0.98, 0.98) * 32000).astype(np.int16))
wavfile.write("trilha2.wav", SR, (np.clip(mix, -0.98, 0.98) * 32000).astype(np.int16))
print("ok", round(N / SR, 1))
