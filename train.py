import os
import re
import nltk
import glob
import random
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

data_path = "data/tweets/processed"
os.chdir(data_path)
raw_files = glob.glob("*.txt")
print(raw_files)


documents= []
all_words  = []
# filtering to english tweeets only
stp = stopwords.words('english')

# tokenize words from every tweet
for f in raw_files:
	text = open(f).read()
	for p in text.split('\n'):
		p = re.sub(r'[^\w\s]','',p)
		p = re.sub(" \d+", " ", p)
		p = [i.lower() for i in list(set(nltk.word_tokenize(p)) - set(stp))]
		all_words+=p
		documents.append((p, f[:-4]))

random.shuffle(documents)

word_features = list(all_words)

print("Sample:")
print(documents[1])
print(word_features[1])
def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % str(word)] = (word in document_words)
	return features

featuresets = [(document_features(d), c) for (d,c) in documents]

train_set, test_set = featuresets[100:], featuresets[:100]
print(len(train_set), len(test_set))

os.chdir("../../../")

save_word_features = open("data/models/word_features.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


'''
 Below contains three different classifiers:
- Multinomial Naive Bayes Classification
- Naive Bayes Classification
- Support Vector Machine (LinearSVC)
'''
# --- Multinomial Naive Bayes Classification ---
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100)

save_classifier = open("data/models/MNB.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

# --- Naive Bayes Classification --- 
# NB_classifier = nltk.NaiveBayesClassifier.train(train_set)
# print("NaiveBayes accuracy:", (nltk.classify.accuracy(NB_classifier, test_set))*100)

# save_classifier = open("data/trained/NAIVE.pickle","wb")
# pickle.dump(NB_classifier, save_classifier)
# save_classifier.close()

# --- Support Vector Machine (LinearSVC) ---
# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(train_set)
# print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, test_set))*100)

# save_classifier = open("data/trained/SVC.pickle","wb")
# pickle.dump(LinearSVC_classifier, save_classifier)
# save_classifier.close()




