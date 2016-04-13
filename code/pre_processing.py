import pandas as pd
import numpy as np
import json
import re
from nltk.stem.porter import *
stemmer = PorterStemmer()
# import sys
# reload(sys)
# sys.setdefaultencoding("ISO-8859-1")

def read_json(path):
    """
        Read .json file
        Args:
            path -- path to the file
        Return:
            json_data -- dictionary of the .son file
    """
    json_file = open('../input/google_dict.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)
    return json_data


def fix_typos(serie, dictionary):
    """
        fix typos using a dictionary found in the kaggle forum
        Args:
            serie -- serie where there are the string that need to be fixed
            dictionary -- dictionary with the typos as key and the correct form
                        as value
        Return:
            fix_serie -- serie without typos

    """
    fix_serie = serie.map(lambda x: dictionary[x] if x in dictionary else x)
    return fix_serie


def str_stem(s):
    """
        Stem string
        Args:
            s -- string
        Return
            s -- stemmed string
    """
    if isinstance(s, str):
        s = re.sub(r"(\w)\.([A-Z])", r"\1 \2", s) #Split words with a.A
        s = s.lower()
        s = s.replace("  "," ")
        s = re.sub(r"([0-9]),([0-9])", r"\1\2", s)
        s = s.replace(","," ")
        s = s.replace("$"," ")
        s = s.replace("?"," ")
        s = s.replace("-"," ")
        s = s.replace("//","/")
        s = s.replace("..",".")
        s = s.replace(" / "," ")
        s = s.replace(" \\ "," ")
        s = s.replace("."," . ")
        s = re.sub(r"(^\.|/)", r"", s)
        s = re.sub(r"(\.|/)$", r"", s)
        s = re.sub(r"([0-9])([a-z])", r"\1 \2", s)
        s = re.sub(r"([a-z])([0-9])", r"\1 \2", s)
        s = s.replace(" x "," xbi ")
        s = re.sub(r"([a-z])( *)\.( *)([a-z])", r"\1 \4", s)
        s = re.sub(r"([a-z])( *)/( *)([a-z])", r"\1 \4", s)
        s = s.replace("*"," xbi ")
        s = s.replace(" by "," xbi ")
        s = s.replace("deckov", "deck over")
        s = re.sub(r"([0-9])( *)\.( *)([0-9])", r"\1.\4", s)
        s = re.sub(r"([0-9]+)( *)(inches|inch|in|')\.?", r"\1in. ", s)
        s = re.sub(r"([0-9]+)( *)(foot|feet|ft|'')\.?", r"\1ft. ", s)
        s = re.sub(r"([0-9]+)( *)(pounds|pound|lbs|lb)\.?", r"\1lb. ", s)
        s = re.sub(r"([0-9]+)( *)(square|sq) ?\.?(feet|foot|ft)\.?", r"\1sq.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(cubic|cu) ?\.?(feet|foot|ft)\.?", r"\1cu.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1gal. ", s)
        s = re.sub(r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1oz. ", s)
        s = re.sub(r"([0-9]+)( *)(centimeters|cm)\.?", r"\1cm. ", s)
        s = re.sub(r"([0-9]+)( *)(milimeters|mm)\.?", r"\1mm. ", s)
        s = re.sub(r"([0-9]+)( *)(degrees|degree)\.?", r"\1deg. ", s)
        s = s.replace(" v "," volts ")
        s = re.sub(r"([0-9]+)( *)(volts|volt)\.?", r"\1volt. ", s)
        s = re.sub(r"([0-9]+)( *)(watts|watt)\.?", r"\1watt. ", s)
        s = re.sub(r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1amp. ", s)
        s = s.replace("  "," ")
        s = s.replace(" . "," ")
        s = (" ").join([str(strNum[z]) if z in strNum else z for z in s.split(" ")])
        s = (" ").join([stemmer.stem(z) for z in s.split(" ")])
        return s
    else:
        return "null"


def import_data():
    """
        import data as pandas dataframe
        Args:

        Return:
            attribute -- dataframe of the product attributes
            product_description -- dataframe of the product description
            test -- test dataframe
            train -- train dataframe
            google_dict -- dictionary that contains correction to the typos
    """

    attribute = pd.read_csv('../input/attributes.csv')
    product_description = pd.read_csv('../input/product_descriptions.csv')
    test = pd.read_csv('../input/test.csv')
    train = pd.read_csv('../input/train.csv')
    google_dict = read_json('../input/google_dict.json')
    return attribute, product_description, test, train, google_dict


def data_merging(train, test, attribute, product_description):
    """
        Merge data in a unique dataframe
        Args:
            train -- train dataframe
            test -- test dataframe
            attribute -- attribute dataframe
            product_description -- product description dataframe
        Return:
            df_all -- dataframe with the information of all the table
            num_train -- num of rows of the train set
    """
    brand = attribute[attribute.name == "MFG Brand Name"][["product_uid", "value"]].rename(columns={"value": "brand"})
    num_train = train.shape[0] # to keep track of the train data when we merge with the test
    df_all = pd.concat((train, test), axis=0, ignore_index=True)
    df_all = pd.merge(df_all, product_description, how='left', on='product_uid')
    df_all = pd.merge(df_all, brand, how='left', on='product_uid')
    return df_all, num_train


def text_processing(table, dictionary):
    """
        Process the text in the table in order to standarize it
        Args:
            table -- dataframe with all the information
            dictionary -- dictionary that contains the typos
        Return:
            table -- table with the text stemmed
    """
    table['search_term'] = fix_typos(table['search_term'], dictionary)
    table['search_term'] = table['search_term'].map(lambda x:str_stem(x))
    table['product_title'] = table['product_title'].map(lambda x:str_stem(x))
    table['product_description'] =table['product_description'].map(lambda x:str_stem(x))
    table['brand'] = table['brand'].map(lambda x:str_stem(x))
    return table

stop_w = ['for', 'xbi', 'and', 'in', 'th','on','sku','with','what','from','that','less','er','ing']
strNum = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}

if __name__=="__main__":
    attribute, product_description, test, train, google_dict = import_data()
    df_all, num_train = data_merging(train, test, attribute, product_description)
    df_all = text_processing(df_all, google_dict)
    df_all.to_csv('df_all.csv')
