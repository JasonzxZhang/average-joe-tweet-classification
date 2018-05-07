import os
import re
import nltk
import glob
import time
import random
import pickle
from functools import partial
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB

'''
Input of a list raw files (path)
Returns a list of tokenized words
'''
def tokenize_files(file):
	try:
		stp = stopwords.words('english')
		lemm = WordNetLemmatizer()
		label = os.path.basename(file)[:-4]
		file = open(file).read()
		doc = []
		for sent in file.split('\n'):
			sent = nltk.word_tokenize(sent)
			tok = [ w.lower()
						for w in sent
						if (w.lower() not in stp and (w.isalpha()))
				  ]
			doc.append((tok, label))
		return doc
	except Exception as e:
		print("ERROR - ", e)

def tok_helper(file_path):
	stp = stopwords.words('english')
	lemm = WordNetLemmatizer()
	label = os.path.basename(file_path)[:-4]
	file = open(file_path).read()
	doc = []
	for sent in file.split('\n'):
		sent = nltk.word_tokenize(sent)
		tok = [ lemm.lemmatize(w.lower())
					for w in sent
					if (w.lower() not in stp and (w.isalpha()))
			  ]
		# lemm.lemmatize(w.lower())
		doc.append((tok, label))
	return doc

'''
Input a list of tokenized lists
Returns the same set without stopwords and punctuations
'''
def filter_lists(tokenized_lists):
	filtered_lists=[]
	for li in tokenized_lists:
		p = Pool()
		filtered_lists.append(list(filter(None,p.map(process_word, li))))
		p.close()
		p.join()
	return filtered_lists

'''
Input a word, will be removed if it's an english stopword
	or a punctuation
Returns word's original form, or None 
'''
def process_word(word):
	stp = stopwords.words('english')
	lemm = WordNetLemmatizer()
	if (word.lower() not in stp and (word.isalpha())):
		# return lemm.lemmatize(word.lower()) # Increase work time 20X
		return word.lower()
	return None

'''
Input a processed list (filtered and lemmatized)
Returns as list of tuples, each word is paried with desired label
'''
def create_doc(filtered_list, category=None):
	try:
		if not category:
			raise Exception('Missing category label in "create_doc"')
		doc = []
		for word in filtered_list:
			doc.append((word, category))
		random.shuffle(doc)
		return doc
	except Exception as e:
		print("ERROR - ", e)

def create_featureset(filtered_list, labels):
	try:
		if not (len(filtered_list) == len(labels)):
			raise Exception('"filtered_list" and "labels" lengths do not matchup')
		featuresets = []
		all_words = flatten_list(filtered_list)
		for li, cat in zip(filtered_list, labels):
			partial_helper = partial(feature_helper, target_list=all_words, label=cat)
			p = Pool()
			featuresets += p.map(partial_helper, li)
			p.close()
			p.join()
		random.shuffle(featuresets)				
		return featuresets
	except Exception as e:
		print("ERROR - ", e)

def feature_helper(word, target_list, label):
	featureset = []
	for w in target_list:
		features = {}
		if word == w:
			features['contains(%s)' % str(w)] = True
		else: 
			features['contains(%s)' % str(w)] = False
		featureset.append((features, label))
		print('featureset', featureset)
	return featureset

def flatten_list(nested_list):
	return [item for sublist in nested_list for item in sublist]

'''
Input a list of all found txt files under default path 
	or define path
Retusn a list of labels (essentially the basename of txt files)
'''
def generate_labels(raw_files):
	labels = []
	for f in raw_files:
		labels.append(os.path.basename(f)[:-4])
	return labels

'''
Input(optional) directory containing training text files
	default sets to "data/tweets/processed"
Returns a list of txt file full path
'''
def grab_training_data(file_path=None):
	if file_path:
		os.chdir(file_path)
		raw_files = glob.glob("*.txt")
	else:
		os.chdir("data/tweets/processed")
		raw_files = glob.glob("*.txt")
	return raw_files

# collect all text files
raw_files = grab_training_data("data/tweets/bk")
raw_files = glob.glob("*.txt")
print(raw_files)

t1 = time.time()

tokenized_lists = []
for f in raw_files: 
	tokenized_lists += tokenize_files(f)

t2 = time.time()
print("tokenized in ", t2-t1, "sec")
print(tokenized_lists)

filtered_list = filter_lists(tokenized_lists)

t3 = time.time()
print("processed in ", t3-t2, "sec")

featuresets = create_featureset(filtered_list, labels)
t4 = time.time()
print("featuresets created in ", t4-t3, "sec")

limit = round(0.1*(len(featuresets)-1)) # 10% of words will be used for testing
train_set, test_set = featuresets[limit:], featuresets[:limit]
# train_set, test_set = featuresets[100:], featuresets[:100]
print("Len train_set, test_set: ",len(train_set), len(test_set))

# os.chdir("../../../")
# # Save trained model with pickle
flatten = [item for sublist in filtered_list for item in sublist]
save_word_features = open("data/models/word_features.pickle","wb")
pickle.dump(flatten, save_word_features)
save_word_features.close()
t5 = time.time()
print("Word feature saved in ", t5-t4, "sec")

# # --- Multinomial Naive Bayes Classification ---
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(featuresets)
# print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100)

t6 = time.time()
print("Training completed in ", t6-t5, "sec")

save_classifier = open("data/models/MNB.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()
t7 = time.time()
print("Training model saved!")
print("Total time elapsed", t7-t1)

'''
tokenized in  29.80887484550476 sec
processed in  38.8754608631134 sec
607455
featuresets created in  1.069188117980957 sec
Len train_set, test_set:  546710 60745
Word feature saved in  0.1994030475616455 sec
MNB_classifier accuracy: 0.11523582187834389
Training completed in  2.9662349224090576 sec
Training model saved!
Total time elapsed 73.19560480117798

'''