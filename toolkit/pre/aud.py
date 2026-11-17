import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly
import make_pre as M
T = M.T
SR = 44100; N = int(M.TOTAL * SR) + SR; rng = np.random.default_rng(3)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
out = np.zeros(N); fx = np.zeros(N)
def put(buf, s, t, g):
    i = int(t * SR); s = s[: max(0, N - i)]; buf[i:i + len(s)] += s * g
def whoosh(d=0.4):
    n = int(d * SR); x = rng.standard_normal(n); t = np.arange(n) / SR; o = np.zeros(n)
    for k in range(0, n, 512):
        fc = 500 + 4000 * (k / n); o[k:k+512] = bp(x[max(0, k-2048):k+512], fc*0.6, fc*1.4)[-len(o[k:k+512]):]
    return o * np.sin(np.pi * t / d) ** 2
def pop():
    n = int(0.25 * SR); t = np.arange(n) / SR; f = 180 + 300 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
def kick():
    n = int(0.08 * SR); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 200, 1800) * np.exp(-t / 0.015)
sr, x = wavfile.read("narr.wav"); x = x.astype(float); x = x.mean(1) if x.ndim > 1 else x
x = resample_poly(x / 32768, SR, sr); put(out, x, M.LEAD, 1.0)
for t in [T("palmeiras", 1) - 0.2, T("provável") - 0.3, T("cruzeiro", 1) - 0.2, T("perigo") - 0.2, T("chave") - 0.3, T("meu") - 0.3, T("comenta") - 0.2]: put(fx, whoosh(), t - 0.2, 0.25)
for t in [T("dois", 1) - 0.1]: put(fx, pop(), t, 0.4)
mix = out / np.abs(out).max() * 0.9 + fx * 0.5
mix = mix[: int(M.TOTAL * SR)]; fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write("trilha.wav", SR, (np.clip(mix, -0.98, 0.98) * 32000).astype(np.int16))
