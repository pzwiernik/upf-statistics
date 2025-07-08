from scholarly import scholarly
import json

# Replace with a valid Google Scholar Profile ID
SCHOLAR_ID = "WgPhMfwAAAAJ"  # Replace with a real ID

# Fetch author data
author = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=["publications"])

# Print raw metadata for the first 3 publications
for i, pub in enumerate(author["publications"][:3]):
    print(f"\nPublication {i+1}:")
    print(json.dumps(pub, indent=4, ensure_ascii=False))
