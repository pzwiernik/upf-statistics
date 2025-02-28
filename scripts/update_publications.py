from scholarly import scholarly
import os
import datetime

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

# Open a log file to track updates
log_file = open(f"{HUGO_CONTENT_DIR}/update_log.txt", "a")
log_file.write(f"\nUpdate run on {current_date}\n")

# Process each Google Scholar profile
for SCHOLAR_ID in SCHOLAR_IDS:
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["publications"])

    # Sort publications by year (most recent first)
    sorted_pubs = sorted(author["publications"], key=lambda x: x["bib"].get("year", 0), reverse=True)

    for pub in sorted_pubs[:5]:  # Fetch the latest 5 papers per author
        pub_title = pub["bib"]["title"]
        pub_year = pub["bib"].get("year", "Unknown Year")
        pub_authors = pub["bib"].get("author", "Unknown Authors")
        pub_venue = pub["bib"].get("venue", "")
        pub_eprint = pub["bib"].get("eprint", "")  # arXiv identifier if available
        pub_url = f"https://scholar.google.com/scholar?oi=bibs&hl=en&q={pub_title.replace(' ', '+')}"

        # Ensure the year is a valid number, default to current year if missing
        try:
            pub_year = int(pub_year)
            pub_date = f"{pub_year}-01-01"  # Default to January 1st of that year
        except ValueError:
            pub_date = f"{datetime.datetime.now().year}-01-01"

        # Convert authors into a proper YAML list
        if isinstance(pub_authors, str):
            pub_authors = pub_authors.split(", ")
        elif not isinstance(pub_authors, list):  
            pub_authors = ["Unknown Author"]

        # Prioritize journal name, fallback to arXiv identifier if available
        pub_source = pub_venue if pub_venue else (f"arXiv:{pub_eprint}" if pub_eprint else "Unknown Venue")

        # Create a safe filename
        safe_filename = pub_title.lower().replace(" ", "_").replace(",", "").replace("'", "").replace(":", "").replace("/", "_")
        filename = f"{HUGO_CONTENT_DIR}/{safe_filename}.md"

        # Generate Markdown file for Hugo
        with open(filename, "w") as md_file:
            md_file.write(f"""---
title: "{pub_title}"
date: {pub_date}
authors:
""")
            for author in pub_authors:
                md_file.write(f"  - \"{author}\"\n")

            md_file.write(f"""publication: "{pub_source}"
publication_url: "{pub_url}"
---
""")

        log_file.write(f"Added: {pub_title} ({pub_date})\n")

log_file.close()
print("✅ Publications updated successfully!")