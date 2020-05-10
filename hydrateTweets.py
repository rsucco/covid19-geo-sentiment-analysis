# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file reads from the chunks of the full dataset TSV and multithreads the hydration process for each chunk
# Prior to running this script, run chunkTsv.sh to chunk the TSV file appropriately

import os
from multiprocessing import Pool, cpu_count

def hydrateFile(filename):
    cmd = ('python3 get_metadata.py -i ' + filename + ' -o ' + filename[:-4] + ".tweets -c 'tweet_id'").format()
    print(cmd)
    os.system(cmd)


tsvFiles = [files[2] for files in os.walk('./data')][0]
tsvFiles = ["data/" + tsvFile for tsvFile in tsvFiles]

with Pool(64) as p:
    p.map(hydrateFile, tsvFiles)