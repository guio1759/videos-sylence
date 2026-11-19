import sys; sys.path.insert(0,'/home/claude/sex20'); sys.path.insert(0,'/home/claude/shop'); import voz, scripts
voz.build('/home/claude/shop/'+sys.argv[1], getattr(scripts, sys.argv[2]))
