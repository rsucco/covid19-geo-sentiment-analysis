# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file aggregates the sentiment of tweets in each state for each week, normalizes them, and generates a heatmap of positive/negative sentiment across the USA.
# The heatmaps are combined with data from the CDC to show the number of hospitalizations in each state for the same time period.

import numpy as np
import matplotlib.pyplot as plt
import json
import csv
import pytz
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon
from datetime import datetime

# Dictionary to translate state abbreviations to names
stateAbbreviations = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
abbreviationsOfStates = dict(map(reversed, stateAbbreviations.items()))

# Set the size of ax to the given width and height in inches
def setSize(w, h, ax):
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figureWidth = float(w)/(r-l)
    figureHeight = float(h)/(t-b)
    ax.figure.set_size_inches(figureWidth, figureHeight)

# Generate and plot the heatmap of the the given dataset
def plotHeatmap(sentiments, cdcData, sentimentType, startDate, endDate, ratios):
    # Replace the abbreviations of the states with their full names
    drawSentiments = {}
    for state in sentiments.keys():
        if len(state) == 2:
            drawSentiments[abbreviationsOfStates[state]] = sentiments[state]
    for state in stateAbbreviations.keys():
        if state not in drawSentiments.keys():
            drawSentiments[state] = 0

    # Create basemap for drawing the states
    m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
    colors={}
    statenames=[]

    # Set the caption and color scheme according to the sentiment type
    if sentimentType == 'pos':
        cmap = plt.cm.Greens
        plt.title('Positive scores and hospitalization rates from ' + str(startDate.date()) + " to " + str(endDate.date()) + \
            '\nValues for small states can be seen in the legend. Close this window to continue to the next time period.')
    elif sentimentType == 'neu':
        cmap = plt.cm.Blues
        plt.title('Neutral scores and hospitalization rates from ' + str(startDate.date()) + " to " + str(endDate.date()) + \
            '\nValues for small states can be seen in the legend. Close this window to continue to the next time period.')
    elif sentimentType == 'neg':
        cmap = plt.cm.Reds
        plt.title('Negative scores and hospitalization rates from ' + str(startDate.date()) + " to " + str(endDate.date()) + \
            '\nValues for small states can be seen in the legend. Close this window to continue to the next time period.')
    else: # Compound sentiment. This is the only one without a one-color gradient
        cmap = plt.cm.RdYlGn
        plt.title('Compound scores and hospitalization rates from ' + str(startDate.date()) + " to " + str(endDate.date()) + \
            '\nValues for small states can be seen in the legend. Close this window to continue to the next time period.')

    # Generate colors based on sentiment weight for each state
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        if statename not in ['District of Columbia','Puerto Rico']:
            sentiment = drawSentiments[statename]
            colors[statename] = cmap(sentiment)[:3]
        statenames.append(statename)
    
    # Create and set position of axes
    ax = plt.gca()
    pos1 = ax.get_position()
    pos2 = [pos1.x0 - 0.15, pos1.y0 + 0.05,  pos1.width, pos1.height] 
    ax.set_position(pos2)  

    # Draw and label all 50 states
    alreadyLabeled = []
    for nshape,seg in enumerate(m.states):
        if statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
            # Add Alaska and Hawaii
            if statenames[nshape] == 'Alaska':
                seg = list(map(lambda seg: (0.35*seg[0] + 1100000, 0.35*seg[1]-1250000), seg))
            if statenames[nshape] == 'Hawaii':
                seg = list(map(lambda seg: (seg[0] + 5500000, seg[1]-1600000), seg))
            color = rgb2hex(colors[statenames[nshape]]) 
            # Draw the polygon for the state. The label is used in generating the legend, but is not directly visible on the state
            stateAbbrev = stateAbbreviations[statenames[nshape]]
            if stateAbbrev in ratios.keys():
                ratio = round(ratios[stateAbbrev], 2)
            else:
                ratio = 0
            if statenames[nshape] not in alreadyLabeled:
                stateLabel = stateAbbrev + ': ' + str(cdcData[statenames[nshape]]) + ' hospitalizations, ' \
                    + str(round(drawSentiments[statenames[nshape]], 2)) + " relative " + sentimentType + " sentiment, " \
                    + str(ratio) + " normalized hospitalizations to " + sentimentType + " sentiment ratio."
                poly = Polygon(seg, facecolor=color, edgecolor='000000', label=stateLabel)
                alreadyLabeled.append(statenames[nshape])
            # Only draw the label once to prevent the legend from having duplicate values
            else:
                poly = Polygon(seg, facecolor=color, edgecolor='000000')
            ax.add_patch(poly)
            # Sort states alphabetically
            handles, labels = ax.get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    # Create the legend and position it appropriately
    ax.legend(handles, labels, fontsize='xx-small', bbox_to_anchor=(1,1.05))
    setSize(12, 6.5, ax)

    # Print the hospitalization numbers on each state
    printedHospitalizations = []
    for nshape,seg in enumerate(m.states):
        shortName = stateAbbreviations[statenames[nshape]]
        if shortName in printedHospitalizations: continue
        x, y = np.array(seg).mean(axis=0)
        plt.text(x+.1, y, cdcData[abbreviationsOfStates[shortName]], ha="center", fontsize="xx-small", color='#333333', backgroundcolor='#FFFFFF')
        printedHospitalizations += [shortName,] 
    plt.show()

