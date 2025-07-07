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

        This is the website of the statistics group in the [Department of Economics and Business](https://www.upf.edu/en/web/econ) at [Universitat Pompeu Fabra](https://www.upf.edu/) in Barcelona, Spain.  
        Our group is part of the [BSE Data Science Center](https://bse.eu/data-science-center).

  - block: collection
    content:
      title: Latest News
      page_type: post          
      count: 5
      filters:
        exclude_featured: false
      order: desc
    design:
      view: compact
      show_author: false
      show_date: true
      columns: "1"
    
  - block: contact
    content:
      title: Find us in Barcelona
      address:
        street: >-
          Universitat Pompeu Fabra, Dept. of Economics  
          Ramon Trias Fargas 25-27
        city: Barcelona
        postcode: "08005"
        country: Spain
        country_code: ES
      coordinates:
        latitude:  "41.389200851208734"
        longitude: "2.1914945521791998"
      autolink: true
    design:
      columns: "1"

  - block: markdown
    content:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: "1"
---