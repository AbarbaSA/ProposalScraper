from bs4 import BeautifulSoup
from urllib.parse import urljoin

SITE_NAME = "APCFNC"
SITE_URL = "https://www.apcfnc.ca/news/"


def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    candidates = set()

    for link in soup.select('a[href*="request-for-proposals"]'):
        href = link.get("href", "").strip()
        if not href:
            continue
        candidates.add(urljoin(SITE_URL, href))

    return sorted(candidates)
