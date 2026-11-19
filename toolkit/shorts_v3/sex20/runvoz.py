import sys; sys.path.insert(0,'/home/claude/sex20'); import voz, scripts
voz.build('/home/claude/sex20/'+sys.argv[1], getattr(scripts, sys.argv[2]))
