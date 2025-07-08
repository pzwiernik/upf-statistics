#!/usr/bin/env python3
"""
Update Hugo Blox publications from Google Scholar.

Improvements:
  • skips duplicates across authors
  • safe YAML via PyYAML
  • retry/back-off for Scholar rate limits
  • optional 'featured' flag if citations ≥ FEATURED_THRESHOLD
"""

from scholarly import scholarly
import yaml, os, datetime, re, time
from pathlib import Path

# ───────────────  CONFIG  ────────────────
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Piotr
    "WgPhMfwAAAAJ",  # Gábor
    "uz27G84AAAAJ",  # Gergő
    "w-EcuBUAAAAJ",  # Chiara
    "1iWGSc0AAAAJ",  # David
    "2bchLEwAAAAJ",  # Eulàlia
    "RsbU0icAAAAJ",  # Lorenzo
]

HUGO_DIR             = Path("content/publication")
MAX_PAPERS_PER_AUTHOR = 3
RETRY_DELAY          = 30      # seconds
FEATURED_THRESHOLD   = 100     # citations ⇒ featured: true
# ─────────────────────────────────────────

HUGO_DIR.mkdir(parents=True, exist_ok=True)
log = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]

def safe_slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def extract_venue(citation: str | None) -> str:
    return citation.strip() if citation else "Unknown Venue"

def yaml_block(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    with path.open("w") as f:
        f.write("---\n")
        f.write(yaml_block(meta))
        f.write("---\n")

seen_titles = set()

for sid in SCHOLAR_IDS:
    try:
        author = scholarly.search_author_id(sid)
        scholarly.fill(author, sections=["publications"])
    except Exception as e:
        log.append(f"Author {sid} failed: {e}\n")
        time.sleep(RETRY_DELAY); continue

    pubs = sorted(
        author["publications"],
        key=lambda p: p["bib"].get("pub_year", "0"), reverse=True
    )[:MAX_PAPERS_PER_AUTHOR]

    for pub in pubs:
        for attempt in (1, 2):
            try:
                scholarly.fill(pub); break
            except Exception as e:
                if attempt == 2:
                    log.append(f"Skip pub: {e}\n"); continue
                time.sleep(RETRY_DELAY)

        title = pub["bib"].get("title", "Unknown Title").strip()
        if title.lower() in seen_titles: continue
        seen_titles.add(title.lower())

        year = str(pub["bib"].get("pub_year", datetime.datetime.now().year))
        date_iso = f"{year}-01-01T00:00:00Z"

        authors_raw = pub["bib"].get("author", "")
        authors = [a.strip() for a in re.split(r",| and ", authors_raw) if a.strip()]

        citation  = pub["bib"].get("citation", "")
        venue     = extract_venue(citation)
        doi       = (pub["bib"].get("doi") or "").strip()
        eprint    = (pub["bib"].get("eprint") or "").strip()
        gs_url    = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"

        if "arxiv" in venue.lower() or eprint:
            pub_type = "preprint"
            pub_url  = f"https://arxiv.org/abs/{eprint}" if eprint else gs_url
        else:
            pub_type = "article-journal"
            pub_url  = gs_url

        featured = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

        meta = {
            "title": title,
            "date": date_iso,
            "publishDate": date_iso,
            "doi": doi,
            "authors": authors or ["Unknown Author"],
            "publication": venue,
            "publication_types": [pub_type],
            "featured": featured,
            "publication_url": pub_url,
            # blanks so Hugo front-matter is valid
            "abstract": "", "summary": "",
            "tags": [], "categories": [], "projects": [],
        }

        write_md(meta, HUGO_DIR / safe_slug(title))
        log.append(f"Added: {title} ({year})\n")

# append log
(HUGO_DIR / "update_log.txt").open("a").writelines(log)
print("✅ Publications updated successfully!")

# After the main loop finishes, prune outdated files
latest_slugs = {safe_slug(t) for t in seen_titles}   # titles we just processed

for md_path in HUGO_DIR.glob("*.md"):
    if md_path.name not in latest_slugs and md_path.name != "update_log.txt":
        md_path.unlink()               # delete the old file
        log.append(f"Removed: {md_path.name}\n")