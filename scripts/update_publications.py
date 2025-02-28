from scholarly import scholarly
import os
import datetime

# List of Google Scholar profile IDs to scrape
SCHOLAR_IDS = [
    "OwnRAwQAAAAJ",  # Replace with actual Google Scholar ID
    "WgPhMfwAAAAJ",  # Add more researchers here
]

# Define Hugo content directory for publications
HUGO_CONTENT_DIR = "content/publication"

# Create publication folder if it doesn’t exist
os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)

# Get the current date for logging
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Open a log file to track updates
log_file = open(f"{HUGO_CONTENT_DIR}/update_log.txt", "a")
log_file.write(f"\nUpdate run on {current_date}\n")

# Process each Google Scholar profile
for SCHOLAR_ID in SCHOLAR_IDS:
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["publications"])

    for pub in author["publications"][:5]:  # Fetch the latest 5 papers per author
        pub_title = pub["bib"]["title"]
        pub_year = pub["bib"].get("year", "Unknown Year")
        pub_authors = pub["bib"].get("author", "Unknown Authors")
        pub_venue = pub["bib"].get("venue", "Unknown Venue")
        pub_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={pub_title.replace(' ', '+')}"

        # Create a safe filename
        filename = f"{HUGO_CONTENT_DIR}/{pub_title.lower().replace(' ', '_')}.md"

        # Generate Markdown file for Hugo
        with open(filename, "w") as md_file:
            md_file.write(f"""---
title: "{pub_title}"
date: {pub_year}-01-01
authors: "{pub_authors}"
publication: "{pub_venue}"
publication_url: "{pub_url}"
---
""")

        log_file.write(f"Added: {pub_title} ({pub_year})\n")

log_file.close()
print("✅ Publications updated successfully!")