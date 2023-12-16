import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import Levenshtein
import json
import support
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from constants import MAX_THREADS

# @Function: Return best match among search results
def get_best_match(soup, target_name, target_year):
    closest_match = None
    best_similarity = -float('inf')
    
    for row in soup.find_all('search-page-media-row'):
        # Extract movie name and release year
        movie_name = row.find('a', {'data-qa': 'info-name'}).get_text().strip()
        release_year = row.get('releaseyear')

        # Calculate absolute year difference
        year_distance = abs(int(target_year) - int(release_year)) if release_year else float('inf')
        
        # Unlikely its the same movie regardless of movie title
        if year_distance > 3:
            continue
        
        # Compute similarity as a float 
        similarity_threshold = 0.8
        name_similarity = support.normalized_levenshtein(target_name, movie_name)
        
        # Update closest match if a closer match is found
        if name_similarity > similarity_threshold and name_similarity > best_similarity:
            best_similarity = name_similarity
            closest_match = row
    
    # If we have found a qualified match, extract its href-value
    if closest_match:
        match_anchor = closest_match.find('a', {'data-qa': 'thumbnail-link'})
        match_url = match_anchor['href'] if match_anchor else None
    else:
        match_url = None
    
    return match_url

# @Function: Extract audience and tomato scores for a movie, given its soup
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

        # Output formatting
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

# @Function: Extract movie performance data (revenue in different markets)
def extract_performance(soup):
    release_info_div = soup.find('div', class_='mojo-performance-summary-table')
    
    if release_info_div:
        release_info = {}
        release_spans = release_info_div.find_all('span', class_='a-size-small')
            
        for span in release_spans:
            try:
                # Extract release type (e.g., "Domestic", "International", "Worldwide")
                release_type = span.get_text(strip=True)
                if release_type.find(' ') != -1:
                    release_type = release_type.split(' ')[0]
                    
                # Extract revenue
                source_span = span.find_next('span', class_='a-size-medium a-text-bold')
                next_span = source_span.find_next('span')
                if next_span.get('class')[0] == 'percent zero':
                    release_info[release_type] = None
                elif next_span.get('class')[0] == 'money':            
                    revenue_text = next_span.get_text(strip=True) if next_span else None
                    revenue = int(revenue_text[1:].replace(',', '')) if revenue_text else None
                    release_info[release_type] = revenue
            except:
                continue
            
        return release_info
    return None

# @Function: Extract general movie info: distributor, domestic opening revenue and budget
def extract_info(soup):
    output = {}
    values = ['Domestic Distributor', 'Domestic Opening', 'Budget']
    
    # Try to extract data for each relevant value
    for keyword in values:
        try:
            tmp_elements = soup.find_all('span', text=keyword)
            for element in tmp_elements:
                # Handle special case: text-value for distributor
                if keyword == 'Domestic Distributor':
                    next_span = element.find_next('span')                    
                    value_text = next_span.get_text(strip=True) if next_span else None
                    index = value_text.find('See full')
                    value_text = value_text[:index].strip()
                    output[keyword] = value_text
                    
                else:
                    value_span = element.find_next('span', class_='money')
                    value_text = value_span.get_text(strip=True) if value_span else None
                    value = int(value_text[1:].replace(',', '')) if value_text else None
                    output[keyword] = value
        except:
            continue
    
    # If dictionary is empty, we rather want to return None
    output = output if output != {} else None
    
    return output

# @Function: Count number of releases movie has undergone
def get_releases(soup):
    try:
        releases_table = soup.find('table', class_='a-bordered a-horizontal-stripes a-size-base-plus')
        rows = len(releases_table.find_all('tr')) - 1
        return rows
    except:
        return None
    
    

