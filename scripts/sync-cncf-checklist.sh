#!/usr/bin/env bash
set -euo pipefail

# Re-sync an already-bootstrapped repo from the live CNCF onboarding issue:
#   1. Regenerate ONBOARDING.md (preserving evidence / Issue|PR links)
#   2. Create local issues for any new checklist slugs
#   3. Close + check boxes for items already checked on the CNCF issue
#   4. Refresh the README dashboard
#
# Usage:
#   ./scripts/sync-cncf-checklist.sh
#   ./scripts/sync-cncf-checklist.sh --onboarding-issue-url URL
#   ./scripts/sync-cncf-checklist.sh --dry-run

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CATALOG_FILE="${ROOT_DIR}/.github/onboarding-items.json"
ITEMS_FILE="${ROOT_DIR}/.github/onboarding-items.generated.json"
ONBOARDING_FILE="${ROOT_DIR}/ONBOARDING.md"
REGISTRY_FILE="${ROOT_DIR}/.github/issue-registry.json"
METADATA_FILE="${ROOT_DIR}/.github/project-metadata.json"
SYNC_PY="${ROOT_DIR}/scripts/sync_cncf_checklist.py"
TRACKING="${ROOT_DIR}/scripts/checklist_tracking.py"
FLAT_FILE="$(mktemp)"
DRY_RUN=false
ONBOARDING_ISSUE_URL=""

cleanup() { rm -f "${FLAT_FILE}"; }
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "${1}" in
    --dry-run) DRY_RUN=true ;;
    --onboarding-issue-url) ONBOARDING_ISSUE_URL="${2:-}"; shift ;;
    -h|--help)
      sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
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
  command -v "${cmd}" >/dev/null 2>&1 || { echo "Error: ${cmd} is required." >&2; exit 1; }
done

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[[ -n "${REPO}" ]] || { echo "Error: could not determine repository." >&2; exit 1; }

if [[ -z "${ONBOARDING_ISSUE_URL}" && -f "${METADATA_FILE}" ]]; then
  ONBOARDING_ISSUE_URL="$(jq -r '.onboarding_issue_url // empty' "${METADATA_FILE}")"
fi
[[ -n "${ONBOARDING_ISSUE_URL}" ]] || {
  echo "Error: pass --onboarding-issue-url or set it in .github/project-metadata.json" >&2
  exit 1
}

echo "Syncing checklist from ${ONBOARDING_ISSUE_URL}..."
python3 "${SYNC_PY}" --issue-url "${ONBOARDING_ISSUE_URL}" --catalog "${CATALOG_FILE}" \
  --output-json "${ITEMS_FILE}" --output-md "${ONBOARDING_FILE}"

if [[ "${DRY_RUN}" == true ]]; then
  echo "[dry-run] Wrote ${ITEMS_FILE} and ${ONBOARDING_FILE}; skipping issue create/close."
  exit 0
fi

if [[ -f "${REGISTRY_FILE}" ]]; then
  registry_json="$(cat "${REGISTRY_FILE}")"
else
  registry_json="$(jq -n --arg repo "${REPO}" --arg src "${ONBOARDING_ISSUE_URL}" \
    '{repository:$repo, created_at:(now|todate), source_issue:$src, issues:{}}')"
fi

label_color() {
  case "${1}" in
    onboarding-item) echo "0E8A16" ;;
    critical) echo "B60205" ;;
    optional) echo "FBCA04" ;;
    cncf-staff) echo "5319E7" ;;
    *) echo "1D76DB" ;;
  esac
}

ensure_label() {
  local label="$1"
  if gh label list --limit 500 --json name -q '.[].name' | grep -qxF "${label}"; then
    return 0
  fi
  gh label create "${label}" --color "$(label_color "${label}")" --description "${label}" 2>/dev/null || true
}

jq -c '.categories[] as $c | $c.items[] | . + {category: $c.id}' "${ITEMS_FILE}" > "${FLAT_FILE}"

while IFS= read -r item; do
  slug="$(jq -r '.slug' <<<"${item}")"
  title="$(jq -r '
    (if .critical then "[Critical] " elif .staff then "[CNCF Staff] " elif .optional then "[Optional] " else "[Onboarding] " end) + .title
  ' <<<"${item}")"
  checked="$(jq -r '.checked // false' <<<"${item}")"
  category="$(jq -r '.category' <<<"${item}")"
  guide="$(jq -r '.guide' <<<"${item}")"
  critical="$(jq -r '.critical // false' <<<"${item}")"
  optional="$(jq -r '.optional // false' <<<"${item}")"
  staff="$(jq -r '.staff // false' <<<"${item}")"

  labels="onboarding-item,category:${category},checklist:${slug}"
  [[ "${critical}" == "true" ]] && labels="${labels},critical"
  [[ "${optional}" == "true" ]] && labels="${labels},optional"
  [[ "${staff}" == "true" ]] && labels="${labels},cncf-staff"

  ensure_label "onboarding-item"
  ensure_label "category:${category}"
  ensure_label "checklist:${slug}"
  [[ "${critical}" == "true" ]] && ensure_label "critical"
  [[ "${optional}" == "true" ]] && ensure_label "optional"
  [[ "${staff}" == "true" ]] && ensure_label "cncf-staff"

  existing="$(jq -r --arg s "${slug}" '.issues[$s] // empty' <<<"${registry_json}")"
  if [[ -z "${existing}" ]]; then
    existing="$(gh issue list --label "checklist:${slug}" --state all --json number -q '.[0].number' 2>/dev/null || true)"
  fi

  if [[ -n "${existing}" && "${existing}" != "null" ]]; then
    issue_number="${existing}"
    echo "Keeping #${issue_number} for ${slug}"
  else
    body="${guide}

**Evidence:** update the \`${slug}\` section in ONBOARDING.md with links/notes, then open a PR with \`Closes #ISSUE_NUMBER\`.

---
**Checklist slug:** \`${slug}\`
**Onboarding doc:** See [ONBOARDING.md](ONBOARDING.md#${slug})"
    echo "Creating issue: ${title}"
    issue_url="$(gh issue create --title "${title}" --label "${labels}" --body "${body}")"
    issue_number="${issue_url##*/}"
    echo "  -> #${issue_number}"
  fi

  registry_json="$(jq --arg s "${slug}" --argjson n "${issue_number}" --arg src "${ONBOARDING_ISSUE_URL}" \
    '.issues[$s]=$n | .source_issue=$src' <<<"${registry_json}")"

  python3 "${TRACKING}" --root "${ROOT_DIR}" link-issue --slug "${slug}" --number "${issue_number}" --repo "${REPO}"

  if [[ "${checked}" == "true" ]]; then
    state="$(gh issue view "${issue_number}" --json state -q .state 2>/dev/null || true)"
    if [[ "${state}" == "OPEN" ]]; then
      gh issue close "${issue_number}" --comment "Already checked on the CNCF onboarding issue."
    fi
    python3 "${TRACKING}" --root "${ROOT_DIR}" complete-checkbox --slug "${slug}"
  fi
done < "${FLAT_FILE}"

printf '%s\n' "${registry_json}" > "${REGISTRY_FILE}"
python3 "${TRACKING}" --root "${ROOT_DIR}" sync-readme

echo
echo "Sync complete. Review ONBOARDING.md / README.md, then commit:"
echo "  git add ONBOARDING.md README.md .github/onboarding-items.generated.json .github/issue-registry.json"
echo "  git commit -m 'Sync onboarding checklist from CNCF issue'"
