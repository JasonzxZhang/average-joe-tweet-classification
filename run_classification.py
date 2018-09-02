import math
from prettytable import PrettyTable
from classify_tweet import Classifier

def main():
	text = input("Input the text for analysis --> ")
	cl = Classifier()
	if text or (not text == ""):
		# Analyzing text with pre-trained model =
		prediciton, probabilities = cl.predict_topic(text=text)

		# Displaying prediction
		print("Prediction: %s" % prediciton)

		# Dispalying probability per category break in a table
		print('\nList probability breakdown')
		pt = PrettyTable()
		pt.field_names = ["Category", "Probability"];
		for key, value in probabilities.items():
			pt.add_row([key, round(value*100 , 2)])
		print(pt)
	else:
		print("INVALID INPUT!")

if __name__ == "__main__":
	main()