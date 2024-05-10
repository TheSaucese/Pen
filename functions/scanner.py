from collections import deque
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup
from get_ports import get_open_ports
from if_wdpress import check_wordpress
from urllib.parse import urljoin
from Wappalyzer import Wappalyzer, WebPage

def WappAlyze(target_url):
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(target_url)
    return wappalyzer.analyze(webpage)

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

def crawl_website(seed_url, max_pages=10):
    visited_urls = set()
    queue = deque([seed_url])
    crawled_urls = []

    while queue and len(crawled_urls) < max_pages:
        current_url = queue.popleft()
        
        if current_url in visited_urls:
            continue

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                visited_urls.add(current_url)
                crawled_urls.append(current_url)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                base_url = response.url

                for link in soup.find_all('a', href=True):
                    url = link['href']
                    if url and not url.startswith('#'):
                        absolute_url = urljoin(base_url, url)
                        if absolute_url not in visited_urls:
                            queue.append(absolute_url)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {current_url}: {e}")

    return crawled_urls

def scrape_urls(target_url):
    try:
        # Check the robots.txt file
        robots_parser = RobotFileParser()
        robots_parser.set_url(urljoin(target_url, 'robots.txt'))
        robots_parser.read()

        response = requests.get(target_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = response.url

            urls = []
            for link in soup.find_all('a', href=True):
                url = link['href']
                if url and not url.startswith('#'):
                    absolute_url = urljoin(base_url, url)
                    if robots_parser.can_fetch('*', absolute_url):
                        urls.append(absolute_url)

            return urls

        else:
            print(f"Failed to retrieve the target website. Status Code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the website: {e}")
        return []
