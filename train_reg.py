import os
import re
import nltk
import glob
import random
import pickle
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

# collect all text files
data_path = "data/tweets/bk"
os.chdir(data_path)
raw_files = glob.glob("*.txt")
print(raw_files)


documents= []
all_words  = []
# filtering to english tweeets only
stp = stopwords.words('english')

t0 = time.time() # Time marker 1 
# tokenize words from every tweet


for f in raw_files:
	text = open(f).read()
	for p in text.split('\n'):
		p = re.sub(r'[^\w\s]','',p)	# individual word or char
		p = re.sub(" \d+", " ", p)	# sub 1 or more digits
		p = [i.lower() for i in list(set(nltk.word_tokenize(p)) - set(stp))]

		all_words+=p
		documents.append((p, f[:-4]))
# print('documents', documents)
# print('documents len', len(documents))
# print('all_words', all_words)
# print('all_words len', len(all_words))
# -----------------------------
t1 = time.time() # Time marker 2

random.shuffle(documents)

t2 = time.time() # Time marker 3

word_features = list(all_words)

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % str(word)] = (word in document_words)
	return features
featuresets = [(document_features(word), category) for (word,category) in documents]

a,b = featuresets[0]
c,d = zip(featuresets[1])
print(len(a),len(c))
print("word_features ",len(word_features))
print("documents ",len(documents))
print("featuresets ",len(featuresets))
# print(a)
t3 = time.time() # Time marker 4


train_set, test_set = featuresets[100:], featuresets[:100]
# print("train_set ", train_set)

# print("test_set", test_set)
os.chdir("../../../")


# Save trained model with pickle
save_word_features = open("data/models/word_features.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

# --- Multinomial Naive Bayes Classification ---
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
# print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100)

save_classifier = open("data/models/MNB.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()




