import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

url = 'https://devfolio.co/hackathons'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    results = []
    for link in links:
        href = link.get('href')
        text = link.text.strip()
        
        # Use urljoin to get the absolute URL
        absolute_url = urljoin(url, href)
        
        # Check if the link is external
        external_link = 'TRUE' if urlparse(absolute_url).hostname != urlparse(url).hostname else 'FALSE'

        if text and external_link == 'TRUE':
            results.append(absolute_url)
    results = results[:-3]
    print(results)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
