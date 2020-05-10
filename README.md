# Final project for CS5664
## Initial setup
You must install the following packages in order to run this code. I've compiled instructions for installation on Ubuntu and Arch Linux:

Arch Linux:

    sudo pacman -S geos dos2unix python-basemap python-basemap-common
    sudo pip install nltk pandas tweepy numpy pyshp pytz matplotlib 
Ubuntu:

    sudo apt update && sudo apt install libgeos libgeos-dev geos dos2unix python3 python3-pip
    sudo pip3 install nltk pandas tweepy numpy pyshp pytz matplotlib 
    sudo pip3 install --user https://github.com/matplotlib/basemap/archive/master.zip
## Required data
You must create a `data` folder in the directory that you clone the repo to on your current computer. In this folder, download [COVID-19 estimates: ihme_covid19.zip from IHME](http://www.healthdata.org/covid/data-downloads) and the [Twiter COVID-19 dataset: full_dataset.tsv.gz from Zenodo](https://zenodo.org/record/3783737). 
