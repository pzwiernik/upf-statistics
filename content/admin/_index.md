---
type: decap_cms       # tells Hugo it’s the CMS page
private: true

# Render this page using the decap_cms output (adds the editor shell).
# We no longer include decap_cms_config, so your static/admin/config.yml wins.
outputs:
  - decap_cms
---