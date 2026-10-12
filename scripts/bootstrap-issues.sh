#!/usr/bin/env bash
set -euo pipefail

# Creates one GitHub issue per CNCF sandbox onboarding item (from
# .github/onboarding-items.json) and writes issue links into ONBOARDING.md.
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - jq installed
#   - Run from the repository root after creating a repo from this template
#
# Usage:
#   ./scripts/bootstrap-issues.sh [--dry-run]
#   ./scripts/bootstrap-issues.sh --project-name "MyProject" [--non-interactive]
#
# Options:
#   --project-name NAME         Project name (prompted if omitted)
#   --onboarding-issue-url URL  Link to your project's cncf/sandbox onboarding issue
#   --accepted-date YYYY-MM-DD  Date of the TOC acceptance vote
#   --non-interactive           Fail if required values are missing instead of prompting

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITEMS_FILE="${ROOT_DIR}/.github/onboarding-items.json"
ONBOARDING_FILE="${ROOT_DIR}/ONBOARDING.md"
REGISTRY_FILE="${ROOT_DIR}/.github/issue-registry.json"
METADATA_FILE="${ROOT_DIR}/.github/project-metadata.json"
APPLY_METADATA="${ROOT_DIR}/scripts/apply_onboarding_metadata.py"
TRACKING="${ROOT_DIR}/scripts/checklist_tracking.py"
DRY_RUN=false
NON_INTERACTIVE=false
PROJECT_NAME=""
ONBOARDING_ISSUE_URL=""
ACCEPTED_DATE=""

SLUGS_FILE="$(mktemp)"
SLUGS_ORDERED_FILE="$(mktemp)"
REGISTRY_TMP="$(mktemp)"
LABELS_FILE="$(mktemp)"
EXISTING_LABELS_FILE="$(mktemp)"
ITEMS_FLAT_FILE="$(mktemp)"

cleanup() {
  rm -f "${SLUGS_FILE}" "${SLUGS_ORDERED_FILE}" "${REGISTRY_TMP}" \
    "${LABELS_FILE}" "${EXISTING_LABELS_FILE}" "${ITEMS_FLAT_FILE}" \
    "${ONBOARDING_FILE}.tmp"
}
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "${1}" in
    --dry-run) DRY_RUN=true ;;
    --non-interactive) NON_INTERACTIVE=true ;;
    --project-name) PROJECT_NAME="${2:-}"; shift ;;
    --onboarding-issue-url) ONBOARDING_ISSUE_URL="${2:-}"; shift ;;
    --accepted-date) ACCEPTED_DATE="${2:-}"; shift ;;
    -h|--help)
      sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: ${1}" >&2
      exit 1
      ;;
  esac
  shift
done

for cmd in gh jq python3; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: ${cmd} is required." >&2
    exit 1
  fi
done

if ! gh api user -q .login >/dev/null 2>&1; then
  echo "Error: gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

if [[ ! -f "${ITEMS_FILE}" || ! -f "${ONBOARDING_FILE}" ]]; then
  echo "Error: required files missing. Run from repository root." >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
if [[ -z "${REPO}" ]]; then
  echo "Error: could not determine repository. Run inside a GitHub repo, or run 'gh repo set-default'." >&2
  exit 1
fi
DEFAULT_REPO_URL="https://github.com/${REPO}"

prompt_value() {
  local var_name="${1}" prompt_text="${2}" default_value="${3}"
  local current_value="${!var_name}"

  if [[ -n "${current_value}" ]]; then
    return 0
  fi
  if [[ "${NON_INTERACTIVE}" == true ]]; then
    echo "Error: --${var_name//_/-} is required in non-interactive mode." >&2
    exit 1
  fi

  local input
  if [[ -n "${default_value}" ]]; then
    read -r -p "${prompt_text} [${default_value}]: " input
    input="${input:-${default_value}}"
  else
    read -r -p "${prompt_text}: " input
  fi
  printf -v "${var_name}" '%s' "${input}"
}

collect_project_info() {
  if [[ "${DRY_RUN}" == true ]]; then
    echo "Project setup (skipped in dry run):"
    echo "  Project name: ${PROJECT_NAME:-<prompted>}"
    echo "  Onboarding issue URL: ${ONBOARDING_ISSUE_URL:-<prompted>}"
    echo "  Accepted date: ${ACCEPTED_DATE:-<prompted>}"
    echo
    return 0
  fi

  echo "Project setup"
  echo "Press Enter to accept [default] values."
  echo
  prompt_value PROJECT_NAME "Project name" ""
  prompt_value ONBOARDING_ISSUE_URL "Your CNCF onboarding issue URL (e.g. https://github.com/cncf/sandbox/issues/487)" ""
  prompt_value ACCEPTED_DATE "TOC acceptance date (YYYY-MM-DD)" ""

  local metadata
  metadata="$(jq -n \
    --arg project_name "${PROJECT_NAME}" \
    --arg onboarding_issue_url "${ONBOARDING_ISSUE_URL}" \
    --arg accepted_date "${ACCEPTED_DATE}" \
    --arg repository "${REPO}" \
    --arg bootstrapped_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '{project_name: $project_name, onboarding_issue_url: $onboarding_issue_url, accepted_date: $accepted_date, repository: $repository, bootstrapped_at: $bootstrapped_at}')"

  export ROOT_DIR PROJECT_METADATA_JSON="${metadata}"
  python3 "${APPLY_METADATA}"
  echo
}

