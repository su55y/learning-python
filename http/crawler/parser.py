from html.parser import HTMLParser
from typing import Set
import urllib.parse as urlparse


class UrlParser(HTMLParser):
    def __init__(self, base: str, allowed_domains: Set[str]):
        super().__init__()
        self.allowed_domains = allowed_domains
        self.base = base
        self.found_links = set()

    def handle_starttag(self, tag: str, attrs):
        if tag != "a":
            return

        for attr, url in attrs:
            if attr != "href" or not url or url == "#":
                continue

            url = urlparse.urljoin(self.base, url)
            url, *_ = urlparse.urldefrag(url)
            parsed = urlparse.urlparse(url)
            if parsed.scheme not in ["http", "https"]:
                continue
            if parsed.netloc not in self.allowed_domains:
                continue

            self.found_links.add(url)
