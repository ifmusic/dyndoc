from subprocess import Popen, PIPE
p1 = Popen(['lsof', '-a', '-i4'], stdout=PIPE)
p2 = Popen(["grep", "LISTEN"], stdin=p1.stdout, stdout=PIPE
print 'JuaJua!'
output = p2.communicate()[0]