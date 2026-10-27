"""Check the historical emoji table in generated HTML; no third-party modules needed."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

EXAMPLES = [
    (":heart:", "\u2764"),
    (":+1:", "\U0001f44d"),
    (":smile:", "\U0001f604"),
    (":sparkles:", "\u2728"),
    (":tada:", "\U0001f389"),
]


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = self.row = self.cell = None
        self.in_code = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
            self.tables.append(self.table)
        elif self.table is not None:
            if tag == "tr":
                self.row = []
                self.table.append(self.row)
            elif tag in ("td", "th"):
                self.cell = {"text": "", "codes": [], "images": []}
                self.row.append(self.cell)
            elif self.cell is not None:
                if tag == "code":
                    self.in_code = True
                    self.cell["codes"].append("")
                elif tag == "img":
                    self.cell["images"].append(dict(attrs))

    def handle_endtag(self, tag):
        if tag == "table":
            self.table = self.row = self.cell = None
        elif tag in ("td", "th"):
            self.cell = None
        elif tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"] += data
            if self.in_code:
                self.cell["codes"][-1] += data


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(html):
    parser = Tables()
    parser.feed(html)
    matches = [
        table for table in parser.tables
        if table and [cell["text"].strip() for cell in table[0]]
        == ["What you see", "What you type"]
    ]
    require(len(matches) == 1, "Expected exactly one Emoji List table")
    rows = matches[0][1:]
    require(len(rows) == len(EXAMPLES), "Expected all five emoji examples")

    for row, (shortcode, symbol) in zip(rows, EXAMPLES):
        require(len(row) == 2, f"{shortcode}: expected two columns")
        visible, literal = row
        text = visible["text"].strip()
        require(not visible["codes"], f"{shortcode}: rendered example is inside code")
        if visible["images"]:
            require(not text and len(visible["images"]) == 1,
                    f"{shortcode}: expected one emoji image without literal text")
            image = visible["images"][0]
            url = urlsplit(image.get("src", ""))
            require(
                "emoji" in image.get("class", "").split()
                and image.get("alt") in (shortcode, symbol)
                and url.scheme == "https"
                and url.netloc == "github.githubassets.com"
                and url.path.startswith("/images/icons/emoji/"),
                f"{shortcode}: unsupported or incorrectly labelled emoji image",
            )
        else:
            require(text.replace("\ufe0f", "").replace("\ufe0e", "") == symbol,
                    f"{shortcode}: rendered column must contain its emoji symbol")
        require(
            literal["text"].strip() == shortcode
            and literal["codes"] == [shortcode]
            and not literal["images"],
            f"{shortcode}: code example must remain literal",
        )


if __name__ == "__main__":
    try:
        validate(Path(sys.argv[1] if len(sys.argv) > 1 else "_site/index.html")
                 .read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        sys.exit(f"Emoji regression check failed: {error}")
    print("Validated 5 rendered emoji examples and 5 literal code examples")
