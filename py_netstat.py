from subprocess import Popen, PIPE
import re
#p0 = Popen(['lsof', '-a', '-i4'])
p1 = Popen(['lsof',  '-i4', '-P'], stdout=PIPE)
while True:
  line = p1.stdout.readline()
  if line != '':
    #the real code does filtering here
    if line.find("LISTEN") > 0:
    	print  line.rstrip()
    	matchObj = re.findall( r"(?P<name>\w+)\s+(?P<pid>\d+)(?:.+)TCP\s+(?P<host>.+):(?P<port>\d+)(?: )\(LISTEN\)", line)
    	print matchObj
  else:
    break
