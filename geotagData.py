# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file converts the 'place' field in a dataset of tweets into a two-character 'state' field

from datetime import datetime

# Declare dictionary of state abbreviations and their full names
states = {'alabama' : 'AL', 'alaska' : 'AK', 'arizona' : 'AZ', 'arkansas' : 'AR', 'california' : 'CA', 'colorado' : 'CO', 
          'connecticut' : 'CT', 'washington, dc' : 'DC', 'delaware' : 'DE', 'florida' : 'FL', 'georgia' : 'GA', 
          'hawaii' : 'HI', 'idaho' : 'ID', 'illinois' : 'IL', 'indiana' : 'IN', 'iowa' : 'IA', 'kansas' : 'KS', 'kentucky' : 'KY',
          'louisiana' : 'LA', 'maine' : 'ME', 'maryland' : 'MD', 'massachusetts' : 'MA', 'michigan' : 'MI', 'minnesota' : 'MN', 
          'mississippi' : 'MS', 'missouri' : 'MO', 'montana' : 'MT', 'nebraska' : 'NE', 'nevada' : 'NV', 'new hampshire' : 'NH',
          'new jersey' : 'NJ', 'new mexico' : 'NM', 'new york' : 'NY', 'north carolina' : 'NC', 'north dakota' : 'ND', 'ohio' : 'OH',
          'oklahoma' : 'OK', 'oregon' : 'OR', 'pennsylvania' : 'PA', 'rhode island' : 'RI', 'south carolina' : 'SC', 'south dakota' : 'SD',
          'tennessee' : 'TN', 'texas' : 'TX', 'utah' : 'UT', 'vermont' : 'VT', 'virginia' : 'VA', 'washington, usa' : 'WA', 'west virginia' : 'WV',
          'wisconsin' : 'WI', 'wyoming' : 'WY', 'puerto rico' : 'PR'}

# For each tweet, get the state that it came from
def getStates(tweets):
    newTweets = {}
    newTweets['tweets'] = []
    # Convert any placenames to states
    for tweet in tweets['tweets']:
        try:
            if tweet['place']['country_code'] == 'US' and tweet['id'] not in (i['id'] for i in newTweets['tweets']):
                newTweet = tweet.copy()
                if tweet['place']['full_name'][-2:] in states.values():
                    newTweet['state'] = tweet['place']['full_name'][-2:]
                else:
                    for state in states.keys():
                        if state in tweet['place']['full_name'].lower() or state in tweet['place']['name'].lower():
                            newTweet['state'] = states[state]
                            break
                        else:
                            newTweet['state'] = 'UNK'
                del newTweet['place']
                try:
                    del newTweet['coordinates']
                except Exception:
                    pass
                newTweets['tweets'].append(newTweet)            
        except:
            continue
    
    finalTweets = {}
    finalTweets['tweets'] = sorted(newTweets['tweets'], key = lambda i: i['timestamp'])
    return finalTweets

# Default parameter for json.dumps to convert datetime objects to strings
def dateConverter(toConvert):
    if isinstance(toConvert, datetime):
        return toConvert.__str__() 

# Write the clean data to a JSON file
def writeJSON(tweets, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, default = dateConverter, indent=4)

with open('./tweets-cleaned-with-geo.json') as f:
    tweets = json.load(f)

tweets = getStates(tweets)
print(len(tweets['tweets']))
writeJSON(tweets, './tweets-cleaned-with-state.json')
print("Tweets written to ./tweets-cleaned-with-state.json")