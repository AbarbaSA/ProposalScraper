from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

SITE_NAME = "Ulnooweg"
SITE_URL = "https://ulnoowegdevelopmentgroup.ca/entrepreneurship/business-support-services/business-opportunities/"


def _find_rfps_section(soup):
    for heading_text in ["RFPs", "Requests for Proposals / Notices"]:
        heading = soup.find(
            lambda tag: tag.name in ("h1", "h2", "h3")
            and heading_text.lower() in tag.get_text(strip=True).lower()
        )
        if heading:
            section = heading.find_parent("section")
            if section:
                return section
            return heading.parent
    return None


def _is_same_site(url):
    parsed = urlparse(url)
    if not parsed.netloc:
        return True
    return parsed.netloc.endswith("ulnoowegdevelopmentgroup.ca")


def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    candidates = set()
    section = _find_rfps_section(soup)
    if not section:
        section = soup

    for link in section.select("a[href]"):
        href = link.get("href", "").strip()
        if not href:
            continue

        full_url = urljoin(SITE_URL, href)
        if full_url.lower().endswith(".pdf"):
            candidates.add(full_url)
            continue

        if not _is_same_site(full_url):
            continue

        if section is not soup:
            candidates.add(full_url)
            continue

        text = link.get_text(" ", strip=True).lower()
        href_lower = full_url.lower()
        if any(keyword in text for keyword in ["rfp", "request for proposals", "notice", "tender", "proposal"]):
            candidates.add(full_url)
            continue
        if any(keyword in href_lower for keyword in ["rfp", "request-for-proposals", "tender", "proposal", "notice"]):
            candidates.add(full_url)

    return sorted(candidates)
