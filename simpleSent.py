#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import numpy, itertools
from collections import defaultdict
from os import path
import unicodecsv as csv
import operator
import io
import codecs


path='/Users/fatimaal-ghamdi/Documents/'

#Pos, neg and comments files
comments = []
pos_list = []
neg_list = []
comments_cleaned = {}
comments_labeled = {}
comments_sentiment = {}
with codecs.open(path+'pr_comments.csv', 'r', encoding='utf-8' ) as c: 
	reader = csv.reader(c, delimiter="\t")#, encoding='utf-8')
	for line in c:
		if line is not '':
			comments.append(line.strip('\n'))
c.close()


with io.open(path+'positive.txt', 'rU', encoding='utf-8') as pos: 
	for line in pos:
		pos_list.append(line.strip("\n").lower())
pos.close()

with io.open(path+'negative.txt', 'rU', encoding='utf-8') as neg: 
	for line in neg:
		neg_list.append(line.strip("\n").lower())
neg.close()

temp = ''
for s in comments:
	temp = ''
	tempList = s.split(',')
	#print(tempList)
	if len(tempList) >= 3:
		for t in range(2, len(tempList)):
			temp = temp+tempList[t]
		if temp is not '':
			comments_cleaned[tempList[0]] = [tempList[1], temp]


#print(comments_cleaned)
#print(len(comments_cleaned))
"""
for w in comments:
	print(w)

print(len(comments))

for w in pos_list:
	print(w)

for w in neg_list:
	print(w)
"""

#Sentiment Analysis
neu_count= 0
pos_count = 0
neg_count = 0
word_count = 0
for c in comments_cleaned.keys():
	pos_count, neu_count, neg_count, word_count = 0, 0, 0, 0
	#print(comments_cleaned[c][1])
	#print(c[1])
	#print(comments_cleaned[c[1]])
	c_tokens = nltk.word_tokenize(comments_cleaned[c][1].lower())
	for w in c_tokens:
		if w in pos_list:
			pos_count += 1
		elif w in neg_list: #if w in neg_list:
			neg_count += 1
		else:
			#print('nu')
			neu_count += 1

		word_count += 1
	if(word_count != 0):
		#if all ([pos_count > neg_count, pos_count >= neu_count]):
		if pos_count > neg_count: # and pos_count >= neu_count:
			comments_sentiment[c] = [comments_cleaned[c][0], comments_cleaned[c][1], 'pos', float(pos_count)/word_count] #len(c_tokens)
		#elif all ([neg_count > pos_count, neg_count >= neu_count]):
		elif neg_count > pos_count: #and neg_count >= neu_count:
			comments_sentiment[c] = [comments_cleaned[c][0], comments_cleaned[c][1], 'neg', float(neg_count)/word_count] #len(c_tokens)
		else:
			#print(word_count)
			#print(neu_count)
			#comments_sentiment[c] = ['neu', float(neu_count)/word_count] #len(c_tokens)
			comments_sentiment[c] = [comments_cleaned[c][0], comments_cleaned[c][1], 'neu', float(neu_count)/word_count]
#print(comments_sentiment)

#Write to CSV file

with open(path+'pr_comments_labeled.csv', 'w') as csvfile:
    fieldnames = ['ID', 'Created_at', 'Comment', 'Label', 'Score']
    writer = csv.DictWriter(csvfile, dialect='excel', encoding='utf-8', fieldnames=fieldnames)
    writer.writeheader()
    #reslst = filter(lambda x: x[0] == '5', comments_sentiment.keys())
    for t in comments_sentiment.keys():
    	if t.startswith('5'):
	        writer.writerow({'ID': t,'Created_at': comments_sentiment[t][0], 'Comment': comments_sentiment[t][1], 
	        	'Label': comments_sentiment[t][2], 'Score': comments_sentiment[t][3]})    
csvfile.close()

