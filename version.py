import requests

def get_wordpress_version(target_url):
    readme_url = target_url + '/readme.html'
    response = requests.get(readme_url)

    if response.status_code == 200:
        version_start = response.text.find('<h1>Version ') + len('<h1>Version ')
        version_end = response.text.find('</h1>', version_start)
        return response.text[version_start:version_end]
    else:
        return "Version information not found."
