"""Trilha 'balanceada': épica com batida, efeitos nos momentos-chave, sem clipar."""
import json, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly

HERE = "/home/claude/work/tat"
SC = json.load(open(f"{HERE}/scenes.json"))
SR = 44100; TOTAL = sum(s["dur"] for s in SC); N = int(TOTAL * SR) + 3 * SR
rng = np.random.default_rng(21)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
mus = np.zeros((2, N)); drm = np.zeros((2, N)); fx = np.zeros((2, N)); vox = np.zeros(N)
def put(buf, s, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    s = s[: N - i] * g
    if buf.ndim == 1: buf[i:i + len(s)] += s; return
    buf[0, i:i + len(s)] += s * (1 - max(0, pan)); buf[1, i:i + len(s)] += s * (1 + min(0, pan))
def tt(n): return np.arange(n) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def wt(k, sub):
    for w, a, b in SC[k]["words"]:
        if sub.lower() in w.lower(): return SC[k]["start"] + a
st = [s["start"] for s in SC]; en = [s["start"] + s["dur"] for s in SC]

def piano(m, d=2.5, vel=1.0):
    n = int(d * SR); t = tt(n); f = hz(m); s = np.zeros(n)
    for k, a in enumerate((1, 0.45, 0.22, 0.12, 0.06), 1):
        s += a * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k) * (0.6 + f / 900))
    return lp(s * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.1), 3500) * vel * 0.5
def pad(notes, d, bright=1400):
    n = int(d * SR); t = tt(n); s = np.zeros(n)
    for m in notes:
        f = hz(m)
        for det in (-0.08, 0.08):
            ff = f * 2 ** (det / 12)
            s += np.sin(2 * np.pi * ff * t) + 0.3 * np.sin(4 * np.pi * ff * t) + 0.12 * np.sin(6 * np.pi * ff * t)
    return lp(s * np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 0.8), bright) / (2 * len(notes))
def strings(m, d):
    n = int(d * SR); t = tt(n); f = hz(m)
    s = sum((2 * ((f * dt * t + o) % 1) - 1) for dt, o in ((1, 0), (1.003, 0.3), (0.997, 0.6)))
    return lp(s * np.minimum(1, t / 0.01) * np.exp(-t / (d * 0.9)), 1800) * 0.18
def bass(m, d):
    n = int(d * SR); t = tt(n); f = hz(m)
    return np.tanh(1.5 * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t))) * np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.03) * 0.5
def kick():
    n = int(0.45 * SR); t = tt(n); f = 48 + 110 * np.exp(-t / 0.03)
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22))
def snare():
    n = int(0.3 * SR); t = tt(n)
    return np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5 + bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t / 0.1) * 0.7
def hat(o=False):
    n = int((0.18 if o else 0.04) * SR); return hp(rng.standard_normal(n), 7500) * np.exp(-tt(n) / (0.05 if o else 0.01)) * 0.5
def tom(f0=110):
    n = int(0.5 * SR); t = tt(n); f = f0 + 60 * np.exp(-t / 0.05)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.25)
def impact(g_noise=0.35):
    n = int(2.4 * SR); t = tt(n); f = 34 + 70 * np.exp(-t / 0.07)
    boom = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7))
    body = lp(rng.standard_normal(n), 2500) * np.exp(-t / 0.12) * g_noise
    tail = lp(rng.standard_normal(n), 900) * np.exp(-t / 1.0) * 0.15
    return (boom + body + tail) * np.minimum(1, t / 0.004)
def riser(d):
    n = int(d * SR); t = tt(n)
    x = rng.standard_normal(n); u = t / d
    return ((lp(x, 900) * (1 - u) + bp(x, 1500, 7000) * u) * 0.6 + np.sin(2 * np.pi * np.cumsum(180 * 6 ** (t / d)) / SR) * 0.12) * (t / d) ** 2.2
def whoosh(d=0.45):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); seg = 512
    for k in range(0, n, seg):
        fc = 400 + 4500 * (k / n) ** 1.5
        out[k:k + seg] = bp(x[max(0, k - 2048):k + seg], fc * 0.6, fc * 1.4)[-len(out[k:k + seg]):]
    return out * np.sin(np.pi * tt(n) / d) ** 2
def crowd(d, roar=True):
    n = int(d * SR); t = tt(n)
    x = bp(rng.standard_normal(n), 300, 2400) + 0.5 * bp(rng.standard_normal(n), 500, 1200) * (1 + 0.35 * np.sin(2 * np.pi * 2.1 * t))
    e = (np.minimum(1, t / 0.2) * np.exp(-np.maximum(0, t - 1.2) / 1.3)) if roar else (np.minimum(1, t / 1.0) * np.minimum(1, (d - t) / 1.0))
    return lp(x * e, 3000)
def heartbeat():
    n = int(0.5 * SR); t = tt(n); s = np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.08)
    return s + np.concatenate([np.zeros(int(0.18 * SR)), s[: n - int(0.18 * SR)] * 0.7])
def whistle(d):
    n = int(d * SR); t = tt(n)
    s = np.sin(2 * np.pi * (2800 + 50 * np.sin(2 * np.pi * 26 * t)) * t)
    return lp(s, 4000) * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08) * 0.2

