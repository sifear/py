#!/usr/bin/env

import re, string

from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class NaiveBayesClassifier(object):

   def __init__(self):
      self.feature_count = {}
      self.category_count = {}

   def train_from_data(self, data):
      for cat, sentence in data.items(): 
         self.train(sentence, cat)
         
   def train(self, sentence, category):
      features = self.get_features(sentence)
      
      for f in features:
         self.increment_feature(f, category)
      
   def get_features(self, item):
      sentence = item.lower()
      sentence = re.sub('[%s]' % re.escape(string.punctuation), '', sentence)
      tokens = [w for w in word_tokenize(sentence) if len(w) > 3 and len(w) < (16)]
   
      p = PorterStemmer()
      all_words = [p.stem(w) for w in tokens]
      all_words_freq = FreqDist(all_words)
      
      print all_words_freq.items()
      
      return all_words
      
   def increment_feature(self, feature, category)
      

if __name__ == '__main__':
   sentences = {}
   sentences['math'] = 'This is a sentence with a few words in it. Mathemathic, numbers, multiply numbers together to get results. Add some numbers together.'
   sentences['literature'] = 'This is a sentence with literaturally stuff. Books with pages and poems and stuff with arts and expression. Also authors.'
   
   c = NaiveBayesClassifier()
   
   c.train_from_data(sentences)


   
   
