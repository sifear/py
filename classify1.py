#!/usr/bin/env
# encoding: utf-8

import string, re

class Classifier(object):

	def __init__(self):
		self.class_count = {}
		self.feature_count = {}
		
	def learn(self, data):
		for categories in data.keys():   # For each category
			for doc in data[categories]:  # get each line (line is document)
				self.count_feature(categories, doc)
				
		print self.feature_count.items()
				
	def count_feature(self, category, doc):
		#print category
		words = doc.split()
		words = [w.translate(None, string.punctuation) for w in words if len(w) > 3 and len(w) < 16]
		for word in words:
			self.feature_count.setdefault(category,{word : 0})
			self.feature_count[category].setdefault(word, 0)
			self.feature_count[category][word] += 1
			
	
if __name__ == '__main__':
	categories = ['hungary','IBM']
	data = {}
	
	for category in categories:
		file = open(category, "r")
		data[category] = file.readlines()
		
	c = Classifier()
	c.learn(data)
	
	print string.punctuation
	print re.escape(string.punctuation)
	print '[%s]' % re.escape(string.punctuation)
