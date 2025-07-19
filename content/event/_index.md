---
title: Recent & Upcoming Events
type: landing
---

sections:
  ##############################################################################
  # 0 · Introductory paragraph for the Seminars section
  ##############################################################################
  - block: markdown
    content:
      title: '<span id="seminars">Seminars</span>'
      text: |
        Our main seminar series is the **Statistics Seminar at UPF**, organized by Chiara Amorino and Lorenzo Cappello.  
        We also run the *Internal Statistics Seminar* and a number of reading seminars.

  ##############################################################################
  # 1 · Dynamic list — Seminars (from *any* folder, filtered by tag)
  ##############################################################################
  - block: collection
    label: Seminars
    anchor: seminars                
    content:
      page_type: event
      tag: seminar                  # picks up both seminar folders
      archive_button: true
      archive_button_url: "/tags/seminar/"   # taxonomy archive
      order: desc
      count: 10
    design:
      view: compact
      show_date: true
      show_location: true
      columns: "1"

  ##############################################################################
  # 2 · Manually-curated Workshops & Conferences (static HTML cards)
  ##############################################################################
  - block: markdown
    content:
      title: '<span id="conferences">Workshops & Conferences (last 10 years)</span>'
      text: |
        <!-- CARD · Mathematical Aspects of Learning - 20 Years Later -->
        <div class="media stream-item view-compact">
          <div class="media-body">
            <div class="section-subheading article-title mb-0">
              <a href="https://www.crm.cat/mathematical-aspects-of-learning-theory/"
                 target="_blank" rel="noopener">
                Mathematical Aspects of Learning — 20 Years Later
              </a>
            </div>
            <div class="article-style">
              Workshop with talks by Piotr Zwiernik, Gergely Neu &amp; others.
            </div>
            <div class="stream-meta article-metadata">
              9–13&nbsp;Sep&nbsp;2024 · Casa Convalescència
            </div>
          </div>
          <a class="ml-3"
             href="https://www.crm.cat/mathematical-aspects-of-learning-theory/"
             target="_blank" rel="noopener"
             aria-label="Mathematical Aspects of Learning 2024">
            <img src="./media/casac.jpeg"
                 alt="Mathematical Aspects of Learning workshop image"
                 width="110" height="110" loading="lazy">
          </a>
        </div>

        <!-- CARD · Mathematical Statistics and Learning 2021 -->
        <div class="media stream-item view-compact mt-3">
          <div class="media-body">
            <div class="section-subheading article-title mb-0">
              <a href="https://dscbarcelona.wixsite.com/msl2020"
                 target="_blank" rel="noopener">
                Mathematical Statistics &amp; Learning 2021
              </a>
            </div>
            <div class="article-style">
              Conference on high-dimensional statistics and ML theory.
            </div>
            <div class="stream-meta article-metadata">
              29&nbsp;Jun – 2&nbsp;Jul&nbsp;2021 · Casa Convalescència
            </div>
          </div>
          <a class="ml-3"
             href="https://dscbarcelona.wixsite.com/msl2020"
             target="_blank" rel="noopener" aria-label="MSL 2021 image">
            <img src="./media/casac.jpeg"
                 alt="MSL 2021 banner"
                 width="110" height="110" loading="lazy">
          </a>
        </div>

        <!-- CARD · Google Focused Award mini-workshop -->
        <div class="media stream-item view-compact mt-3">
          <div class="media-body">
            <div class="section-subheading article-title mb-0">
              Google Focused Award Mini-workshop
            </div>
            <div class="article-style">
              Joint UPF &amp; Google Zurich workshop on machine-learning theory.
            </div>
            <div class="stream-meta article-metadata">
              7–8&nbsp;Mar&nbsp;2021 · UPF Campus Ciutadella
            </div>
          </div>
          <a class="ml-3" href="#" aria-label="Workshop image">
            <img src="./media/upf.jpeg"
                 alt="Mini-workshop banner"
                 width="110" height="110" loading="lazy">
          </a>
        </div>

        <!-- CARD · BayesComp 2018 -->
        <div class="media stream-item view-compact mt-3">
          <div class="media-body">
            <div class="section-subheading article-title mb-0">
              <a href="https://www.maths.nottingham.ac.uk/plp/pmztk/bayescomp/"
                 target="_blank" rel="noopener">
                10<sup>th</sup> BayesComp 2018
              </a>
            </div>
            <div class="article-style">
              Advances in scalable Bayesian computation.
            </div>
            <div class="stream-meta article-metadata">
              26–28&nbsp;Mar&nbsp;2018 · UPF Auditorium
            </div>
          </div>
          <a class="ml-3"
             href="https://www.maths.nottingham.ac.uk/plp/pmztk/bayescomp/"
             target="_blank" rel="noopener">
            <img src="./media/bayescomp.jpeg"
                 alt="BayesComp 2018 logo"
                 width="110" height="110" loading="lazy">
          </a>
        </div>
    design:
      columns: "1"