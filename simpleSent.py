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

path='/Users/fatimaal-ghamdi/Documents/'

#Pos, neg and comments files
comments = []
pos_list = []
neg_list = []
comments_sentiment = {}
with io.open(path+'comments.txt', 'rU', encoding='utf-8') as c: 
	for line in c:
		comments.append(line.strip("\n"))
c.close()

with io.open(path+'positive.txt', 'rU', encoding='utf-8') as pos: 
	for line in pos:
		pos_list.append(line.strip("\n").lower())
pos.close()

with io.open(path+'negative.txt', 'rU', encoding='utf-8') as neg: 
	for line in neg:
		neg_list.append(line.strip("\n").lower())
neg.close()

"""
for w in comments:
	print(w)

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
for c in comments:
	pos_count, neu_count, neg_count, word_count = 0, 0, 0, 0
	c_tokens = nltk.word_tokenize(c.lower())
	for w in c_tokens:
		if w in pos_list:
			pos_count += 1
		elif w in neg_list: #if w in neg_list:
			neg_count += 1
		#else:
			#print('nu')
			#neu_count += 1

		word_count += 1
	if(word_count != 0):
		#if all ([pos_count > neg_count, pos_count >= neu_count]):
		if pos_count > neg_count: # and pos_count >= neu_count:
			comments_sentiment[c] = ['pos', float(pos_count)/word_count] #len(c_tokens)
		#elif all ([neg_count > pos_count, neg_count >= neu_count]):
		elif neg_count > pos_count: #and neg_count >= neu_count:
			comments_sentiment[c] = ['neg', float(neg_count)/word_count] #len(c_tokens)
		#else:
			#print(word_count)
			#print(neu_count)
			#comments_sentiment[c] = ['neu', float(neu_count)/word_count] #len(c_tokens)
#print(comments_sentiment)

#Write to CSV file

with open(path+'comments_labeled.csv', 'w') as csvfile:
    fieldnames = ['Comment', 'Label', 'Score']
    writer = csv.DictWriter(csvfile, dialect='excel', encoding='utf-8', fieldnames=fieldnames)
    writer.writeheader()
    for t in comments_sentiment.keys():
        writer.writerow({'Comment': t,'Label': comments_sentiment[t][0], 'Score': comments_sentiment[t][1]})    
csvfile.close()

