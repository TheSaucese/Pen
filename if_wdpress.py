import requests
from bs4 import BeautifulSoup

def check_wordpress(target_url):
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for common WordPress CSS classes or other elements
    if (
        soup.find(class_='wp-block-columns')
        or soup.find(class_='wp-block-group')
        or soup.find(id='wpadminbar')
        or soup.find('meta', attrs={'name': 'generator', 'content': 'WordPress'})
        or 'wp-content' in response.text
    ):
        return True

    return False
