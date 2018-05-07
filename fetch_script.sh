python3 tweep.py -s technology -l en --limit 500 -o ./data/tweets/technology.txt
python3 tweep.py -s business -l en --limit 500 -o ./data/tweets/business.txt
python3 tweep.py -s politics -l en --limit 500 -o ./data/tweets/politics.txt
python3 tweep.py -s entertainment -l en --limit 500 -o ./data/tweets/entertainment.txt
python3 tweep.py -s sports -l en --limit 500 -o ./data/tweets/sports.txt
python3 tweep.py -s health -l en --limit 500 -o ./data/tweets/health.txt
python3 tweep.py -s gaming -l en --limit 500 -o ./data/tweets/gaming.txt
python3 tweep.py -s food -l en --limit 500 -o ./data/tweets/food.txt
python3 tweep.py -s fashion -l en --limit 500 -o ./data/tweets/fashion.txt
python3 tweep.py -s music -l en --limit 500 -o ./data/tweets/music.txt

python3 filter_tweets.py

