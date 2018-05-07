### Text Classificaiton/ Topic Models
Topic:
- technology 
- business
- politics
- entertainment
- sports
- health
- gaming
- food
- fashion
- music 


### Dependencies
- numpy
- scipy
- sklearn
- nltk
	- nltk.download('stopwords')
	- nltk.download('punkt')
- punkt

<!-- Add tweep requirements -->

### Crawl Data
'''python3 fetch_script.sh'''
defaults 



### Source:
- crawling tweets: [tweep] (https://github.com/haccer/tweep)
<<<<<<< HEAD
- classifier: [Tweet-Classifier] (https://github.com/Parassharmaa/Tweet-Classifier)
- http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

### Process
The raw data txt documents contain tweets under defined categories, such as 'entertainment' or 'sports'. Each document will be tokenized into separate words. Then, all the non-essential information, such as stopwords ('I', 'the', etc.), timestamp, usernames, will be deprecated. The remaining words will be stemmed, which means transforming a word into its regular term form ("stemming"-->"stem"). Finally, words and their corresponding labels (categories) are stored into a set and passed onto the "Multinomial Naive Bayes Classifier" for training. The result is stored in a pickle file, and used for prediction.