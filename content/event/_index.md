---
title: Recent & Upcoming Events
type: landing

sections:
  ##############################################################################
  # 0 · Introductory paragraph for the Seminars section
  ##############################################################################
  - block: markdown
    content:
      title: '<span id="seminars">Seminars</span>'
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
      anchor: seminars     

  ##############################################################################
  # 2 · Manually-curated Workshops & Conferences (HTML cards)
  ##############################################################################
  - block: markdown
    content:
      title: '<span id="conferences">Workshops & Conferences (last 10 years)</span>'
      text: |
        <!-- Your existing HTML content remains unchanged -->
    design:
      anchor: conferences     
      columns: "1"
---