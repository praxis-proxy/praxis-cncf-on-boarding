---
name: Onboarding item
description: Track one item of the CNCF sandbox onboarding checklist
title: "[Onboarding] "
labels:
  - onboarding-item
body:
  - type: markdown
    attributes:
      value: |
        Use this template for a custom onboarding item. For standard items, run
        `./scripts/bootstrap-issues.sh` instead — it creates all predefined items automatically.

        **Workflow**
        1. Open the matching section in `ONBOARDING.md` (instructions and issue link are on the checklist line).
        2. Add evidence and open a pull request that only changes `ONBOARDING.md`.
        3. Include `Closes #ISSUE_NUMBER` in the PR description (replace with this issue's number).
        4. When the PR opens, the box is checked and linked automatically. When it merges, this issue closes.

  - type: textarea
    attributes:
      label: Work to complete
      description: Describe what needs to be done for this onboarding item.
    validations:
      required: true

  - type: input
    attributes:
      label: ONBOARDING.md section
      description: Which section (slug) in ONBOARDING.md should be updated?
      placeholder: maintainer-list-pr
    validations:
      required: false
