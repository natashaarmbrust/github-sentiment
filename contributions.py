import mysql.connector
import csv 
import matplotlib.pyplot as plt
import matplotlib

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

project_ids = queryDB(conn, "select id from projects where forked_from is null;")

projects_to_commits =  {} 
for ID in [x[0] for x in project_ids]:
  commits = "select project_id, created_at from commits where project_id = {} ORDER BY created_at;".format(ID)
  rows = queryDB(conn, commits)
  rows = [r[1] for r in rows] #.strftime('%m/%d/%Y')
  projects_to_commits[ID] = rows 

conn.close()

fig = plt.figure()
for ID,datetimes in projects_to_commits.items():
  dates = matplotlib.dates.date2num(datetimes)
  plt.plot_date(datetimes,range(1, len(dates) + 1), 'b-')

fig.autofmt_xdate()
plt.show()


#takes in dictionary of project ids to list of creation at dates 
def create_csv(dictionary):
  for k,v in projects_to_commits.items():
    with open(str(k) + '.csv', 'w') as csvfile:
      fieldnames = ['Commit Creation', 'Total Number of Commits']
      writer = csv.writer(csvfile,delimiter=" ")
      writer.writerow(fieldnames)
      for i,c in enumerate(v):
        writer.writerow([c,i])


# Total number of commits per project 
#commit_number = "select projects.id, count(*) from projects join commits on projects.id = commits.project_id where projects.forked_from is null group by projects.id;"