from interpreter import *

text_input  = sys.argv[1:]

list_of_results = []
benchmark_sentences_file = open('benchmark_conversations/funct_test.txt')
read_sentences = benchmark_sentences_file.read()
sentences_lowercase = read_sentences.lower()
list_of_sentences = sentences_lowercase.split('.')
#for text_input in list_of_sentences:
#    print(text_input)
#    sent_wo_stpwrds = clean_input(text_input)
#    print(sent_wo_stpwrds)


#    uri_term_dict_shallow, lbl_uri_index = uri_term_mapper(sent_wo_stpwrds)
#    uri_multiword = extract_relevant_terms(uri_term_dict_shallow, lbl_uri_index)
#    candidates = select_candidates(uri_multiword)
#    decision_index = llh_mapping(candidates)
#    print(decision_index)


text_input = "he largely used java and python during that project"


sent_wo_stpwrds = clean_input(text_input)
print(sent_wo_stpwrds)
