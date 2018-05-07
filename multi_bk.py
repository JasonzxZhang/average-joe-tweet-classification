import os
import re
import nltk
import glob
import time
import random
import pickle
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
def tokenize_files(files):
	try:
		p = Pool() #optional param 'processes={#}'
		tokenized_list =  p.map(tok_helper, files)
		p.close()
		p.join()
		return tokenized_list
	except Exception as e:
		print("ERROR - ", e)

def tok_helper(file_path):
	file = open(file_path).read()
	return list(set(nltk.word_tokenize(file)))

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
# TODO: documents = p.map(create_doc, all_docs)

def create_featureset(filtered_list, labels):
	try:
		if not (len(filtered_list) == len(labels)):
			raise Exception('"filtered_list" and "labels" lengths do not matchup')
		featuresets = []
		flatten = lambda l: [item for sublist in l for item in sublist]
		p = Pool()
		all_words = list(p.map(flatten, filtered_list))
		p.close()
		p.join()

		for li, label in zip(filtered_list, labels):
			for w in li:
				# features['contains(%s)' % str(w)] = search_helper(w, filtered_list) # w in set(word) 
				features = {}
				features['contains(%s)' % str(w)] = True
				featuresets.append((features, label))
		return featuresets
	except Exception as e:
		print("ERROR - ", e)

def search_helper(word, filtered_list):
	for filtered_label_list in filtered_list:
		if word in filtered_label_list:
			return True
	return False


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
# os.chdir("data/tweets/processed")
raw_files = grab_training_data("data/tweets/processed")
print(raw_files)
labels = generate_labels(raw_files)
print(labels)

t1 = time.time()

tokenized_lists = tokenize_files(raw_files)

t2 = time.time()
print("tokenized in ", t2-t1, "sec")

filtered_list = filter_lists(tokenized_lists)

t3 = time.time()
print("processed in ", t3-t2, "sec")

featuresets = create_featureset(filtered_list, labels)
print(len(featuresets))
t4 = time.time()
print("featuresets created in ", t4-t3, "sec")

flatten = [item for sublist in filtered_list for item in sublist]
limit = round(0.1*(len(featuresets)-1)) # 10% of words will be used for testing
train_set, test_set = featuresets[limit:], featuresets[:limit]
# train_set, test_set = featuresets[100:], featuresets[:100]
print("Len train_set, test_set: ",len(train_set), len(test_set))

os.chdir("../../../")
# # Save trained model with pickle
save_word_features = open("data/models/word_features.pickle","wb")
pickle.dump(flatten, save_word_features)
save_word_features.close()
t5 = time.time()
print("Word feature saved in ", t5-t4, "sec")

# # --- Multinomial Naive Bayes Classification ---
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100)

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