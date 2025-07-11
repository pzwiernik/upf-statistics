---
title: Recent & Upcoming Events
type: landing

sections:
  ##############################################################################
  # 0 · Introductory paragraph for the Seminars section
  ##############################################################################
  - block: markdown
    content:
      title: Seminars
      text: |
        Our main seminar series is the **Statistics Seminar at UPF**, organized by Chiara Amorino and Lorenzo Cappello.  
        We also run the *Internal Statistics Seminar* and a number of reading seminars.

  ##############################################################################
  # 1 · Dynamic list — seminars (.md files in content/event/)
  ##############################################################################
  - block: collection
    content:
      title: 
      page_type: event
      order: desc
      count: 20
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

  ##############################################################################
  # 2 · Manually-curated Workshops & Conferences (HTML cards)
  ##############################################################################
  - block: markdown
    content:
      title: Workshops & Conferences (last 10 years)
      text: |
        <!-- Your existing HTML content remains unchanged -->
    design:
      columns: "1"
---