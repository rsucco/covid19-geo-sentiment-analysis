## Initial setup
You must install some packages in order to run this code. I've only tested this on Linux, although I've included what should be valid instructions of macOS, and Windows users should be able to follow the Ubuntu instructions within Windows Subsystem for Linux. I plan to containerize this application eventually which should make things easier. For now, I've written setup instructions for Arch Linux, Ubuntu, and macOS:

Arch Linux:

    sudo pacman -S geos dos2unix python-basemap python-basemap-common python python-pip split
    sudo pip install nltk pandas tweepy numpy pyshp pytz matplotlib 
Ubuntu:

    sudo apt update && sudo apt install libgeos libgeos-dev geos dos2unix python3 python3-pip
    sudo pip3 install nltk pandas tweepy numpy pyshp pytz matplotlib 
macOS:

    mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
    brew install python3 dos2unix geos
    pip3 install https://github.com/matplotlib/basemap/archive/master.zip
    pip3 install nltk pandas tweepy numpy pyshp pytz matplotlib 
    
You must also ensure that you have a JSON file name api_keys.json in the top-level directory of the project. In this file, you must have fields for 'consumer_key', 'consumer_secret', 'access_token', and 'access_token_secret'. These will be given to you by Twitter upon approval to use their API.

## Required data
You must create a `data` folder in the directory that you clone the repo to on your current computer. In this folder, download [COVID-19 estimates: ihme_covid19.zip from IHME](http://www.healthdata.org/covid/data-downloads) and the [Twiter COVID-19 dataset: full_dataset.tsv.gz from Zenodo](https://zenodo.org/record/3783737). Due to the terms of use, I am not allowed to distribute the rehydrated tweets, but all of the code here is sufficient to do it yourself.

## Conducting Analysis
The data collection and cleaning scripts take a considerable amount of time, due in large part to the Twitter's API's rate limit. Run the scripts in this order, making sure that you have already downloaded the required data files to the `data` directory:

    ./chunkTsv.sh
    python3 hydrateTweets.py # This one could take days to finish running
    ./fixJsonFormat.sh
    python3 cleanData.py
    python3 geotagStatesData.py
    python3 analyzeSentiment.py
    python3 generateHeatmap.py
