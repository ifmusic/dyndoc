import sqlite3
conn = sqlite3.connect('db_dyndoc.db')

conn.execute('DELETE FROM hosts')

conn.commit()

#En el ejemplo, paso la PK como None o Null para que sqlite autoasigne un uint64++
hosts = [(None,'10.0.0.1', '', 'host01.local'),
          (None, '10.0.0.2', '', 'host02.local')
            ]
conn.executemany('INSERT INTO hosts VALUES (?,?,?,?)', hosts)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()