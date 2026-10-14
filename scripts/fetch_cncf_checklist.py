#!/usr/bin/env python3
"""Fetch a project's CNCF onboarding issue and build a local checklist JSON.

The issue body is authoritative for sections and checkbox items. Guides, slugs,
and flags come from the generic catalog in .github/onboarding-items.json when
titles match; unmatched CNCF lines still become local items so nothing active
on the CNCF issue is dropped.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CATALOG_FILE = ROOT / ".github" / "onboarding-items.json"
GENERATED_FILE = ROOT / ".github" / "onboarding-items.generated.json"

CHECKBOX = re.compile(r"^- \[([ xX])\] (.+)$")
HEADING = re.compile(r"^## (.+?)\s*$")
MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
NON_ALNUM = re.compile(r"[^a-z0-9]+")


def parse_issue_url(url: str) -> Tuple[str, str, int]:
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]
    # /owner/repo/issues/N
    if len(parts) < 4 or parts[2] != "issues":
        raise ValueError(
            f"Expected a GitHub issue URL like https://github.com/cncf/sandbox/issues/487, got: {url}"
        )
    owner, repo, _, number = parts[0], parts[1], parts[2], parts[3]
    return owner, repo, int(number)


def fetch_issue_body(owner: str, repo: str, number: int) -> str:
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{owner}/{repo}/issues/{number}",
            "--jq",
            ".body",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    body = result.stdout
    if not body.strip():
        raise RuntimeError(f"Issue {owner}/{repo}#{number} has an empty body")
    return body


def strip_md_links(text: str) -> str:
    return MD_LINK.sub(r"\1", text)


def normalize(text: str) -> str:
    text = strip_md_links(text).lower()
    text = text.replace("`", "")
    text = NON_ALNUM.sub(" ", text)
    return " ".join(text.split())


def slugify(text: str, used: set[str]) -> str:
    base = normalize(text)
    # Prefer meaningful tokens; drop very common words
    stop = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "to",
        "of",
        "for",
        "in",
        "on",
        "your",
        "project",
        "with",
        "that",
        "this",
        "are",
        "is",
        "be",
        "any",
        "if",
        "it",
        "as",
    }
    tokens = [t for t in base.split() if t not in stop and len(t) > 1][:6]
    base_slug = "-".join(tokens) or "checklist-item"
    slug = base_slug
    n = 2
    while slug in used:
        slug = f"{base_slug}-{n}"
        n += 1
    used.add(slug)
    return slug


def category_id_from_heading(heading: str) -> str:
    norm = normalize(heading)
    if "required" in norm and "before" in norm:
        return "required"
    if "review" in norm and "document" in norm:
        return "review-documents"
    if "contribute" in norm or "transfer" in norm:
        return "contribute-transfer"
    if "update" in norm and "document" in norm:
        return "project-details"
    if "staff" in norm:
        return "cncf-staff"
    if "final" in norm:
        return "final"
    return slugify(heading, set())


def load_catalog(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: List[Dict[str, Any]] = []
    for category in data.get("categories", []):
        for item in category.get("items", []):
            phrases = [item["title"]] + list(item.get("match_phrases", []))
            entries.append(
                {
                    **item,
                    "category_id": category["id"],
                    "category_heading": category["heading"],
                    "category_intro": category.get("intro", ""),
                    "_norms": [normalize(p) for p in phrases if p],
                }
            )
    return entries


def score_match(cncf_norm: str, catalog_norm: str) -> int:
    if not catalog_norm or not cncf_norm:
        return 0
    if cncf_norm == catalog_norm:
        return 100
    if catalog_norm in cncf_norm:
        return 80 + min(len(catalog_norm), 19)
    if cncf_norm in catalog_norm:
        return 70 + min(len(cncf_norm), 19)
    c_tokens = set(catalog_norm.split())
    i_tokens = set(cncf_norm.split())
    if not c_tokens:
        return 0
    overlap = len(c_tokens & i_tokens)
    if overlap == 0:
        return 0
    # Require solid overlap so unrelated staff items don't collide.
    ratio = overlap / len(c_tokens)
    if ratio < 0.5 and overlap < 3:
        return 0
    return int(50 * ratio) + overlap


def match_catalog(
    cncf_title: str, catalog: List[Dict[str, Any]], used_slugs: set[str]
) -> Optional[Dict[str, Any]]:
    cncf_norm = normalize(cncf_title)
    best: Optional[Dict[str, Any]] = None
    best_score = 0
    for entry in catalog:
        if entry["slug"] in used_slugs:
            continue
        for phrase in entry["_norms"]:
            score = score_match(cncf_norm, phrase)
            if score > best_score:
                best_score = score
                best = entry
    # Threshold: avoid weak matches
    if best and best_score >= 55:
        return best
    return None


def short_title_from_cncf(text: str, max_len: int = 100) -> str:
    plain = strip_md_links(text).strip()
    # First sentence-ish chunk
    for sep in (". ", "; ", " — ", " - "):
        if sep in plain:
            plain = plain.split(sep, 1)[0].strip()
            break
    if len(plain) > max_len:
        plain = plain[: max_len - 1].rstrip() + "…"
    return plain


def parse_body(body: str) -> List[Dict[str, Any]]:
    """Return list of {heading, intro_lines, items:[{checked, text}]}."""
    sections: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    intro_buf: List[str] = []

    def ensure_section(heading: str) -> Dict[str, Any]:
        nonlocal current, intro_buf
        if current is not None:
            current["intro"] = "\n".join(intro_buf).strip()
            sections.append(current)
        intro_buf = []
        current = {"heading": heading.strip(), "intro": "", "items": []}
        return current

    for raw in body.splitlines():
        line = raw.rstrip()
        heading = HEADING.match(line)
        if heading:
            ensure_section(heading.group(1))
            continue
        box = CHECKBOX.match(line)
        if box:
            if current is None:
                ensure_section("Onboarding checklist")
            assert current is not None
            current["items"].append(
                {
                    "checked": box.group(1).lower() == "x",
                    "text": box.group(2).strip(),
                }
            )
            continue
        if current is not None and not current["items"]:
            # Collect prose before first checkbox as category intro
            if line.strip() and not line.strip().startswith("#"):
                intro_buf.append(line.strip())

    if current is not None:
        current["intro"] = "\n".join(intro_buf).strip()
        sections.append(current)

    # Drop sections with no checklist items
    return [s for s in sections if s["items"]]


def build_checklist(issue_url: str, catalog_path: Path) -> Dict[str, Any]:
    owner, repo, number = parse_issue_url(issue_url)
    body = fetch_issue_body(owner, repo, number)
    sections = parse_body(body)
    if not sections:
        raise RuntimeError(
            f"No checklist checkboxes found in {issue_url}. "
            "Confirm the URL points at a CNCF onboarding issue with a markdown checklist."
        )

    catalog = load_catalog(catalog_path)
    used_slugs: set[str] = set()
    categories: List[Dict[str, Any]] = []
    matched = 0
    unmatched = 0

    for section in sections:
        heading = section["heading"]
        cat_id = category_id_from_heading(heading)
        # Prefer catalog intro for known category ids when CNCF intro is empty
        catalog_intro = ""
        for entry in catalog:
            if entry["category_id"] == cat_id and entry.get("category_intro"):
                catalog_intro = entry["category_intro"]
                break
        intro = section["intro"] or catalog_intro
        # Staff section heuristic
        staff_section = cat_id == "cncf-staff" or "staff" in normalize(heading)

        items_out: List[Dict[str, Any]] = []
        for raw_item in section["items"]:
            text = raw_item["text"]
            hit = match_catalog(text, catalog, used_slugs)
            optional = normalize(text).startswith("optional")
            if hit:
                used_slugs.add(hit["slug"])
                matched += 1
                item = {
                    "slug": hit["slug"],
                    "title": hit["title"],
                    "guide": hit["guide"],
                    "evidence_hint": hit.get("evidence_hint", "_Notes or links here._"),
                    "checked": raw_item["checked"],
                    "cncf_text": text,
                }
                for flag in ("critical", "optional", "staff"):
                    if hit.get(flag):
                        item[flag] = True
                if optional:
                    item["optional"] = True
                if staff_section and not item.get("critical"):
                    item["staff"] = True
                items_out.append(item)
            else:
                unmatched += 1
                slug = slugify(text, used_slugs)
                title = short_title_from_cncf(text)
                item = {
                    "slug": slug,
                    "title": title,
                    "guide": strip_md_links(text),
                    "evidence_hint": "_Notes or links proving completion._",
                    "checked": raw_item["checked"],
                    "cncf_text": text,
                }
                if optional:
                    item["optional"] = True
                if staff_section:
                    item["staff"] = True
                items_out.append(item)

        categories.append(
            {
                "id": cat_id,
                "heading": heading.title() if heading.isupper() else heading,
                "intro": intro,
                "items": items_out,
            }
        )

    return {
        "source_issue": issue_url.rstrip("/"),
        "catalog": str(catalog_path.relative_to(ROOT)),
        "matched_guides": matched,
        "unmatched_items": unmatched,
        "categories": categories,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-url", required=True, help="CNCF onboarding issue URL")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=CATALOG_FILE,
        help="Guide catalog JSON (default: .github/onboarding-items.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GENERATED_FILE,
        help="Where to write generated checklist JSON",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print JSON to stdout instead of writing a file",
    )
    args = parser.parse_args()

    try:
        data = build_checklist(args.issue_url, args.catalog)
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    payload = json.dumps(data, indent=2) + "\n"
    if args.stdout:
        sys.stdout.write(payload)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        total = sum(len(c["items"]) for c in data["categories"])
        checked = sum(
            1 for c in data["categories"] for i in c["items"] if i.get("checked")
        )
        print(
            f"Wrote {args.output} ({total} items, {checked} already checked; "
            f"{data['matched_guides']} matched guides, {data['unmatched_items']} new)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
