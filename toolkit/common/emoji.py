"""Emojis ANIMADOS do Google (Noto Animated Emoji, licença CC BY 4.0) em assets/emoji/*.gif.
Uso: import emoji; paste(img, emoji.get("rindo", 220, t), x, y)   # t = tempo desde que o emoji apareceu
Nomes: rindo chorando_rindo fogo grito chorando palhaco olhos caveira bufando trofeu bola festa palmas oculos
       explodindo reza coracao_verde careta espiando bravo congelado dinheiro coroa sirene sono pensando
Novos: https://fonts.gstatic.com/s/e/notoemoji/latest/<codigo-hex>/512.gif (ver lista em googlefonts.github.io/noto-emoji-animation).
Crédito (CC BY): "Noto Animated Emoji – Google (CC BY 4.0)" pequeno na tela final junto do crédito da música.
"""
import functools, os
from PIL import Image, ImageSequence

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "emoji")
if not os.path.isdir(DIR): DIR = "/home/claude/videos-sylence/assets/emoji"
CREDIT = "Emoji: Noto Animated Emoji – Google (CC BY 4.0)"


@functools.lru_cache(64)
def _frames(name, size):
    im = Image.open(os.path.join(DIR, name + ".gif")); out = []
    for f in ImageSequence.Iterator(im):
        d = f.info.get("duration", 40) or 40
        out.append((f.convert("RGBA").resize((size, size), Image.LANCZOS), d / 1000))
    tot = sum(d for _, d in out)
    return out, tot


def get(name, size, t):
    fr, tot = _frames(name, int(size)); t = t % tot; acc = 0
    for im, d in fr:
        acc += d
        if t < acc: return im
    return fr[-1][0]


def names():
    return sorted(f[:-4] for f in os.listdir(DIR) if f.endswith(".gif"))
