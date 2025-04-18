from scholarly import scholarly
import os
import datetime
import re
import time

# List of Google Scholar profile IDs to scrape
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Replace with actual Google Scholar ID
    "WgPhMfwAAAAJ",  # Add more researchers here
    "L3x4IcgAAAAJ",  # Add more researchers here
    "w-EcuBUAAAAJ",  # Add more researchers here
    "1iWGSc0AAAAJ",  # Add more researchers here
    "2bchLEwAAAAJ",  # Add more researchers here
    "RsbU0icAAAAJ",  # Add more researchers here
]

# Define Hugo content directory
HUGO_CONTENT_DIR = "content/publication"

# Create publication folder if it doesn’t exist
os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)

# Get the current date for logging
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Open a log file to track updates
log_file = open(f"{HUGO_CONTENT_DIR}/update_log.txt", "a")
log_file.write(f"\nUpdate run on {current_date}\n")

# Function to extract venue from citation
def extract_venue(citation):
    if citation:
        return citation  # Use full citation for journal name
    return "Unknown Venue"

# Process each Google Scholar profile
for SCHOLAR_ID in SCHOLAR_IDS:
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["publications"])

    # Sort publications by year (most recent first)
    sorted_pubs = sorted(author["publications"], key=lambda x: x["bib"].get("pub_year", "0"), reverse=True)

    for pub in sorted_pubs[:5]:  # Fetch the latest 5 papers per author
        scholarly.fill(pub)  # Fetch full metadata

        pub_title = pub["bib"].get("title", "Unknown Title")
        pub_year = pub["bib"].get("pub_year", "Unknown Year")
        pub_authors = pub["bib"].get("author", "Unknown Authors")
        pub_citation = pub["bib"].get("citation", "")
        pub_eprint = pub["bib"].get("eprint", "").strip()  # ArXiv ID if available
        pub_doi = pub["bib"].get("doi", "").strip()  # DOI if available
        pub_venue = extract_venue(pub_citation)  # Use full citation for journal name
        pub_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={pub_title.replace(' ', '+')}"

        # Determine publication type
        if "arXiv" in pub_venue or "arXiv preprint" in pub_venue or pub_eprint:
            pub_type = "preprint"
            if pub_eprint:
                pub_url = f"https://arxiv.org/abs/{pub_eprint}"  # Correct ArXiv link
        else:
            pub_type = "article-journal"

        # Ensure the year is valid
        try:
            pub_year = int(pub_year)
            pub_date = f"{pub_year}-01-01T00:00:00Z"
        except ValueError:
            pub_date = f"{datetime.datetime.now().year}-01-01T00:00:00Z"

        # Convert authors into a proper YAML list format
        if isinstance(pub_authors, str):
            pub_authors = re.split(r',| and ', pub_authors)  # Splits on commas and 'and'
            pub_authors = [author.strip() for author in pub_authors if author.strip()]
        elif not isinstance(pub_authors, list):
            pub_authors = ["Unknown Author"]

        # Create a safe filename
        safe_filename = pub_title.lower().replace(" ", "_").replace(",", "").replace("'", "").replace(":", "").replace("/", "_") + ".md"
        filename = f"{HUGO_CONTENT_DIR}/{safe_filename}"

        # Generate Markdown file for Hugo
        with open(filename, "w") as md_file:
            md_file.write(f"""---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "{pub_title}"
date: {pub_date}
publishDate: {pub_date}
doi: "{pub_doi}"

authors:
""")
            for author in pub_authors:
                md_file.write(f"  - \"{author}\"\n")

            md_file.write(f"""publication: "{pub_venue}"
publication_types: ["{pub_type}"]

abstract: ""

# Summary. An optional shortened abstract.
summary: ""

tags: []
categories: []
featured: false

# Custom links (optional).
url_pdf: ""
url_code: ""
url_dataset: ""
url_poster: ""
url_project: ""
url_slides: ""
url_source: ""
url_video: ""

# Associated Projects (optional).
projects: []

# Slides (optional).
slides: ""

publication_url: "{pub_url}"
---
""")

        log_file.write(f"Added: {pub_title} ({pub_date})\n")

log_file.close()
print("✅ Publications updated successfully!")
