import requests
from bs4 import BeautifulSoup

def scrape_website(target_url):
    # Send an HTTP GET request to the target URL
    response = requests.get(target_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and print all the URLs in the website
        print("URLs:")
        for link in soup.find_all('a'):
            url = link.get('href')
            if url and not url.startswith('#'):
                print(url)

        # Find and print all the forms in the website
        print("\nForms:")
        for form in soup.find_all('form'):
            print(form)

    else:
        print(f"Failed to retrieve the target website. Status Code: {response.status_code}")