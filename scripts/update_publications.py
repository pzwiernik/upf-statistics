#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar.

• Fetch up to FETCH_LIMIT per author, keep newest MAX_PAPERS_PER_AUTHOR
• Robust date sort (handles arXiv YYMM) to decide “newest”
• Writes Markdown tagged with  source: scholar
• Deletes any previously generated file not rewritten this run
• Duplicate guard: first DOI, else arXiv ID, else canonical title
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

FETCH_LIMIT            = 10   # pull this many, then choose newest 3
MAX_PAPERS_PER_AUTHOR   = 3
FEATURED_THRESHOLD      = 100
MAX_RETRIES             = 3
RETRY_DELAY             = 30  # seconds

TAG_FIELD = "source"
TAG_VALUE = "scholar"

HUGO_DIR = Path("content/publication")
HUGO_DIR.mkdir(parents=True, exist_ok=True)
# ────────────────────────── #

# optional free-proxy rotation
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
    """Return (year, month) for reliable sorting newest→oldest."""
    year = pub["bib"].get("pub_year")
    if year and str(year).isdigit():
        return (int(year), 0)

    eprint = (pub["bib"].get("eprint") or "").strip()
    m = re.match(r"(\d{2})(\d{2})\.\d{4,5}", eprint)   # 2309.xxxxx
    if m:
        y, mo = m.groups()
        return (2000 + int(y), int(mo))
    m = re.match(r".*/(\d{2})\d{4}", eprint)           # math/0501234
    if m:
        return (2000 + int(m.group(1)), 0)

    return (1900, 0)

def dedup_key(pub: dict, title: str) -> str:
    """Key that is identical for duplicate records."""
    doi    = (pub["bib"].get("doi") or "").lower().strip()
    if doi:
        return "doi:" + doi
    eprint = (pub["bib"].get("eprint") or "").lower().strip()
    if eprint:
        return "eprint:" + eprint
    canon = re.sub(r"[^a-z0-9]+", "", title.lower())
    return "title:" + canon
# ─────────────────────────

log_lines  = [f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n"]
seen_keys  = set()
new_files  = set()   # filenames generated this run

for sid in SCHOLAR_IDS:

    # fetch author (limited)
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(
                sid, filled=False, publication_limit=FETCH_LIMIT
            )
            scholarly.fill(
                author,
                sections=["publications"],
                publication_limit=FETCH_LIMIT,
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

    pubs = sorted(author["publications"], key=best_date, reverse=True) \
           [:MAX_PAPERS_PER_AUTHOR]

    for pub in pubs:
        # fill pub details
        ok = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                ok = True
                break
            except (MaxTriesExceededException, Exception) as e:
                if attempt == MAX_RETRIES:
                    log_lines.append(f"Skip pub ({sid}): {e}\n")
                else:
                    time.sleep(RETRY_DELAY)
        if not ok:
            continue

        title = pub["bib"].get("title", "Unknown").strip()
        key   = dedup_key(pub, title)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        year, _   = best_date(pub)
        date_iso  = f"{year}-01-01T00:00:00Z"
        authors   = [a.strip() for a in re.split(r",| and ", pub["bib"].get("author", "")) if a.strip()] or ["Unknown Author"]
        venue     = (pub["bib"].get("citation") or "").strip() or "Unknown Venue"
        doi       = (pub["bib"].get("doi") or "").strip()
        eprint    = (pub["bib"].get("eprint") or "").strip()
        gs_url    = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"
        is_pre    = "arxiv" in venue.lower() or eprint
        pub_url   = f"https://arxiv.org/abs/{eprint}" if is_pre and eprint else gs_url
        pub_type  = "preprint" if is_pre else "article-journal"
        featured  = pub.get("num_citations", 0) >= FEATURED_THRESHOLD

        meta = {
            TAG_FIELD: TAG_VALUE,
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

        fname = safe_slug(title)
        write_md(meta, HUGO_DIR / fname)
        new_files.add(fname)
        log_lines.append(f"Added: {title} ({year})\n")

# ─── prune stale files ───
for md_path in HUGO_DIR.glob("*.md"):
    if md_path.name in new_files:
        continue
    head = md_path.read_text(encoding="utf-8").splitlines()[:15]
    if any(f"{TAG_FIELD}: {TAG_VALUE}" in line for line in head):
        md_path.unlink()
        log_lines.append(f"Removed old: {md_path.name}\n")

# append log
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log_lines)
print("✅ Publications updated successfully!")