BPM = 92; BEAT = 60 / BPM; BAR = 4 * BEAT
MIN = [(47, [59, 62, 66]), (43, [59, 62, 67]), (50, [57, 62, 66]), (45, [57, 61, 64])]   # Bm G D A
MAJ = [(50, [62, 66, 69]), (45, [61, 64, 69]), (47, [62, 66, 71]), (43, [62, 67, 71])]   # D A Bm G
K, SN = kick(), snare()

def music(t0, t1, prog, level, bright=1600):
    """level 0: pad+piano; 1: +strings pulse; 2: +kick/hat/bass; 3: full (snare, open hats)"""
    t = t0; k = 0
    while t < t1 - 0.1:
        root, ch = prog[k % 4]; d = min(BAR, t1 - t)
        put(mus, pad([root + 12] + ch, d + 0.8, bright), t, 0.3)
        put(mus, piano(ch[0] + 12, 2.5, 0.7), t, 0.35); put(mus, piano(ch[2] + 12, 2.0, 0.5), t + BEAT * 2, 0.3)
        for i in range(8 if level >= 1 else 0):
            ts = t + i * BEAT / 2
            if ts < t1: put(mus, strings(ch[i % 3] + 12, BEAT / 2), ts, 0.9 if level >= 2 else 0.6, 0.3 if i % 2 else -0.3)
        if level >= 2:
            for b in range(4):
                tb = t + b * BEAT
                if tb >= t1: break
                put(drm, K, tb, 0.8 if b in (0, 2) or level >= 3 else 0.0)
                put(mus, bass(root - 12, BEAT * 0.9), tb, 0.55)
                for h in range(2):
                    th = tb + h * BEAT / 2
                    if th < t1: put(drm, hat(level >= 3 and h == 1), th, 0.35, 0.2)
                if level >= 3 and b in (1, 3): put(drm, SN, tb, 0.5)
        t += BAR; k += 1


def G(k, sub, off=0.0):
    for w, a, b in SC[k]["words"]:
        if w.lower().strip(".,:;!?") == sub.lower(): return SC[k]["start"] + a + off
    raise KeyError(sub)
def thump():
    n = int(0.18 * SR); t = tt(n); f = 90 + 80 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) + lp(rng.standard_normal(n), 2500) * np.exp(-t / 0.015) * 0.5
def swish():
    n = int(0.6 * SR); t = tt(n); return bp(rng.standard_normal(n), 2000, 7000) * np.exp(-t / 0.18) * np.minimum(1, t / 0.02)
LOFI = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]   # Am F C G
for k in range(1, len(SC)): put(fx, whoosh(0.7), st[k] - 0.35, 0.22)
kicks = [G(2, "bola", -0.2), G(2, "escanteio", 0.5), G(4, "chute", -0.2), G(5, "ataque", -0.3), G(7, "recuo", -0.3), G(7, "pegar", 0.7), st[8], st[8] + 1.5]
for kt in kicks: put(fx, thump(), kt, 0.5)
put(fx, swish(), G(4, "chute", 0.25), 0.4); put(fx, crowd(2.5), G(4, "chute", 0.3), 0.18)
put(fx, swish(), st[8] + 1.85, 0.35)
put(fx, whistle(0.4), G(6, "estreiam", -0.2), 0.8)
put(fx, impact(0.1), G(8, "var", -0.2), 0.25)
put(fx, whistle(0.35), G(9, "escanteio", -0.2), 0.7)
for k in range(len(SC)):
    r, x = wavfile.read(f"{HERE}/narr/n{k}.wav"); x = x.astype(float)
    if x.ndim > 1: x = x.mean(1)
    x /= 32768.0
    if r != SR: x = resample_poly(x, SR, r)
    put(vox, x, st[k] + 0.3)
vox = vox / (np.abs(vox).max() + 1e-9) * 0.9
L = int(0.3 * SR); envv = np.convolve(np.abs(vox), np.ones(L) / L, "same")
duck = 1 - 0.55 * np.clip(envv / (envv.max() * 0.2), 0, 1)
duck = np.convolve(duck, np.ones(int(0.15 * SR)) / int(0.15 * SR), "same")

def bus(x, peak):
    x = x / (np.abs(x).max() + 1e-9)
    return np.tanh(1.6 * x) / np.tanh(1.6) * peak   # soft saturation = no harsh peaks
m = 0 * mus
f = bus(fx, 0.22)
mix = m * duck + f * (0.55 + 0.45 * duck) + vox[None, :]
nt = int(TOTAL * SR); mix = mix[:, :nt]; fo = int(1.6 * SR); mix[:, nt - fo:] *= np.linspace(1, 0, fo)
# simple look-ahead limiter
env = np.max(np.abs(mix), 0); win = int(0.01 * SR)
env = np.convolve(env, np.ones(win) / win, "same") * 1.0
g = np.minimum(1, 0.9 / np.maximum(env, 1e-6)); g = np.minimum.accumulate(g[::-1])[::-1] if False else g
g = np.convolve(g, np.ones(win) / win, "same")
mix = np.clip(mix * g, -0.98, 0.98)
wavfile.write(f"{HERE}/trilha.wav", SR, (mix.T * 32000).astype(np.int16))
print("ok", TOTAL)
