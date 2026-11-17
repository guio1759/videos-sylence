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
OFF = {"Five_Armies": 0, "Interloper": 20, "Dreamer": 8, "Heartbreaking": 0, "Rising_Game": 4, "Volatile_Reaction": 10, "Wholesome": 0}
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
    if sc == "tz_title": put(t0, "tambor_impacto", 0.4)
    if sc in ("tz_broke", "crewe_after", "drama_bench", "email_x"): put(t0 + 0.15, "tambor_impacto", 0.3)
    if sc == "tz_gamer": put(t0 + 0.6, "tambor_impacto", 0.25)
    if sc == "crewe": put(t0, "estadio_ambiente", 0.12); put(t0 + 11.5, "estadio_ambiente", 0.12)
    if sc == "crewe_goal":
        tg = min(4.2, (s["t1"] - t0) * 0.55); put(t0, "estadio_ambiente", 0.1); put(t0 + tg - 0.15, "chute_bola_2", 0.35); put(t0 + tg + 0.35, "whoosh_boom", 0.35); put(t0 + tg + 0.5, "torcida_aww", 0.35)
    if sc == "rick_injury": put(wt("terceiro"), "whoosh_boom", 0.35)
    if sc == "rick_call": put(t0 + 0.1, "apito_curto", 0.0)
    if sc.startswith("walk_") and sc != "walk_murrey_pre":
        sp = 0.45 if sc in ("walk_kofi", "walk_ollie") else 0.8
        for k in range(3): put(t0 + k * sp, "whoosh_grave", 0.2)
        put(t0 + sp * 3, "whoosh_boom", 0.35); put(t0 + sp * 3 + 0.1, "torcida_comemora", 0.12)
    if sc == "fixtures_bad": put(wt("vigesimo"), "tambor_impacto", 0.3)
    if sc == "headline_out": put(t0, "torcida_grito_homens", 0.15)
    if sc == "assist": put(t0 + 0.2, "chute_bola_1", 0.3); put(t0 + M.wt(s, "letra") - 0.2, "torcida_reacao_gol", 0.3)
    if sc == "kaikai_goal": put(t0 + 1.3, "chute_bola_2", 0.35); put(t0 + 1.7, "torcida_grita_gol", 0.32)
    if sc == "fixtures_good": put(t0 + 1, "torcida_comemora", 0.15)
    if sc == "base_race": put(wt("chinelo") - 0.3, "whoosh_3", 0.3)
    if sc in ("boxing", "boxing_sub"): put(t0, "estadio_ambiente", 0.12)
    if sc == "boxing_sub": put(t0 + 0.2, "apito_curto", 0.3)
    if sc == "murrey_goal": put(t0, "estadio_ambiente", 0.12); put(t0 + 2.6, "chute_bola_2", 0.4)
    if sc == "murrey_goal_x": put(t0, "torcida_grita_gol", 0.45); put(t0 + 0.4, "torcida_comemora", 0.3); put(t0, "whoosh_boom", 0.3)
    if sc == "hug": put(t0, "torcida_comemora", 0.2)
    if sc == "ovr_up": put(t0 + M.wt(s, "cinquenta", 1), "camera_click", 0.35)
    if sc == "ab": put(t0, "tambor_impacto", 0.35)
envf = 1 - 0.4 * np.clip(env / 0.12, 0, 1)
mix = voice + music + fx * envf
fo = int(0.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write("bed.wav", SR, (np.clip(music + fx * 0.6, -0.98, 0.98) * 32000).astype(np.int16))
wavfile.write("trilha2.wav", SR, (np.clip(mix, -0.98, 0.98) * 32000).astype(np.int16))
print("ok", round(N / SR, 1))
