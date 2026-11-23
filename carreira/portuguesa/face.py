from PIL import Image
import functools
@functools.lru_cache(32)
def face(k, hk=1.15):
    im = Image.open(f'/home/claude/por/img/{k}_cut.png').convert('RGBA'); w, h = im.size
    im = im.crop((0, 0, w, min(h, int(w * hk))))
    tw = int(im.height * 1.12); out = Image.new('RGBA', (max(tw, im.width), im.height), (0, 0, 0, 0))
    out.alpha_composite(im, ((out.width - im.width) // 2, 0)); return out
