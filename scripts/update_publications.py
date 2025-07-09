#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar
and keep **only the three most-recent papers per author**.

• Deletes every old *.md in content/publication/ that is
  not re-generated during the current run.
• Limits Scholar requests via `publication_limit=3`
  so the run is fast and friendly.
"""

from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException
from pathlib import Path
import yaml, datetime, re, time, sys

# ─────────── CONFIG ──────────── #
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",   # Piotr Zwiernik
    "WgPhMfwAAAAJ",   # Gábor Lugosi
    "uz27G84AAAAJ",   # Gergely Neu
    "w-EcuBUAAAAJ",   # Chiara Amorino
    "1iWGSc0AAAAJ",   # David Rossell
    "2bchLEwAAAAJ",   # Eulàlia Nualart
    "RsbU0icAAAAJ",   # Lorenzo Cappello
]

MAX_PAPERS       = 3          # newest N per author
FEATURED_CITES   = 100        # citations ⇒ featured
MAX_RETRIES      = 3
RETRY_DELAY_SECS = 30

HUGO_DIR = Path("content/publication")
HUGO_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH  = HUGO_DIR / "update_log.txt"
# ─────────────────────────────── #

# Optional proxy rotation
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)

# ───────── helper utilities ───────── #
def slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def dump_yaml(d: dict) -> str:
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    path.write_text(f"---\n{dump_yaml(meta)}---\n", encoding="utf-8")
# ──────────────────────────────────── #

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
log_lines = [f"\nRun {timestamp}\n"]
seen_titles, keep_files = set(), set()

for sid in SCHOLAR_IDS:
    # ── fetch author (max 3 pubs) ──
    author = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(
                sid,
                filled=False,
                publication_limit=MAX_PAPERS,
            )
            scholarly.fill(
                author,
                sections=["publications"],
                sortby="year",
                publication_limit=MAX_PAPERS,
            )
            break
        except MaxTriesExceededException as e:
            if attempt == MAX_RETRIES:
                log_lines.append(f"⚠️  author {sid}: {e}\n")
            else:
                time.sleep(RETRY_DELAY_SECS)

    pubs = author.get("publications", []) if author else []
    for pub in pubs:                         # already at most 3
        # fill pub details
        ok = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                ok = True
                break
            except MaxTriesExceededException as e:
                if attempt == MAX_RETRIES:
                    log_lines.append(f"⚠️  pub {sid}: {e}\n")
                else:
                    time.sleep(RETRY_DELAY_SECS)
        if not ok:
            continue

        title = pub["bib"].get("title", "Unknown").strip()
        if title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())

        # Year handling
        year = str(pub["bib"].get("pub_year") or datetime.datetime.now().year)
        date_iso = f"{year}-01-01T00:00:00Z"

        authors = [
            a.strip() for a in re.split(r",| and ", pub["bib"].get("author", ""))
            if a.strip()
        ] or ["Unknown Author"]

        venue  = (pub["bib"].get("citation") or "").strip() or "Unknown Venue"
        doi    = (pub["bib"].get("doi") or "").strip()
        eprint = (pub["bib"].get("eprint") or "").strip()
        gs_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"

        is_preprint = "arxiv" in venue.lower() or eprint
        pub_type = "preprint" if is_preprint else "article-journal"
        pub_url  = f"https://arxiv.org/abs/{eprint}" if is_preprint and eprint else gs_url
        featured = pub.get("num_citations", 0) >= FEATURED_CITES

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

        fname = slug(title)
        write_md(meta, HUGO_DIR / fname)
        keep_files.add(fname)
        log_lines.append(f"✅  {title} ({year})\n")

# ────── prune old markdown files ──────
deleted = 0
for path in HUGO_DIR.glob("*.md"):
    if path.name not in keep_files:
        path.unlink()
        deleted += 1

log_lines.append(f"Kept {len(keep_files)} files, deleted {deleted} stray files.\n")
LOG_PATH.open("a", encoding="utf-8").writelines(log_lines)
print("✨ Done.")