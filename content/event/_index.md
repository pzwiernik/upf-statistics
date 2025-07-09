---
title: Recent & Upcoming Events
type: landing

sections:
##############################################################################
# 1 · Dynamic list — seminars (.md files in content/event/)
##############################################################################
- block: collection
  content:
    title: Seminars
    page_type: event
    order: desc
    count: 20
  design:
    view: compact
    show_date: true
    show_location: true
    columns: "1"

##############################################################################
# 2 · Manually-curated Workshops & Conferences (HTML cards)
##############################################################################
- block: markdown
  content:
    title: Workshops & Conferences
    text: |
      <!-- CARD 1 ────────────────────────────────────────────────────────── -->
      <div class="media stream-item view-compact">
        <div class="media-body">
          <div class="section-subheading article-title mb-0">
            <a href="https://example.com/graphical-models-2024" target="_blank" rel="noopener">
              Barcelona Workshop on Graphical Models
            </a>
          </div>
          <div class="article-style">
            Hands-on meeting on structure learning & inference in graphical models.
          </div>
          <div class="stream-meta article-metadata">
            3–5&nbsp;Jul&nbsp;2024 · UPF Campus Ciutadella
          </div>
        </div>

        <!-- thumbnail (appears on the right) -->
        <a class="ml-3" href="https://example.com/graphical-models-2024" target="_blank" rel="noopener">
          <img src="/media/event/gm2024.jpg" alt="Graphical Models Workshop"
               width="110" height="110" loading="lazy">
        </a>
      </div>

      <!-- CARD · Google Focused Award Mini-workshop ───────────────────────── -->
      <div class="media stream-item view-compact">
        <div class="media-body">
          <div class="section-subheading article-title mb-0">
            <!-- no public website → linkless title -->
            Google Focused Award Mini-workshop
          </div>

          <div class="article-style">
            Joint UPF & Google Zurich workshop on machine-learning theory.
          </div>

          <div class="stream-meta article-metadata">
            7–8&nbsp;Mar&nbsp;2021 · UPF Campus Ciutadella
          </div>
        </div>

        <!-- thumbnail on the right -->
        <a class="ml-3" href="#" aria-label="Workshop image">
          <img src="/media/event/download-6-.jpeg"
               alt="Mini-workshop banner"
               width="110" height="110" loading="lazy">
        </a>
      </div>

      <!-- CARD 2 ────────────────────────────────────────────────────────── -->
      <div class="media stream-item view-compact">
        <div class="media-body">
          <div class="section-subheading article-title mb-0">
            <a href="https://example.com/bayescomp-2025" target="_blank" rel="noopener">
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

        <a class="ml-3" href="https://example.com/bayescomp-2025" target="_blank" rel="noopener">
          <img src="/media/event/bayescomp2025.png" alt="BayesComp 2025 logo"
               width="110" height="110" loading="lazy">
        </a>
      </div>
  design:
    columns: "1"
---