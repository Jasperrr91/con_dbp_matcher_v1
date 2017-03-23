import os
import sys
import json
unigrams = open("lexstat/unigrams_cs.txt")
dictionary_of_unigrams = {}
for unigram_entry in unigrams.readlines():
    term, count = unigram_entry.split("\t")
    if int(count) > 50000:
            dictionary_of_unigrams[term.strip('\n').lower()] = count.strip('\n')

with open('lexstat/unigrams.json', 'w') as newjson:
    json.dump(dictionary_of_unigrams, newjson, indent=4)

