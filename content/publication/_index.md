---
title: Publications
type: landing          # makes this page use widget sections

sections:
  # ——— All publications, rendered in “citation” style ———
  - block: publications
    content:
      title: All Publications        # heading text (optional)
      filters:
        # leave empty to list every publication,
        # or filter by tag / category / publication_type
        publication_type: []
    design:
      view: citation                 # ← the “cite-as-APA” layout
      columns: "1"

  # ——— Highlighted items written manually ———
  - block: markdown
    content:
      title: Highlighted Publications
      text: |
        ## Theory
        - Paper 1

        ## Applications
        - Paper 1
    design:
      columns: "1"
---