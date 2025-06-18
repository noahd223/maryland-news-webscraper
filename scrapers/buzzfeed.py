# buzzfeed.py
import re
import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone

#run in terminal 
#python buzzfeed.py



BASE_URL = "https://www.buzzfeed.com"
SOURCE = "BuzzFeed"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/15.1 Safari/605.1.15"
}


def get_article_links() -> list[str]:
    """
    Scrape the BuzzFeed homepage for article URLs.
    We look for hrefs under BASE_URL whose final path segment contains a hyphen.
    """
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # normalize relative URLs
        if href.startswith("/"):
            href = urljoin(BASE_URL, href)
        if not href.startswith(BASE_URL):
            continue

        # strip query‐strings/fragments
        clean = href.split("?")[0].split("#")[0]
        # get last segment
        last_seg = urlparse(clean).path.rstrip("/").split("/")[-1]
        # BuzzFeed slugs always have at least one hyphen
        if "-" in last_seg:
            links.add(clean)

    print(f"[DEBUG] Found {len(links)} potential article link(s)")
    return list(links)


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_article(url: str) -> dict:
    """
    Given an article URL, fetches metadata: source, URL, section, publication date,
    headline, headline length, word count, and scrape date.
    """
    soup = get_soup(url)

    # 1) Section (if available)
    section = None
    meta_section = soup.find("meta", attrs={"property": "article:section"})
    if meta_section and meta_section.get("content"):
        section = meta_section["content"].strip()

    # 2) Publication date
    pub_date = None
    # primary: meta tag
    meta_pub = soup.find("meta", attrs={"property": "article:published_time"})
    if meta_pub and meta_pub.get("content"):
        pub_date = meta_pub["content"].strip()
    else:
        # fallback: JSON-LD script
        ld = soup.find("script", type="application/ld+json")
        if ld and ld.string:
            try:
                import json
                data = json.loads(ld.string)
                # if it's a list, find the first with datePublished
                if isinstance(data, list):
                    for entry in data:
                        if entry.get("datePublished"):
                            pub_date = entry["datePublished"]
                            break
                elif data.get("datePublished"):
                    pub_date = data["datePublished"]
            except Exception:
                pass

    # 3) Headline
    headline = ""
    h1 = soup.find("h1")
    if h1:
        headline = h1.get_text(strip=True)
    headline_len = len(headline.split())

    # 4) Word count
    article_tag = soup.find("article")
    paras = article_tag.find_all("p") if article_tag else soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paras)
    word_count = len(text.split())

    # 5) Scrape date (timezone-aware UTC)
    scrape_date = datetime.now(timezone.utc).isoformat()

    return {
        "source": SOURCE,
        "url": url,
        "section": section,
        "publication_date": pub_date,
        "headline": headline,
        "headline_length": headline_len,
        "word_count": word_count,
        "scrape_date": scrape_date,
    }


if __name__ == "__main__":
    # test: grab up to 5 articles and print only valid ones
    urls = get_article_links()[:10]
    print(f"[DEBUG] URLs to parse ({len(urls)}): {urls}\n")
    for u in urls:
        try:
            info = parse_article(u)
            # filter out non-articles
            if info["headline_length"] == 0 or info["word_count"] == 0:
                print(f"[SKIP] Non-article page: {u}\n")
                continue
            print(info, "\n")
        except Exception as e:
            print(f"Failed to parse {u}: {e}\n")
