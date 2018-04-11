import pickle
import nltk
# import warnings
# warnings.filterwarnings('ignore')

classifier = pickle.load(open('data/models/MNB.pickle', 'rb'))
word_features = pickle.load(open('data/models/word_features.pickle', 'rb'))

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def predict_topic(s):
	token = nltk.word_tokenize(s.lower())
	return classifier.classify(document_features(token))


text = input("Enter text here: ")
classified_topic = predict_topic(text)

print("Text:\t\t'", text, "'")
print("Category-->\t", classified_topic)

# filter text
# Map-Reduce filter text
# train model

'''
Backlog:
- Keep track of crawled tweets, by logging the UTC timestamps
- append to pickle instead of writing new
'''

