# scanner.py

import requests
from bs4 import BeautifulSoup
from get_ports import get_open_ports
from if_wdpress import check_wordpress

def is_wordpress(target_url):
    if check_wordpress(target_url):
        return "The website is built with WordPress."
    else:
        return "The website is not built with WordPress."

def open_ports(target_url):
    open_ports_result = ""
    num_open_ports = 0

    open_ports = get_open_ports(target_url)
    if open_ports:
        open_ports_result += f"Open Ports and Services for {target_url}:\n"
        for port, service in open_ports.items():
            open_ports_result += f"Port: {port}, Service: {service}\n"
        num_open_ports = len(open_ports)
    else:
        open_ports_result += "No open ports found or unable to retrieve information.\n"

    return open_ports_result, num_open_ports

def scrape_urls(target_url):
        try:
            # Send an HTTP GET request to the target URL
            response = requests.get(target_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all the URLs in the website
                urls = []
                for link in soup.find_all('a', href=True):
                    url = link['href']
                    if url and not url.startswith('#'):
                        urls.append(url)

                return urls

            else:
                print(f"Failed to retrieve the target website. Status Code: {response.status_code}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the website: {e}")
            return []

