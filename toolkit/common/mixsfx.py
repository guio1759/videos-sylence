"""Mixa narracao + efeitos reais da biblioteca assets/sfx.
uso: from mixsfx import mix
mix("narr.wav", total_s, events=[(t, "whoosh_1", 0.3), (t, "torcida_reacao_gol", 0.25), ...], out="trilha.wav", lead=0.2, bed=("estadio_ambiente", 0.06))
- narracao sempre por cima; efeitos curtos 0.25-0.4; torcida 0.2-0.3; ambiente (bed) 0.04-0.08 com fade.
"""
import sys, numpy as np
sys.path.insert(0, "/home/claude/work/sfx")
from scipy.io import wavfile
from scipy.signal import resample_poly
import sfxlib
SR = 44100
def _put(buf, s, t, g):
    i = int(max(0, t) * SR); s = s[: max(0, len(buf) - i)]; buf[i:i + len(s)] += s * g
def mix(narr, total, events=(), out="trilha.wav", lead=0.2, bed=None):
    N = int(total * SR); voice = np.zeros(N); fx = np.zeros(N)
    sr, x = wavfile.read(narr); x = x.astype(float); x = x.mean(1) if x.ndim > 1 else x
    x = resample_poly(x / 32768, SR, sr); _put(voice, x, lead, 1.0)
    voice = voice / max(1e-6, np.abs(voice).max()) * 0.9
    if bed:
        b = sfxlib.load(bed[0]); reps = int(np.ceil(N / len(b))); b = np.tile(b, reps)[:N]
        f = int(1.0 * SR); b[:f] *= np.linspace(0, 1, f); b[-f:] *= np.linspace(1, 0, f); fx += b * bed[1]
    for t, name, g in events: _put(fx, sfxlib.load(name), t, g)
    # ducking: abaixa efeitos onde a voz esta forte
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, "same"); duck = 1 - 0.45 * np.clip(env / 0.15, 0, 1)
    m = voice + fx * duck
    fo = int(0.5 * SR); m[-fo:] *= np.linspace(1, 0, fo)
    wavfile.write(out, SR, (np.clip(m, -0.98, 0.98) * 32000).astype(np.int16))
