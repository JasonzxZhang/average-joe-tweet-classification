import pickle
import nltk
from nltk import ProbDistI
from prettytable import PrettyTable


class Classifier(object):
	"""docstring for Classifier"""
	def __init__(self):
		super(Classifier, self).__init__()
		self.classifier = pickle.load(open('data/models/MNB.pickle', 'rb'))
		self.word_features = pickle.load(open('data/models/word_features.pickle', 'rb'))

	def predict_topic(self, text=None):
		'''
		Classify topic based on input text

		Parameters:
		-----------------------------------------------
		text (str) - tweets to be analyzed

		Returns:
		-----------------------------------------------
		( numpy.str_ , dict{str:float} ) - a tuple of
			"category of the prediction"
			str('label')
				e.g.	'entertainment'
			&.................................................
			"all non-zero probabilities on each categories"
			{'label':'probability'}
				e.g.	dict {
							'entertainment' : 0.8189,
							'technology' : 0.1811
						}

		'''
		if not text:
			print("No text passed into 'predict_topic()'")
			return None

		# converts to set of words
		token = nltk.word_tokenize(text.lower()) 

		# return the label with max probibility based on Bayes'
		prediction = self.classifier.classify(self.document_features(token))

		# return a dict of all labels with non-zero probabilities
		probDistI = self.classifier.prob_classify(self.document_features(token))
		p_distribution = { 
			str(label):probDistI.prob(label)
			for label in probDistI.samples()
		}
		return (prediction, p_distribution)

	def document_features(self, document):
		'''
		Classify topic based on input text

		Parameters:
		-----------------------------------------------
		document (str) - tweets to be analyzed

		Returns:
		-----------------------------------------------
		dict{str:bool} - 
			a dict of "words" & "its existence in current trained document"
			{'contains(label)':'existence'}
				e.g.	dict {
							'contains(hello)' : True,
							'contains(world)' : False
						}
		'''
		document_words = set(document)
		features = {}
		for word in self.word_features:
			print 
			features['contains(%s)' % word] = (word in document_words)
		return features

'''
Backlog:
- Keep track of crawled tweets, by logging the UTC timestamps
- append to pickle instead of writing new
'''

