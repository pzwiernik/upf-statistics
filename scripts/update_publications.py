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

        pub_title = pub["bib"].get("title", "Unknown Title")
        pub_authors = pub["bib"].get("author", "Unknown Authors")
        pub_citation = pub["bib"].get("citation", "")
        pub_eprint = pub["bib"].get("eprint", "")  # ArXiv ID if available
        pub_doi = pub["bib"].get("doi", "")
        pub_venue = extract_venue(pub_citation) if pub_citation else (f"arXiv:{pub_eprint}" if pub_eprint else "Unknown Venue")
        pub_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={pub_title.replace(' ', '+')}"

        pub_date = f"{pub_year}-01-01"
        publish_date = f"{pub_year}-09-01T00:00:00Z"  # Simulating a valid format

        # Convert authors into a list if missing
        if isinstance(pub_authors, str):
            pub_authors = pub_authors.split(", ")
        elif not isinstance(pub_authors, list):  
            pub_authors = ["Unknown Author"]

        # Create a **subfolder** for each publication (required by Hugo Blox)
        safe_foldername = pub_title.lower().replace(" ", "_").replace(",", "").replace("'", "").replace(":", "").replace("/", "_")
        pub_folder = os.path.join(HUGO_CONTENT_DIR, safe_foldername)
        os.makedirs(pub_folder, exist_ok=True)
        filename = os.path.join(pub_folder, "index.md")

        # Store filenames for tracking
        new_filenames.add(safe_foldername)  # Track folder names

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
publication_types: ["article-journal"]

# Journal or conference name.
publication: "*{pub_venue}*"

abstract: ""
summary: ""

tags: []
featured: false

url_pdf: ""
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
existing_folders = {f for f in os.listdir(HUGO_CONTENT_DIR) if os.path.isdir(os.path.join(HUGO_CONTENT_DIR, f))}
folders_to_delete = existing_folders - new_filenames

for folder in folders_to_delete:
    folder_path = os.path.join(HUGO_CONTENT_DIR, folder)
    os.system(f"rm -rf {folder_path}")  # Remove outdated publication folders
    log_file.write(f"Deleted: {folder_path}\n")
    print(f"🗑 Deleted old publication: {folder_path}")

log_file.close()
print("✅ Publications updated successfully!")
