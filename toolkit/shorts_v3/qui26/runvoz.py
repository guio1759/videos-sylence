import sys; sys.path.insert(0,'/home/claude/qui26'); import voz, scripts, os
os.makedirs('/home/claude/qui26/'+sys.argv[1], exist_ok=True)
voz.build('/home/claude/qui26/'+sys.argv[1], getattr(scripts, sys.argv[2]))
