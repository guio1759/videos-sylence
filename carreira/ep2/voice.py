"""Acelera a voz, corta silêncios e gera tempos por palavra (faster-whisper local)."""
import numpy as np, wave, subprocess, json, re, unicodedata
from script2 import BLOCKS
SR = 24000; TEMPO = 1.1
def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def squeeze(a, maxgap=0.22, keep=0.16, thr=0.012):
    win = int(0.02 * SR); env = np.sqrt(np.convolve(a * a, np.ones(win) / win, "same"))
    quiet = env < thr; out = []; i = 0; n = len(a)
    # tira silêncio do começo/fim
    nz = np.where(~quiet)[0]; a = a[max(0, nz[0] - int(0.05 * SR)): nz[-1] + int(0.08 * SR)]; quiet = quiet[max(0, nz[0] - int(0.05 * SR)): nz[-1] + int(0.08 * SR)]
    n = len(a)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            L = j - i
            if L > maxgap * SR: out.append(a[i:i + int(keep * SR / 2)]); out.append(a[j - int(keep * SR / 2):j])
            else: out.append(a[i:j])
            i = j
        else:
            j = i
            while j < n and not quiet[j]: j += 1
            out.append(a[i:j]); i = j
    return np.concatenate(out)
parts = []; offs = []
t = 0.0
for k in range(len(BLOCKS)):
    a = squeeze(load(f"raw_{k}.wav"))
    gap = np.zeros(int(0.35 * SR), np.float32)
    offs.append(t); parts += [a, gap]; t += (len(a) + len(gap)) / SR
full = np.concatenate(parts)
w = wave.open("narr_slow.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(full, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "narr_slow.wav", "-af", f"atempo={TEMPO}", "-ar", "44100", "narr.wav"], check=True)
print("dur", round(len(full) / SR / TEMPO, 1))
