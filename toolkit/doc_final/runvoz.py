import sys, os; sys.path.insert(0, '/home/claude/doc'); import voz
from roteiro import CAPS
for cid, mus, off, sents in CAPS:
    if len(sys.argv) > 1 and cid not in sys.argv[1:]: continue
    d = f'/home/claude/doc/{cid}'; os.makedirs(d, exist_ok=True)
    voz.build(d, [(s, r, 0.28) for _, s, r in sents])
