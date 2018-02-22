#!/usr/bin/env
# redoing mason's script

import re, string

from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class NaiveBayesClassifier(object):

   def __init__(self):
      self.feature_count = {}
      self.category_count = {}


   def train_from_data(self, data):
      for cat, sentence in data.items():     # for each category, sentence pair
         self.train(sentence, cat)
         
   def train(self, sentence, category):
      features = self.get_features(sentence) # stems from a sentence
      
      for f in features:                     # for each stem: if not stored then store, 
         self.increment_feature(f, category) # and then increase associated counter,
                                             # i.e. we count occurances of stem in training data for given category
      self.increment_category(category)
      
   def get_features(self, item):
      sentence = item.lower()
      sentence = re.sub('[%s]' % re.escape(string.punctuation), '', sentence)
      tokens = [w for w in word_tokenize(sentence) if len(w) > 3 and len(w) < (16)]
   
      p = PorterStemmer()
      all_words = [p.stem(w) for w in tokens]
      all_words_freq = FreqDist(all_words)
      
      return all_words
      
   def increment_feature(self, feature, category):
      self.feature_count.setdefault(feature, {})
      self.feature_count[feature].setdefault(category, 0)
      self.feature_count[feature][category] += 1
   
   def increment_category(self, category):
      self.category_count.setdefault(category, 0)
      self.category_count[category] += 1

   def get_category_count(self, category):
      if category in self.category_count:
         return float(self.category_count[category])
      else:
         return 0.0
         
   def get_feature_count(self, feature, category):
      if feature in self.feature_count and category in self.feature_count[feature]:
         return float(self.feature_count[feature][category])
      else:
         return 0.0
      
   def probability(self, item, category):
      category_prob = self.get_category_count(category) / sum(self.category_count.values())
      
      return self.document_probability(item, category) * category_prob
      
   def document_probability(self, item, category):
      features = self.get_features(item)
      
      p = 1
      
      for f in features:
         p *= self.wighted_prob(f, category)
         
      return p
      
   def wighted_prob(self, feature, category, weight=1.0, ap=0.5):
      basic_prob = self.feature_prob(feature, category)
      
      totals = sum([self.get_feature_count(feature, category) for category in self.category_count.keys()])
      w_prob = ((weight*ap) + (totals * basic_prob)) / (weight + totals)
      
      return w_prob
      
   def feature_prob(self, feature, category):
      if self.get_category_count(category) == 0:
         return 0
      
      return (self.get_feature_count(feature, category) / self.get_category_count(category))
      
if __name__ == '__main__':
   sentences = {}
   sentences['math'] = 'This is a sentence with a few words in it. Mathemathic, numbers, multiply numbers together to get results. Add some numbers together. Books can be used to store the equations and diagrams.'
   sentences['literature'] = 'This is a sentence with literaturally stuff. Books with pages and poems and stuff with arts and expression. Also authors.'
   
   c = NaiveBayesClassifier()
   
   c.train_from_data(sentences)
   
   print c.category_count.items()
   #print c.feature_count.items()
   print c.probability("very literatury sentence with book with poems and text in it","literature")
   print c.probability("very literatury sentence with book with poems and text in it","math")
	
   print c.probability("very mathy stuff with numbers and equations and diagrams","literature")
   print c.probability("very mathy studd with numbers and equations and diagrams","math")
   
   
