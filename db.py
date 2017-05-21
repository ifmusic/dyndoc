
import sqlite3
import pprint, pickle
import sys

#TODO: put this pickle code aside...


#Missing C style forward function declarations
def get_hostid_byIPv4(ipv4):
	try:
		conn = sqlite3.connect('db_dyndoc.db')
		c.execute('SELECT * FROM hosts WHERE ipv4=?', ipv4)
		return c.fetchone()
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

if len(sys.argv) == 1:
	print 'Must specify a file to unpickle...'
	exit()
else:
	file_to_unpickle =  sys.argv[1]

#unpack binary file with hosts services data
pkl_file = open(file_to_unpickle, 'rb') # Described as insecure; people need to take some chances
data1 = pickle.load(pkl_file)
pprint.pprint(data1)
pkl_file.close()

#Load that data into the DB
conn = sqlite3.connect('db_dyndoc.db')

#TODO: Flag this!
conn.execute('DELETE FROM hosts')
conn.execute('DELETE FROM hosts_services')
conn.commit()

#DB> binding, tcpportbinding , processname, pid
#PY> ProcessName, Pid, binding, tcpport

#We have to change the natural order of columns and values
# id_service_id , id_host , ip_binding,tcpport_binding,processname,pid 

conn.executemany('INSERT INTO hosts_services  VALUES (?,?,?,?,?)', data1)


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()