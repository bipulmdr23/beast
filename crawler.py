import json
import requests
from bs4 import BeautifulSoup

start_url = 'https://stackoverflow.com'

data = []

def crawl(url, depth):
    try:
        print('Crawling url: "%s" at depth: %d' % (url, depth))
        response = requests.get(url)
    except:
        print('failed to perform HTTP GET request on "%s"\n' % url)
        return
    content = BeautifulSoup(response.text, 'lxml')

    title = content.find('title').text
    description = content.get_text()

    if description is None:
        description = ''
    else:
        description = description.strip().replace('\n', ' ')

    result ={
        'url': url,
        'title': title,
        'description': description
    }

    data.append(result)
    #print('\n\nReturn:\n\n', json.dumps(result, indent=2))

    if depth ==0:
        return

    try:
        links = content.find_all('a')
    except:
        return
    
    for link in links:
        try:
            if 'http' not in link['href']:
                follow_url = url + link['href']
            else:
                follow_url = link['href']
            crawl(follow_url, depth - 1)
        except KeyError:
            pass
    
    return

crawl(start_url, 1)
print(len(data))