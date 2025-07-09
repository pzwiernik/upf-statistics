---
title: Recent & Upcoming Events
type: landing

sections:
  #######################################################################
  # 1 · Dynamic list – Just list all event .md files (most recent first)
  #######################################################################
  - block: collection
    content:
      title: Seminars
      page_type: event
      order: desc         # newest first
      count: 20           # show up to 20 events
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

  #######################################################################
  # 2 · Manually-curated block – Workshops & Conferences
  #######################################################################
  - block: markdown
    content:
      title: Workshops & Conferences
      text: |
        <div class="media stream-item view-compact">
          <div class="media-body">
            <p class="article-title mb-0">
              <a href="https://example.com/workshop-graphical-models-2024"
                 target="_blank" rel="noopener">
                Barcelona Workshop on Graphical Models
              </a>
              &nbsp;—&nbsp;
              3–5 July 2024 · UPF Campus Ciutadella
            </p>
          </div>
        </div>

        <div class="media stream-item view-compact">
          <div class="media-body">
            <p class="article-title mb-0">
              <a href="https://example.com/bayesian-computing-2025"
                 target="_blank" rel="noopener">
                10<sup>th</sup> Bayesian Computing Conference
              </a>
              &nbsp;—&nbsp;
              12–14 Jan 2025 · UPF Auditorium
            </p>
          </div>
        </div>
    design:
      columns: "1"
---