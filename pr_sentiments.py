import mysql.connector
import csv 
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors as mcolors
import datetime 
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

project_ids = queryDB(conn, "select projects.id as id, pull_requests.pullreq_id as pullred_id from (select id from projects where forked_from is null) as projects join pull_requests on projects.id = pull_requests.base_repo_id;")[:-1]

projects_to_pr_comments =  {} 

sid = SentimentIntensityAnalyzer()
for ID, PR_ID in project_ids:
  comments = "select created_at, body from pull_request_comments where pull_request_id = {} ORDER BY created_at;".format(PR_ID)
  rows = queryDB(conn, comments)
  dates = []
  scores = []
  for date, comment in rows:
    ss = sid.polarity_scores(comment)
    dates.append(date)
    scores.append(ss['compound'])

  if len(dates) > 0:
    if ID in projects_to_pr_comments:
      current = projects_to_pr_comments[ID]
      current[0].extend(dates)
      current[1].extend(scores)
    else:
      projects_to_pr_comments[ID] = [dates,scores]
  


conn.close()

plt.figure(figsize=(9, 9)) 
ax = plt.subplot(111)
plt.title("Sentiment Analysis Over Time for Pull Requests on the Top 90 Repositories on Github", fontsize=16) 
plt.ylabel("Sentiment", fontsize=12)
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.    
# Ticks on the right and top of the plot are generally unnecessary chartjunk.    
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    

i = 0 
for ID,date_scores in projects_to_pr_comments.items():
  indices = [i[0] for i in sorted(enumerate(date_scores[0]), key=lambda x:x[1])]
  sorted_dates = []
  sorted_scores = []
  for i in indices:
    sorted_dates.append(date_scores[0][i])
    sorted_scores.append(date_scores[1][i])
  plt.plot_date(sorted_dates,sorted_scores, '-b')
  i += 1

plt.show()
