---
title: Recent & Upcoming Events
type: landing

sections:
  - block: collection
    content:
      title: Seminars
      page_type: event
      filters:
        event_type: ["seminar", "internal"]
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
        event_type: ["workshop", "conference"]
      order: desc
      offset: 0
      count: 10
    design:
      view: compact
      show_date: true
      show_location: false
      columns: "1"
---