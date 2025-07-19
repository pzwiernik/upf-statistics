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
      We also run the *Internal Statistics Seminar* and a number of reading seminars.

##############################################################################
# 1 · Dynamic list — Seminars
##############################################################################
- block: collection
  label: Seminars
  content:
    page_type: event
    tag: seminar
    past_events: true          # include past & upcoming talks
    order: desc
    count: 10
    archive_button: true
    archive_button_url: "/tag/seminar/"
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"
    anchor: seminars           # in-page target for /event/#seminars

##############################################################################
# 2 · Dynamic list — Conferences & Workshops
##############################################################################
- block: collection
  label: Conferences
  content:
    page_type: event
    tag: conference
    past_events: true
    order: desc
    count: 10
    archive_button: true
    archive_button_url: "/tag/conference/"
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"
    anchor: conferences        # target for /event/#conferences