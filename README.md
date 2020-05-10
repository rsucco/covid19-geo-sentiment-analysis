# Final project for CS5664
## Initial setup
You must install the following packages in order to run this code. You may want to create a virtualenv to install the pip packages. The software may or may not work on other versions of the pip packages, but these are the ones I've tested it with. I've compiled instructions for installation on Ubuntu and Arch Linux:

Arch Linux:

    sudo pacman -S geos dos2unix
    sudo pip uninstall shapely
    sudo pip install nltk==3.5 pandas==1.0.1 tweepy==3.8.0 numpy==1.18.4 pyshp==2.1.0
    sudo pip install shapely --no-binary shapely
    sudo pip install cartopy
Ubuntu:

    sudo apt update && sudo apt install geos dos2unix python3 python3-pip
    sudo pip3 uninstall shapely
    sudo pip3 install nltk==3.5 pandas==1.0.1 tweepy==3.8.0 numpy==1.18.4 pyshp==2.1.0
    sudo pip3 install shapely --no-binary shapely
    sudo pip3 install cartopy
## Required data
You must create a `data` folder in the directory that you clone the repo to on your current computer. In this folder, download [COVID-19 estimates: ihme_covid19.zip from IHME](http://www.healthdata.org/covid/data-downloads) and the [Twiter COVID-19 dataset: full_dataset.tsv.gz from Zenodo](https://zenodo.org/record/3783737). 
