#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar.

Key points
──────────
• Fetches up to FETCH_LIMIT=10 pubs per author, then keeps the 3 newest
• Custom date key handles arXiv IDs (YYMM) when Scholar omits pub_year
• Robust retries + proxy + safe YAML
• Adds/overwrites Markdown files, avoids duplicates across authors
"""

from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException
import yaml, datetime, re, time
from pathlib import Path

# ───────── CONFIG ───────── #
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",   # Piotr Zwiernik
    "WgPhMfwAAAAJ",   # Gábor Lugosi
    "uz27G84AAAAJ",   # Gergely Neu
    "w-EcuBUAAAAJ",   # Chiara Amorino
    "1iWGSc0AAAAJ",   # David Rossell
    "2bchLEwAAAAJ",   # Eulàlia Nualart
    "RsbU0icAAAAJ",   # Lorenzo Cappello
]

FETCH_LIMIT            = 10   # pull this many, then pick freshest 3
MAX_PAPERS_PER_AUTHOR   = 3   # final number to keep
FEATURED_THRESHOLD      = 100 # citations ⇒ featured
MAX_RETRIES             = 3
RETRY_DELAY             = 30  # seconds

HUGO_DIR = Path("content/publication")
HUGO_DIR.mkdir(parents=True, exist_ok=True)
# ────────────────────────── #

# try free proxy list
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)

# ───── helper utils ─────
def safe_slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def yaml_dump(obj: dict) -> str:
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    path.write_text(f"---\n{yaml_dump(meta)}---\n", encoding="utf-8")

def best_date(pub: dict) -> tuple[int, int]:
    """Return (year, month) for robust sorting."""
    year = pub["bib"].get("pub_year")
    if year and str(year).isdigit():
        return (int(year), 0)

    eprint = (pub["bib"].get("eprint") or "").strip()

    # modern arXiv YYMM.xxxxx
    m = re.match(r"(\d{2})(\d{2})\.\d{4,5}", eprint)
    if m:
        y, mth = m.groups()
        return (2000 + int(y), int(mth))

    # legacy format math/0501234                      → 2005
    m = re.match(r".*/(\d{2})\d{4}", eprint)
    if m:
        return (2000 + int(m.group(1)), 0)

    # fallback very old
    return (1900, 0)
# ─────────────────────────

log_lines   = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]
seen_titles = set()

for sid in SCHOLAR_IDS:

    # ── fetch author list (limited) ──
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(
                sid,
                filled=False,
                publication_limit=FETCH_LIMIT
            )
            scholarly.fill(
                author,
                sections=["publications"],
                publication_limit=FETCH_LIMIT
            )
            break
        except (MaxTriesExceededException, Exception) as e:
            if attempt == MAX_RETRIES:
                log_lines.append(f"Skip author {sid}: {e}\n")
            else:
                time.sleep(RETRY_DELAY)

    if not author or "publications" not in author:
        log_lines.append(f"Skip author {sid}: no publications key\n")
        continue

    # sort locally and keep newest three
    pubs = sorted(
        author["publications"],
        key=best_date,
        reverse=True
    )[:MAX_PAPERS_PER_AUTHOR]

    for pub in pubs:

        # ── fetch pub details ──
        fetched = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)   # full metadata
                fetched = True
                break
            except (MaxTriesExceededException, Exception) as e:
                if attempt == MAX_RETRIES:
                    log_lines.append(f"Skip pub ({sid}): {e}\n")
                else:
                    time.sleep(RETRY_DELAY)
        if not fetched:
            continue

        title = pub["bib"].get("title", "Unknown").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        # derive fields
        y, mth = best_date(pub)
        date_iso = f"{y}-01-01T00:00:00Z"
        authors = [a.strip() for a in re.split(r",| and ", pub["bib"].get("author", "")) if a.strip()] or ["Unknown Author"]
        venue   = (pub["bib"].get("citation") or "").strip() or "Unknown Venue"
        doi     = (pub["bib"].get("doi") or "").strip()
        eprint  = (pub["bib"].get("eprint") or "").strip()
        gs_url  = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"
        is_pre  = "arxiv" in venue.lower() or eprint
        pub_url = f"https://arxiv.org/abs/{eprint}" if is_pre and eprint else gs_url
        pub_type = "preprint" if is_pre else "article-journal"
        featured = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

        meta = {
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

        write_md(meta, HUGO_DIR / safe_slug(title))
        log_lines.append(f"Added: {title} ({y})\n")

# append log
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log_lines)
print("✅ Publications updated successfully!")