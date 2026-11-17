"""Efeitos sonoros CC0 (Openverse/Freesound/Wikimedia) para os videos. load(nome) -> np.float32 mono 44100Hz."""
import os, functools, numpy as np
from scipy.io import wavfile
DIR = os.path.dirname(os.path.abspath(__file__)); SR = 44100
@functools.lru_cache(None)
def load(name):
    sr, x = wavfile.read(os.path.join(DIR, name + ".wav")); return x.astype(np.float32) / 32768
def names(): return sorted(f[:-4] for f in os.listdir(DIR) if f.endswith(".wav"))
