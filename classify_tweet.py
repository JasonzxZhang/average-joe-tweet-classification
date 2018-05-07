import pickle
import nltk
from nltk import ProbDistI
from prettytable import PrettyTable

def predict_topic(text=None):
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

	# TODO: add lemmatizer

	# return the label with max probibility based on Bayes'
	prediction = classifier.classify(document_features(token))

	# return a dict of all labels with non-zero probabilities
	probDistI = classifier.prob_classify(document_features(token))
	p_distribution = { 
		str(label):probDistI.prob(label)
		for label in probDistI.samples()
	}
	return (prediction, p_distribution)

def document_features(document):
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
	for word in word_features:
		if word:
			features['contains(%s)' % word] = (word in document_words)
		else:
			features['contains(%s)' % word] = False
	return features

def print_analysis(text=None, prediction=None, prob=None):
	'''
	Pretty print predicted category and in-depth probability report

	'''
	if not(text and prediction and prob):
		print("Insufficient params for 'print_analysis()'")
		return

	table = PrettyTable(['Category', 'Probability(%)'])
	for k, v in prob.items():
		v = float(("%0.2f"%(v*100)))
		table.add_row([k,v])
	print("Input text:\t'", text, "'")
	print("Classified as:\t", classified_topic)
	print(table.get_string(sortby="Probability(%)", reversesort=True))

classifier = pickle.load(open('data/models/MNB.pickle', 'rb'))
word_features = pickle.load(open('data/models/word_features.pickle', 'rb'))

text = input("Enter text here: ")
classified_topic, prob = predict_topic(text)
print_analysis(text, classified_topic, prob)

'''
Backlog:
- Keep track of crawled tweets, by logging the UTC timestamps
- append to pickle instead of writing new
'''

