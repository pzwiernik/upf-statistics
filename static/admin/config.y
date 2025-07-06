backend:
  name: github
  repo: pzwiernik/upf-statistics  # change to your GitHub org/repo
  branch: main                    # or your default branch
  auth_type: implicit
  app_id: Ov23liH7FdORtpnUHkkT  # Replace this in step 5

media_folder: "static/uploads"
public_folder: "/uploads"

collections:
  - name: "people"
    label: "People"
    folder: "content/authors"
    create: true
    slug: "{{slug}}"
    fields:
      - {label: "Name", name: "title", widget: "string"}
      - {label: "First Name", name: "first_name", widget: "string"}
      - {label: "Last Name", name: "last_name", widget: "string"}
      - {label: "Role", name: "role", widget: "string"}
      - {label: "Organizations", name: "organizations", widget: "list", fields: [{label: "Name", name: "name", widget: "string"}, {label: "URL", name: "url", widget: "string"}]}
      - {label: "Interests", name: "interests", widget: "list"}
      - {label: "User Groups", name: "user_groups", widget: "list"}