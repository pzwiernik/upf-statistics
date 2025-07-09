---
title: Recent & Upcoming Events
type: landing

sections:
########################################################################
# 1 · Dynamic list — all seminar-type .md files (newest first)
########################################################################
- block: collection
  content:
    title: Seminars
    page_type: event
    order: desc          # newest first
    count: 20            # show up to 20
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"

########################################################################
# 2 · Manually-curated Workshops & Conferences (HTML cards)
########################################################################
- block: markdown
  content:
    title: Workshops & Conferences
    text: |
      <!-- copy-paste & edit a card for each event -->
      <!-- CARD 1 ---------------------------------------------------- -->
      <div class="media stream-item view-compact">
        <!-- thumbnail (right-hand side) -->
        <a class="ml-3" href="https://example.com/graphical-models-2024"
           target="_blank" rel="noopener">
          <img src="/media/event/gm2024.jpg" alt="Graphical Models Workshop"
               width="110" height="110" loading="lazy">
        </a>

        <!-- main text -->
        <div class="media-body">
          <!-- line 1 – title (linked) -->
          <div class="section-subheading article-title mb-0">
            <a href="https://example.com/graphical-models-2024"
               target="_blank" rel="noopener">
              Barcelona Workshop on Graphical Models
            </a>
          </div>

          <!-- line 2 – short description -->
          <div class="article-style">
            Hands-on meeting on structure learning &
            inference in graphical models.
          </div>

          <!-- line 3 – date · venue -->
          <div class="stream-meta article-metadata">
            3–5&nbsp;Jul&nbsp;2024 · UPF Campus Ciutadella
          </div>
        </div>
      </div>

      <!-- CARD 2 ---------------------------------------------------- -->
      <div class="media stream-item view-compact">
        <a class="ml-3" href="https://example.com/bayescomp-2025"
           target="_blank" rel="noopener">
          <img src="/media/event/bayescomp2025.png" alt="BayesComp 2025 logo"
               width="110" height="110" loading="lazy">
        </a>

        <div class="media-body">
          <div class="section-subheading article-title mb-0">
            <a href="https://example.com/bayescomp-2025"
               target="_blank" rel="noopener">
              10<sup>th</sup> Bayesian Computing Conference
            </a>
          </div>

          <div class="article-style">
            Advances in scalable Bayesian computation.
          </div>

          <div class="stream-meta article-metadata">
            12–14&nbsp;Jan&nbsp;2025 · UPF Auditorium
          </div>
        </div>
      </div>
  design:
    columns: "1"
---