label_color() {
  case "${1}" in
    onboarding-item) echo "0E8A16" ;;
    critical) echo "B60205" ;;
    optional) echo "FBCA04" ;;
    cncf-staff) echo "5319E7" ;;
    category:*) echo "1D76DB" ;;
    checklist:*) echo "1D76DB" ;;
    *) echo "BFD4F2" ;;
  esac
}

label_description() {
  case "${1}" in
    onboarding-item) echo "Part of the CNCF sandbox onboarding checklist" ;;
    critical) echo "Required before CNCF staff can proceed" ;;
    optional) echo "Optional item" ;;
    cncf-staff) echo "Completed by CNCF staff; track for follow-up" ;;
    category:*) echo "Onboarding category: ${1#category:}" ;;
    checklist:*) echo "Checklist item: ${1#checklist:}" ;;
    *) echo "" ;;
  esac
}

reverse_lines() {
  if command -v tac >/dev/null 2>&1; then tac "$1"; else tail -r "$1"; fi
}

# Flatten onboarding-items.json into one JSON object per line: slug, title,
# category id, critical/optional/staff flags, guide, evidence hint.
flatten_items() {
  jq -c '.categories[] as $c | $c.items[] | . + {category: $c.id}' "${ITEMS_FILE}" > "${ITEMS_FLAT_FILE}"
}

build_checklist_order() {
  # Order comes from ONBOARDING.md (### slug headings), not the JSON file, so
  # the created-issue order always matches what's rendered in the doc.
  grep -oE '<!-- checklist:[a-z0-9-]+ -->' "${ONBOARDING_FILE}" \
    | sed -E 's/<!-- checklist:([a-z0-9-]+) -->/\1/' \
    | awk '!seen[$0]++' > "${SLUGS_ORDERED_FILE}"
}

validate_checklist_order() {
  local items_file doc_file only_items only_doc
  items_file="$(mktemp)"
  doc_file="$(mktemp)"
  jq -r '[.categories[].items[].slug] | .[]' "${ITEMS_FILE}" | LC_ALL=C sort > "${items_file}"
  LC_ALL=C sort "${SLUGS_ORDERED_FILE}" > "${doc_file}"

  if cmp -s "${items_file}" "${doc_file}"; then
    rm -f "${items_file}" "${doc_file}"
    return 0
  fi

  local only_map only_app
  only_map="$(comm -23 "${items_file}" "${doc_file}" || true)"
  only_app="$(comm -13 "${items_file}" "${doc_file}" || true)"
  rm -f "${items_file}" "${doc_file}"

  echo "Error: checklist slugs in ONBOARDING.md do not match .github/onboarding-items.json" >&2
  if [[ -n "${only_map}" ]]; then
    echo "  Present in onboarding-items.json but missing from ONBOARDING.md:" >&2
    sed 's/^/    - /' <<< "${only_map}" >&2
  fi
  if [[ -n "${only_app}" ]]; then
    echo "  Present in ONBOARDING.md but missing from onboarding-items.json:" >&2
    sed 's/^/    - /' <<< "${only_app}" >&2
  fi
  echo "  Fix: python3 scripts/render_onboarding_template.py (only if you haven't started tracking real issues yet)." >&2
  exit 1
}

ensure_labels() {
  local label color description
  echo "Fetching existing repository labels..."
  gh label list --limit 500 --json name -q '.[].name' | sort > "${EXISTING_LABELS_FILE}"

  {
    echo "onboarding-item"
    echo "critical"
    echo "optional"
    echo "cncf-staff"
    jq -r '.categories[].id' "${ITEMS_FILE}" | sed 's/^/category:/'
    jq -r '.categories[].items[].slug' "${ITEMS_FILE}" | sed 's/^/checklist:/'
  } | sort -u > "${LABELS_FILE}"

  while IFS= read -r label; do
    [[ -z "${label}" ]] && continue
    if grep -qxF "${label}" "${EXISTING_LABELS_FILE}"; then
      continue
    fi
    color="$(label_color "${label}")"
    description="$(label_description "${label}")"
    if [[ "${DRY_RUN}" == true ]]; then
      echo "[dry-run] Would create label: ${label}"
      continue
    fi
    echo "Creating label: ${label}"
    gh label create "${label}" --color "${color}" --description "${description}"
  done < "${LABELS_FILE}"
}

