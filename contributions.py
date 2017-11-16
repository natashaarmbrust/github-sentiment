import mysql.connector
import csv 
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors as mcolors
import datetime 

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

# Sort colors by hue, saturation, value and name.
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
colors = [name for hsv, name in by_hsv]

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

project_ids = queryDB(conn, "select id from projects where forked_from is null;")[:-1]

projects_to_commits =  {} 
for ID in [x[0] for x in project_ids]:
  commits = "select project_id, created_at from commits where project_id = {} ORDER BY created_at;".format(ID)
  rows = queryDB(conn, commits)
  rows = [r[1] for r in rows] #.strftime('%m/%d/%Y')
  projects_to_commits[ID] = rows 

conn.close()

plt.figure(figsize=(9, 9)) 
ax = plt.subplot(111)
plt.title("Total Number of Project Commits Over Time for the Top 90 Repositories on Github", fontsize=16) 
plt.ylabel("Total Number of Commits", fontsize=12)
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.    
# Ticks on the right and top of the plot are generally unnecessary chartjunk.    
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    

i = 0
min_date = datetime.date(2010,1,1)
max_date = min_date
for ID,datetimes in projects_to_commits.items():
  plt.plot_date(datetimes,range(1, len(datetimes) + 1), colors[i])
  i+=1
  if datetimes[-1].date() > max_date:
    max_date = datetimes[-1].date()

min_date = datetime.date(2010,1,1)
plt.xlim(min_date,max_date)
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