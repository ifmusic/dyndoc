import sqlite3
import pprint, pickle

#TODO: put this pickle code aside...

pkl_file = open('data-192.168.0.17', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)


pkl_file.close()



conn = sqlite3.connect('db_dyndoc.db')

conn.execute('DELETE FROM hosts')

conn.commit()

# PK as Null gets autoassinged as a uint64++
hosts = [(None,'10.0.0.1', '', 'host01.local'),
          (None, '10.0.0.2', '', 'host02.local'),
           (None, '10.0.0.3', '', 'host03.local')
            ]
conn.executemany('INSERT INTO hosts VALUES (?,?,?,?)', hosts)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()