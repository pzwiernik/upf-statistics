---
title: Recent & Upcoming Events
type: landing
---

sections:
  # ------------------------------------------------------------------
  # 0 · Intro text
  # ------------------------------------------------------------------
  - block: markdown
    content:
      title: '<span id="seminars">Seminars</span>'
      text: |
        Our main seminar series is the **Statistics Seminar at UPF**, organised by Chiara Amorino and Lorenzo Cappello.  
        We also run the *Internal Statistics Seminar* and a number of reading seminars.

  # ------------------------------------------------------------------
  # 1 · Dynamic list — Seminars
  # ------------------------------------------------------------------
  - block: collection
    label: Seminars
    anchor: seminars
    content:
      page_type: event
      tag: seminar
      past_events: true           # ← show past as well as future
      archive_button: true
      archive_button_url: "/tag/seminar/"   # change to /tags/… if your taxonomy uses plural
      order: desc
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

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