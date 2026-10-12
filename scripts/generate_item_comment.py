#!/usr/bin/env python3
"""Render a single checklist item's section as a comment for the external
CNCF onboarding issue.

Used by .github/workflows/sync-checklist.yml right after a checklist item's
local issue closes (i.e. its PR merged), so CNCF can see progress item by
item instead of only at the very end.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONBOARDING_FILE = ROOT / "ONBOARDING.md"
ITEMS_FILE = ROOT / ".github" / "onboarding-items.json"
METADATA_FILE = ROOT / ".github" / "project-metadata.json"

ITEM_HEADING = re.compile(r"^### ([a-z0-9-]+)\s*$")
CATEGORY_HEADING = re.compile(r"^## (.+?)\s*$")
CHECKLIST_LINE = re.compile(r"^- \[([ xX])\].*<!-- checklist:([a-z0-9-]+) -->(.*)$")
EVIDENCE_HEADING = re.compile(r"^\*\*Evidence:\*\*\s*$")
ANY_HEADING = re.compile(r"^#{1,6}\s")


def extract_item(text: str, slug: str) -> dict:
    """Pull {title, checked, tracking, evidence, category} for one slug."""
    current_slug = None
    current_category = ""
    collecting_evidence = False
    evidence_lines: list[str] = []
    result = {"title": "", "checked": False, "tracking": "", "evidence": "", "category": ""}
    found = False

    for line in text.splitlines():
        cat = CATEGORY_HEADING.match(line)
        if cat and not ITEM_HEADING.match(line):
            current_category = cat.group(1).strip()

        heading = ITEM_HEADING.match(line)
        if heading:
            if found:
                break  # left the target item's section
            current_slug = heading.group(1)
            collecting_evidence = False
            evidence_lines = []
            if current_slug == slug:
                found = True
                result["category"] = current_category
            continue

        if not found:
            continue

        if ANY_HEADING.match(line) and not heading:
            collecting_evidence = False
            continue

        match = CHECKLIST_LINE.match(line)
        if match and match.group(2) == slug:
            result["checked"] = match.group(1).lower() == "x"
            result["tracking"] = match.group(3).strip()
            title = re.sub(r"^- \[[ xX]\]\s*", "", line.strip())
            title = re.sub(r"\s*<!-- checklist:[a-z0-9-]+ -->.*$", "", title)
            result["title"] = title.strip()
            continue

        if EVIDENCE_HEADING.match(line.strip()):
            collecting_evidence = True
            continue

        if collecting_evidence:
            stripped = line.strip()
            if stripped and not (stripped.startswith("_") and stripped.endswith("_")):
                evidence_lines.append(stripped)

    result["evidence"] = "\n".join(evidence_lines).strip()
    return result


def render_comment(item: dict, slug: str, local_repo: str, local_issue_number: str) -> str:
    box = "x" if item["checked"] else " "
    title = item["title"] or slug
    lines = [
        f"<!-- onboarding-item-update:{slug} -->",
        f"**Progress update — {item['category']}**" if item["category"] else "**Progress update**",
        "",
        f"- [{box}] {title}",
    ]
    if item["evidence"]:
        for evidence_line in item["evidence"].splitlines():
            lines.append(f"  {evidence_line}")

    footer_bits = []
    tracking = item["tracking"].strip()
    if tracking.startswith("(") and tracking.endswith(")"):
        # Strip exactly the one outer wrapping paren pair added by
        # pr_token_linked/issue_token_linked; the inner markdown link has its
        # own matching parens that must be preserved.
        tracking = tracking[1:-1]
    if tracking:
        footer_bits.append(tracking)
    if local_repo and local_issue_number:
        footer_bits.append(
            f"tracking issue [{local_repo}#{local_issue_number}](https://github.com/{local_repo}/issues/{local_issue_number})"
        )
    if footer_bits:
        lines.append("")
        lines.append(f"<sub>{' · '.join(footer_bits)}</sub>")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--local-repo", default="")
    parser.add_argument("--local-issue-number", default="")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not ONBOARDING_FILE.is_file():
        print("Error: ONBOARDING.md not found.", file=sys.stderr)
        return 1

    item = extract_item(ONBOARDING_FILE.read_text(encoding="utf-8"), args.slug)
    if not item["title"]:
        print(f"Error: slug '{args.slug}' not found in ONBOARDING.md.", file=sys.stderr)
        return 1

    comment = render_comment(item, args.slug, args.local_repo, args.local_issue_number)
    args.output.write_text(comment, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
