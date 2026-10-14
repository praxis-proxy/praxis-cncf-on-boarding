#!/usr/bin/env python3
"""Render ONBOARDING.md from checklist JSON.

Default input is .github/onboarding-items.json (guide catalog / template
maintenance). Bootstrap writes .github/onboarding-items.generated.json from
the project's live CNCF issue and renders from that instead.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist_tracking import issue_token_placeholder  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ITEMS = ROOT / ".github" / "onboarding-items.json"


def checklist_line(slug: str, title: str, checked: bool = False) -> str:
    mark = "x" if checked else " "
    return f"- [{mark}] {title} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"


def flag_prefix(item: dict) -> str:
    if item.get("critical"):
        return "[Critical] "
    if item.get("staff"):
        return "[CNCF Staff] "
    if item.get("optional"):
        return "[Optional] "
    return ""


def render(data: dict) -> str:
    source_issue = data.get("source_issue", "")

    lines = [
        "# CNCF Sandbox Onboarding",
        "",
        f"Single source of truth for completing [CNCF Sandbox onboarding]({source_issue}) after your project's TOC acceptance vote.",
        "",
        "**Work here only:** each item shows `(Issue: …)` until a PR with `Closes #N` **merges**; automation then checks the box and shows `(PR: …)` here and in [README.md](README.md). Edit evidence below; do not edit README or toggle boxes yourself.",
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
            checked = bool(item.get("checked"))

            lines.append(f"### {slug}")
            lines.append("")
            lines.append("<!-- field-guide:start -->")
            lines.extend(item["guide"].splitlines())
            lines.append("<!-- field-guide:end -->")
            lines.append("")
            lines.append(checklist_line(slug, item["title"], checked=checked))
            lines.append("")
            lines.append("**Evidence:**")
            lines.append("")
            lines.append(item.get("evidence_hint", "_Notes or links here._"))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--items",
        type=Path,
        default=DEFAULT_ITEMS,
        help="Checklist JSON to render (default: guide catalog)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "ONBOARDING.md",
        help="Output markdown path",
    )
    args = parser.parse_args()
    data = json.loads(args.items.read_text(encoding="utf-8"))
    args.output.write_text(render(data), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
