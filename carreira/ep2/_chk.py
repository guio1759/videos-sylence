import sys; sys.argv=["x","shots"]
import make2 as M
miss=set(); orig=M.wt
def wt(shot, word, nth=0):
    k=0
    for w in shot["words"]:
        if M.norm(w["w"])==M.norm(word):
            if k==nth: return orig(shot,word,nth)
            k+=1
    miss.add((shot["scene"],word,nth)); return 0.0
M.wt=wt
import traceback
errs=[]
for s in M.SHOTS:
    for f in (0.1,0.5,0.95):
        T=s["t0"]+(s["t1"]-s["t0"])*f
        for W,H in ((1920,1080),(1080,1920)):
            try: M.frame(T,W,H)
            except Exception as e: errs.append((s["scene"],repr(e))); 
print("miss",sorted(miss)); print("errs",sorted(set(errs)))
