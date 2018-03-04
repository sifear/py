#!/usr/bin/env
# encoding: utf-8

import string, re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

class Classifier(object):

	def __init__(self):
		self.class_count = {}
		self.feature_count = {}
		
	def learn(self, data):
		for categories in data.keys():   # For each category
			for doc in data[categories]:  # get each line (line is document)
				self.count_feature(categories, doc)
				self.class_count.setdefault(categories, 0)
				self.class_count[categories] += 1
				
	def count_feature(self, category, doc):
		#print category
		words = doc.split()
		words = [w.translate(None, string.punctuation).lower() for w in words if len(w) > 3 and len(w) < 16]
		p = PorterStemmer()
		words = [p.stem(w.decode('utf-8')) for w in words]
		for word in words:
			self.feature_count.setdefault(category,{word : 0})
			self.feature_count[category].setdefault(word, 0)
			self.feature_count[category][word] += 1

	def probability(self, document, category):
		# p(category, document) = p(document, category) * p(category)

		prob = self.prob_of_doc(document, category) * self.prob_of_category(category) 
		print prob

	def prob_of_doc(self, document, category):
		p = 1.0
		considered = 0
		for feature in word_tokenize(document):
			ps = PorterStemmer()
			f = ps.stem(feature.translate(None, string.punctuation).lower().decode('utf-8'))
			if len(f) < 3 and len(f) > 16:
				continue	
			else:
				considered += 1
			p *= self.features_in_category(f, category)

		p /= considered
		return p

	def features_in_category(self, feature, category):
		return float(self.feature_count.get(category, {'na' : 'na'}).get(feature, 1))

	def prob_of_category(self, category):
		#print 'Class prob: ' + str(float(self.class_count[category]) / float(sum(self.class_count.values())))
		return float(self.class_count[category]) / float(sum(self.class_count.values()))
	
if __name__ == '__main__':
	categories = ['hungary','IBM']
	data = {}
	
	for category in categories:
		file = open(category, "r")
		data[category] = file.readlines()
		
	c = Classifier()
	c.learn(data)

	c.probability("Hungary is a central european country with a president, with some international company", "hungary");
	c.probability("Hungary is a central european country with a president, with some international company ", "IBM");

	c.probability("ibm is an technology company that is on the stock exchange and computers and business", "hungary");
	c.probability("ibm is an technology company that is on the stock exchange and computers and business", "IBM");
	
	#print string.punctuation
	#print re.escape(string.punctuation)
	#print '[%s]' % re.escape(string.punctuation)