# Get the average sentiment values by state
def getSentimentByState(tweets, sentiment, startDate, endDate):
    sentimentSum = {}
    sentimentCount = {}
    for tweet in tweets['tweets']:
        # Convert the timestamp field to a datetime object
        timestamp = datetime.strptime(tweet['timestamp'], '%Y-%m-%d %H:%M:%S%z')
        # Only calculate sentiment for the specified date range
        if timestamp > startDate and timestamp < endDate:
            if tweet['state'] in sentimentSum.keys():
                sentimentSum[tweet['state']] += tweet['sentiment'][sentiment]
                sentimentCount[tweet['state']] += 1
            else:
                sentimentSum[tweet['state']] = tweet['sentiment'][sentiment]
                sentimentCount[tweet['state']] = 1
    stateSentiments = {}
    # Calculate average for the given time period
    for state in sentimentSum.keys():
        stateSentiments[state] = sentimentSum[state] / sentimentCount[state]
    return stateSentiments

# Normalize the sentiment values from 0 to 1
def normalizeSentiment(stateSentiments):
    valMin, valMax = min(stateSentiments.values()), max(stateSentiments.values())
    newSentiments = {}
    for state, val in stateSentiments.items():
        newSentiments[state] = (val - valMin) / (valMax - valMin)
    return newSentiments

# Generate date ranges in the form of tuples for the tweets, based on the number of slices desired
def getDateRanges(tweets, numSlices):
    dateranges = []
    # Generate a list of all the timestamp fields in all the tweets and convert them to datetime objects
    dates = list(datetime.strptime(tweet['timestamp'], '%Y-%m-%d %H:%M:%S%z') for tweet in tweets['tweets'])
    firstDate = min(dates)
    lastDate = max(dates)
    slices = []
    sliceSize = (lastDate - firstDate) / numSlices
    # Generate and return the list of tuples of time slices
    for i in range(numSlices):
        slices.append([(firstDate + sliceSize * i), (firstDate + sliceSize * (i + 1))])
    return slices

# Load the CDC data for a given date range
def loadCDCData(filename, startDate, endDate):
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        # Only read the values needed
        data = {rows[0]:{'state' : rows[1], 'date' : rows[2], 'hospitalizations' : rows[3]} for rows in reader}
        # Delete the first line with the field names
        del data['V1']
    usData = {}
    for state in stateAbbreviations.keys():
        usData[state] = {}
    for record in data:
        # Get the date and number of hospitalizations from the record. Only proceed if the record is in the desired time range
        recordDate = datetime.strptime(data[record]['date'], '%Y-%m-%d').date()
        if data[record]['state'] in stateAbbreviations.keys() and recordDate >= startDate.date() and recordDate <= endDate.date() :
            usData[data[record]['state']][data[record]['date']] = data[record]['hospitalizations']
    return usData

# Calculate the average hospitalization rate for a given portion of the CDC data
def averageCDCData(data):
    averagedData = {}
    for state in data:
        hospitalizations = list(float(item[1]) for item in data[state].items())
        average = int(sum(hospitalizations) / len(hospitalizations))
        averagedData[state] = average
    return averagedData

# Calculate the ratios of the given sentiment to hospitalizations and normalize it
def calculateRatios(normalizedSentiments, cdcData):
    # Normalize CDC data
    normalizedCdcData = {}
    valMin, valMax = min(cdcData.values()), max(cdcData.values())
    for state, val in cdcData.items():
        normalizedCdcData[state] = (val - valMin) / (valMax - valMin)

    # Calculate all the ratios
    ratios = {}
    for state in normalizedSentiments.keys():
        if state == 'UNK': continue
        if normalizedSentiments[state] == 0:
            ratios[state] = 0
            continue
        ratios[state] = normalizedCdcData[abbreviationsOfStates[state]] / normalizedSentiments[state]
    # Normalize all the ratios
    normalizedRatios = {}
    valMin, valMax = min(ratios.values()), max(ratios.values())
    for state, val in ratios.items():
        normalizedRatios[state] = (val - valMin) / (valMax - valMin)
    return ratios

# Load the cleaned JSON file with the tweets we need
with open('./tweets-states-sentiment.json') as f:
    tweets = json.load(f)

numRanges = int(input("Enter number of date ranges to generate. Higher numbers will increase the granuality in the time dimension \
but will lead to smaller sample sizes and less accurate data. (Default 4)\n") or 4)

typesStr = str(input("Enter the types of sentiment that you would like to analyze in the format cpnu\n\
For instance, enter cp to analyze compound and positive, n to analyze just negative, un for neutral and negative.\n\
Reports will be displayed in the order that you enter their letters.\n\
c: compound, p: positive, n: negative, u: neutral. (Default all)\n") or 'cpnu')

sentimentTypes = []
for char in typesStr:
    if char == 'c':
        sentimentTypes.append('compound')
    elif char == 'p':
        sentimentTypes.append('pos')
    elif char == 'n':
        sentimentTypes.append('neg')
    elif char == 'u':
        sentimentTypes.append('neu')

# Get date ranges to work with
dateranges = getDateRanges(tweets, numRanges)

# Load the CDC data
cdcData = loadCDCData('data/Hospitalization_all_locs.csv', dateranges[0][0], dateranges[-1][1])

# Draw all the graphs
for sentimentType in sentimentTypes:
    for daterange in dateranges:
        stateSentiments = getSentimentByState(tweets, sentimentType, daterange[0], daterange[1])
        normalizedSentiments = normalizeSentiment(stateSentiments)
        cdcData = loadCDCData('data/Hospitalization_all_locs.csv', daterange[0], daterange[1])
        cdcData = averageCDCData(cdcData)
        ratios = calculateRatios(normalizedSentiments, cdcData)
        plotHeatmap(normalizedSentiments, cdcData, sentimentType, daterange[0], daterange[1], ratios)
