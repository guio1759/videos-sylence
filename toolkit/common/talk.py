"""Bonecos 3D FALANDO (grátis): boca sincronizada com a voz via Rhubarb Lip Sync + piscada + cabeça mexendo.

Rhubarb (MIT, github.com/DanielSWolf/rhubarb-lip-sync) é baixado pelo setup.sh em /home/claude/tools.
Modo "phonetic" (funciona em português).

Uso:
    import talk
    cues = talk.lipsync("/caminho/fala.wav")             # [(t0, t1, 'A'..'H'/'X'), ...]
    T = talk.Talker(talk.CHARS["reporter"])              # ou Talker({"img":..., "mouth":(x,y,w), "eyes":[(x,y,w,h),...]})
    im = T.frame(t, cues, energy)                        # RGBA do personagem no tempo t (cutout=True tira o fundo)

Novos personagens: gere com cfimg.py pedindo "mouth closed, looking straight at camera" e anote boca/olhos
(coordenadas em pixels da imagem 1024x1024) no dicionário CHARS. NUNCA usar rosto de pessoa real.
"""
import json, math, os, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RHUBARB = "/home/claude/tools/Rhubarb-Lip-Sync-1.13.0-Linux/rhubarb"
ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "chars")
if not os.path.isdir(ASSET): ASSET = "/home/claude/videos-sylence/assets/chars"

CHARS = {
    "reporter": {"img": "reporter.jpg", "mouth": (500, 532, 140), "eyes": [(410, 390, 92, 80), (580, 382, 92, 80)]},
    "torcedor": {"img": "torcedor.jpg", "mouth": (516, 566, 104), "eyes": [(440, 430, 84, 70), (590, 426, 84, 70)]},
}


def lipsync(wav):
    """Roda o Rhubarb (cache em <wav>.cues.json). Retorna lista (t0, t1, forma)."""
    out = wav + ".cues.json"
    if not os.path.exists(out):
        tmp = wav + ".16k.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-ac", "1", "-ar", "16000", tmp], check=True)
        subprocess.run([RHUBARB, "-q", "-r", "phonetic", "-f", "json", tmp, "-o", out], check=True)
    d = json.load(open(out))
    return [(c["start"], c["end"], c["value"]) for c in d["mouthCues"]]


def shift(cues, dt):
    return [(a + dt, b + dt, v) for a, b, v in cues]


def shape_at(cues, t):
    for a, b, v in cues:
        if a <= t < b: return v
    return "X"


