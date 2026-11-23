import sys; sys.argv=["x","shots"]
from gfx import *
from PIL import Image, ImageDraw, ImageFilter
W,H=1280,720
im=Image.new("RGBA",(W,H),(14,14,16,255))
st=Image.open("/tmp/claude-0/img/stadium.jpg").convert("RGBA").resize((W,W)).crop((0,200,W,200+H)); st.putalpha(110); im.alpha_composite(st)
g=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(g); d.ellipse((300,-300,1300,600),fill=(246,178,40,120)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(140)))
tr=Image.new("RGBA",(W,H),(0,0,0,0)); dd=ImageDraw.Draw(tr); cx=W//2; r=420; dd.arc((cx-r,140-r*0.2,cx+r,140+r*1.6),200,340,fill=(255,255,255,120),width=14); im.alpha_composite(tr)
gl=avatar("gildo",640); im.alpha_composite(gl,(-50,H-gl.height+40))
m=avatar("murrey",560); im.alpha_composite(m,(W-m.width+60,H-m.height+30))
cr=crest(190); im.alpha_composite(cr,(W//2-95,40))
f=font("blk",84)
def T(xy,s,f,fill):
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(lay).text((xy[0]+5,xy[1]+7),s,font=f,fill=(0,0,0,220),anchor="mm"); im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(im).text(xy,s,font=f,fill=fill,anchor="mm",stroke_width=4,stroke_fill=(0,0,0))
T((W//2,320),"DA PIZZA",f,(255,255,255)); T((W//2,410),"→ WEMBLEY",font("blk",96),(246,178,40))
c=chip("MODO CARREIRA • EP.2",40); im.alpha_composite(c,(W//2-c.width//2,490))
im.convert("RGB").save("/home/claude/videos-sylence/2026-11/carreira/ep2/thumb_ep2.jpg",quality=92)
