# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file analyzes the sentiment of every tweet in a JSON file and writes a new JSON with the sentiment added

import json
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

# Read a JSON file into a dictionary
def readJSON(jsonFile):
    with open(jsonFile) as f:
        tweets = json.load(f)
        return tweets

# Tokenize and remove stop words from a tweet and add the tokenized tweets to the tweets' dictionaries under the 'tokenized' key
# Also add the filtered text under the 'filtered' key
def removeStopWords(oldTweets):
    newTweets = {}
    newTweets['tweets'] = []
    stopWords = set(stopwords.words('english'))
    stopWords.update(set(string.punctuation))
    extraStopWords = ['https', 'http', '..', '...', 'amp', 'I', '`', '``', '’', '’’', \
                          '\'t', '\'s', '\'\'', '“', '”', 'us', 'n\'t', 'one', 'two', 'three', \
                         'four', 'five', 'six', 'seven', 'eight', 'nine', '\'re', '.•']
    stopWords.update(extraStopWords)
    for tweet in oldTweets['tweets']:
        tokenizedTweet = word_tokenize(tweet['text'])
        tweet['tokenized'] = [word.lower() for word in tokenizedTweet if not word.lower() in stopWords]
        tweet['filtered'] = " ".join(tweet['tokenized'])
        newTweets['tweets'].append(tweet)
    return newTweets

# Analyze the sentiments of the tweets and add them to the tweets' dictionaries under the 'sentiment' key
def analyzeSentiment(oldTweets):
    newTweets = {}
    newTweets['tweets'] = []
    analyzer = SentimentIntensityAnalyzer()
    for tweet in oldTweets['tweets']:
        tweet['sentiment'] = analyzer.polarity_scores(tweet['filtered'])
        newTweets['tweets'].append(tweet)
    return newTweets

# Default parameter for json.dumps to convert datetime objects to strings
def dateConverter(toConvert):
    if isinstance(toConvert, datetime):
        return toConvert.__str__() 

# Write the clean data to a JSON file
def writeJSON(tweets, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, default = dateConverter, indent=4)

tweets = readJSON('./tweets-cleaned-with-state.json')
tweets = removeStopWords(tweets)
tweets = analyzeSentiment(tweets)
writeJSON(tweets, './tweets-states-sentiment.json')
print("Tweets written to ./tweets-state-sentiment.json")