import requests
import numpy as np
from bs4 import BeautifulSoup
from constants import HEADERS, TIMEOUT, PARSER
import Levenshtein
import os
import pandas as pd

def request_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except:
        print(f'Error occured while scraping {url}')
        return None
        
    soup = BeautifulSoup(response.text, PARSER)
    return soup

def normalized_levenshtein(s1, s2):
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return None
    return 1 - (Levenshtein.distance(s1, s2) / max_len)

def standardize_nan(df):
    values_to_replace = ['{}', '[]', '', 'NA', 'N/A', '-', 'nan', '\\N']
    replace_map = {value: np.nan for value in values_to_replace}
    df = df.replace(replace_map)
    
    return df

def concatenate_folder(root):
    df_list = []
    for file in os.listdir(root):
        tmp = pd.read_csv(root + file)
        df_list.append(tmp)
    
    concat_df = pd.concat(df_list, axis=0).drop(columns=['Unnamed: 0']).drop_duplicates().reset_index(drop=True)
    concat_df = standardize_nan(concat_df)
    concat_df = concat_df.replace(0, np.nan)
    
    return concat_df