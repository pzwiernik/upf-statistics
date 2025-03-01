from scholarly import scholarly
import os
import datetime
import re
import time

# List of Google Scholar profile IDs to scrape
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Replace with actual Google Scholar ID
    "WgPhMfwAAAAJ",  # Add more researchers here
]

# Define Hugo content directory
HUGO_CONTENT_DIR = "content/publication"

# Create publication folder if it doesn’t exist
os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)

# Get the current date for logging
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Compute the threshold year (last two years)
current_year = datetime.datetime.now().year
year_threshold = current_year - 2  # Only keep papers from this year or last year

# Open a log file to track updates
log_file = open(f"{HUGO_CONTENT_DIR}/update_log.txt", "a")
log_file.write(f"\nUpdate run on {current_date}\n")

# Function to extract venue from citation
def extract_venue(citation):
    if citation:
        match = re.search(r'([^,]+), \d{4}', citation)  # Extract first part before the year
        return match.group(1) if match else citation
    return "Unknown Venue"

# Track new publication filenames to prevent deletion
new_filenames = set(["index.md"])  # Always keep index.md

# Process each Google Scholar profile
for SCHOLAR_ID in SCHOLAR_IDS:
    print(f"🔍 Fetching publications for Scholar ID: {SCHOLAR_ID}")

    # Fetch author profile
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["publications"])

    # Sort publications by year (most recent first)
    sorted_pubs = sorted(author["publications"], key=lambda x: x["bib"].get("pub_year", "0"), reverse=True)

    for pub in sorted_pubs:
        pub_year = pub["bib"].get("pub_year", "Unknown Year")
        try:
            pub_year = int(pub_year)
        except ValueError:
            continue  # Skip if year is invalid

        if pub_year < year_threshold:
            continue  # Skip older papers

        # Fetch metadata with timeout
        try:
            scholarly.fill(pub, sections=["bib"])
            time.sleep(1.5)  # Prevent rate-limiting
        except Exception as e:
            print(f"⚠️ Error fetching metadata for {pub['bib'].get('title', 'Unknown Title')}: {e}")
            continue

        pub_title = pub["bib"].get("title", "Unknown Title").strip()
        pub_authors = pub["bib"].get("author", "Unknown Authors")
        pub_citation = pub["bib"].get("citation", "").strip()
        pub_eprint = pub["bib"].get("eprint", "").strip()  # ArXiv ID if available
        pub_doi = pub["bib"].get("doi", "").strip()
        pub_venue = extract_venue(pub_citation) if pub_citation else (f"arXiv:{pub_eprint}" if pub_eprint else "Unknown Venue")
        pub_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={pub_title.replace(' ', '+')}"

        pub_date = f"{pub_year}-01-01T00:00:00Z"
        publish_date = f"{pub_year}-09-01T00:00:00Z"  # Simulating a valid format

        # Convert authors into a proper YAML list format
        if isinstance(pub_authors, str):
            pub_authors = re.split(r',| and ', pub_authors)  # Splits on commas and 'and'
            pub_authors = [author.strip() for author in pub_authors if author.strip()]
        elif not isinstance(pub_authors, list):
            pub_authors = ["Unknown Author"]

        # Ensure proper formatting of venue/journal
        pub_venue = f"*{pub_venue}*" if pub_venue else "Unknown Venue"
        pub_venue = pub_venue.replace("(", "\\(").replace(")", "\\)")  # Escape parentheses for Hugo

        # Determine publication type
        if "arXiv" in pub_venue:
            pub_type = "preprint"
            url_pdf = f"https://arxiv.org/pdf/{pub_eprint}.pdf" if pub_eprint else ""
            pub_url = f"https://arxiv.org/abs/{pub_eprint}" if pub_eprint else pub_url
        else:
            pub_type = "article-journal"
            url_pdf = ""

        # Create a safe filename
        safe_filename = pub_title.lower().replace(" ", "_").replace(",", "").replace("'", "").replace(":", "").replace("/", "_") + ".md"
        filename = os.path.join(HUGO_CONTENT_DIR, safe_filename)

        # Store filenames for tracking
        new_filenames.add(safe_filename)  # Track filename

        # Generate Markdown file for Hugo
        with open(filename, "w") as md_file:
            md_file.write(f"""---
title: "{pub_title}"
authors:
""")
            for author in pub_authors:
                md_file.write(f"  - \"{author}\"\n")

            md_file.write(f"""date: "{pub_date}"
publishDate: "{publish_date}"
doi: "{pub_doi}"

# Publication type.
publication_types: ["{pub_type}"]

# Journal or conference name.
publication: {pub_venue}

abstract: ""
summary: ""

tags: []
featured: false

# Links
url_pdf: "{url_pdf}"
url_code: ""
url_dataset: ""
url_poster: ""
url_project: ""
url_slides: ""
url_source: ""
url_video: ""

projects: []
slides: ""

publication_url: "{pub_url}"
---
""")

        log_file.write(f"Added: {pub_title} ({pub_date})\n")

# **DELETE OLD PUBLICATIONS BUT KEEP index.md**
existing_files = {f for f in os.listdir(HUGO_CONTENT_DIR) if f.endswith(".md")}
files_to_delete = existing_files - new_filenames

for file_name in files_to_delete:
    file_path = os.path.join(HUGO_CONTENT_DIR, file_name)
    os.remove(file_path)
    log_file.write(f"Deleted: {file_path}\n")
    print(f"🗑 Deleted old publication: {file_path}")

log_file.close()
print("✅ Publications updated successfully!")
