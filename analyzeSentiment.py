# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file uses pointwise mutual informatino to analyze the sentiment of tweets

import json
from sklearn.metrics import mutual_info_score


def readJSON(jsonFile):
    with open(jsonFile) as f:
        tweets = json.load(f)
        return tweets['tweets']

tweets = readJSON('./tweets-cleaned-with-geo.json')
c = 0
p = 0
i = 0 

print(c, p, i)