import json

list_of_json_files = ["dbp/light.json"]

def create_knowledge_base(list_of_json_files):
    list_of_dict = []
    for json_file in list_of_json_files:
        jsonfile = open(json_file)
        json_dict = json.load(jsonfile)
        list_of_dict.append(json_dict)
    return list_of_dict

def labels_to_uri_indexer(dbpedia_input):
    lbl_uri_index = {}
    for dbp_cat in knowledge:
        for label, instances_list in dbp_cat.items():
            for inst_data in instances_list:
                uri = inst_data['uri']
                for term in inst_data['labels']:
                    label = term.lower()
                    lbl_uri_index[label] = uri
    return lbl_uri_index

def store_index(lbl_uri_index):
    with open('dbp/lbl-uri_index.json', 'w') as lbluriindex:
        json.dump(lbl_uri_index, lbluriindex, indent=4)

knowledge = create_knowledge_base(list_of_json_files)
lbl_uri_index = labels_to_uri_indexer(knowledge)
store_index(lbl_uri_index)
