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
 #     text: |-
#        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer tempus augue non tempor egestas. Proin nisl nunc, dignissim in accumsan dapibus, auctor ullamcorper neque. Quisque at elit felis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean eget elementum odio. Cras interdum eget risus sit amet aliquet. In volutpat, nisl ut fringilla dignissim, arcu nisl suscipit ante, at accumsan sapien nisl eu eros.
      address:
        street: Universitat Pompeu Fabra, Department of Economics and Business, Ramon Trias Fargas, 25-27
        city: Barcelona
  #      region: CA
        postcode: '08005'
        country: Spain
        country_code: ES
      coordinates:
        latitude: '41.389200851208734'
        longitude: '2.1914945521791998'
      appointment_url: 'https://calendly.com'
      #contact_links:
      #  - icon: comments
      #    icon_pack: fas
      #    name: Discuss on Forum
      #    link: 'https://discourse.gohugo.io'
    
      # Automatically link email and phone or display as text?
      autolink: true
    
      # Email form provider
      form:
        provider: netlify
        formspree:
          id:
        netlify:
          # Enable CAPTCHA challenge to reduce spam?
          captcha: false
    design:
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
