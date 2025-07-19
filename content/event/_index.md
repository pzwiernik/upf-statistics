---
title: Recent & Upcoming Events
type: landing
---

sections:
##############################################################################
# 0 · Intro paragraph
##############################################################################
- block: markdown
  content:
    title: '<span id="seminars">Seminars</span>'
    text: |
      Our main seminar series is the **Statistics Seminar at UPF**, organised by Chiara Amorino and Lorenzo Cappello.  
      We also run the *Internal Statistics Seminar* and several reading seminars.

##############################################################################
# 1 · Dynamic list — Seminars (past + upcoming)
##############################################################################
- block: collection
  label: Seminars
  content:
    page_type: event
    filters:
      tag: seminar           # ← tag filter belongs INSIDE `filters`
      exclude_past:   false  # show past
      exclude_future: false  # show future
    order: desc
    count: 10
    archive_button: true
    archive_button_url: "/tag/seminar/"
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"
    anchor: seminars         # in-page target for /event/#seminars

##############################################################################
# 2 · Dynamic list — Conferences & Workshops
##############################################################################
- block: collection
  label: Conferences
  content:
    page_type: event
    filters:
      tag: conference
      exclude_past:   false
      exclude_future: false
    order: desc
    count: 10
    archive_button: true
    archive_button_url: "/tag/conference/"
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"
    anchor: conferences      # in-page target for /event/#conferences