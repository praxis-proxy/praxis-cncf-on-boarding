#!/usr/bin/env python3
"""Re-sync ONBOARDING.md from a live CNCF onboarding issue.

Preserves Evidence blocks for slugs that still exist. Used after bootstrap when
the CNCF checklist changes, or to align an already-bootstrapped repo.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_cncf_checklist import build_checklist  # noqa: E402
from render_onboarding_template import render  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / ".github" / "onboarding-items.json"
GENERATED = ROOT / ".github" / "onboarding-items.generated.json"
ONBOARDING = ROOT / "ONBOARDING.md"
METADATA = ROOT / ".github" / "project-metadata.json"

ITEM_HEADING = re.compile(r"^### ([a-z0-9-]+)\s*$")
EVIDENCE_HEADING = re.compile(r"^\*\*Evidence:\*\*\s*$")
ANY_HEADING = re.compile(r"^#{1,6}\s")
TRACKING = re.compile(r" \((?:Issue|PR):.*\)\s*$")


def extract_evidence(text: str) -> dict[str, str]:
    """Map slug -> evidence body (excluding placeholder-only hints)."""
    evidence: dict[str, str] = {}
    current = None
    collecting = False
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, collecting, buf
        if current and buf:
            body = "\n".join(buf).strip()
            if body and not (body.startswith("_") and body.endswith("_") and len(body) < 80):
                evidence[current] = body
        current, collecting, buf = None, False, []

    for line in text.splitlines():
        heading = ITEM_HEADING.match(line)
        if heading:
            flush()
            current = heading.group(1)
            continue
        if current is None:
            continue
        if EVIDENCE_HEADING.match(line.strip()):
            collecting = True
            buf = []
            continue
        if collecting:
            if ANY_HEADING.match(line) and not ITEM_HEADING.match(line):
                flush()
                continue
            if ITEM_HEADING.match(line):
                flush()
                current = ITEM_HEADING.match(line).group(1)
                continue
            buf.append(line)

    flush()
    return evidence


def extract_tracking(text: str) -> dict[str, str]:
    """Map slug -> full tracking suffix like '(Issue: [#12](...))'."""
    tracking: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        heading = ITEM_HEADING.match(line)
        if heading:
            current = heading.group(1)
            continue
        if current and "<!-- checklist:" in line:
            m = TRACKING.search(line)
            if m:
                tracking[current] = m.group(0).strip()
            current = None
    return tracking


def apply_preserved(onboarding: str, evidence: dict[str, str], tracking: dict[str, str]) -> str:
    lines = onboarding.splitlines()
    out: list[str] = []
    current = None
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = ITEM_HEADING.match(line)
        if heading:
            current = heading.group(1)
            out.append(line)
            i += 1
            continue

        if current and f"<!-- checklist:{current} -->" in line:
            if current in tracking:
                base = TRACKING.sub("", line.rstrip())
                out.append(f"{base} {tracking[current]}")
            else:
                out.append(line)
            i += 1
            continue

        if current and EVIDENCE_HEADING.match(line.strip()):
            out.append(line)
            i += 1
            # Skip generated hint lines until next heading/blank section end
            while i < len(lines) and not ITEM_HEADING.match(lines[i]) and not (
                lines[i].startswith("## ") and not lines[i].startswith("### ")
            ):
                # stop before next ### or ##
                if lines[i].startswith("#"):
                    break
                i += 1
            out.append("")
            if current in evidence:
                out.append(evidence[current])
            else:
                out.append("_Notes or links here._")
            out.append("")
            current = None
            continue

        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-url", default="", help="CNCF onboarding issue URL")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--output-json", type=Path, default=GENERATED)
    parser.add_argument("--output-md", type=Path, default=ONBOARDING)
    args = parser.parse_args()

    issue_url = args.issue_url
    if not issue_url and METADATA.is_file():
        issue_url = json.loads(METADATA.read_text(encoding="utf-8")).get(
            "onboarding_issue_url", ""
        )
    if not issue_url:
        print("Error: pass --issue-url or set onboarding_issue_url in project-metadata.json", file=sys.stderr)
        return 1

    old_text = args.output_md.read_text(encoding="utf-8") if args.output_md.is_file() else ""
    evidence = extract_evidence(old_text) if old_text else {}
    tracking = extract_tracking(old_text) if old_text else {}

    data = build_checklist(issue_url, args.catalog)
    args.output_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    rendered = render(data)
    merged = apply_preserved(rendered, evidence, tracking)
    args.output_md.write_text(merged, encoding="utf-8")

    total = sum(len(c["items"]) for c in data["categories"])
    print(
        f"Synced {total} items from {issue_url} → {args.output_md} "
        f"(preserved evidence for {len(evidence)} slug(s), tracking for {len(tracking)} slug(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
