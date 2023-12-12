import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import Levenshtein
import json
import support


def get_best_match(soup, target_name, target_year):
    closest_match = None
    best_similarity = -float('inf')
    
    for row in soup.find_all('search-page-media-row'):
        # Extract movie name and release year
        movie_name = row.find('a', {'data-qa': 'info-name'}).get_text().strip()
        release_year = row.get('releaseyear')

        # Calculate absolute year difference
        year_distance = abs(int(target_year) - int(release_year)) if release_year else float('inf')
        
        if year_distance > 3:
            continue
        
        # Compute similarity as a float 
        similarity_threshold = 0.8
        name_similarity = support.normalized_levenshtein(target_name, movie_name)
        
        # Update closest match if a closer match is found
        if name_similarity > similarity_threshold and name_similarity > best_similarity:
            best_similarity = name_similarity
            closest_match = row
    
    if closest_match:
        match_anchor = closest_match.find('a', {'data-qa': 'thumbnail-link'})
        match_url = match_anchor['href'] if match_anchor else None
    else:
        match_url = None
    
    return match_url


def get_scores(href,soup):
    try:
        # Find the script tag and parse 
        script_tag = soup.find('script', {'id': 'scoreDetails'})
        json_data = json.loads(script_tag.text)
    except:
        print(f'Could not extract JSON-data for href: {href}')
        return None
    
    scoreboard = json_data.get('scoreboard', None)
    if scoreboard:
        # Extract audience-score details
        audience_score = scoreboard.get('audienceScore', None)
        
        audience_banded_rating_count = audience_score.get('bandedRatingCount', None) if audience_score else None
        audience_liked_count = audience_score.get('likedCount', None) if audience_score else None
        audience_not_liked_count = audience_score.get('notLikedCount', None) if audience_score else None
        audience_rating_count = audience_score.get('ratingCount', None) if audience_score else None
        audience_review_count = audience_score.get('reviewCount', None) if audience_score else None
        audience_avg_rating = audience_score.get('averageRating', None) if audience_score else None
        audience_score_rt = audience_score.get('value', None) if audience_score else None

        # Extract tomato-score details
        tomato_score = scoreboard.get('tomatometerScore', None)
        
        tomato_banded_rating_count = tomato_score.get('bandedRatingCount', None) if tomato_score else None
        tomato_liked_count = tomato_score.get('likedCount', None) if tomato_score else None
        tomato_not_liked_count = tomato_score.get('notLikedCount', None) if tomato_score else None
        tomato_rating_count = tomato_score.get('ratingCount', None) if tomato_score else None
        tomato_review_count = tomato_score.get('reviewCount', None) if tomato_score else None
        tomato_avg_rating = tomato_score.get('averageRating', None) if tomato_score else None
        tomato_score_rt = tomato_score.get('value', None) if tomato_score else None

        scores = {'audience_banded_rating_count': audience_banded_rating_count,
                'audience_rating_count': audience_rating_count,
                'audience_liked_count': audience_liked_count,
                'audience_not_liked_count': audience_not_liked_count,
                'audience_review_count': audience_review_count,
                'audience_avg_rating': audience_avg_rating,
                'audience_score': audience_score_rt,
                'tomato_banded_rating_count': tomato_banded_rating_count,
                'tomato_rating_count': tomato_rating_count,
                'tomato_liked_count': tomato_liked_count,
                'tomato_not_liked_count': tomato_not_liked_count,
                'tomato_review_count': tomato_review_count,
                'tomato_avg_rating': tomato_avg_rating,
                'tomato_score': tomato_score_rt
                }
        
        return scores
    else:
        return None


def scrape_page_rt(imdb_id, movie_name, release_year):
    
    search_term = quote(movie_name)
    url = f'https://www.rottentomatoes.com/search?search={search_term}'
    print(url)
    
    search_soup = support.request_soup(url)
    
    if not search_soup:
        return None

    href = get_best_match(search_soup, movie_name, release_year)
    
    if not href:
        return None
    
    page_soup = support.request_soup(href)
    json_data = get_scores(href, page_soup)
    
    if not json_data:
        return None
    
    movie_details = {'imdb_id': imdb_id,
                     'movie_name': movie_name,
                     'release_year': release_year,
                     }
    movie_details.update(json_data)
    
    return movie_details