# @Function: Retrieves and scrapes relevant rottentomatoes page
def scrape_rottentomatoes_page(imdb_id, movie_name, release_year):
    # Define requests-url and retrieve soup (parsed response)
    search_term = quote(movie_name)
    url = f'https://www.rottentomatoes.com/search?search={search_term}'
    print(url)
    search_soup = support.request_soup(url)
    if not search_soup:
        return None

    # Retrieve best match among search results
    href = get_best_match(search_soup, movie_name, release_year)
    if not href:
        return None
    
    # Request soup for relevant page and extract scores
    page_soup = support.request_soup(href)
    json_data = get_scores(href, page_soup)
    if not json_data:
        return None
    
    # Format output
    movie_details = {'imdb_id': imdb_id,
                     'movie_name': movie_name,
                     'release_year': release_year,
                     }
    movie_details.update(json_data)
    
    return movie_details

# @Function: Scrapes boxofficemojo for budget and revenue-data
def scrape_boxofficemojo_page(imdb_id):
    # Define url and request soup
    url = f'https://www.boxofficemojo.com/title/{imdb_id}/'
    print(url)
    soup = support.request_soup(url)
    if not soup:
        return None
    
    # Extract data from soup
    performance = extract_performance(soup)
    budget = extract_info(soup)
    releases = get_releases(soup)
    
    # Get values for 
    performance_worldwide = performance.get('Worldwide', None) if performance else None
    performance_domestic = performance.get('Domestic', None) if performance else None
    performance_international = performance.get('International', None) if performance else None
    movie_budget = budget.get('Budget', None) if budget else None
    
    # Compute relevant metrics
    roi = float((performance_worldwide - movie_budget) / movie_budget) if performance_worldwide and movie_budget else None
    percentage_domestic = float(performance_domestic / performance_worldwide) if performance_domestic and performance_worldwide else None
    percentage_international = float(performance_international / performance_worldwide) if performance_international and performance_worldwide else None
    
    # Format output
    output = {
        'imdb_id': imdb_id,
        'source_url': url,
        'domestic_distributor': budget.get('Domestic Distributor', None) if budget else None,
        'domestic_opening': budget.get('Domestic Opening', None) if budget else None,
        'budget': movie_budget,
        'releases': releases,
        'performance_domestic': performance_domestic,
        'performance_international': performance_international,
        'performance_worldwide': performance_worldwide,
        'metric_roi': roi,
        'percentage_domestic': percentage_domestic,
        'percentage_international': percentage_international,
    }

    return output


# @Function: Multithreaded execution to reduce runtime
def multithreaded_execution_rottentomatoes(records):
    assert isinstance(records, list) # records must be a list of dictionaries
    assert len(records) > 0 # records cannot be empty
    required_keys = {'imdb_id', 'imdb_name', 'year'}
    assert all(required_keys.issubset(x.keys()) for x in records) # all dictionaries must have appropriate keys
    
    results = []
    failed = 0

    # Performing scraping on MAX_THREADS = 14 workers
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_record = {executor.submit(scrape_rottentomatoes_page, record['imdb_id'], record['imdb_name'], record['year']): record for record in records}

        # When task is completed, append to results. Increment failed if unsuccessfull 
        for future in as_completed(future_to_record):
            result = future.result()
            
            if result is not None:
                results.append(result)
            else:
                failed += 1

    # Creating a new DataFrame from the processed data
    rottentomatoes_df = pd.DataFrame(results)
    
    return rottentomatoes_df

# @Function: Multithreaded execution to reduce runtime
def multithreaded_execution_boxofficemojo(records):
    assert isinstance(records, list) # records must be a list
    assert len(records) > 0 # records cannot be empty
    assert all(isinstance(x,str) for x in records)

    results = []
    failed = 0

    with ThreadPoolExecutor(max_workers=14) as executor:
        future_to_record = {executor.submit(scrape_boxofficemojo_page, record): record for record in records}

        for future in as_completed(future_to_record):
            result = future.result()
            if result is not None:
                results.append(result)
            else:
                failed += 1

    # Creating a new DataFrame from the processed data
    boxofficemojo_df = pd.DataFrame(results)

    return boxofficemojo_df