import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           'Content-Type': 'text/html; charset=UTF-8'}

parser = 'html.parser'

def extract_movie_info(soup):
    try:
        a_tag = soup.find('a', class_='ipc-metadata-list-summary-item__t')
    
        # Extracting movie ID and title
        href = a_tag['href']
        print(href)
        #movie_id = re.search(r'/title/(tt\d+)/', href).group(1)
        movie_id = href.split('/?ref')[0].split('/')[-1]
        
        print(movie_id)
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


def retrieve_imdb_key(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except:
        print(f'Error occured while scraping {url}')
        return None
    
    soup = BeautifulSoup(response.text, parser)
    
    movie_id, movie_title, year = extract_movie_info(soup)
    
    return {'imdb_id': movie_id, 'imdb_name': movie_title, 'year': year}


urls = ['https://www.imdb.com/find/?q=Philomena', 'https://www.imdb.com/find/?q=Billy%20Budd']

for u in urls:
    print(retrieve_imdb_key(u))