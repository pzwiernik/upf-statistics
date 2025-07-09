#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from Google Scholar (fast version).
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
MAX_PAPERS   = 3       # keep newest N per author
FEATURED_CIT = 100     # citations ≥ X ⇒ featured
MAX_RETRIES  = 3
DELAY        = 30      # s between retries
HUGO_DIR     = Path("content/publication")
# ────────────────────────── #

HUGO_DIR.mkdir(parents=True, exist_ok=True)

pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)

# ───────── helpers ─────────
def safe_slug(title: str) -> str:
    return re.sub(r"[^\w\-]+", "_", title.lower()).strip("_") + ".md"

def arxiv_date(eprint: str, year_fallback: str) -> str:
    """
    Convert YYMM.xxxxx → YYYY-MM-01 ISO date. If parsing fails,
    fall back to YYYY-01-01.
    """
    m = re.match(r"^(\d{2})(\d{2})\.\d{4,5}$", eprint)
    if m:
        yy, mm = m.groups()
        yyyy   = f"20{yy}"
        return f"{yyyy}-{mm}-01T00:00:00Z"
    return f"{year_fallback}-01-01T00:00:00Z"

def dump_yaml(d: dict) -> str:
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, path: Path) -> None:
    path.write_text(f"---\n{dump_yaml(meta)}---\n", encoding="utf-8")
# ──────────────────────────

log, seen = [], set()
log.append(f"Update run on {datetime.datetime.now():%Y-%m-%d %H:%M}\n")

# clean out old .md files first − ensures max-N guarantee
for old in HUGO_DIR.glob("*.md"):
    old.unlink()

for sid in SCHOLAR_IDS:

    # fetch author with built-in pub limit
    author = None
    for a in range(1, MAX_RETRIES + 1):
        try:
            author = scholarly.search_author_id(
                sid,
                filled=False,
                publication_limit=MAX_PAPERS
            )
            scholarly.fill(
                author,
                sections=["publications"],
                sortby="year",          # <<<< valid option
                publication_limit=MAX_PAPERS,
            )
            break
        except MaxTriesExceededException as e:
            if a == MAX_RETRIES:
                log.append(f"Skip author {sid}: {e}\n")
            else:
                time.sleep(DELAY)
    if not author or "publications" not in author:
        continue

    for pub in author["publications"]:
        # retry on each pub
        ok = False
        for a in range(1, MAX_RETRIES + 1):
            try:
                scholarly.fill(pub)
                ok = True
                break
            except MaxTriesExceededException as e:
                if a == MAX_RETRIES:
                    log.append(f"Skip pub ({sid}): {e}\n")
                else:
                    time.sleep(DELAY)
        if not ok:
            continue

        title = pub["bib"].get("title", "Unknown").strip()
        if title.lower() in seen:
            continue
        seen.add(title.lower())

        year    = str(pub["bib"].get("pub_year", datetime.datetime.now().year))
        eprint  = (pub["bib"].get("eprint") or "").strip()
        date_iso = arxiv_date(eprint, year) if eprint else f"{year}-01-01T00:00:00Z"

        authors = [a.strip() for a in re.split(r",| and ", pub["bib"].get("author","")) if a.strip()] or ["Unknown Author"]
        venue   = (pub["bib"].get("citation") or "").strip() or "Unknown Venue"
        doi     = (pub["bib"].get("doi") or "").strip()
        gs_url  = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={title.replace(' ', '+')}"

        is_pp   = "arxiv" in venue.lower() or eprint
        pub_type= "preprint" if is_pp else "article-journal"
        url     = f"https://arxiv.org/abs/{eprint}" if is_pp and eprint else gs_url
        featured= pub.get("num_citations", 0) >= FEATURED_CIT

        meta = {
            "title":             title,
            "date":              date_iso,
            "publishDate":       date_iso,
            "doi":               doi,
            "authors":           authors,
            "publication":       venue,
            "publication_types": [pub_type],
            "featured":          featured,
            "publication_url":   url,
            "abstract":          "",
            "summary":           "",
            "tags":              [],
            "categories":        [],
            "projects":          [],
        }

        write_md(meta, HUGO_DIR / safe_slug(title))
        log.append(f"Added: {title} ({date_iso[:10]})\n")

(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log)
print("✅ Publications updated successfully!")