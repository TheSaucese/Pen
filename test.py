#1/ import of libraries---------------
#2/ function needed : a/Web Scraping Functions:url,forms...
#_____________________b/Network Scanning Functions:ports ,proto
#_____________________c/Subdomain Enumeration Functions:
#_____________________d/Function for WordPress Detection:
#_____________________e/function for WordPress Version Detection 
#_____________________f/check subdomain status (200ok or 401 forbiden)
#_____________________g/plugin +version 
#_____________________d/
import requests
from bs4 import BeautifulSoup
import nmap
from if_wdpress import check_wordpress
#from version import get_wordpress_version
from scrabe import scrape_website
#from ip import get_website_info
from get_ports import get_open_ports

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    scrape_website(target_url)
   # ip_address, server = get_website_info(target_url)
    open_ports = get_open_ports(target_url)
    if check_wordpress(target_url):
        print("The website is built with WordPress.")
    else:
        print("The website is not built with WordPress.")

    if open_ports:
        print(f"Open Ports and Services for {target_url}:")
        for port, service in open_ports.items():
           print(f"Port: {port}, Service: {service}")
    else:
        print("No open ports found or unable to retrieve information.")
