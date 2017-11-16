import csv 
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors as mcolors

path = '/Users/fatimaal-ghamdi/Documents/'
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

# Sort colors by hue, saturation, value and name.
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
colors = [name for hsv, name in by_hsv]


#Reading csv file
comments_labeled = {}
with open(path+'comments_labeled.csv', 'r') as csvfile:
    fieldnames = ['Comment', 'Label', 'Score']
    reader = csv.reader(csvfile)
    for row in reader:
      comments_labeled[row[0]]=[row[1], row[2]]
  
csvfile.close()

#print(comments_labeled)



plt.figure(figsize=(12, 6)) 
ax = plt.subplot(111)

plt.title("Total number of Comments with Negative Sentiment", fontsize=16) 
plt.ylabel("Number of Comments", fontsize=12)
plt.xlabel("Negative Sentiment Scores", fontsize=12)

ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    
i = 0
count = 0
neg_comments={}
pos_comments={}

for l, s in comments_labeled.items():
    if s[0] == 'neg':
        neg_comments[l]=s[1]
    if s[0] == 'pos':
        pos_comments[l]=s[1]

#print(neg_comments)
#for negative comments
for k, s in neg_comments.items():
    count += 1
    plt.plot(s, sum(x == s for x in neg_comments.values()), 'r--')
    plt.axis([0, 1, 0, 39980])
plt.xlim(0, 1)
plt.show()

"""
#for positive comments
for k, s in neg_comments.items():
    count += 1
    plt.plot(s, sum(x == s for x in neg_comments.values()), 'r--')
    plt.axis([0, 1, 0, 39980])

plt.show()
"""
