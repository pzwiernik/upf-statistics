---
title: Recent & Upcoming Events
type: landing
---

sections:
  # --------------------------------------------------------------------
  # 0 · Intro text
  # --------------------------------------------------------------------
  - block: markdown
    content:
      title: '<span id="seminars">Seminars</span>'
      text: |
        Our main seminar series is the **Statistics Seminar at UPF**, organised by Chiara Amorino and Lorenzo Cappello.  
        We also run the *Internal Statistics Seminar* and a number of reading seminars.

  # --------------------------------------------------------------------
  # 1 · Dynamic list — seminars
  # --------------------------------------------------------------------
  - block: collection
    label: Seminars
    content:
      page_type: event
      tag: seminar
      archive_button: true
      archive_button_url: "/tags/seminar/"   # taxonomy archive (plural “tags”)
      order: desc
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"
      anchor: seminars          # ← keep it here; no longer hijacks the button

  # --------------------------------------------------------------------
  # 2 · Static Workshops & Conferences cards (unchanged)
  # --------------------------------------------------------------------
  - block: markdown
    content:
      title: '<span id="conferences">Workshops & Conferences (last 10 years)</span>'
      text: |
        <!-- your HTML cards here (unchanged) -->
    design:
      columns: "1"