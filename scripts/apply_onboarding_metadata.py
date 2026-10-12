#!/usr/bin/env python3
"""Apply bootstrap metadata (project name, onboarding issue, dates) to README.md.

Deliberately simple string replacement only — no section parsing. ONBOARDING.md
items don't carry project metadata, so there's no risk of the "silently drops
adjacent checklist lines" class of bug that section-rewriting scripts have.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path


def update_readme(content: str, metadata: dict) -> str:
    project_name = metadata["project_name"]
    onboarding_issue_url = metadata.get("onboarding_issue_url", "")
    accepted_date = metadata.get("accepted_date", "")
    target_date = metadata.get("target_completion_date", "")

    content = content.replace(
        "> **Project name:** _Replace with your project name_",
        f"> **Project name:** {project_name}",
    )
    content = content.replace(
        "> **CNCF onboarding issue:** _Link to your project's onboarding issue in cncf/sandbox_",
        f"> **CNCF onboarding issue:** {onboarding_issue_url}" if onboarding_issue_url else "> **CNCF onboarding issue:** _Link to your project's onboarding issue in cncf/sandbox_",
    )
    content = content.replace(
        "> **Accepted (TOC vote):** _YYYY-MM-DD_",
        f"> **Accepted (TOC vote):** {accepted_date}" if accepted_date else "> **Accepted (TOC vote):** _YYYY-MM-DD_",
    )
    content = content.replace(
        "> **Target completion (accepted + 30 days):** _YYYY-MM-DD_",
        f"> **Target completion (accepted + 30 days):** {target_date}" if target_date else "> **Target completion (accepted + 30 days):** _YYYY-MM-DD_",
    )
    content = content.replace(
        "# CNCF Sandbox Onboarding",
        f"# {project_name} — CNCF Sandbox Onboarding",
        1,
    )
    return content


def compute_target_date(accepted_date: str) -> str:
    if not accepted_date:
        return ""
    try:
        parsed = datetime.strptime(accepted_date, "%Y-%m-%d")
    except ValueError:
        return ""
    return (parsed + timedelta(days=30)).strftime("%Y-%m-%d")


def main() -> int:
    root = Path(os.environ["ROOT_DIR"])
    metadata = json.loads(os.environ["PROJECT_METADATA_JSON"])

    if metadata.get("accepted_date") and not metadata.get("target_completion_date"):
        metadata["target_completion_date"] = compute_target_date(metadata["accepted_date"])

    readme_path = root / "README.md"
    readme_path.write_text(update_readme(readme_path.read_text(), metadata), encoding="utf-8")

    metadata_path = root / ".github" / "project-metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"Updated {readme_path.name} and {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
