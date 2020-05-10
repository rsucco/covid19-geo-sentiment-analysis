# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file cleans up the data collected from Twitter, retaining only the relevant tweets.
# If you're running out of memory, try only doing the ones with the geo data.

import json
import os
from datetime import datetime

# Load a JSON file to a dictionary
def loadJson(jsonFile):
    with open(os.path.join(os.getcwd(), jsonFile)) as f:
        tweets = json.load(f)
        return tweets['tweets']

# Read a JSON file and extract only the tweets that we want for our analysis
def cleanFile(jsonFile, requireGeo):
    tweets = loadJson(jsonFile)
    newTweets = {}
    newTweets['tweets'] = []
    for tweet in tweets:
        if tweet['lang'] == 'en' and (not requireGeo or tweet['place'] is not None or tweet['coordinates'] is not None):
            newTweet = {}
            newTweet['timestamp'] = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
            newTweet['id'] = tweet['id']
            newTweet['text'] = tweet['text']
            newTweet['hashtags'] = tweet['entities']['hashtags']
            newTweet['user_mentions'] = tweet['entities']['user_mentions']
            newTweet['user'] = {}
            newTweet['user']['id'] = tweet['user']['id']
            newTweet['user']['followers_count'] = tweet['user']['followers_count']
            newTweet['user']['friends_count'] = tweet['user']['friends_count']
            if tweet['coordinates'] is not None:
                newTweet['coordinates'] = tweet['coordinates']
            if tweet['place'] is not None:
                newTweet['place'] = tweet['place']
            newTweet['retweets'] = tweet['retweet_count']
            newTweet['favorites'] = tweet['favorite_count']
            newTweets['tweets'].append(newTweet)
    return newTweets

# Default parameter for json.dumps to convert datetime objects to strings
def dateConverter(toConvert):
    if isinstance(toConvert, datetime):
        return toConvert.__str__() 

# Write the clean data to a JSON file
def writeJSON(tweets, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, default = dateConverter, indent=4)

# Get a list of all the data files
jsonFiles = [files[2] for files in os.walk('data')][0]
jsonFiles = ["data/" + jsonFile for jsonFile in jsonFiles if '.json' in jsonFile]

# Clean and all the tweets and write them to one JSON file
allTweets = {}
allTweets['tweets'] = []
geoTweets = {}
geoTweets['tweets'] = []
for jsonFile in jsonFiles:
    print("Cleaning", jsonFile)
    cleanJson = cleanFile(jsonFile, True)['tweets']
    geoTweets['tweets'].extend(cleanJson)
    cleanJson = cleanFile(jsonFile, False)['tweets']
    allTweets['tweets'].extend(cleanJson)
print("geotweets", len(geoTweets['tweets']))
print("alltweets", len(allTweets['tweets']))
writeJSON("There are", geoTweets, 'tweets in tweets-cleaned-with-geo.json')
writeJSON("There are", allTweets, 'tweets in tweets-cleaned-all.json')
