import sys; sys.argv=["x","preview"]
import make_ep1 as M
from PIL import Image, ImageDraw, ImageFilter
W,H=1280,720
im=Image.new("RGBA",(W,H),(14,14,16,255))
g=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(g); d.ellipse((300,-300,1300,600),fill=(246,178,40,120)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(140)))
st=Image.open("img/abbey.jpg").convert("RGBA").resize((W,W)).crop((0,200,W,200+H)); st.putalpha(70); im.alpha_composite(st)
r=M.avatar("rick",640); im.alpha_composite(r,(-40,H-r.height+40))
m=M.avatar("murrey",560); im.alpha_composite(m,(W-m.width+60,H-m.height+30))
cr=Image.open("/home/claude/carreira/assets/cambridge_united.png").convert("RGBA").resize((210,210)); im.alpha_composite(cr,(W//2-105,40))
f=M.font("blk",92); f2=M.font("blk",70)
def T(xy,s,f,fill):
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(lay).text((xy[0]+5,xy[1]+7),s,font=f,fill=(0,0,0,220),anchor="mm"); im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(im).text(xy,s,font=f,fill=fill,anchor="mm",stroke_width=4,stroke_fill=(0,0,0))
T((W//2,330),"4ª DIVISÃO",f,(255,255,255)); T((W//2,420),"→ CHAMPIONS",f,(246,178,40))
c=M.chip("MODO CARREIRA • EP.1",M.font("blk",40)); im.alpha_composite(c,(W//2-c.width//2,500))
im.convert("RGB").save("thumb_ep1.jpg",quality=92)
