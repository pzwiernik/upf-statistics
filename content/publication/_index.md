---
title: Publications           # Page title in tab / breadcrumbs
type:  landing                # Tell Hugo-Blox this page holds widgets

sections:
  # ─────────── 1. Full list rendered in citation view ───────────
  - block: collection
    content:
      title: All Publications
      page_type: publication       # ← list items from content/publication/
      filters:
        featured: false            # set to true if you only want featured
      order: desc
      count: 100                   # how many to show (0 = unlimited)
    design:
      view: citation               # APA/IEEE compact style
      columns: "1"

  # ─────────── 2. Manually curated highlights ───────────
  - block: markdown
    content:
      title: Highlighted Publications
      text: |
        ## Theory
        - Paper&nbsp;1

        ## Applications
        - Paper&nbsp;1
    design:
      columns: "1"
---