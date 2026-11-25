"""Fundos em VÍDEO real e grátis (Pixabay Videos; a mesma chave das fotos). Licença Pixabay: uso comercial, sem crédito obrigatório.
Só cenas genéricas: estádio, torcida, sinalizador, bola, gramado, cidade, céu. NUNCA vídeo de jogador/pessoa identificável em destaque.
Opcional: Pexels (chave grátis em ~/.secrets/pexels_key ou PEXELS_KEY) como segunda fonte.

Uso:
    python3 bgvideo.py "stadium crowd night" pasta [n]      -> baixa n vídeos (mp4) + creditos.txt
    import bgvideo; B = bgvideo.BG("arquivo.mp4", dim=110, blur=0)   # B.frame(T) -> RGBA 1080x1920 (loop)
"""
import json, os, subprocess, sys, urllib.parse, urllib.request
import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920
CACHE = "/home/claude/work/bgvideo"


def _key(env, f):
    k = os.environ.get(env); p = os.path.expanduser(f)
    return k or (open(p).read().strip() if os.path.exists(p) else None)


def _get(url, out=None, hdr=None):
    req = urllib.request.Request(url, headers={"User-Agent": "videos-sylence/1.0", **(hdr or {})})
    with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
    if out: open(out, "wb").write(data)
    return data


def buscar(q, pasta=CACHE, n=3, min_w=1280):
    os.makedirs(pasta, exist_ok=True); outs, cred = [], []
    k = _key("PIXABAY_KEY", "~/.secrets/pixabay_key")
    if k:
        d = json.loads(_get(f"https://pixabay.com/api/videos/?key={k}&q={urllib.parse.quote(q)}&safesearch=true&per_page={max(3, n * 2)}"))
        for h in d.get("hits", []):
            if len(outs) >= n: break
            v = h["videos"].get("large") or h["videos"].get("medium")
            if not v or not v.get("url") or v.get("width", 0) < min_w: v = h["videos"].get("medium")
            if not v or not v.get("url"): continue
            o = os.path.join(pasta, f"pxb_{h['id']}.mp4")
            if not os.path.exists(o): _get(v["url"], o)
            outs.append(o); cred.append(f"{os.path.basename(o)}: Pixabay {h['pageURL']} ({h.get('duration')} s)")
    pk = _key("PEXELS_KEY", "~/.secrets/pexels_key")
    if pk and len(outs) < n:
        d = json.loads(_get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page={n}&orientation=portrait", hdr={"Authorization": pk}))
        for v in d.get("videos", []):
            if len(outs) >= n: break
            f = sorted([x for x in v["video_files"] if x.get("width")], key=lambda x: -x["width"])
            f = next((x for x in f if x["width"] <= 1920), f[-1] if f else None)
            if not f: continue
            o = os.path.join(pasta, f"pex_{v['id']}.mp4")
            if not os.path.exists(o): _get(f["link"], o)
            outs.append(o); cred.append(f"{os.path.basename(o)}: Pexels {v['url']}")
    with open(os.path.join(pasta, "creditos.txt"), "a") as fh: fh.write("\n".join(cred) + "\n")
    return outs


class BG:
    """Decodifica o trecho uma vez (meia resolução, 30 fps) e devolve o quadro do tempo T em loop, cobrindo 9:16."""
    def __init__(self, path, t0=0.0, dur=6.0, dim=110, blur=0, sat=1.0, fps=30):
        w, h = W // 2, H // 2
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps}"
        if sat != 1.0: vf += f",eq=saturation={sat}"
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-t", str(dur), "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        n = len(raw) // (w * h * 3); self.fr = np.frombuffer(raw[:n * w * h * 3], np.uint8).reshape(n, h, w, 3)
        # vai-e-volta (ping-pong) para o loop não dar pulo
        self.idx = list(range(n)) + list(range(n - 2, 0, -1)); self.fps = fps; self.dim = dim; self.blur = blur

    def frame(self, T):
        a = self.fr[self.idx[int(T * self.fps) % len(self.idx)]]
        im = Image.fromarray(a).resize((W, H), Image.BILINEAR)
        if self.blur: im = im.filter(ImageFilter.GaussianBlur(self.blur))
        im = im.convert("RGBA")
        if self.dim: im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, self.dim)))
        return im


if __name__ == "__main__":
    print(buscar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else CACHE, int(sys.argv[3]) if len(sys.argv) > 3 else 3))
