#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar.

Features
────────────────────────────────────────────────────────
• pulls the latest N papers for each Scholar ID
• avoids duplicates across authors
• safe YAML via PyYAML (no quoting headaches)
• flag papers as `featured` if they reach a citation threshold
• retries with free proxy rotation; skips author after MAX_RETRIES
• writes/update_log.txt   (append-only)

Author: GitHub Actions bot
"""

from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException
import yaml, os, datetime, re, time
from pathlib import Path

# ─────────────── CONFIG ──────────────── #
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Piotr Zwiernik
    "WgPhMfwAAAAJ",  # Gábor Lugosi
    "uz27G84AAAAJ",  # Gergely Neu
    "w-EcuBUAAAAJ",  # Chiara Amorino
    "1iWGSc0AAAAJ",  # David Rossell
    "2bchLEwAAAAJ",  # Eulàlia Nualart
    "RsbU0icAAAAJ",  # Lorenzo Cappello
]

MAX_PAPERS_PER_AUTHOR = 5      # newest N papers per scholar
FEATURED_THRESHOLD     = 100   # citations ≥ X ⇒ featured: true

MAX_RETRIES  = 3               # scholar retries per author
RETRY_DELAY  = 30              # seconds to wait between retries

HUGO_DIR = Path("content/publication")
# ───────────────────────────────────────── #

HUGO_DIR.mkdir(parents=True, exist_ok=True)

# ───── optional: free proxy rotation ───── #
pg = ProxyGenerator()
if pg.FreeProxies():           # returns True if proxy list fetched successfully
    scholarly.use_proxy(pg)
# ───────────────────────────────────────── #

def safe_slug(title: str) -> str:
    """Convert title to a safe filename."""
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def extract_venue(citation: str | None) -> str:
    return citation.strip() if citation else "Unknown Venue"

def yaml_block(data: dict) -> str:
    """Safe YAML dump without key sorting (PyYAML)."""
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml_block(meta))
        f.write("---\n")

log_lines = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]
seen_titles = set()

for sid in SCHOLAR_IDS:
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(sid)
            scholarly.fill(author, sections=["publications"])
            break  # success
        except MaxTriesExceededException as e:
            if attempt == MAX_RETRIES:
                log_lines.append(f"Skip author {sid}: {e}\n")
            else:
                time.sleep(RETRY_DELAY)
    if author is None:
        continue  # move to next scholar ID

    pubs = sorted(
        author["publications"],
        key=lambda p: p["bib"].get("pub_year", "0"), reverse=True
    )[:MAX_PAPERS_PER_AUTHOR]

    for pub in pubs:
        # retry fill on each pub
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                break
            except MaxTriesExceededException as e:
                if attempt == MAX_RETRIES:
                    log_lines.append(f"Skip pub ({sid}): {e}\n")
                    pub = None
                else:
                    time.sleep(RETRY_DELAY)
        if pub is None:
            continue

        title = pub["bib"].get("title", "Unknown Title").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        year = str(pub["bib"].get("pub_year", datetime.datetime.now().year))
        date_iso = f"{year}-01-01T00:00:00Z"

        # authors list
        authors_raw = pub["bib"].get("author", "")
        authors = [a.strip() for a in re.split(r",| and ", authors_raw) if a.strip()] or ["Unknown Author"]

        citation = pub["bib"].get("citation", "")
        venue = extract_venue(citation)
        doi = (pub["bib"].get("doi") or "").strip()
        eprint = (pub["bib"].get("eprint") or "").strip()
        gs_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"

        if "arxiv" in venue.lower() or eprint:
            pub_type = "preprint"
            pub_url  = f"https://arxiv.org/abs/{eprint}" if eprint else gs_url
        else:
            pub_type = "article-journal"
            pub_url  = gs_url

        featured = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

        md_meta = {
            "title": title,
            "date": date_iso,
            "publishDate": date_iso,
            "doi": doi,
            "authors": authors,
            "publication": venue,
            "publication_types": [pub_type],
            "featured": featured,
            "publication_url": pub_url,
            "abstract": "",
            "summary": "",
            "tags": [],
            "categories": [],
            "projects": [],
        }

        write_md(md_meta, HUGO_DIR / safe_slug(title))
        log_lines.append(f"Added: {title} ({year})\n")

# append/update log
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log_lines)
print("✅ Publications updated successfully!")