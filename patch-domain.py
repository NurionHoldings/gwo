#!/usr/bin/env python3
"""Inject production domain meta tags and footer website link."""

from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://www.globalworkforceoperations.com"

META_BLOCK = """  <link rel="canonical" href="{url}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Global Workforce Operations" />
  <meta property="og:type" content="website" />
"""

WEBSITE_LINE = (
    '웹사이트 <a href="https://www.globalworkforceoperations.com" '
    'rel="noopener">www.globalworkforceoperations.com</a><br>'
)


def page_url(path: Path) -> str:
    if path.name == "index.html":
        return f"{SITE}/"
    return f"{SITE}/{path.name}"


def patch_head(text: str, url: str) -> str:
    if 'rel="canonical"' in text:
        return text
    block = META_BLOCK.format(url=url)
    return text.replace(
        '  <link rel="stylesheet" href="assets/site.css" />',
        block + '  <link rel="stylesheet" href="assets/site.css" />',
        1,
    )


def patch_footer(text: str) -> str:
    text = text.replace(
        'W. <a href="https://www.globalworkforceoperations.com" '
        'rel="noopener">www.globalworkforceoperations.com</a><br>',
        WEBSITE_LINE,
    )
    if "globalworkforceoperations.com" in text:
        return text
    return text.replace(
        'T. <a href="tel:01065009495">010-6500-9495</a><br><br>',
        'T. <a href="tel:01065009495">010-6500-9495</a><br>' + WEBSITE_LINE + "<br>",
    )


def main():
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = patch_head(patch_footer(text), page_url(path))
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)

    robots = ROOT / "robots.txt"
    robots.write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://www.globalworkforceoperations.com/sitemap.xml\n",
        encoding="utf-8",
    )
    print("wrote robots.txt")


if __name__ == "__main__":
    main()
