from pymongo import MongoClient
from collections import defaultdict
import unicodecsv as csv

# pprint library is used to make the output look more pretty

from pprint import pprint

path = '/Users/fatimaal-ghamdi/Documents/'
client = MongoClient('localhost', 27017)
db=client['msr14']
collection = db['pull_request_comments']

temp = defaultdict(list)
try:
	posts = db.pull_request_comments.find()
	print '\n All data from pull_request_comments table \n'
	for x in posts:
		temp[x['_id']] = [x['created_at'], x['body']]
	    #print x

except Exception, e:
    print str(e)

print(temp)
print(len(temp))


with open(path+'pr_comments.csv', 'w') as csvfile:
    fieldnames = ['ID', 'Created_at', 'Comment']
    writer = csv.DictWriter(csvfile, dialect='excel', encoding='utf-8', fieldnames=fieldnames)
    writer.writeheader()
    for t in temp.keys():
        writer.writerow({'ID': t,'Created_at': temp[t][0], 'Comment': temp[t][1]})    
csvfile.close()