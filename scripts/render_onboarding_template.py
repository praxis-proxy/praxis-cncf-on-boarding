#!/usr/bin/env python3
"""Render ONBOARDING.md from .github/onboarding-items.json (template maintenance).

Run this after editing onboarding-items.json to regenerate ONBOARDING.md.
Re-running is safe before bootstrap (placeholders only); after bootstrap,
regenerating would reset Issue/PR links, so only run this when adding or
restructuring checklist items, not during normal use.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist_tracking import issue_token_placeholder  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ITEMS_FILE = ROOT / ".github" / "onboarding-items.json"


def checklist_line(slug: str, title: str) -> str:
    return f"- [ ] {title} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"


def flag_prefix(item: dict) -> str:
    if item.get("critical"):
        return "[Critical] "
    if item.get("staff"):
        return "[CNCF Staff] "
    if item.get("optional"):
        return "[Optional] "
    return ""


def render() -> str:
    data = json.loads(ITEMS_FILE.read_text())
    source_issue = data.get("source_issue", "")

    lines = [
        "# CNCF Sandbox Onboarding",
        "",
        f"Single source of truth for completing [CNCF Sandbox onboarding]({source_issue}) after your project's TOC acceptance vote.",
        "",
        "**Work here only:** each item shows `(Issue: …)` until you open a PR with `Closes #N`; automation then checks the box and shows `(PR: …)` here and in [README.md](README.md). Edit evidence below; do not edit README or toggle boxes yourself.",
        "",
        "Onboarding should be completed within **one month** of acceptance. When everything is done (or intentionally N/A), run `./scripts/generate-status-report.sh` to produce an update for your CNCF onboarding issue.",
        "",
        "---",
        "",
    ]

    for category in data["categories"]:
        lines.append(f"## {category['heading']}")
        lines.append("")
        if category.get("intro"):
            lines.append(category["intro"])
            lines.append("")

        for item in category["items"]:
            slug = item["slug"]
            title = flag_prefix(item) + item["title"]

            lines.append(f"### {slug}")
            lines.append("")
            lines.append("<!-- field-guide:start -->")
            lines.extend(item["guide"].splitlines())
            lines.append("<!-- field-guide:end -->")
            lines.append("")
            lines.append(checklist_line(slug, item["title"]))
            lines.append("")
            lines.append("**Evidence:**")
            lines.append("")
            lines.append(item.get("evidence_hint", "_Notes or links here._"))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    out = ROOT / "ONBOARDING.md"
    out.write_text(render())
    print(f"Wrote {out}")
