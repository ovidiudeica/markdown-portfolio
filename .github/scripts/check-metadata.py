"""Validate the rendered portfolio's social metadata and reject regressions.

No third-party dependencies or external requests; validates only generated HTML.
"""
import argparse
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

SITE = "https://ovidiudeica.github.io/markdown-portfolio"
HOME = SITE + "/"
IMAGE = SITE + "/assets/images/og-preview.png"
DESCRIPTION = (
    "A Markdown learning portfolio built with Jekyll and the Cayman theme on "
    "GitHub Pages. It demonstrates headings, images, links, emoji, lists and "
    "text emphasis."
)
ALT = "Markdown portfolio homepage preview"


class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.in_head = False
        self.tags = defaultdict(list)
        self.raw_tags = defaultdict(list)
        self.canonicals = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        attrs = dict(attrs)
        if tag == "meta":
            name = attrs.get("property") or attrs.get("name")
            if name:
                self.tags[name].append(attrs.get("content", ""))
                self.raw_tags[name].append(self.get_starttag_text())
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append((attrs.get("href", ""), self.get_starttag_text()))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(html):
    head = Head(html)
    require(len(head.canonicals) == 1 and head.canonicals[0][0] == HOME,
            "canonical URL missing, duplicated, or incorrect")
    expected = {
        "description": DESCRIPTION,
        "og:url": HOME,
        "og:site_name": "Welcome to my portfolio!",
        "og:description": DESCRIPTION,
        "og:type": "website",
        "og:image": IMAGE,
        "og:image:width": "1200",
        "og:image:height": "627",
        "og:image:alt": ALT,
    }
    for name, value in expected.items():
        require(head.tags[name] == [value], f"{name}: expected exactly {value!r}")
    require(len(head.tags["og:title"]) == 1 and bool(head.tags["og:title"][0]),
            "og:title missing or duplicated")
    return head


def negative_tests(html):
    head = validate(html)
    image_tag = head.raw_tags["og:image"][0]
    width_tag = head.raw_tags["og:image:width"][0]
    alt_tag = head.raw_tags["og:image:alt"][0]
    canonical_tag = head.canonicals[0][1]
    url_tag = head.raw_tags["og:url"][0]
    mutations = {
        "missing image": html.replace(image_tag, "", 1),
        "wrong image origin": html.replace(image_tag, image_tag.replace(SITE, "https://example.invalid"), 1),
        "missing image baseurl": html.replace(image_tag, image_tag.replace("/markdown-portfolio/", "/"), 1),
        "duplicated image baseurl": html.replace(image_tag, image_tag.replace("/markdown-portfolio/", "/markdown-portfolio/markdown-portfolio/"), 1),
        "wrong width": html.replace(width_tag, width_tag.replace("1200", "600"), 1),
        "wrong image alt": html.replace(alt_tag, alt_tag.replace(ALT, "Incorrect alt"), 1),
        "wrong canonical": html.replace(canonical_tag, canonical_tag.replace(HOME, SITE + "/wrong"), 1),
        "wrong og:url": html.replace(url_tag, url_tag.replace(HOME, SITE + "/wrong"), 1),
        "duplicate image": html.replace("</head>", image_tag + "</head>", 1),
        "duplicate canonical": html.replace("</head>", canonical_tag + "</head>", 1),
        "duplicate og:url": html.replace("</head>", url_tag + "</head>", 1),
    }
    for name, broken in mutations.items():
        require(broken != html, f"negative fixture unchanged: {name}")
        try:
            validate(broken)
        except ValueError:
            continue
        raise ValueError(f"negative regression not detected: {name}")
    return len(mutations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", nargs="?", default="_site/index.html")
    parser.add_argument("--negative-tests", action="store_true")
    args = parser.parse_args()
    html = Path(args.html).read_text(encoding="utf-8")
    validate(html)
    print("PASS: canonical, Open Graph, image details and description")
    if args.negative_tests:
        print(f"PASS: {negative_tests(html)} negative metadata regression cases rejected")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Portfolio metadata regression failed: {exc}")