build_issue_body() {
  local slug="${1}"
  jq -r --arg s "${slug}" '
    select(.slug == $s) |
    (.guide // "") + "\n\n**Evidence:** update the `" + $s + "` section in ONBOARDING.md with links/notes, then open a PR with `Closes #ISSUE_NUMBER`.\n\n---\n**Checklist slug:** `" + $s + "`\n**Onboarding doc:** See [ONBOARDING.md](ONBOARDING.md#" + $s + ")"
  ' "${ITEMS_FLAT_FILE}"
}

build_issue_title() {
  local slug="${1}"
  jq -r --arg s "${slug}" '
    select(.slug == $s) |
    (if .critical then "[Critical] " elif .staff then "[CNCF Staff] " elif .optional then "[Optional] " else "[Onboarding] " end) + .title
  ' "${ITEMS_FLAT_FILE}"
}

build_issue_labels() {
  local slug="${1}"
  jq -r --arg s "${slug}" '
    select(.slug == $s) |
    ["onboarding-item", ("category:" + .category), ("checklist:" + $s)]
    + (if .critical then ["critical"] else [] end)
    + (if .optional then ["optional"] else [] end)
    + (if .staff then ["cncf-staff"] else [] end)
    | join(",")
  ' "${ITEMS_FLAT_FILE}"
}

collect_project_info
flatten_items
build_checklist_order
validate_checklist_order

# GitHub's default issues view sorts by Newest first, so create the last
# checklist item first to make the first item land at the top of that view.
reverse_lines "${SLUGS_ORDERED_FILE}" > "${SLUGS_FILE}"
total="$(wc -l < "${SLUGS_ORDERED_FILE}" | tr -d ' ')"

echo "Bootstrapping ${total} onboarding issues for ${REPO}..."
echo "Completion order (top to bottom in the issues list):"
while IFS= read -r slug; do
  echo "  - $(build_issue_title "${slug}")"
done < "${SLUGS_ORDERED_FILE}"
echo

ensure_labels
echo

echo "{" > "${REGISTRY_TMP}"
echo "  \"repository\": \"${REPO}\"," >> "${REGISTRY_TMP}"
echo "  \"created_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "${REGISTRY_TMP}"
echo "  \"issues\": {" >> "${REGISTRY_TMP}"

first_entry=true
while IFS= read -r slug; do
  title="$(build_issue_title "${slug}")"
  labels="$(build_issue_labels "${slug}")"
  body="$(build_issue_body "${slug}")"
  placeholder="#ISSUE_$(echo "${slug}" | tr '[:lower:]-' '[:upper:]_')"
  body="${body//\#ISSUE_NUMBER/${placeholder}}"

  if [[ "${DRY_RUN}" == true ]]; then
    echo "[dry-run] Would create: ${title}"
    issue_number="0"
  else
    existing="$(gh issue list --label "checklist:${slug}" --state all --json number -q '.[0].number' 2>/dev/null || true)"
    if [[ -n "${existing}" && "${existing}" != "null" ]]; then
      echo "Issue already exists for ${slug}: #${existing}"
      issue_number="${existing}"
    else
      echo "Creating issue: ${title}"
      issue_url="$(gh issue create --title "${title}" --label "${labels}" --body "${body}")"
      issue_number="${issue_url##*/}"
      echo "  -> #${issue_number}"
    fi
  fi

  if [[ "${first_entry}" == true ]]; then first_entry=false; else echo "," >> "${REGISTRY_TMP}"; fi
  printf '    "%s": %s' "${slug}" "${issue_number}" >> "${REGISTRY_TMP}"

  if [[ "${DRY_RUN}" == false ]]; then
    python3 "${TRACKING}" --root "${ROOT_DIR}" link-issue --slug "${slug}" --number "${issue_number}" --repo "${REPO}"
  fi
done < "${SLUGS_FILE}"

echo >> "${REGISTRY_TMP}"
echo "  }" >> "${REGISTRY_TMP}"
echo "}" >> "${REGISTRY_TMP}"

if [[ "${DRY_RUN}" == true ]]; then
  echo
  echo "Dry run complete. No files modified."
  exit 0
fi

mv "${REGISTRY_TMP}" "${REGISTRY_FILE}"
trap - EXIT

python3 "${TRACKING}" --root "${ROOT_DIR}" sync-readme

echo
echo "Updated ONBOARDING.md, README.md, and wrote ${REGISTRY_FILE}"
echo
echo "Next steps:"
echo "  git add ONBOARDING.md README.md .github/project-metadata.json .github/issue-registry.json"
echo "  git commit -m 'Bootstrap CNCF sandbox onboarding checklist issues'"
echo "  git push"
