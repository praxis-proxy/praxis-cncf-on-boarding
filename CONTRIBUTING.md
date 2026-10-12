# Contributing to Onboarding

This repository tracks [CNCF Sandbox onboarding](https://github.com/cncf/sandbox/issues/487) after your project's TOC acceptance vote.

## Workflow

### 1. Bootstrap checklist issues

After creating your repository from this template, run:

```bash
./scripts/bootstrap-issues.sh
```

This prompts for basic info (project name, your CNCF onboarding issue URL, acceptance date), creates one GitHub issue per checklist item, and writes issue links onto the matching checklist lines in **[ONBOARDING.md](ONBOARDING.md)**.

### 2. Work on checklist items (ONBOARDING.md only)

Open **[ONBOARDING.md](ONBOARDING.md)** and stay in that file for all onboarding work.

Each section includes:

- Instructions (guide) for what to complete, taken from the CNCF onboarding checklist
- A checklist line with `(Issue: [#N](…))` (after bootstrap)
- An **Evidence** area for links/notes proving completion

Pick an issue, edit the relevant section(s) in `ONBOARDING.md`, and open a pull request with `Closes #N`. Do **not** manually check the checklist box — automation marks it `[x]` and updates `(PR: …)` in **both** `ONBOARDING.md` and [README.md](README.md). **Do not edit README** for evidence or tracking.

Progress and the checklist dashboard live in README only; they update automatically.

### 3. Close issues via pull requests

Reference the checklist issue in your PR description:

```markdown
Closes #12
```

Supported keywords: `Closes`, `Fixes`, `Resolves` (case insensitive).

### 4. Checklist sync

The [sync-checklist-pr workflow](.github/workflows/sync-checklist-pr.yml) runs when you open or update a PR with `Closes #N`. On your PR branch it:

1. Replaces `(Issue: …)` with `(PR: …)`
2. Checks the box (`[x]`) in `ONBOARDING.md`
3. Mirrors those lines and refreshes progress in README

The [sync-checklist workflow](.github/workflows/sync-checklist.yml) runs when the local issue closes (i.e. the PR merged, or the issue was closed directly for a staff-tracked item). It:

1. Checks the box on `main` directly if it wasn't already (no follow-up bot PR)
2. **Posts a comment on your CNCF onboarding issue** with just that item — checkbox, evidence, and a link back to the tracking issue/PR

This gives CNCF live, item-by-item visibility instead of one report at the end.

### 5. CNCF staff items

Items labeled `[CNCF Staff]` are completed by CNCF, not by your project (DevStats, CLOMonitor, LFX Insights, PCC activation, landscape listing, etc.). Track them here so you know what to follow up on, and check the box once CNCF confirms — closing that issue also posts a progress comment.

### 6. One-time setup for automatic CNCF comments

The per-item comment step needs two things, both set once:

1. **`onboarding_issue_url` in `.github/project-metadata.json`** — set automatically by `./scripts/bootstrap-issues.sh` (or edit the file directly).
2. **A `CNCF_SANDBOX_TOKEN` repository secret** — a GitHub personal access token with `public_repo` scope is enough, since `cncf/sandbox` is public. `GITHUB_TOKEN` cannot post to a different repository, so this PAT is required. Add it under **Settings → Secrets and variables → Actions**.

If either is missing, the workflow logs a message and skips the comment — it does not fail the run.

### 7. Full status report (optional)

For an initial full update, or to re-sync if some automatic comments failed, generate a report matching the original CNCF checklist structure:

```bash
# Write ONBOARDING-STATUS.md (gitignored, generated)
./scripts/generate-status-report.sh

# Or post it directly as a comment on your CNCF onboarding issue
./scripts/generate-status-report.sh --post
```

## Branch naming

Use descriptive branch names:

- `onboarding/maintainers-file`
- `onboarding/security-policy`
- `onboarding/artwork-pr`

## Pull request template

Pull requests should include:

- `Closes #N` for each completed item
- Which section(s) in `ONBOARDING.md` were updated
- A brief summary of changes

## Labels

Issues created by the bootstrap script use these labels:

| Label | Meaning |
| --- | --- |
| `onboarding-item` | Part of the onboarding checklist |
| `checklist:<slug>` | Maps to a specific checkbox in ONBOARDING.md |
| `critical` | Required before CNCF staff can proceed |
| `optional` | Optional item |
| `cncf-staff` | Completed by CNCF staff; track for follow-up |
| `category:*` | Onboarding section grouping |

## References

- [CNCF Sandbox onboarding issue this template is based on](https://github.com/cncf/sandbox/issues/487)
- [CNCF Sandbox repository](https://github.com/cncf/sandbox)
- [CNCF project services](https://contribute.cncf.io/resources/project-services/)
