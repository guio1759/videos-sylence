"""Pinta a camiseta preta de um avatar com a camisa do Cambridge (âmbar com gola preta). Uso: edite N (arquivo: altura relativa do pescoço) e rode."""
import numpy as np
from PIL import Image
from scipy import ndimage
AMB=np.array([246,178,40],float)
def recolor(src,dst,neck):
    im=Image.open(src).convert('RGBA'); a=np.array(im).astype(float); H,W=a.shape[:2]
    rgb=a[...,:3]; al=a[...,3]
    face=rgb[int(H*.38):int(H*.48),int(W*.44):int(W*.56)].reshape(-1,3); skin=np.median(face,0)
    dist=np.sqrt(((rgb-skin)**2).sum(-1))
    yy=np.arange(H)[:,None]
    m=(al>40)&(yy>H*neck)&(dist>50)&(rgb.max(-1)<150)
    m=ndimage.binary_closing(m,iterations=3)&(al>40)&(dist>35)
    m=ndimage.binary_opening(m,iterations=2)
    lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1)); keep=[i+1 for i,s in enumerate(sizes) if s>W*H*0.003]
    m=np.isin(lab,keep)
    L=rgb.max(-1); ref=np.percentile(L[m],95) if m.any() else 1
    shade=np.clip(0.6+0.55*(L/ref),0.55,1.15)[...,None]
    top=np.full(W,H)
    ys,xs=np.nonzero(m)
    for x in np.unique(xs): top[x]=ys[xs==x].min()
    band=int(H*0.022); collar=m&(yy<top[None,:]+band)&(np.abs(np.arange(W)[None,:]-W/2)<W*0.22)
    out=rgb.copy(); body=m&~collar
    out[body]=(AMB*shade)[body]; out[collar]=np.array([22,22,24])
    a[...,:3]=np.clip(out,0,255); Image.fromarray(a.astype(np.uint8)).save(dst)
N={'kofi':.8,'ollie':.75,'theo':.79,'tomas':.66,'arlo':.58,'pai_gildo':.7,'mae_rick':.63}
for k,n in N.items(): recolor(f'/home/claude/ep1/img/f_{k}.png',f'f_{k}.png',n)
c=Image.new('RGB',(250*7,250),(90,90,90))
for i,k in enumerate(N):
    im=Image.open(f'f_{k}.png'); im.thumbnail((250,250)); c.paste(im,(i*250,0),im)
c.save('chk.jpg')
