#!/usr/bin/env python3
"""Issue/PR tracking on checklist lines in ONBOARDING.md and README.md.

Single source of truth is ONBOARDING.md. README.md mirrors checklist lines
and holds the only progress indicator. Checklist lines look like:

    - [ ] Title <!-- checklist:slug --> (Issue: [#12](https://github.com/org/repo/issues/12))

After a PR with `Closes #12` is opened, the line becomes:

    - [x] Title <!-- checklist:slug --> (PR: [#34](https://github.com/org/repo/pull/34))
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ONBOARDING_FILENAME = "ONBOARDING.md"

CHECKLIST_LINE = re.compile(r"^- \[[ xX]\].*<!-- checklist:[a-z0-9-]+ -->.*$")
CHECKLIST_LINE_PARTS = re.compile(
    r"^- \[([ xX])\] (.+?) <!-- checklist:[a-z0-9-]+ -->\s*(\(.*\))?\s*$"
)
CHECKLIST_SLUG = re.compile(r"<!-- checklist:([a-z0-9-]+) -->")
TRACKING_SUFFIX = re.compile(r" \((Issue|PR):.*\)\s*$")

START_DASHBOARD = "<!-- onboarding-dashboard:start -->"
END_DASHBOARD = "<!-- onboarding-dashboard:end -->"
START_PROGRESS = "<!-- checklist-progress:start -->"
END_PROGRESS = "<!-- checklist-progress:end -->"
BAR_WIDTH = 20

# Item headings are H3 (`### slug`); category headings are H2 with prose text
# and never match this pattern, so they're safely ignored by the parsers below.
ITEM_HEADING = re.compile(r"^### ([a-z0-9-]+)\s*$")


def onboarding_path(root: Path) -> Path:
    return root / ONBOARDING_FILENAME


def issue_token_placeholder(slug: str) -> str:
    token = f"#ISSUE_{slug.upper().replace('-', '_')}"
    return f"(Issue: {token})"


def issue_token_linked(repo: str, issue_number: int) -> str:
    return f"(Issue: [#{issue_number}](https://github.com/{repo}/issues/{issue_number}))"


def pr_token_linked(repo: str, pr_number: int) -> str:
    return f"(PR: [#{pr_number}](https://github.com/{repo}/pull/{pr_number}))"


def strip_tracking_suffix(line: str) -> str:
    return TRACKING_SUFFIX.sub("", line.rstrip())


def set_checklist_line_tracking(line: str, slug: str, tracking: str) -> str:
    marker = f"<!-- checklist:{slug} -->"
    if marker not in line or not CHECKLIST_LINE.match(line):
        return line
    base = strip_tracking_suffix(line)
    return f"{base} {tracking}"


def apply_issue_link(content: str, slug: str, issue_number: int, repo: str) -> str:
    placeholder = issue_token_placeholder(slug)
    linked = issue_token_linked(repo, issue_number)
    lines = []
    for line in content.splitlines():
        if f"<!-- checklist:{slug} -->" in line and placeholder in line:
            lines.append(line.replace(placeholder, linked))
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def apply_pr_link(content: str, slug: str, pr_number: int, repo: str) -> str:
    tracking = pr_token_linked(repo, pr_number)
    lines = [
        set_checklist_line_tracking(line, slug, tracking)
        if f"<!-- checklist:{slug} -->" in line
        else line
        for line in content.splitlines()
    ]
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def mark_checkbox_complete(content: str, slug: str) -> str:
    marker = f"<!-- checklist:{slug} -->"
    pattern = re.compile(rf"^- \[ \] (.+?{re.escape(marker)})( .*)?$", re.MULTILINE)

    def repl(match: "re.Match[str]") -> str:
        suffix = match.group(2) or ""
        return f"- [x] {match.group(1)}{suffix}"

    return pattern.sub(repl, content, count=1)


def slug_for_issue(registry: Dict[str, int], issue_number: int) -> Optional[str]:
    for slug, num in registry.items():
        if int(num) == int(issue_number):
            return slug
    return None


def load_issue_registry(path: Path) -> Dict[str, int]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: int(v) for k, v in data.get("issues", {}).items()}


def parse_closing_issues(text: str) -> List[int]:
    pattern = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.IGNORECASE)
    return sorted({int(m.group(1)) for m in pattern.finditer(text or "")})


def slug_complete(content: str, slug: str) -> bool:
    marker = f"<!-- checklist:{slug} -->"
    for line in content.splitlines():
        if marker in line and re.match(r"^- \[[xX]\]", line):
            return True
    return False


def compute_progress(content: str) -> Tuple[int, int]:
    slugs = sorted(set(CHECKLIST_SLUG.findall(content)))
    completed = sum(1 for slug in slugs if slug_complete(content, slug))
    return completed, len(slugs)


def render_progress_block(completed: int, total: int) -> str:
    percent = round((completed / total) * 100) if total else 0
    filled = round((completed / total) * BAR_WIDTH) if total else 0
    bar = ("█" * filled) + ("░" * (BAR_WIDTH - filled))
    return (
        f"> **Onboarding progress:** **{completed} / {total}** items complete ({percent}%)  \n"
        f"> `{bar}` {percent}%"
    )


def update_marked_block(path: Path, start: str, end: str, block: str) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    if start not in content or end not in content:
        return False
    pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    replacement = f"{start}\n{block}\n{end}" if block else f"{start}{end}"
    new_content = pattern.sub(replacement, content, count=1)
    if new_content == content:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


def build_readme_dashboard(onboarding: str) -> str:
    lines: List[str] = []
    current_slug: Optional[str] = None
    checklist_row: Optional[str] = None

    def flush() -> None:
        nonlocal current_slug, checklist_row
        if current_slug and checklist_row:
            lines.append(f"- {checklist_row}")
        current_slug, checklist_row = None, None

    in_guide = False
    for raw in onboarding.splitlines():
        heading = ITEM_HEADING.match(raw)
        if heading:
            flush()
            current_slug = heading.group(1)
            in_guide = False
            continue
        if current_slug is None:
            continue
        stripped = raw.strip()
        if stripped == "<!-- field-guide:start -->":
            in_guide = True
            continue
        if stripped == "<!-- field-guide:end -->":
            in_guide = False
            continue
        if in_guide:
            continue
        parts = CHECKLIST_LINE_PARTS.match(raw.strip())
        if parts:
            checked = parts.group(1).lower() == "x"
            title = parts.group(2).strip()
            tracking = (parts.group(3) or "").strip()
            emoji = "✅" if checked else "⬜"
            checklist_row = f"{emoji} [{title}]({ONBOARDING_FILENAME}#{current_slug}) {tracking}".rstrip()

    flush()
    return "\n".join(lines).rstrip() + "\n"


def sync_readme(root: Path) -> bool:
    readme = root / "README.md"
    onboarding = onboarding_path(root)
    if not readme.is_file() or not onboarding.is_file():
        return False

    onboarding_text = onboarding.read_text(encoding="utf-8")
    completed, total = compute_progress(onboarding_text)
    progress_block = render_progress_block(completed, total)
    dashboard_block = build_readme_dashboard(onboarding_text)

    changed_progress = update_marked_block(readme, START_PROGRESS, END_PROGRESS, progress_block)
    changed_dashboard = update_marked_block(readme, START_DASHBOARD, END_DASHBOARD, dashboard_block)
    return changed_progress or changed_dashboard


def update_files_for_pr(root: Path, repo: str, pr_number: int, issue_numbers: List[int]) -> Tuple[bool, List[str]]:
    registry_path = root / ".github" / "issue-registry.json"
    registry = load_issue_registry(registry_path)
    path = onboarding_path(root)
    before = path.read_text(encoding="utf-8")
    content = before
    changed_slugs: List[str] = []

    for issue_number in issue_numbers:
        slug = slug_for_issue(registry, issue_number)
        if not slug:
            continue
        # Closes #N is enough: swap Issue -> PR and check the box in one step.
        content = apply_pr_link(content, slug, pr_number, repo)
        content = mark_checkbox_complete(content, slug)
        changed_slugs.append(slug)

    if not changed_slugs or content == before:
        return False, []

    path.write_text(content, encoding="utf-8")
    sync_readme(root)
    return True, changed_slugs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    sub = parser.add_subparsers(dest="command", required=True)

    link_issue = sub.add_parser("link-issue")
    link_issue.add_argument("--slug", required=True)
    link_issue.add_argument("--number", type=int, required=True)
    link_issue.add_argument("--repo", required=True)

    link_pr = sub.add_parser("link-pr")
    link_pr.add_argument("--repo", required=True)
    link_pr.add_argument("--pr-number", type=int, required=True)
    link_pr.add_argument("--issue-numbers", nargs="+", type=int, required=True)

    complete = sub.add_parser("complete-checkbox")
    complete.add_argument("--slug", required=True)

    sub.add_parser("sync-readme")
    sub.add_parser("progress")

    args = parser.parse_args()
    root = args.root
    path = onboarding_path(root)

    if args.command == "link-issue":
        text = apply_issue_link(path.read_text(encoding="utf-8"), args.slug, args.number, args.repo)
        path.write_text(text, encoding="utf-8")
        sync_readme(root)
        return 0

    if args.command == "link-pr":
        changed, slugs = update_files_for_pr(root, args.repo, args.pr_number, args.issue_numbers)
        if not changed:
            print("No checklist lines updated for PR", file=sys.stderr)
            return 0
        print(f"Updated PR links and checked boxes for: {', '.join(slugs)}")
        return 0

    if args.command == "complete-checkbox":
        text = mark_checkbox_complete(path.read_text(encoding="utf-8"), args.slug)
        path.write_text(text, encoding="utf-8")
        sync_readme(root)
        return 0

    if args.command == "sync-readme":
        sync_readme(root)
        return 0

    if args.command == "progress":
        completed, total = compute_progress(path.read_text(encoding="utf-8"))
        percent = round((completed / total) * 100) if total else 0
        print(f"Onboarding progress: {completed}/{total} ({percent}%)")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
