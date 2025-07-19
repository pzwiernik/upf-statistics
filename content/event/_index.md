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
    anchor: seminars              # target for /event/#seminars
    content:
      page_type: event
      tag: seminar
      event_filter: all           # ← show past and upcoming
      archive_button: true
      archive_button_url: "/tag/seminar/"
      order: desc
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

  # ------------------------------------------------------------------
  # 2 · Dynamic list — Conferemces
  # ------------------------------------------------------------------
  - block: collection
    label: Conferences
    anchor: conferences              # target for /event/#seminars
    content:
      page_type: event
      tag: conference
      event_filter: all           # ← show past and upcoming
      archive_button: true
      archive_button_url: "/tag/conference/"
      order: desc
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

