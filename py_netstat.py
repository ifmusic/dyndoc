from subprocess import Popen, PIPE
import re,  pprint, pickle
import socket

DEBUG = 1

def Print( s ):
	if DEBUG : print s

listening_apps = []

fqdn = socket.gethostbyaddr(socket.gethostname())[0]
#TODO : handle errors calling lsof
msg = "Obteniendo servicios en "+ (fqdn) + "..."
Print(msg)

p1 = Popen(['lsof', '-P'], stdout=PIPE)
while True:
  line = p1.stdout.readline()
  if line != '':
    #the real code does filtering here
    	matchObj = re.findall( r"(?P<name>\w+)\s+(?P<pid>\d+)(?:.+)TCP\s+(?P<host>.+):(?P<port>\d+)(?: )\(LISTEN\)", line)
    	if matchObj != [] : 
    	 Print(matchObj)
    	 listening_apps.append(matchObj)
  else:
    break 
#TO DO: Handle write errors
output = open('/tmp/data.pkl', 'wb')

# Pickle the list using the highest protocol available.
pickle.dump(listening_apps, output, -1)
output.close()



