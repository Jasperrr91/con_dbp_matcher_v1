import sys
import json
from interpreter import *

#text = "is it correct to say that alan turing and noam chomsky are the giants in theoretical computer science"
import operator
import operator

input_text = sys.argv[1:]

#Clean the input string from stopwords by using the nltk language resource
sent_wo_stpwrds = clean_input(input_text)
#print("sentences without stopwords")
#print(sent_wo_stpwrds)

print("Map the singlewords to the DBPedia entries and the concerned URI's....")
#Map the extracted terms from input string to DBPedia links, and reverse them.
uri_term_dict_shallow, lbl_uri_index  = uri_term_mapper(sent_wo_stpwrds)
#for x,y in uri_term_dict_shallow.items():
#    print(x,y)

print("Map the URI's of the DBPedia entries to potential multiword...")
#Map the uri's to the potential multiwords tha refer to a single concept each
uri_multiword = extract_relevant_terms(uri_term_dict_shallow, lbl_uri_index)
#for x,y in uri_multiword.items():
#    print(x,y)

print("Print selected candidates...")
#Select the most likely multiwords of candidates to be nominated for LLH-based decision
candidates = select_candidates(uri_multiword)
#for x,y in candidates.items():
#    print(x,y)

print("Nominate candidates for LLH...")
#Create the dictionary of the nominated candidates for LLH-bases selection
decision_index = llh_mapping(candidates)
#for x,y in decision_index.items():
#    print(x,y)

print("And the winner is.......")
#Select the most likely entity!
the_winner = select_winning_entity(decision_index)
for x,y in the_winner.items():
    print(x,y)