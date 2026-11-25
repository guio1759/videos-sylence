"""Fotos REAIS animadas de jeito bonito e fluido (estilo edit): Ken Burns, recorte 2.5D com contorno, cartão polaroide,
transição de chicote, gradação de cor. Fotos vêm de fotos_cc.py (Wikimedia, com crédito) ou do usuário.

Principais:
    kb(img, t, dur, z=(1.05, 1.18), f0=(.5,.5), f1=(.5,.45))      -> RGBA 1080x1920, zoom/pan contínuo (Ken Burns)
    pan_wide(img, t, dur, x0=0.0, x1=1.0)                          -> panorâmica atravessando a foto (estádio)
    pop3d(img, t, dur, focus=(.5,.4))                              -> fundo desfocado + jogador recortado "saindo" da foto
    polaroid(img, w, rot=0)                                        -> cartão com borda branca e sombra
    whip(a, b, u)                                                  -> transição de chicote entre dois quadros (u 0..1)
    credit(img, texto)                                             -> crédito pequeno da foto (obrigatório nas fotos CC)
"""
import functools, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

W, H = 1080, 1920


def _ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


@functools.lru_cache(32)
def load(path, grade=True):
    im = Image.open(path).convert("RGB")
    if grade:  # leve "look de edit": contraste, saturação e nitidez
        im = ImageEnhance.Contrast(im).enhance(1.08); im = ImageEnhance.Color(im).enhance(1.12)
        im = im.filter(ImageFilter.UnsharpMask(2, 60, 2))
    return im.convert("RGBA")


@functools.lru_cache(8)
def vignette(strength=150):
    m = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(m)
    d.ellipse((-W // 8, -H // 10, W // 4 + W // 8, H // 4 + H // 10), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(40)).resize((W, H))
    v = Image.new("RGBA", (W, H), (0, 0, 0, strength)); v.putalpha(ImageOps.invert(m).point(lambda x: x * strength // 255)); return v


def _cover(img, z, fx, fy, ar=W / H):
    iw, ih = img.size
    if iw / ih > ar: ch = ih / z; cw = ch * ar
    else: cw = iw / z; ch = cw / ar
    x0 = min(max(0, fx * iw - cw / 2), iw - cw); y0 = min(max(0, fy * ih - ch / 2), ih - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)


def kb(img, t, dur, z=(1.05, 1.18), f0=(0.5, 0.5), f1=(0.5, 0.45), vig=120):
    u = _ease(t / max(dur, 1e-3)); zz = z[0] + (z[1] - z[0]) * u
    out = _cover(img, zz, f0[0] + (f1[0] - f0[0]) * u, f0[1] + (f1[1] - f0[1]) * u)
    if vig: out.alpha_composite(vignette(vig))
    return out


def pan_wide(img, t, dur, x0=0.0, x1=1.0, zoom=1.0, vig=110):
    """Atravessa uma foto larga (panorama de estádio) da esquerda para a direita."""
    iw, ih = img.size; ch = ih / zoom; cw = ch * W / H; u = _ease(t / max(dur, 1e-3))
    xc = (x0 + (x1 - x0) * u) * (iw - cw)
    out = img.crop((int(xc), int((ih - ch) / 2), int(xc + cw), int((ih + ch) / 2))).resize((W, H), Image.BICUBIC)
    if vig: out.alpha_composite(vignette(vig))
    return out


@functools.lru_cache(16)
def cutout(path):
    cp = path + ".cut.png"
    if not os.path.exists(cp):
        from rembg import remove, new_session  # u2net_human_seg: recorta pessoa; leve
        remove(Image.open(path).convert("RGB"), session=new_session("u2net_human_seg")).save(cp)
    im = Image.open(cp).convert("RGBA"); bb = im.getchannel("A").point(lambda a: 255 if a > 40 else 0).getbbox()
    return im.crop(bb) if bb else im


@functools.lru_cache(16)
def sticker(path, h, stroke=10, col=(255, 255, 255)):
    """Recorte com contorno branco e sombra (look figurinha/edit)."""
    c = cutout(path); c = c.resize((int(c.width * h / c.height), int(h)), Image.LANCZOS)
    pad = stroke * 3; base = Image.new("RGBA", (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", base.size, 0); a.paste(c.getchannel("A"), (pad, pad))
    ring = a.filter(ImageFilter.MaxFilter(stroke * 2 + 1)); sh = a.filter(ImageFilter.GaussianBlur(stroke * 2))
    base.paste(Image.new("RGBA", base.size, (0, 0, 0, 160)), (stroke // 2, stroke), sh)
    base.paste(Image.new("RGBA", base.size, col + (255,)), (0, 0), ring)
    base.alpha_composite(c, (pad, pad)); return base


def pop3d(path, t, dur, focus=(0.5, 0.42), h=1500, y=1180, x=None, delay=0.0, blur=14, dim=110):
    """Fundo = a própria foto desfocada e escurecida em Ken Burns; frente = pessoa recortada com contorno, entrando de baixo
    e se mexendo mais rápido que o fundo (paralaxe 2.5D)."""
    img = load(path); bg = kb(img, t, dur, (1.15, 1.3), focus, focus, vig=0).filter(ImageFilter.GaussianBlur(blur))
    bg.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, dim)))
    u = _ease((t - delay) / 0.45) if t > delay else 0
    if u > 0:
        st = sticker(path, int(h)); sc = 0.92 + 0.08 * _ease((t - delay) / max(dur, 1e-3)) + 0.04 * (1 - u)
        s2 = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
        cx = (x if x is not None else W / 2) + 18 * math.sin(t * 0.9); cy = y + (1 - u) * 600
        bg.alpha_composite(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)))
    bg.alpha_composite(vignette(100)); return bg


def polaroid(img, w, rot=0, border=0.045, shadow=True):
    if isinstance(img, str): img = load(img)
    w = int(w); im = img.copy(); im.thumbnail((w, int(w * 1.6)), Image.LANCZOS)
    b = int(w * border); card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b + int(b * 2.2)), (250, 250, 246, 255))
    card.alpha_composite(im, (b, b))
    out = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    if not shadow: return out
    sh = Image.new("RGBA", (out.width + 60, out.height + 60), (0, 0, 0, 0)); a = out.getchannel("A")
    sh.paste(Image.new("RGBA", out.size, (0, 0, 0, 150)), (34, 40), a); sh = sh.filter(ImageFilter.GaussianBlur(16))
    sh.alpha_composite(out, (20, 20)); return sh


def whip(a, b, u):
    """Chicote: a sai borrando para a esquerda, b entra borrando da direita (u = 0..1)."""
    u = _ease(u); k = int(60 * math.sin(math.pi * u)) + 1
    src = a if u < 0.5 else b; off = int((-u if u < 0.5 else 1 - u) * W * 0.6)
    fr = Image.new("RGBA", (W, H)); fr.alpha_composite(src, (off, 0))
    return fr.filter(ImageFilter.BoxBlur(k)) if k > 2 else fr


def credit(img, s, y=H - 150, size=24):
    from PIL import ImageFont
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", size)
    d = ImageDraw.Draw(img); tw = d.textlength(s, font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 12, y - 18, W / 2 + tw / 2 + 12, y + 18), 10, fill=(0, 0, 0, 120))
    d.text((W / 2, y), s, font=f, fill=(235, 235, 235), anchor="mm")
