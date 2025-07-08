#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar.

Key features
────────────
• pulls the latest N papers for each Scholar ID
• avoids duplicates across authors
• safe YAML via PyYAML
• optional 'featured' flag for highly cited papers
• retries with free-proxy rotation; skips author or pub after MAX_RETRIES
• writes content/publication/*.md  and update_log.txt
"""

from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException
import yaml, os, datetime, re, time, traceback
from pathlib import Path

# ─────────────── CONFIG ─────────────── #
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Piotr Zwiernik
    "WgPhMfwAAAAJ",  # Gábor Lugosi
    "uz27G84AAAAJ",  # Gergely Neu
    "w-EcuBUAAAAJ",  # Chiara Amorino
    "1iWGSc0AAAAJ",  # David Rossell
    "2bchLEwAAAAJ",  # Eulàlia Nualart
    "RsbU0icAAAAJ",  # Lorenzo Cappello
]

MAX_PAPERS_PER_AUTHOR = 3
FEATURED_THRESHOLD    = 100   # citations ⇒ featured
MAX_RETRIES           = 3
RETRY_DELAY           = 30    # seconds

HUGO_DIR = Path("content/publication")
# ─────────────────────────────────────── #

HUGO_DIR.mkdir(parents=True, exist_ok=True)

# optional free-proxy rotation
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)

# ───────── helper utilities ────────────
def safe_slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def extract_venue(cit: str | None) -> str:
    return cit.strip() if cit else "Unknown Venue"

def yaml_block(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml_block(meta))
        f.write("---\n")
# ───────────────────────────────────────

log = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]
seen_titles = set()

for sid in SCHOLAR_IDS:
    # ─── fetch author with retries ───
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(sid)
            scholarly.fill(author, sections=["publications"])
            break
        except (MaxTriesExceededException, AttributeError, Exception) as e:
            if attempt == MAX_RETRIES:
                log.append(f"Skip author {sid}: {e}\n")
                author = None
            else:
                time.sleep(RETRY_DELAY)
    if author is None:
        continue

    pubs = sorted(
        author["publications"],
        key=lambda p: p["bib"].get("pub_year", "0"),
        reverse=True,
    )[:MAX_PAPERS_PER_AUTHOR]

    for pub in pubs:
        # ─── fetch publication with retries ───
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                success = True
                break
            except (MaxTriesExceededException, AttributeError, Exception) as e:
                if attempt == MAX_RETRIES:
                    log.append(f"Skip pub ({sid}): {e}\n")
                else:
                    time.sleep(RETRY_DELAY)
        if not success:
            continue

        title = pub["bib"].get("title", "Unknown Title").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        year      = str(pub["bib"].get("pub_year", datetime.datetime.now().year))
        date_iso  = f"{year}-01-01T00:00:00Z"
        authors   = [a.strip() for a in re.split(r",| and ", pub["bib"].get("author", "")) if a.strip()] or ["Unknown Author"]
        venue     = extract_venue(pub["bib"].get("citation", ""))
        doi       = (pub["bib"].get("doi") or "").strip()
        eprint    = (pub["bib"].get("eprint") or "").strip()
        gs_url    = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"
        pub_type  = "preprint" if ("arxiv" in venue.lower() or eprint) else "article-journal"
        pub_url   = f"https://arxiv.org/abs/{eprint}" if (pub_type == "preprint" and eprint) else gs_url
        featured  = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

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
            # blanks to keep Hugo happy
            "abstract": "",
            "summary": "",
            "tags": [],
            "categories": [],
            "projects": [],
        }

        write_md(md_meta, HUGO_DIR / safe_slug(title))
        log.append(f"Added: {title} ({year})\n")

# write log
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log)
print("✅ Publications updated successfully!")