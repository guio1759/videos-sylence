"""Fontes extras grátis (Google Fonts, licença OFL/Apache) em assets/fonts.
Uso: from fonts import F; f = F("anton", 120)
anton = condensada de manchete | bebas = títulos altos e finos | bangers = quadrinho/zoeira | luckiest = cartoon gordinha (zoeira)
"""
import functools, os
from PIL import ImageFont
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "fonts")
if not os.path.isdir(DIR): DIR = "/home/claude/videos-sylence/assets/fonts"
FILES = {"anton": "Anton-Regular.ttf", "bebas": "BebasNeue-Regular.ttf", "bangers": "Bangers-Regular.ttf", "luckiest": "LuckiestGuy-Regular.ttf"}
@functools.lru_cache(128)
def F(name, size): return ImageFont.truetype(os.path.join(DIR, FILES[name]), int(size))
