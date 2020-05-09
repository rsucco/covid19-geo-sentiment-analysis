#! /bin/bash
# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This file chunks the large full_dataset.tsv file into more manageable chunks

cd ./data
split -l 150000 full_dataset.tsv data-

for file in `ls data-* | grep -v data-aa`; do
    sed -i '1itweet_id\tdate\ttime' $file
done
for file in `ls data-*`; do
    mv $file $file.tsv
done
