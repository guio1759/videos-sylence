from com import *
import inspect, gfx as _G
_src = inspect.getsource(_G.newspaper).replace('"CAMBRIDGE DAILY"', 'brand')
_src = _src.replace('def newspaper(w, year, headline, sub="", sepia=False):', 'def newspaper(w, year, headline, sub="", sepia=False, brand="JORNAL DO FUTEBOL"):')
exec(_src, _G.__dict__); newspaper = _G.newspaper
RAIN = [(228, 3, 3), (255, 140, 0), (255, 237, 0), (0, 128, 38), (0, 77, 255), (117, 7, 135)]
def rainbow(img, y, h, alpha=255):
    d = ImageDraw.Draw(img)
    for k, c in enumerate(RAIN): d.rectangle((0, y + k * h / 6, W, y + (k + 1) * h / 6), fill=c + (alpha,))
def goldball(sz, t=0):
    sz = int(sz); im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(40):
        r = sz / 2 * (1 - k / 40); c = (int(200 + 55 * k / 40), int(150 + 80 * k / 40), int(30 + 90 * k / 40))
        d.ellipse((sz / 2 - r - k * sz / 400, sz / 2 - r - k * sz / 400, sz / 2 + r - k * sz / 400, sz / 2 + r - k * sz / 400), fill=c)
    d.ellipse((2, 2, sz - 2, sz - 2), outline=(120, 80, 10), width=max(3, sz // 60))
    for a in range(0, 360, 60):
        x = sz / 2 + sz * 0.28 * math.cos(math.radians(a + t * 20)); y = sz / 2 + sz * 0.28 * math.sin(math.radians(a + t * 20))
        d.regular_polygon((x, y, sz * 0.07), 5, fill=(170, 110, 20))
    return im
def quote(text, who, w=960):
    f = font("blk", 54); lines = wrap(text, f, w - 100)
    h = 120 + len(lines) * 66 + 70; p = panel(w, h, (250, 250, 252, 255), 26, (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.text((40, 10), "“", font=font("blk", 130), fill=(200, 200, 205))
    for i, l in enumerate(lines): d.text((60, 100 + i * 66), l, font=f, fill=INK)
    d.text((60, h - 60), who, font=font("bd", 38), fill=(110, 110, 120))
    return p
def calendar(w, u, t):
    h = 260; p = panel(w, h, (14, 14, 20, 240), 24); d = ImageDraw.Draw(p)
    ms = ["AGO", "SET", "OUT", "NOV", "DEZ", "JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL"]
    cw = (w - 60) / 12
    for i, m in enumerate(ms):
        x = 30 + i * cw; on = i < 12 * u
        d.rounded_rectangle((x + 4, 120, x + cw - 4, 200), 10, fill=GOLD if (i == 4 and on) else ((60, 160, 90) if on else (60, 60, 70)))
        d.text((x + cw / 2, 160), m, font=font("blk", 28), fill=INK if on else WHITE, anchor="mm")
    d.text((30, 40), "2022", font=font("blk", 44), fill=WHITE); d.text((w - 30, 40), "2023", font=font("blk", 44), fill=WHITE, anchor="ra")
    return p
GOLD = (255, 205, 60)
ARG = (110, 180, 230)
