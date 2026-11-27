import sys; sys.argv=['doc.py','c1','x']
exec(open('/home/claude/doc/doc.py').read().split('if __name__')[0])
from rembg import remove, new_session
import os
def cut(key, out):
    if not os.path.exists(out):
        im = Image.open(P[key]).convert("RGB"); r = remove(im, session=new_session("u2net")); r.save(out)
    return Image.open(out)
def make(word1, word2, col2, out):
    bgp = cover(photo("cent"), 1.15, 0.5, 0.6).convert("RGBA")
    bgp = ImageEnhance.Brightness(bgp).enhance(0.55)
    img = bgp.copy(); img.alpha_composite(vig(160))
    ab = cut("abel2", "/home/claude/doc/thumb/abel_cut.png"); ab = ab.crop(ab.getchannel("A").getbbox())
    ab = ab.resize((int(ab.width * 1000 / ab.height), 1000), Image.LANCZOS)
    # contorno branco
    a = ab.getchannel("A").filter(ImageFilter.MaxFilter(15)); st = Image.new("RGBA", ab.size, (255, 255, 255, 255)); st.putalpha(a)
    img.alpha_composite(st, (W - ab.width - 20, H - ab.height + 40)); img.alpha_composite(ab, (W - ab.width - 20, H - ab.height + 40))
    paste(img, logo("PAL", 190), 170, 150, 1); paste(img, tx("x", 90, WHITE), 300, 150, 1); paste(img, logo("EST", 190), 420, 150, 1)
    paste(img, text_el(word1, F("anton", 290), AMB, 16), 560, 470, 1, 1.0, -3)
    paste(img, text_el(word2, F("anton", 170), col2, 12), 560, 720, 1, 1.0, -3)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92)
make("58 ANOS", "A REVANCHE", WHITE, "/home/claude/doc/thumb/neutra.jpg")
