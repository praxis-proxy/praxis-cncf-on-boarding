# CNCF Sandbox Onboarding

Single source of truth for completing [CNCF Sandbox onboarding](https://github.com/cncf/sandbox/issues/487) after your project's TOC acceptance vote.

**Work here only:** each item shows `(Issue: …)` until you open a PR with `Closes #N`; automation then checks the box and shows `(PR: …)` here and in [README.md](README.md). Edit evidence below; do not edit README or toggle boxes yourself.

Onboarding should be completed within **one month** of acceptance. When everything is done (or intentionally N/A), run `./scripts/generate-status-report.sh` to produce an update for your CNCF onboarding issue.

---

## Required before CNCF staff can proceed

A signed Project Contribution Agreement and trademark transfer are required **before** CNCF staff can complete the rest of onboarding. Other items can be worked on in parallel.

### ip-policy-review

<!-- field-guide:start -->
Review the [CNCF IP Policy](https://github.com/cncf/foundation/blob/main/charter.md#11-ip-policy). Ensure the project uses a CNCF-compatible license — inbound projects must use **Apache 2.0**. (Dependency licenses are tracked separately in `license-scan-import`.)
<!-- field-guide:end -->

- [ ] Review and understand the CNCF IP Policy <!-- checklist:ip-policy-review --> (Issue: #ISSUE_IP_POLICY_REVIEW)

**Evidence:**

_Confirm license is Apache 2.0 and link to the LICENSE file._

### license-policy-review

<!-- field-guide:start -->
Review the [CNCF Allowlist License Policy](https://github.com/cncf/foundation/blob/main/policies-guidance/allowed-third-party-license-policy.md). This governs licenses used by third-party dependencies. CNCF FOSSA or CNCF Snyk can check compliance — pick one (tracked in `license-scan-import`).
<!-- field-guide:end -->

- [ ] Review and understand the CNCF Third Party License Policy <!-- checklist:license-policy-review --> (Issue: #ISSUE_LICENSE_POLICY_REVIEW)

**Evidence:**

_Note which scanning service you'll use (FOSSA or Snyk)._

### trademark-guidelines-review

<!-- field-guide:start -->
Review the [Linux Foundation trademark guidelines](https://www.linuxfoundation.org/trademark-usage/). Let the TOC know if you plan to change your project name.
<!-- field-guide:end -->

- [ ] Review and understand the LF trademark guidelines <!-- checklist:trademark-guidelines-review --> (Issue: #ISSUE_TRADEMARK_GUIDELINES_REVIEW)

**Evidence:**

_Confirm review complete; note any planned name change (or N/A)._

### trademark-transfer

<!-- field-guide:start -->
Transfer any existing trademark and logo assets to the Linux Foundation via the Project Contribution Agreement. CNCF staff sends this document to the contact emails listed in your Sandbox application.
<!-- field-guide:end -->

- [ ] Transfer trademark and logo assets to the Linux Foundation <!-- checklist:trademark-transfer --> (Issue: #ISSUE_TRADEMARK_TRANSFER)

**Evidence:**

_Date Contribution Agreement was signed, or status if pending._

## Review and understand other documents

### technical-leadership-principles

<!-- field-guide:start -->
Read the [Technical Leadership Principles](https://contribute.cncf.io/maintainers/community/leadership-principles/), which outline expected behavior for maintainers in leadership roles.
<!-- field-guide:end -->

- [ ] Review the Technical Leadership Principles <!-- checklist:technical-leadership-principles --> (Issue: #ISSUE_TECHNICAL_LEADERSHIP_PRINCIPLES)

**Evidence:**

_Confirm review complete._

### project-proposal-process

<!-- field-guide:start -->
Read the [CNCF project proposal process and requirements](https://github.com/cncf/toc/blob/main/process/README.md).
<!-- field-guide:end -->

- [ ] Review the project proposal process and requirements <!-- checklist:project-proposal-process --> (Issue: #ISSUE_PROJECT_PROPOSAL_PROCESS)

**Evidence:**

_Confirm review complete._

### cncf-services-review

<!-- field-guide:start -->
Read about [services available to CNCF projects](https://contribute.cncf.io/resources/project-services/).
<!-- field-guide:end -->

- [ ] Review services available for your project at the CNCF <!-- checklist:cncf-services-review --> (Issue: #ISSUE_CNCF_SERVICES_REVIEW)

**Evidence:**

_Confirm review complete._

### online-program-guidelines

<!-- field-guide:start -->
Read the CNCF online program guidelines (webinars, meetups, events) provided by CNCF staff.
<!-- field-guide:end -->

- [ ] Review the online program guidelines <!-- checklist:online-program-guidelines --> (Issue: #ISSUE_ONLINE_PROGRAM_GUIDELINES)

**Evidence:**

_Confirm review complete._

### telemetry-policy-review

<!-- field-guide:start -->
Read the CNCF telemetry data collection and usage policy.
<!-- field-guide:end -->

- [ ] Review the telemetry data collection and usage policy <!-- checklist:telemetry-policy-review --> (Issue: #ISSUE_TELEMETRY_POLICY_REVIEW)

**Evidence:**

_Confirm review complete._

### cncf-staff-office-hours

<!-- field-guide:start -->
Optional: book time with CNCF staff to walk through available resources, work through onboarding tasks together, or ask questions.
<!-- field-guide:end -->

- [ ] Optional: book time with CNCF staff <!-- checklist:cncf-staff-office-hours --> (Issue: #ISSUE_CNCF_STAFF_OFFICE_HOURS)

**Evidence:**

_Meeting date, or N/A if not needed._

## Contribute and transfer other materials

### neutral-github-org

<!-- field-guide:start -->
This makes the project transferable to the CNCF's GitHub Enterprise account. If it's already in another GitHub Enterprise account, remove it from there first.
<!-- field-guide:end -->

- [ ] Move the project to its own separate neutral GitHub organization <!-- checklist:neutral-github-org --> (Issue: #ISSUE_NEUTRAL_GITHUB_ORG)

**Evidence:**

_Neutral GitHub org name/URL._

### ghe-invite-accepted

<!-- field-guide:start -->
CNCF will add `thelinuxfoundation` as an organization owner to ensure neutral hosting.
<!-- field-guide:end -->

- [ ] Accept the invite to join the CNCF GitHub Enterprise account <!-- checklist:ghe-invite-accepted --> (Issue: #ISSUE_GHE_INVITE_ACCEPTED)

**Evidence:**

_Date invite accepted._

### slack-migration

<!-- field-guide:start -->
CNCF staff can help. This improves discoverability, lets CNCF enforce its Code of Conduct, and enables unlimited message retention. If you already have a large Slack/Discord community, CNCF may instead link to it from a pointer channel in the CNCF Slack workspace.
<!-- field-guide:end -->

- [ ] Migrate Slack channels to the Kubernetes or CNCF Slack workspace <!-- checklist:slack-migration --> (Issue: #ISSUE_SLACK_MIGRATION)

**Evidence:**

_Migration status or link to pointer channel._

### maintainers-circle-slack

<!-- field-guide:start -->
Join `#maintainers-circle` on CNCF Slack to find and share knowledge with other project teams.
<!-- field-guide:end -->

- [ ] Join the #maintainers-circle Slack channel <!-- checklist:maintainers-circle-slack --> (Issue: #ISSUE_MAINTAINERS_CIRCLE_SLACK)

**Evidence:**

_Confirm joined._

### domain-transfer

<!-- field-guide:start -->
If your project has its own domain(s), transfer them to the CNCF. LF Contact: `projects@cncf.io`. Project Selection: CNCF.
<!-- field-guide:end -->

- [ ] Transfer project domain(s) to the CNCF <!-- checklist:domain-transfer --> (Issue: #ISSUE_DOMAIN_TRANSFER)

**Evidence:**

_Domain(s) transferred, or N/A if none._

### artwork-pr

<!-- field-guide:start -->
Submit project artwork to [cncf/artwork](https://github.com/cncf/artwork). If you don't have artwork, CNCF can help design some.
<!-- field-guide:end -->

- [ ] Submit a pull request with your artwork <!-- checklist:artwork-pr --> (Issue: #ISSUE_ARTWORK_PR)

**Evidence:**

_Link to the artwork PR._

### analytics-transfer

<!-- field-guide:start -->
If you use Google Analytics, add `projects@cncf.io` as an admin of your existing account so it can be moved to a CNCF-managed account. If you don't have GA, note your current analytics setup instead.
<!-- field-guide:end -->

- [ ] Transfer website analytics to the CNCF <!-- checklist:analytics-transfer --> (Issue: #ISSUE_ANALYTICS_TRANSFER)

**Evidence:**

_Analytics status, or N/A._

## Update and document project details

### maintainer-list-pr

<!-- field-guide:start -->
Create/verify `MAINTAINERS.md` and open a PR against the aggregated CNCF maintainer list.
<!-- field-guide:end -->

- [ ] Create a maintainer list and add it to the aggregated CNCF maintainer list <!-- checklist:maintainer-list-pr --> (Issue: #ISSUE_MAINTAINER_LIST_PR)

**Evidence:**

_Link to MAINTAINERS.md and the PR against the aggregated list._

### maintainer-emails

<!-- field-guide:start -->
Email maintainer addresses to `project-onboarding@cncf.io` (not shared publicly). Also link each maintainer's GitHub ID with their LF profile.
<!-- field-guide:end -->

- [ ] Provide maintainer emails for mailing list and Service Desk access <!-- checklist:maintainer-emails --> (Issue: #ISSUE_MAINTAINER_EMAILS)

**Evidence:**

_Date emailed; confirm LF profile linking._

### dco-enabled

<!-- field-guide:start -->
Enable the [DCO GitHub App](https://github.com/apps/dco) on every repo in scope. A CLA may be used in addition to the DCO, not instead of it.
<!-- field-guide:end -->

- [ ] Ensure the DCO app is enabled for all project GitHub repositories <!-- checklist:dco-enabled --> (Issue: #ISSUE_DCO_ENABLED)

**Evidence:**

_List repos with DCO enabled._

### coc-in-readme

<!-- field-guide:start -->
Explicitly reference the CNCF Code of Conduct (or your adopted version) in the project's `README.md` on GitHub.
<!-- field-guide:end -->

- [ ] Reference the CNCF Code of Conduct in README.md <!-- checklist:coc-in-readme --> (Issue: #ISSUE_COC_IN_README)

**Evidence:**

_Link to the README section._

### lf-footer

<!-- field-guide:start -->
Add the Linux Foundation footer to your website per [LF branding guidelines](https://github.com/cncf/foundation/blob/main/website-guidelines.md). If you don't have a dedicated website, adopt these guidelines for `README.md` instead.
<!-- field-guide:end -->

- [ ] Add the LF footer to your website (or README if no website) <!-- checklist:lf-footer --> (Issue: #ISSUE_LF_FOOTER)

**Evidence:**

_Link to footer on the site or README section._

### governance-doc

<!-- field-guide:start -->
Document written, open governance in a `GOVERNANCE.md` file at the root of your repo.
<!-- field-guide:end -->

- [ ] Start a GOVERNANCE.md documenting open governance <!-- checklist:governance-doc --> (Issue: #ISSUE_GOVERNANCE_DOC)

**Evidence:**

_Link to GOVERNANCE.md._

### security-doc

<!-- field-guide:start -->
Document a security policy in a `SECURITY.md` file at the root of your repo. See [CNCF security guidelines](https://contribute.cncf.io/maintainers/security/security-guidelines/#3-securitymd).
<!-- field-guide:end -->

- [ ] Start a SECURITY.md security policy <!-- checklist:security-doc --> (Issue: #ISSUE_SECURITY_DOC)

**Evidence:**

_Link to SECURITY.md._

### openssf-badge

<!-- field-guide:start -->
Register and begin working toward an [OpenSSF Best Practices Badge](https://www.bestpractices.dev/).
<!-- field-guide:end -->

- [ ] Start an OpenSSF Best Practices Badge <!-- checklist:openssf-badge --> (Issue: #ISSUE_OPENSSF_BADGE)

**Evidence:**

_Link to the badge page/status._

### license-scan-import

<!-- field-guide:start -->
Import all repos in scope into CNCF FOSSA or CNCF Snyk (see `license-policy-review`).
<!-- field-guide:end -->

- [ ] Import all project repos into a license scanning service <!-- checklist:license-scan-import --> (Issue: #ISSUE_LICENSE_SCAN_IMPORT)

**Evidence:**

_Service used and confirmation all repos are imported._

## CNCF staff tasks (track and follow up)

These are completed by CNCF staff, not the project. Track them here so you know what to follow up on; check the box once staff confirms completion.

### devstats

<!-- field-guide:start -->
CNCF staff adds the project to [DevStats](https://all.devstats.cncf.io/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to DevStats <!-- checklist:devstats --> (Issue: #ISSUE_DEVSTATS)

**Evidence:**

_Link to the project's DevStats dashboard once available._

### clomonitor

<!-- field-guide:start -->
CNCF staff adds the project to [CLOMonitor](https://clomonitor.io/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to CLOMonitor <!-- checklist:clomonitor --> (Issue: #ISSUE_CLOMONITOR)

**Evidence:**

_Link to the project's CLOMonitor report card._

### lfx-insights-onboarding

<!-- field-guide:start -->
CNCF staff adds the project to [LFX Insights](https://insights.linuxfoundation.org/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to LFX Insights <!-- checklist:lfx-insights-onboarding --> (Issue: #ISSUE_LFX_INSIGHTS_ONBOARDING)

**Evidence:**

_Link to LFX Insights for the project._

### lfx-pcc-activation

<!-- field-guide:start -->
CNCF staff activates the project in the LFX Project Control Center (PCC).
<!-- field-guide:end -->

- [ ] CNCF staff: activate the project in the LFX Project Control Center <!-- checklist:lfx-pcc-activation --> (Issue: #ISSUE_LFX_PCC_ACTIVATION)

**Evidence:**

_Confirmation date once activated._

### landscape-listing-onboarding

<!-- field-guide:start -->
After PCC activation, CNCF staff adds the project to the [Cloud Native Landscape](https://landscape.cncf.io/), including the `lfx_slug` in the landscape configuration file.
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to the Cloud Native Landscape <!-- checklist:landscape-listing-onboarding --> (Issue: #ISSUE_LANDSCAPE_LISTING_ONBOARDING)

**Evidence:**

_Link to the landscape PR/entry._

### license-scanner-team

<!-- field-guide:start -->
CNCF staff adds the maintainers team to the chosen license scanner service (FOSSA or Snyk).
<!-- field-guide:end -->

- [ ] CNCF staff: add the maintainers team to the license scanner <!-- checklist:license-scanner-team --> (Issue: #ISSUE_LICENSE_SCANNER_TEAM)

**Evidence:**

_Confirmation maintainers have scanner access._

### groupsio-list

<!-- field-guide:start -->
CNCF staff creates a groups.io maintainer list for the project in the LFX Project Control Center.
<!-- field-guide:end -->

- [ ] CNCF staff: create a groups.io project maintainer list in PCC <!-- checklist:groupsio-list --> (Issue: #ISSUE_GROUPSIO_LIST)

**Evidence:**

_Groups.io list name/link._

### groupsio-maintainers-list

<!-- field-guide:start -->
CNCF staff adds the project's groups.io maintainer list to `maintainers@cncf.io`.
<!-- field-guide:end -->

- [ ] CNCF staff: add the project's groups.io list to maintainers@cncf.io <!-- checklist:groupsio-maintainers-list --> (Issue: #ISSUE_GROUPSIO_MAINTAINERS_LIST)

**Evidence:**

_Confirmation complete._

### welcome-email

<!-- field-guide:start -->
CNCF staff sends a welcome email confirming maintainer mailing list and Service Desk access.
<!-- field-guide:end -->

- [ ] CNCF staff: send a welcome email confirming maintainer list access <!-- checklist:welcome-email --> (Issue: #ISSUE_WELCOME_EMAIL)

**Evidence:**

_Date welcome email received._

## Final review

### onboarding-complete

<!-- field-guide:start -->
When every item above is complete (or intentionally N/A), post a status update on your CNCF onboarding issue and ask CNCF staff to confirm and close it. Run `./scripts/generate-status-report.sh` to produce a paste-ready update, or `./scripts/generate-status-report.sh --post` to post it directly as a comment.
<!-- field-guide:end -->

- [ ] Final review: confirm all items complete and request sign-off <!-- checklist:onboarding-complete --> (Issue: #ISSUE_ONBOARDING_COMPLETE)

**Evidence:**

_Link to the comment confirming onboarding complete, and the closed onboarding issue._
