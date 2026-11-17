"""Cartas estilo FIFA para a série Modo Carreira (Cambridge United)."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

D = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(D, "assets")
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FC = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


def font(sz, cond=False):
    return ImageFont.truetype(FC if cond else FB, sz)


def clean_avatar(path, thr=170):
    """Remove o halo amarelado do PNG transparente gerado pela IA."""
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v >= thr else 0)
    a = a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(a)
    bb = a.getbbox()
    return im.crop(bb) if bb else im


def card_shape(w, h):
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    c = int(w * 0.16)
    d.polygon([(c, 0), (w - c, 0), (w, c), (w, h - int(h * 0.13)), (w // 2, h),
               (0, h - int(h * 0.13)), (0, c)], fill=255)
    return m


def gradient(w, h, top, bot):
    g = Image.new("RGB", (w, h))
    px = g.load()
    for y in range(h):
        t = y / (h - 1)
        col = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = col
    return g


TIERS = {  # cor da carta pelo overall (estilo FIFA)
    "bronze": ((214, 160, 110), (120, 72, 38), (40, 24, 12)),
    "prata": ((232, 236, 240), (140, 148, 158), (25, 28, 32)),
    "ouro": ((255, 222, 120), (196, 140, 30), (40, 28, 6)),
    "base": ((255, 190, 60), (30, 30, 30), (255, 255, 255)),  # promessa da base: âmbar e preto
}


def tier(ovr, promessa=False):
    if promessa:
        return "base"
    return "ouro" if ovr >= 75 else "prata" if ovr >= 65 else "bronze"


def make_card(avatar, name, ovr, pos, stats, w=520, promessa=False, crest="cambridge_united.png",
              flag=None):
    h = int(w * 1.42)
    top, bot, ink = TIERS[tier(ovr, promessa)]
    base = gradient(w, h, top, bot).convert("RGBA")
    # brilho diagonal
    shine = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shine).polygon([(0, int(h * .1)), (w, 0), (w, int(h * .22)), (0, int(h * .42))], fill=38)
    base = Image.composite(Image.new("RGBA", (w, h), (255, 255, 255, 255)), base, shine)
    d = ImageDraw.Draw(base)
    # avatar
    av = avatar if isinstance(avatar, Image.Image) else clean_avatar(avatar)
    aw = int(w * 0.78)
    av = av.resize((aw, int(av.height * aw / av.width)), Image.LANCZOS)
    ah = int(h * 0.50)
    if av.height > ah:
        av = av.crop((0, 0, av.width, ah))
    base.alpha_composite(av, (w - aw - int(w * .02), int(h * 0.60) - av.height))
    # overall e posição
    d.text((int(w * .09), int(h * .07)), str(ovr), font=font(int(w * .19)), fill=ink)
    d.text((int(w * .11), int(h * .07) + int(w * .21)), pos, font=font(int(w * .085)), fill=ink)
    cr = Image.open(os.path.join(A, crest)).convert("RGBA")
    cs = int(w * .14)
    cr.thumbnail((cs, cs), Image.LANCZOS)
    base.alpha_composite(cr, (int(w * .11), int(h * .07) + int(w * .33)))
    if flag:
        fl = Image.open(flag).convert("RGBA")
        fl.thumbnail((cs, int(cs * .7)), Image.LANCZOS)
        base.alpha_composite(fl, (int(w * .11), int(h * .07) + int(w * .50)))
    # faixa do nome
    d.line([(int(w * .12), int(h * .615)), (int(w * .88), int(h * .615))], fill=ink, width=2)
    fn = font(int(w * .1), cond=True)
    while d.textlength(name.upper(), font=fn) > w * .8:
        fn = font(fn.size - 2, cond=True)
    d.text((w // 2, int(h * .665)), name.upper(), font=fn, fill=ink, anchor="mm")
    d.line([(int(w * .12), int(h * .715)), (int(w * .88), int(h * .715))], fill=ink, width=2)
    # atributos
    keys = ["RIT", "FIN", "PAS", "DRI", "DEF", "FÍS"] if pos != "GOL" else ["ELA", "MAN", "CHU", "REF", "VEL", "POS"]
    fs = font(int(w * .07))
    fl_ = font(int(w * .062), cond=True)
    for i, k in enumerate(keys):
        col, row = i // 3, i % 3
        x = int(w * (.17 if col == 0 else .56))
        y = int(h * (.735 + row * .058))
        d.text((x, y), str(stats[i]), font=fs, fill=ink)
        d.text((x + int(w * .13), y + 3), k, font=fl_, fill=ink)
    d.line([(w // 2, int(h * .735)), (w // 2, int(h * .9))], fill=ink, width=2)
    # recorte com borda
    m = card_shape(w, h)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(base, (0, 0), m)
    edge = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
    out.paste(Image.new("RGBA", (w, h), ink + (255,)), (0, 0), ImageChops.multiply(edge, m))
    return out


if __name__ == "__main__":
    import sys
    c = make_card(os.path.join(A, "gildo_ai.png"), "Gildo", 61, "PE", [88, 58, 60, 72, 30, 52], promessa=True)
    c.save(sys.argv[1] if len(sys.argv) > 1 else "/tmp/card.png")
