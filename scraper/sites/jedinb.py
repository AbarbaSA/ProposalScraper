from bs4 import BeautifulSoup
from urllib.parse import urljoin

SITE_NAME = "JEDINB"
SITE_URL = "https://jedinb.ca/rfp"


def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    candidates = set()

    for link in soup.select('a[href]'):
        href = link.get("href", "").strip()
        if not href:
            continue
        if href.lower().endswith(".pdf"):
            candidates.add(urljoin(SITE_URL, href))
            continue
        text = link.get_text(strip=True).lower()
        if text == "click here":
            candidates.add(urljoin(SITE_URL, href))
            continue
        if href.startswith("/s/"):
            candidates.add(urljoin(SITE_URL, href))

    return sorted(candidates)
