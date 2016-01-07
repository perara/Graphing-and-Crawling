from bs4 import BeautifulSoup
import urllib.request
import re
from urllib.parse import urlparse
import validators


def filter_url(url):
    url = url.replace("\n", "")
    url = url.replace(",", "")
    url = url.replace("\\", "")
    return url

def get_html(url):
    try:
        return urllib.request.urlopen(url, timeout=10).read()
    except:
        return None


# Fetch page html
def scrape(data, blacklist=[]):
    url = data['url']
    n = data['n']

    # Add this URL to blacklist
    blacklist.append(url)

    print("b:" + str(len(blacklist)) + " | n:" + str(n) + " | " + url)

    html = get_html(url)

    # If no html was returned, exit without any new hosts
    if html is None:
        return []

    # Get all URLS from HTML document
    query = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(html))

    # Create an list of unique urls
    urls = set()
    for full_url in query:

        # Parse the url, Ignore if malformed!
        try:
            parsed_url = urlparse(full_url)
        except:
            continue

        # Build URL
        new_url = parsed_url.scheme + "://" + parsed_url.netloc
        new_url = filter_url(new_url)

        # Validate URL
        is_valid = validators.url(new_url)

        if new_url == url or new_url in blacklist or not is_valid:
            "Print: " + new_url + " blacklisted!"
            continue

        # Add URL to return queue
        urls.add(new_url)

    return [{
        'url': new_url,
        'n': n + 1
    } for new_url in urls]


