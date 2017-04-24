from subprocess import Popen, PIPE
import re,  pprint, pickle
import socket
import sys

DEBUG = 1

def Print( s ):
	if DEBUG : print s

if len(sys.argv) == 1:
  print 'Must specify a file to pickle...'
  exit()
else:
  file_to_pickle =  sys.argv[1]

listening_apps = []

fqdn = socket.gethostbyaddr(socket.gethostname())[0]
#TODO : handle errors calling lsof
msg = "Obteniendo servicios en "+ (fqdn) + "..."
Print(msg)

p1 = Popen(['lsof', '-P','-n', '-i'], stdout=PIPE)
while True:
  line = p1.stdout.readline()
  if line != '':
      #the real code does filtering here
      matchObj = re.findall( r"(?P<name>\w+)\s+(?P<pid>\d+)(?:.+)TCP\s+(?P<host>.+):(?P<port>\d+)(?: )\(LISTEN\)", line)
      #Obtiene:
      #ProcessName, Pid, binding, tcpport
      if matchObj != []:
       tmp=[]
       host_id = fqdn
       tmp.append(host_id)
       matchObj=list(matchObj[0])
       tmp.extend(matchObj)
       listening_apps.append(tmp)
       Print(tmp)
  else:
    break 
#TO DO: Handle write errors
output = open('/tmp/services['+file_to_pickle+'].pkl', 'wb')

# Pickle the list using the highest protocol available.
pickle.dump(listening_apps, output, -1)
output.close()



