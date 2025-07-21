#!/usr/bin/env python3
"""
Update Hugo-Blox publication pages from arXiv.

• Pulls newest N papers for each author query below
• Writes files to  content/publication/_arxiv/
• Deletes *all* files in that folder on every run so only
  the latest arXiv papers remain.  Your hand-written
  publications elsewhere are left untouched.

Requires:  pip install arxiv PyYAML
"""

from pathlib import Path
import datetime, re, shutil, yaml, arxiv

# ────────── CONFIG ────────── #
ARXIV_QUERIES = {                     # anything valid in the arXiv API
    "Piotr Zwiernik":    'au:"Piotr Zwiernik"',
    "Gábor Lugosi":      'au:"Gabor Lugosi"',
    "Gergely Neu":       'au:"Gergely Neu"',
    "Chiara Amorino":    'au:"Chiara Amorino"',
    "David Rossell":     'au:"David Rossell"',
    "Eulàlia Nualart":   'au:"Eulalia Nualart"',
    "Lorenzo Cappello":  'au:"Lorenzo Cappello"',
}

MAX_PAPERS_PER_AUTHOR = 3   # newest N per author
HUGO_DIR = Path("content/publication/_arxiv")
# ─────────────────────────── #

def safe_slug(title: str) -> str:
    slug = re.sub(r"[^\w\-]+", "_", title.lower()).strip("_")
    return f"{slug[:80]}.md"   # keep filenames reasonable

def yaml_block(d: dict) -> str:
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True)

def write_md(meta: dict, md_path: Path) -> None:
    md_path.write_text(f"---\n{yaml_block(meta)}---\n", encoding="utf-8")

### 1. Wipe & recreate target folder ###
if HUGO_DIR.exists():
    shutil.rmtree(HUGO_DIR)
HUGO_DIR.mkdir(parents=True, exist_ok=True)

log = [f"arXiv update run {datetime.datetime.utcnow():%Y-%m-%d %H:%M} UTC\n"]

### 2. Query arXiv and write Markdown ###
seen = set()
for name, query in ARXIV_QUERIES.items():
    search = arxiv.Search(
        query=query,
        max_results=MAX_PAPERS_PER_AUTHOR,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    for result in search.results():
        title = result.title.strip().replace("\n", " ")
        if title.lower() in seen:
            continue
        seen.add(title.lower())

        date_iso = result.published.strftime("%Y-%m-%dT%H:%M:%SZ")
        authors  = [a.name for a in result.authors] or ["Unknown Author"]
        doi      = result.doi or ""
        venue    = result.journal_ref or "arXiv"
        pdf_url  = result.pdf_url
        abs_url  = result.entry_id    # canonical https://arxiv.org/abs/...

        meta = {
            "title": title,
            "date": date_iso,
            "publishDate": date_iso,
            "doi": doi,
            "authors": authors,
            "publication": venue,
            "publication_types": ["preprint"],
            "featured": False,
            "publication_url": abs_url,
            "url_pdf": pdf_url,
            "generated": "arxiv",      # ← tag so you know it’s auto-created
            # empty fields for Hugo-Blox
            "abstract": "",
            "summary": "",
            "tags": [],
            "categories": [],
            "projects": [],
        }

        write_md(meta, HUGO_DIR / safe_slug(title))
        log.append(f"Added: {title} ({date_iso[:4]})\n")

### 3. Append to (or create) update_log ###
(HUGO_DIR / "update_log.txt").open("a", encoding="utf-8").writelines(log)
print("✅ arXiv publications updated.")