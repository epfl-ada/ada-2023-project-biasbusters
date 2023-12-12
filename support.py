import requests
from bs4 import BeautifulSoup
from constants import HEADERS, TIMEOUT, PARSER
import Levenshtein

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