from subprocess import Popen, PIPE
import re,  pprint, pickle
import socket
import sys
import hashlib

DEBUG = 0

def Print( s ):
  if DEBUG : print s

def getIPv4Address():
  ipv4address=[]
  p1 = Popen(['ifconfig'], stdout=PIPE)
  while True:
    line = p1.stdout.readline()
    if line != '':
     matchObj = re.search( r"(addr\:|inet\s)(?P<ip>((\d+)\.){3}((\d+)))", line)
     if matchObj != None:
      #print matchObj
      Print(matchObj.group('ip'))
      tmpIp=matchObj.group('ip')
      ipv4address.append(tmpIp)
    else:
     return ipv4address

def getServices(hostid):
  listening_apps=[]
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
         tmp.append(hostid)
         matchObj=list(matchObj[0])
         tmp.extend(matchObj)
         listening_apps.append(tmp)
         Print(tmp)
    else:
      return  listening_apps

def main():
  if len(sys.argv) == 1:
    print 'Must specify a file to pickle...'
    exit()
  else:
    file_to_pickle =  sys.argv[1]

  #fqdn = socket.gethostbyaddr(socket.gethostname())[0]
  #TODO : handle errors calling lsof
  #msg = "Obteniendo servicios en "+ (fqdn) + "..."
  #Print(msg)

  #Get IPv4 address
  ipv4=getIPv4Address()
  Print(ipv4) 
  
  #Get an ID for the host out of the hash of all its IPv4 addresses
  host_id = hashlib.md5(','.join(ipv4)).hexdigest()

  #Get listening services
  listening_apps = getServices(host_id)
  Print(listening_apps)

  #TO DO: Handle write errors
  output = open('/tmp/services['+file_to_pickle+'].pkl', 'wb')

  # Pickle the list using the highest protocol available.
  pickle.dump(listening_apps, output, -1)
  output.close()
  return 0

if __name__ == "__main__":
    main()



