import sys; sys.path.insert(0,'/home/claude/sab21b'); import voz, scripts, os
os.makedirs('/home/claude/sab21b/'+sys.argv[1], exist_ok=True)
voz.build('/home/claude/sab21b/'+sys.argv[1], getattr(scripts, sys.argv[2]))
