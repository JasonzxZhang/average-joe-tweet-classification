import os
import re
import nltk
import glob
import random
import pickle
import time
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB


data_path = "data/tweets/bk"
os.chdir(data_path)
raw_files = glob.glob("*.txt")


def process_word(word):
	# remove english stopwords and punctuations
	stopword = stopwords.words('english')
	lemm = WordNetLemmatizer()
	if (word.lower() not in stopword and (word.isalpha())):
		return lemm.lemmatize(word.lower())
	return None

def tokenize_files(files,label_name=None):
	try:
		# if not label_name:
		# 	label_name = os.path.basename(file)[:-4]
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

# print(tok)
# t1 = time.time()
# filtered_list = list(map(process_word, tok))
# t2 = time.time()
# print(t1-t2)
# filtered_list = list(filter(None, filtered_list))
# t3 = time.time()
# print(t2-t3)
# print(filtered_list)

# print(raw_files)
t1 = time.time()
filtered_list = tokenize_files(raw_files)
t2 = time.time()
print(t2-t1)
print(filtered_list)