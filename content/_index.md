---
# Leave the homepage title empty to use the site title
title:
date: 2022-10-24
type: landing

sections:
  - block: hero
    content:
      title: |
        UPF Statistics
      image:
        filename: welcome.png
      text: |
        <br>
        
        This is the website of the statistics group in  the [Department of Economics and Business](https://www.upf.edu/en/web/econ)  at [Universitat Pompeu Fabra](https://www.upf.edu/) in Barcelona, Spain. Our group is part of the [BSE Data Science Center](https://bse.eu/data-science-center).   
  
  - block: collection
    content:
      title: Latest News
      subtitle:
      text:
      count: 5
      filters:
        author: ''
        category: ''
        exclude_featured: false
        publication_type: ''
        tag: ''
      offset: 0
      order: desc
      page_type: post
    design:
      view: compact
      show_author: false
      show_date: true
      columns: '1'

- block: contact
  content:
    title: Contact
    # text: |-
    #   Optional free-text paragraph here …

    address:
      street: >-
        Universitat Pompeu Fabra, Department of Economics and Business,
        Ramon Trias Fargas 25-27
      city: Barcelona
      # region: CA            # uncomment/add if you need a region
      postcode: "08005"
      country: Spain
      country_code: ES

    coordinates:
      latitude: "41.389200851208734"
      longitude: "2.1914945521791998"

    appointment_url: "https://calendly.com"

    # contact_links:
    #   - icon: comments
    #     icon_pack: fas
    #     name: Discuss on Forum
    #     link: "https://discourse.gohugo.io"

    autolink: true          # auto-link email/phone if present

    form:
      provider: netlify
      netlify:
        captcha: false
      formspree:
        id: ""              # leave blank if not using Formspree
  design:
    columns: "1"

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
