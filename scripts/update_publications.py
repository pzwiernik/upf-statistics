#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar (fast version).

Changes vs. previous script
───────────────────────────
• Pass `publication_limit` to scholarly → Google returns only the newest N pubs
• Keeps retry / proxy / robust error handling
• Removes the later Python slice (already limited at source)

Author: GitHub Actions bot
"""

from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException
import yaml, datetime, re, time
from pathlib import Path

# ─────────── CONFIG ─────────── #
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",   # Piotr Zwiernik
    "WgPhMfwAAAAJ",   # Gábor Lugosi
    "uz27G84AAAAJ",   # Gergely Neu
    "w-EcuBUAAAAJ",   # Chiara Amorino
    "1iWGSc0AAAAJ",   # David Rossell
    "2bchLEwAAAAJ",   # Eulàlia Nualart
    "RsbU0icAAAAJ",   # Lorenzo Cappello
]

MAX_PAPERS_PER_AUTHOR = 3      # pull only N newest pubs
FEATURED_THRESHOLD    = 100    # citations ≥ X ⇒ featured: true
MAX_RETRIES           = 3
RETRY_DELAY           = 30     # seconds

HUGO_DIR = Path("content/publication")
HUGO_DIR.mkdir(parents=True, exist_ok=True)
# ────────────────────────────── #

# optional free-proxy rotation
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)

# ────── helpers ──────
def safe_slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def yaml_dump(d: dict) -> str:   # pretty YAML
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    path.write_text(f"---\n{yaml_dump(meta)}---\n", encoding="utf-8")
# ─────────────────────

log = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]
seen_titles = set()

for sid in SCHOLAR_IDS:

    # ── fetch author (limit pubs at source) ──
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(
                sid,
                filled=False,
                publication_limit=MAX_PAPERS_PER_AUTHOR
            )
            scholarly.fill(
                author,
                sections=["publications"],
                sortby="pub_year",
                publication_limit=MAX_PAPERS_PER_AUTHOR
            )
            break
        except (MaxTriesExceededException, Exception) as e:
            if attempt == MAX_RETRIES:
                log.append(f"Skip author {sid}: {e}\n")
            else:
                time.sleep(RETRY_DELAY)
    if author is None:
        continue

    for pub in author["publications"]:

        # ── fetch pub details with retries ──
        fetched = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                fetched = True
                break
            except (MaxTriesExceededException, Exception) as e:
                if attempt == MAX_RETRIES:
                    log.append(f"Skip pub ({sid}): {e}\n")
                else:
                    time.sleep(RETRY_DELAY)
        if not fetched:
            continue

        title = pub["bib"].get("title", "Unknown").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        year   = str(pub["bib"].get("pub_year", datetime.datetime.now().year))
        date   = f"{year}-01-01T00:00:00Z"
        authors = [a.strip() for a in re.split(r",| and ", pub["bib"].get("author", "")) if a.strip()] or ["Unknown Author"]

        venue  = (pub["bib"].get("citation") or "").strip() or "Unknown Venue"
        doi    = (pub["bib"].get("doi") or "").strip()
        eprint = (pub["bib"].get("eprint") or "").strip()
        gs_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"

        is_preprint = "arxiv" in venue.lower() or eprint
        pub_type = "preprint" if is_preprint else "article-journal"
        pub_url  = f"https://arxiv.org/abs/{eprint}" if is_preprint and eprint else gs_url
        featured = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

        meta = {
            "title": title,
            "date": date,
            "publishDate": date,
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

        write_md(meta, HUGO_DIR / safe_slug(title))
        log.append(f"Added: {title} ({year})\n")

# write log file
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log)
print("✅ Publications updated successfully!")