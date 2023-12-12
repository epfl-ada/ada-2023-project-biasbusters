import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import numpy as np
import json
import support

def tmdb_api(movie_name):
    query = quote(movie_name)
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YmVjZjA1ODc2NGRlMGNiZWJhYjE2YTYyZjNmZjlkYSIsInN1YiI6IjY1Nzg5YzQ0MjBlY2FmMDEwMGQyOTM4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1kVNP3UXQ9p2h2K1hhwjIQm4CNDjrxMQ5rPoASctTiA"
    }

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    
    return json_data


def get_original_title(movie_name):
    if not movie_name:
        return None
    
    json_data = tmdb_api(movie_name)
    results = json_data.get('results', None)
    
    if results:
        original_title = results[0].get('original_title', None)
        title = results[0].get('title', None)
        similarity = support.normalized_levenshtein(title, movie_name)
        if similarity > 0.8:
            return original_title
        elif movie_name.lower().find(title.lower()) != -1 or title.lower().find(movie_name.lower()) != -1:
            return original_title
    return None


def extract_movie_info(soup):
    try:
        a_tag = soup.find('a', class_='ipc-metadata-list-summary-item__t')
        # Extracting movie ID and title
        href = a_tag['href']
        movie_id = href.split('/?ref')[0].split('/')[-1]
        movie_title = a_tag.text
    except:
        movie_id = None
        movie_title = None
        
    try:
        # Find the <span> tag containing the year
        year_span = soup.find('span', class_='ipc-metadata-list-summary-item__li')
        year = year_span.text if year_span else None
    except:
        year = None

    return movie_id, movie_title, year

def get_best_match(soup, target_name, target_year):
    best_similarity = -float('inf')
    
    best_imdb_id = None
    best_movie_name = None
    best_release_year = None
    
    # Find all list items in the HTML
    list_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')

    for item in list_items[0:5]:
        tv_show_tag = item.find_all('span', class_='ipc-metadata-list-summary-item__li')
        is_tv_show = any("TV Series" in tag.text for tag in tv_show_tag)
        
        if is_tv_show:
            continue
        
        # Extract the movie title
        title_tag = item.find('a', class_='ipc-metadata-list-summary-item__t')
        if title_tag:
            movie_name = title_tag.text.strip()
        else:
            continue
        
        year_tag = item.find('span', class_='ipc-metadata-list-summary-item__li')
        if year_tag:
            release_year = year_tag.text.strip()
        else:
            continue  
        
        try:
            year_distance = abs(int(target_year) - int(release_year)) if release_year and str(release_year).isdigit() and str(target_year).isdigit() else float('inf')
        except ValueError:
            continue
        if year_distance > 3:
            continue
        
        # Compute similarity as a float 
        similarity_threshold = 0.8
        name_similarity = support.normalized_levenshtein(target_name, movie_name)
        
        # Update closest match if a closer match is found
        if name_similarity > similarity_threshold and name_similarity > best_similarity:
            best_similarity = name_similarity
            best_imdb_id = title_tag['href'].split('/?')[0].split('title/')[1]
            best_movie_name = movie_name
            best_release_year = release_year

            if year_distance == 0 or name_similarity == 1.0:
                break
            
        elif year_distance <= 2:
            if movie_name.lower().find(target_name.lower()) != -1 or target_name.lower().find(movie_name.lower()) != -1:
                best_similarity = name_similarity
                best_imdb_id = title_tag['href'].split('/?')[0].split('title/')[1]
                best_movie_name = movie_name
                best_release_year = release_year
                break
            
            original_title = get_original_title(target_name)
            if original_title:
                title_similarity = support.normalized_levenshtein(original_title, movie_name)
                
                if title_similarity > similarity_threshold and title_similarity > best_similarity:
                    best_similarity = title_similarity
                    best_imdb_id = title_tag['href'].split('/?')[0].split('title/')[1]
                    best_movie_name = movie_name
                    best_release_year = release_year

                    if year_distance == 0 or name_similarity == 1.0:
                        break
            
            
    return best_imdb_id, best_movie_name, best_release_year


def retrieve_imdb_key(movie_name, release_year=None):
    has_paranthesis = False
    
    if release_year == np.nan:
        release_year = None
    
    if movie_name.find('(') != -1:
        has_paranthesis = True
        search_term = quote(movie_name.split('(')[0])
    else:    
        search_term = quote(movie_name)
    
    url = f'https://www.imdb.com/find/?q={search_term}'
    print(url)
    
    soup = support.request_soup(url)
    
    if not soup:
        return None
    
    best_match = get_best_match(soup, movie_name, release_year)
    
    if best_match:
        return {'imdb_id': best_match[0],'imdb_name': best_match[1], 'imdb_year': best_match[2], 'movie_name': movie_name, 'release_year': release_year} 
    elif has_paranthesis:
        search_term = quote(movie_name.split('(')[1].replace(')',''))
        url = f'https://www.imdb.com/find/?q={search_term}'
        soup = support.request_soup(url)
        
        if not soup:
            return None
        
        best_match = get_best_match(soup, movie_name, release_year)
        
        if best_match:
            return {'imdb_id': best_match[0],'imdb_name': best_match[1], 'imdb_year': best_match[2], 'movie_name': movie_name, 'release_year': release_year} 

    return None