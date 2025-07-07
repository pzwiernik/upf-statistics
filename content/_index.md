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

  - block: markdown
    content:
      title:
      subtitle:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
