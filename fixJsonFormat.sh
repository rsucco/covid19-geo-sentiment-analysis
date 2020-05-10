#! /bin/bash
# Ryan Succo / Molly Illjevich
# CS5664 Final Project
#
# This script fixes the formatting to valid JSON. It depends on the dos2unix utility and has only been tested on Linux.

cd ./data
for filename in `ls *.tweets`; do
    dos2unix $filename
    sed '1i{"tweets": [' $filename > temp
    awk 'BEGIN{getline line} {print line; line=$0 ",";} END{print $0}' temp > $filename.json
    rm temp
    echo ']}' >> $filename.json
    echo "Fixed $filename"
done