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
# 1 · Dynamic list — Seminars
##############################################################################
- block: collection
  label: Seminars
  content:
    page_type: event
    tag: seminar
    filters:
      exclude_past: false        # show past events
      exclude_future: false      # show future events
    order: desc
    count: 10
    archive_button: true
    archive_button_url: "/tag/seminar/"
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"
    anchor: seminars             # target for /event/#seminars

##############################################################################
# 2 · Dynamic list — Conferences & Workshops
##############################################################################
- block: collection
  label: Conferences
  content:
    page_type: event
    tag: conference
    filters:
      exclude_past: false
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
    anchor: conferences          # target for /event/#conferences