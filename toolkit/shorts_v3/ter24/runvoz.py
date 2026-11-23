import sys; sys.path.insert(0,'/home/claude/ter24'); import voz, scripts, os
os.makedirs('/home/claude/ter24/'+sys.argv[1], exist_ok=True)
voz.build('/home/claude/ter24/'+sys.argv[1], getattr(scripts, sys.argv[2]))
