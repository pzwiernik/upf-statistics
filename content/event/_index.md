---
title: Recent & Upcoming Events
type: landing

sections:
  - block: collection
    content:
      title: Seminars
      page_type: event
      filters:
        event: ["Statistics Seminar", "Internal Statistics Seminar"]
      order: desc
      offset: 0
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

  - block: collection
    content:
      title: Workshops & Conferences
      page_type: event
      filters:
        event: ["Workshop", "Conference"]
      order: desc
      offset: 0
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"
---