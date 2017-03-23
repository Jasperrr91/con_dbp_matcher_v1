import json
import sys
import operator
import functools
import itertools
from collections import defaultdict
from nltk.corpus import stopwords
from lbl_uri_indexer import knowledge

#text = "is it correct to say that alan turing and noam chomsky are the giants"
#text = sys.argv[1:]
#print(text)
# gamma ray observatory
#alan turing

def clean_input(text):
    listerms = []
    for term in text:
        if term not in stopwords.words('english'):
            listerms.append(term)
    return listerms

def uri_term_mapper(sent_wo_stpwrds):
    trm_uri = {}
    lbl_uri_index = json.load(open("dbp/lbl-uri_index.json"))
    for term in sent_wo_stpwrds:
        uri_list_dup = []
        for enti_term, uri in lbl_uri_index.items():
            if term in enti_term:
                uri_list_dup.append(uri)
                uri_list = list(set(uri_list_dup))
                trm_uri[term] = uri_list
    listoftuples_uri_term = []
    uri_term_dict = defaultdict(list)
    for term, urilist in trm_uri.items():
        for uri in urilist:
            listoftuples_uri_term.append((uri, term))
    for uri, term in listoftuples_uri_term:
        uri_term_dict[uri].append(term)
    return uri_term_dict, lbl_uri_index

def extract_relevant_terms(uri_term_dict_shallow, lbl_uri_index):
    clean_dict = {}
    multiwords = []
    for uri, word_combination in uri_term_dict_shallow.items():
        if len(word_combination) >= 2:
            merged_term = ' '.join(word_combination)
            for label, index_uri in lbl_uri_index.items():
                if merged_term == label:
                    clean_dict[uri] = word_combination
                    for sw in word_combination:
                        multiwords.append(sw)
        if len(word_combination) == 1:
            for term in word_combination:
                if term not in multiwords:
                    clean_dict[uri] = word_combination
    return clean_dict



def select_candidates(uri_wordcombinations):
    relevant_candidates = {}
    mw_lenghts = []
    maximal_mw_length = ''
    for uri, wordcombination in uri_wordcombinations.items():
        mw_lenghts.append(len(wordcombination))
        maximal_mw_length = max(mw_lenghts)
    for uri, wordcombination in uri_wordcombinations.items():
        if len(wordcombination) == maximal_mw_length:
            relevant_candidates[uri] = wordcombination
    return relevant_candidates


def calculate_llh(ment_cnt_dbp, list_freq_corpus):
    multipl_all_freqs = functools.reduce(operator.mul, list_freq_corpus, 1)
    llh = ment_cnt_dbp/multipl_all_freqs
    return llh


def llh_mapping(candidates):
    unigram_file = open('lexstat/unigrams.json')
    unigram_dict = json.load(unigram_file)
    concept = {}
    for uri, multiword in candidates.items():
        concept_info = {}
        mention_count = ''
        singleword_termfrequencies = []
        concept_info['uri'] = uri
        for dictionary in knowledge:
            for instance in dictionary['instance']:
                if uri == instance['uri']:
                    for project in instance['projects']:
                        mention_count = project['mentions']
                        concept_info['mentioncount'] = mention_count
        likely_lbl = ' '.join(multiword)
        for word in multiword:
            for term, freq in unigram_dict.items():
                if word == term:
                    singleword_termfrequencies.append(int(freq))
        concept_info['frequency'] = singleword_termfrequencies
        llh = calculate_llh(mention_count, singleword_termfrequencies)
        concept_info['LLH'] = llh
        concept[likely_lbl] = concept_info
    return concept



def select_winning_entity(decision_index):
    winning_instance = {}
    target_key = max(decision_index, key=lambda dbp_instance: decision_index[dbp_instance]['LLH'])
    winning_instance['winner'] = target_key
    for dbp_inst_key,inst_inform in decision_index.items():
        if target_key == dbp_inst_key:
            uri = inst_inform['uri']
            for inst in knowledge:
                for label in inst['instance']:
                    if label['uri'] == uri:
                        winning_instance['types'] = label['types']
    return winning_instance
