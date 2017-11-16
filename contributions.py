import mysql.connector

hostname = 'localhost'
username = '' # no privlidges set so this works
password = ''
database = 'msr14'

conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)

# Simple routine to run a query on a database and print the results:
def queryDB(conn, query) :
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

result = queryDB(conn, "select language,count(*) from projects where forked_from is null group by language;")

for l, c in result:
  print l, c

conn.close()