class Talker:
    def __init__(self, spec, cutout=False, size=None):
        self.spec = spec
        p = spec["img"] if os.path.isabs(spec["img"]) else os.path.join(ASSET, spec["img"])
        im = Image.open(p).convert("RGBA")
        if cutout:
            cp = p + ".cut.png"
            if not os.path.exists(cp):
                from rembg import remove, new_session   # u2net: leve (o modelo padrão bria tem 1 GB e estoura a memória)
                remove(im, session=new_session("u2net")).save(cp)
            im = Image.open(cp).convert("RGBA")
        self.base = im
        mx, my, mw = spec["mouth"]
        arr = np.asarray(im.convert("RGB")).astype(int)
        def samp(x, y, r=6):
            x, y = int(x), int(y); return tuple(arr[max(0, y - r):y + r, max(0, x - r):x + r].reshape(-1, 3).mean(0).astype(int))
        # pele: média das bochechas ao lado da boca
        self.skin = tuple(int((a + b) / 2) for a, b in zip(samp(mx - mw * 0.75, my - mw * 0.05), samp(mx + mw * 0.75, my - mw * 0.05)))
        self.lip = tuple(int(c * k) for c, k in zip(self.skin, (0.72, 0.42, 0.42)))
        self.size = size
        # versões sem boca / com olhos fechados por inpainting (sombras naturais da pele)
        import cv2
        rgb = np.asarray(im.convert("RGB")).copy(); bgr = rgb[:, :, ::-1].copy()
        mm = np.zeros(bgr.shape[:2], np.uint8)
        cv2.ellipse(mm, (int(mx), int(my)), (int(mw * 0.58), int(mw * 0.24)), 0, 0, 360, 255, -1)
        nm = cv2.inpaint(bgr, mm, 9, cv2.INPAINT_TELEA)[:, :, ::-1]
        self.nomouth = Image.fromarray(nm).convert("RGBA"); self.nomouth.putalpha(im.getchannel("A"))
        em = np.zeros(bgr.shape[:2], np.uint8)
        for ex, ey, ew, eh in spec.get("eyes", []):
            cv2.ellipse(em, (int(ex), int(ey)), (int(ew * 0.62), int(eh * 0.62)), 0, 0, 360, 255, -1)
        ce = cv2.inpaint(bgr, em, 11, cv2.INPAINT_TELEA)[:, :, ::-1]
        self.closed = Image.fromarray(ce).convert("RGBA"); self.closed.putalpha(im.getchannel("A"))

    @functools.lru_cache(32)
    def _mouth(self, v):
        mx, my, mw = self.spec["mouth"]; W = int(mw * 1.6); H = int(mw * 1.1)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); cx, cy = W / 2, H / 2
        # cobre a boca original com pele (borda suave)
        dark = (60, 22, 26); teeth = (250, 248, 240); tongue = (205, 85, 95); lw = max(3, int(mw * 0.05))
        def opening(w, h, top_teeth=True, tng=False, full_teeth=False):
            box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            d.ellipse(box, fill=dark, outline=self.lip, width=lw)
            if full_teeth: d.rectangle((cx - w * 0.38, cy - h * 0.35, cx + w * 0.38, cy + h * 0.1), fill=teeth)
            elif top_teeth: d.chord((cx - w * 0.42, cy - h * 0.48, cx + w * 0.42, cy + h * 0.2), 180, 360, fill=teeth)
            if tng: d.chord((cx - w * 0.32, cy, cx + w * 0.32, cy + h * 0.5), 0, 180, fill=tongue)
        if v in ("X", "A"):
            d.arc((cx - mw * 0.4, cy - mw * 0.22, cx + mw * 0.4, cy + mw * 0.1), 25, 155, fill=self.lip, width=lw + 1)
        elif v == "B": opening(mw * 0.72, mw * 0.2)
        elif v == "C": opening(mw * 0.78, mw * 0.34)
        elif v == "D": opening(mw * 0.82, mw * 0.5, tng=True)
        elif v == "E": opening(mw * 0.55, mw * 0.42)
        elif v == "F": opening(mw * 0.36, mw * 0.3, top_teeth=False)
        elif v == "G": opening(mw * 0.7, mw * 0.2, full_teeth=True)
        elif v == "H": opening(mw * 0.72, mw * 0.34, tng=True)
        return lay

    def frame(self, t, cues=(), energy=0.0, blink_every=3.3):
        mx, my, mw = self.spec["mouth"]; v = shape_at(cues, t)
        if v == "X": im = self.base.copy()   # boca fechada = a original do personagem
        else:
            im = self.nomouth.copy(); lay = self._mouth(v)
            lay = lay.filter(ImageFilter.GaussianBlur(0.8)); im.alpha_composite(lay, (int(mx - lay.width / 2), int(my - lay.height / 2)))
        ph = (t + (sum(map(ord, self.spec["img"])) % 7) * 0.37) % blink_every
        if ph < 0.14 and self.spec.get("eyes"):  # piscada: pálpebra desce (pele do inpainting) e sobe
            k = 1 - abs(ph - 0.07) / 0.07
            m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m); d = ImageDraw.Draw(im)
            for ex, ey, ew, eh in self.spec["eyes"]:
                top = ey - eh * 0.66; bot = top + eh * 1.32 * k
                dm.rectangle((ex - ew * 0.66, top, ex + ew * 0.66, bot), fill=255)
            m = m.filter(ImageFilter.GaussianBlur(2)); im.paste(self.closed, (0, 0), m)
            if k > 0.75:
                for ex, ey, ew, eh in self.spec["eyes"]:
                    d.arc((ex - ew * 0.55, ey - eh * 0.25, ex + ew * 0.55, ey + eh * 0.35), 15, 165, fill=(45, 28, 28), width=max(3, int(ew * 0.07)))
        # cabeça viva: leve balanço + pulo com a energia da voz
        ang = 1.6 * math.sin(t * 1.7) + 2.2 * energy * math.sin(t * 9)
        sc = 1.0 + 0.012 * math.sin(t * 2.3) + 0.025 * energy
        im = im.rotate(ang, resample=Image.BICUBIC, center=(mx, my + mw * 0.8))
        if self.size: im = im.resize((int(self.size * sc), int(self.size * sc)), Image.LANCZOS)
        elif sc != 1: im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        return im


def energy_env(wav, fps=30):
    """Energia da voz por frame (0–1), para o balanço da cabeça."""
    import soundfile as sf
    a, sr = sf.read(wav, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    hop = int(sr / fps); n = len(a) // hop
    e = np.array([np.sqrt((a[k * hop:(k + 1) * hop] ** 2).mean()) for k in range(n)])
    return np.clip(e / (e.max() + 1e-9) * 1.4, 0, 1)
