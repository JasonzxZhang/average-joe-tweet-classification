from multiprocessing import Pool
import os
import re
import glob
import time
'''
TESTING!!
'''
def filter(text):
	text = re.sub(r'.*GMT ', '', text)	# removes UTC timestamps
	text = re.sub(r'.*UTC ', '', text)	# removes UTC timestamps
	text = re.sub(r'<.+?>', '', text)	# removes usernames and emojis
	text = re.sub(r'http\S+', '', text)	# removes URLS
	return text

def process_data(file, filename):
	# txt to list, separate by lines
	listified_text = []
	file = open(file).read()
	for p in file.split('\n'):
		listified_text.append(p)

	t0 = time.time()

	# Map - Reduce processing all text
	p = Pool() #optional param 'processes={#}'
	filtered_doc = p.map(filter, listified_text)
	p.close()
	p.join()

	t1 = time.time()
	print("Finished filtering in ", t1-t0)

	listified_text = []
	file = open(file).read()
	for p in file.split('\n'):
		l = filter(p)
		listified_text.append(l)

	t2 = time.time()
	print("Finished filtering in ", t2-t1)

	


if __name__ == "__main__":
	# Iterates through all files
	raw_data_path = "data/"
	os.chdir(raw_data_path)
	raw_files = glob.glob("*.txt")
	print("Files in queue: ", raw_files)
	for i, document in enumerate(raw_files):
		filename = str(raw_files[i])
		print(filename)
		# process_data(document, filename)