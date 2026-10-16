# CNCF Sandbox Onboarding

Single source of truth for completing [CNCF Sandbox onboarding](https://github.com/cncf/sandbox/issues/540) after your project's TOC acceptance vote.

**Work here only:** each item shows `(Issue: …)` until a PR with `Closes #N` **merges**; automation then checks the box and shows `(PR: …)` here and in [README.md](README.md). Edit evidence below; do not edit README or toggle boxes yourself.

Onboarding should be completed within **one month** of acceptance. When everything is done (or intentionally N/A), run `./scripts/generate-status-report.sh` to produce an update for your CNCF onboarding issue.

---

## Required Before Proceeding With Onboarding

A "Project Contribution Agreement" must be completed and any existing trademarks **MUST** be transferred to the Linux Foundation **BEFORE** the CNCF staff onboarding tasks can be completed. Other tasks can be done by projects themselves in the meantime.

### ip-policy-review

<!-- field-guide:start -->
Review the [CNCF IP Policy](https://github.com/cncf/foundation/blob/main/charter.md#11-ip-policy). Ensure the project uses a CNCF-compatible license — inbound projects must use **Apache 2.0**. (Dependency licenses are tracked separately in `license-scan-import`.)
<!-- field-guide:end -->

- [x] Review and understand the CNCF IP Policy <!-- checklist:ip-policy-review --> (Issue: [#36](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/36))

**Evidence:**

All licenses are Apache 2.0

### license-policy-review

<!-- field-guide:start -->
Review the [CNCF Allowlist License Policy](https://github.com/cncf/foundation/blob/main/policies-guidance/allowed-third-party-license-policy.md). This governs licenses used by third-party dependencies. CNCF FOSSA or CNCF Snyk can check compliance — pick one (tracked in `license-scan-import`).
<!-- field-guide:end -->

- [x] Review and understand the CNCF Third Party License Policy <!-- checklist:license-policy-review --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

FOSSA

### trademark-guidelines-review

<!-- field-guide:start -->
Review the [Linux Foundation trademark guidelines](https://www.linuxfoundation.org/trademark-usage/). Let the TOC know if you plan to change your project name.
<!-- field-guide:end -->

- [x] Review and understand the LF trademark guidelines <!-- checklist:trademark-guidelines-review --> (PR: [#43](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/43))

**Evidence:**

No name changes planned

### trademark-transfer

<!-- field-guide:start -->
Transfer any existing trademark and logo assets to the Linux Foundation via the Project Contribution Agreement. CNCF staff sends this document to the contact emails listed in your Sandbox application.
<!-- field-guide:end -->

- [x] Transfer trademark and logo assets to the Linux Foundation <!-- checklist:trademark-transfer --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

Trademarks done, no logos yet.

## Review and understand other documents

### technical-leadership-principles

<!-- field-guide:start -->
Read the [Technical Leadership Principles](https://contribute.cncf.io/maintainers/community/leadership-principles/), which outline expected behavior for maintainers in leadership roles.
<!-- field-guide:end -->

- [x] Review the Technical Leadership Principles <!-- checklist:technical-leadership-principles --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

read it

### project-proposal-process

<!-- field-guide:start -->
Read the [CNCF project proposal process and requirements](https://github.com/cncf/toc/blob/main/process/README.md).
<!-- field-guide:end -->

- [x] Review the project proposal process and requirements <!-- checklist:project-proposal-process --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

read it

### cncf-services-review

<!-- field-guide:start -->
Read about [services available to CNCF projects](https://contribute.cncf.io/resources/project-services/).
<!-- field-guide:end -->

- [ ] Review services available for your project at the CNCF <!-- checklist:cncf-services-review --> (Issue: [#30](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/30))

**Evidence:**

_Notes or links here._

### online-program-guidelines

<!-- field-guide:start -->
Read the CNCF online program guidelines (webinars, meetups, events) provided by CNCF staff.
<!-- field-guide:end -->

- [x] Review the online program guidelines <!-- checklist:online-program-guidelines --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

done

### telemetry-policy-review

<!-- field-guide:start -->
Read the CNCF telemetry data collection and usage policy.
<!-- field-guide:end -->

- [x] Review the telemetry data collection and usage policy <!-- checklist:telemetry-policy-review --> (PR: [#60](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/60))

**Evidence:**

Reviewed

### cncf-staff-office-hours

<!-- field-guide:start -->
Optional: book time with CNCF staff to walk through available resources, work through onboarding tasks together, or ask questions.
<!-- field-guide:end -->

- [ ] Optional: book time with CNCF staff <!-- checklist:cncf-staff-office-hours --> (Issue: [#27](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/27))

**Evidence:**

_Notes or links here._

## Contribute and transfer other materials

### neutral-github-org

<!-- field-guide:start -->
This makes the project transferable to the CNCF's GitHub Enterprise account. If it's already in another GitHub Enterprise account, remove it from there first.
<!-- field-guide:end -->

- [x] Move the project to its own separate neutral GitHub organization <!-- checklist:neutral-github-org --> (PR: [#38](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/38))

**Evidence:**

https://github.com/praxis-proxy

### ghe-invite-accepted

<!-- field-guide:start -->
CNCF will add `thelinuxfoundation` as an organization owner to ensure neutral hosting.
<!-- field-guide:end -->

- [ ] Accept the invite to join the CNCF GitHub Enterprise account <!-- checklist:ghe-invite-accepted --> (Issue: [#25](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/25))

**Evidence:**

_Notes or links here._

### slack-migration

<!-- field-guide:start -->
CNCF staff can help. This improves discoverability, lets CNCF enforce its Code of Conduct, and enables unlimited message retention. If you already have a large Slack/Discord community, CNCF may instead link to it from a pointer channel in the CNCF Slack workspace.
<!-- field-guide:end -->

- [x] Migrate Slack channels to the Kubernetes or CNCF Slack workspace <!-- checklist:slack-migration --> (PR: [#41](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/41))

**Evidence:**

Channel exists already https://cloud-native.slack.com/archives/C0BK0RSP5RC

### maintainers-circle-slack

<!-- field-guide:start -->
Join `#maintainers-circle` on CNCF Slack to find and share knowledge with other project teams.
<!-- field-guide:end -->

- [x] Join the #maintainers-circle Slack channel <!-- checklist:maintainers-circle-slack --> (PR: [#49](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/49))

**Evidence:**

Joined `#maintainers-circle` on CNCF Slack: https://cloud-native.slack.com/archives/C014YQ8CDCG/p1791906432352529

### domain-transfer

<!-- field-guide:start -->
If your project has its own domain(s), transfer them to the CNCF. LF Contact: `projects@cncf.io`. Project Selection: CNCF.
<!-- field-guide:end -->

- [x] Transfer project domain(s) to the CNCF <!-- checklist:domain-transfer --> (PR: [#42](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/42))

**Evidence:**

https://jira.linuxfoundation.org/plugins/servlet/desk/portal/2?requestGroup=19

### artwork-pr

<!-- field-guide:start -->
Submit project artwork to [cncf/artwork](https://github.com/cncf/artwork). If you don't have artwork, CNCF can help design some.
<!-- field-guide:end -->

- [x] Submit a pull request with your artwork <!-- checklist:artwork-pr --> (PR: [#62](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/62))

**Evidence:**

[Artwork PR](https://github.com/cncf/artwork/pull/687)

### analytics-transfer

<!-- field-guide:start -->
If you use Google Analytics, add `projects@cncf.io` as an admin of your existing account so it can be moved to a CNCF-managed account. If you don't have GA, note your current analytics setup instead.
<!-- field-guide:end -->

- [ ] Transfer website analytics to the CNCF <!-- checklist:analytics-transfer --> (Issue: [#20](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/20))

**Evidence:**

_Notes or links here._

## Update and document project details

### dot-project-repo

<!-- field-guide:start -->
Create or ensure your [`.project` repo](https://contribute.cncf.io/blog/2026/04/22/introducing-dot-project-for-maintainers) is up to date with maintainer information.
<!-- field-guide:end -->

- [x] Create or update the .project repo with maintainer information <!-- checklist:dot-project-repo --> (PR: [#59](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/59))

**Evidence:**

https://github.com/praxis-proxy/.project

### lfx-profile

<!-- field-guide:start -->
Ensure each maintainer has an up-to-date [LFX Individual Dashboard profile](https://openprofile.dev/) with an active email address for mailing list and Service Desk access.
<!-- field-guide:end -->

- [ ] Ensure each maintainer has an up-to-date LFX Individual Dashboard profile <!-- checklist:lfx-profile --> (Issue: [#54](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/54))

**Evidence:**

_Notes or links here._

### dco-enabled

<!-- field-guide:start -->
Enable the [DCO GitHub App](https://github.com/apps/dco) on every repo in scope. A CLA may be used in addition to the DCO, not instead of it.
<!-- field-guide:end -->

- [x] Ensure the DCO app is enabled for all project GitHub repositories <!-- checklist:dco-enabled --> (PR: [#44](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/44))

**Evidence:**

All

### coc-in-readme

<!-- field-guide:start -->
Explicitly reference the CNCF Code of Conduct (or your adopted version) in the project's `README.md` on GitHub.
<!-- field-guide:end -->

- [x] Reference the CNCF Code of Conduct in README.md <!-- checklist:coc-in-readme --> (PR: [#48](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/48))

**Evidence:**

The [project README](https://github.com/praxis-proxy/praxis/blob/main/README.md#contributing) references the Code of Conduct, and [`CODE_OF_CONDUCT.md`](https://github.com/praxis-proxy/praxis/blob/main/CODE_OF_CONDUCT.md) explicitly adopts the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/main/code-of-conduct.md).

### lf-footer

<!-- field-guide:start -->
Add the Linux Foundation footer to your website per [LF branding guidelines](https://github.com/cncf/foundation/blob/main/policies-guidance/website-guidelines.md). If you don't have a dedicated website, adopt these guidelines for `README.md` instead.
<!-- field-guide:end -->

- [x] Add the LF footer to your website (or README if no website) <!-- checklist:lf-footer --> (PR: [#61](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/61))

**Evidence:**

https://github.com/praxis-proxy/praxis-proxy.github.io/pull/23

### governance-doc

<!-- field-guide:start -->
Document written, open governance in a `GOVERNANCE.md` file at the root of your repo.
<!-- field-guide:end -->

- [x] Start a GOVERNANCE.md documenting open governance <!-- checklist:governance-doc --> (PR: [#46](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/46))

**Evidence:**

https://github.com/praxis-proxy/praxis/blob/main/GOVERNANCE.md

### security-doc

<!-- field-guide:start -->
Document a security policy in a `SECURITY.md` file at the root of your repo. See [CNCF security guidelines](https://contribute.cncf.io/maintainers/security/security-guidelines/#3-securitymd).
<!-- field-guide:end -->

- [x] Start a SECURITY.md security policy <!-- checklist:security-doc --> (PR: [#45](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/45))

**Evidence:**

https://github.com/praxis-proxy/praxis/blob/main/SECURITY.md

### openssf-badge

<!-- field-guide:start -->
Register and begin working toward an [OpenSSF Best Practices Badge](https://www.bestpractices.dev/).
<!-- field-guide:end -->

- [x] Start an OpenSSF Best Practices Badge <!-- checklist:openssf-badge --> (PR: [#47](https://github.com/praxis-proxy/praxis-cncf-on-boarding/pull/47))

**Evidence:**

Registered and passing (100%): https://www.bestpractices.dev/projects/13756

### license-scan-import

<!-- field-guide:start -->
Import all repos in scope into CNCF FOSSA or CNCF Snyk (see `license-policy-review`).
<!-- field-guide:end -->

- [ ] Import all project repos into a license scanning service <!-- checklist:license-scan-import --> (Issue: [#11](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/11))

**Evidence:**

_Notes or links here._

## CNCF staff tasks to support the project

These are completed by CNCF staff, not the project. Track them here so you know what to follow up on; check the box once staff confirms completion.

### devstats

<!-- field-guide:start -->
CNCF staff adds the project to [DevStats](https://all.devstats.cncf.io/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to DevStats <!-- checklist:devstats --> (Issue: [#10](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/10))

**Evidence:**

_Notes or links here._

### clomonitor

<!-- field-guide:start -->
CNCF staff adds the project to [CLOMonitor](https://clomonitor.io/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to CLOMonitor <!-- checklist:clomonitor --> (Issue: [#9](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/9))

**Evidence:**

_Notes or links here._

### lfx-insights-onboarding

<!-- field-guide:start -->
CNCF staff adds the project to [LFX Insights](https://insights.linuxfoundation.org/).
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to LFX Insights <!-- checklist:lfx-insights-onboarding --> (Issue: [#8](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/8))

**Evidence:**

_Notes or links here._

### lfx-pcc-activation

<!-- field-guide:start -->
CNCF staff activates the project in the LFX Project Control Center (PCC).
<!-- field-guide:end -->

- [ ] CNCF staff: activate the project in the LFX Project Control Center <!-- checklist:lfx-pcc-activation --> (Issue: [#7](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/7))

**Evidence:**

_Notes or links here._

### landscape-listing-onboarding

<!-- field-guide:start -->
After PCC activation, CNCF staff adds the project to the [Cloud Native Landscape](https://landscape.cncf.io/), including the `lfx_slug` in the landscape configuration file.
<!-- field-guide:end -->

- [ ] CNCF staff: add the project to the Cloud Native Landscape <!-- checklist:landscape-listing-onboarding --> (Issue: [#6](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/6))

**Evidence:**

_Notes or links here._

### license-scanner-team

<!-- field-guide:start -->
CNCF staff adds the maintainers team to the chosen license scanner service (FOSSA or Snyk).
<!-- field-guide:end -->

- [ ] CNCF staff: add the maintainers team to the license scanner <!-- checklist:license-scanner-team --> (Issue: [#5](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/5))

**Evidence:**

_Notes or links here._

### groupsio-list

<!-- field-guide:start -->
CNCF staff creates a groups.io maintainer list for the project in the LFX Project Control Center.
<!-- field-guide:end -->

- [x] CNCF staff: create a groups.io project maintainer list in PCC <!-- checklist:groupsio-list --> (Issue: [#4](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/4))

**Evidence:**

_Notes or links here._

### cncf-service-desk

<!-- field-guide:start -->
CNCF staff creates the project in the CNCF Service Desk.
<!-- field-guide:end -->

- [x] CNCF staff: create project in CNCF Service Desk <!-- checklist:cncf-service-desk --> (Issue: [#55](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/55))

**Evidence:**

_Notes or links here._

### onboard-project-workflow

<!-- field-guide:start -->
CNCF staff runs the [Onboard Project workflow](https://github.com/cncf/maintainer-manager/actions/workflows/onboard-project.yml).
<!-- field-guide:end -->

- [x] CNCF staff: run Onboard Project workflow <!-- checklist:onboard-project-workflow --> (Issue: [#56](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/56))

**Evidence:**

_Notes or links here._

### groupsio-maintainers-list

<!-- field-guide:start -->
CNCF staff adds the project's groups.io maintainer list to `maintainers@cncf.io`.
<!-- field-guide:end -->

- [x] CNCF staff: add the project's groups.io list to maintainers@cncf.io <!-- checklist:groupsio-maintainers-list --> (Issue: [#3](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/3))

**Evidence:**

_Notes or links here._

### welcome-email

<!-- field-guide:start -->
CNCF staff sends a welcome email confirming maintainer mailing list and Service Desk access.
<!-- field-guide:end -->

- [ ] CNCF staff: send a welcome email confirming maintainer list access <!-- checklist:welcome-email --> (Issue: [#2](https://github.com/praxis-proxy/praxis-cncf-on-boarding/issues/2))

**Evidence:**

_Notes or links here._
