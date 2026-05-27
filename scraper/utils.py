import requests
from urllib.parse import urljoin

try:
    import cloudscraper
except ImportError:
    cloudscraper = None

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.apcfnc.ca/",
    "Connection": "keep-alive",
}


def fetch_html(url):
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
    if response.status_code == 403 and cloudscraper is not None:
        scraper = cloudscraper.create_scraper(
            browser={"custom": DEFAULT_HEADERS},
            delay=1,
        )
        response = scraper.get(url, timeout=20)

    response.raise_for_status()
    return response.text


def normalize_url(base, url):
    return urljoin(base, url.strip())
