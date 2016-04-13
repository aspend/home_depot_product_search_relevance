import pandas as pd
import numpy as np
import json

def read_json(path):
    '''
    Read .json file
    Args:
        path -- path to the file
    Return:
        json_data -- dictionary of the .son file
    '''
    json_file = open('../input/google_dict.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)
    return json_data

def fix_typos(serie, dictionary):
    fix_serie = serie.map(lambda x: dictionary[x] if x in dictionary else x)
    return fix_serie



if __name__=="__main__":
    attribute = pd.read_csv('../input/attributes.csv')
    product_description = pd.read_csv('../input/product_descriptions.csv')
    test = pd.read_csv('../input/test.csv')
    train = pd.read_csv('../input/train.csv')
    google_dict = read_json('../input/google_dict.json')
    test['search_term'] = fix_typos(test['search_term'], google_dict)
    train['search_term'] = fix_typos(train['search_term'], google_dict)
    
