#!/usr/bin/env bash
set -euo pipefail

# Generates ONBOARDING-STATUS.md from ONBOARDING.md — a paste-ready update for
# your CNCF onboarding issue's "Quote reply" checklist.
#
# Usage:
#   ./scripts/generate-status-report.sh              # write ONBOARDING-STATUS.md
#   ./scripts/generate-status-report.sh --post        # also post as a comment
#   ./scripts/generate-status-report.sh --post --onboarding-issue-url URL

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATOR="${ROOT_DIR}/scripts/generate_status_report.py"
METADATA_FILE="${ROOT_DIR}/.github/project-metadata.json"
OUTPUT_FILE="${ROOT_DIR}/ONBOARDING-STATUS.md"
POST=false
ISSUE_URL=""

while [[ $# -gt 0 ]]; do
  case "${1}" in
    --post) POST=true ;;
    --onboarding-issue-url) ISSUE_URL="${2:-}"; shift ;;
    -h|--help)
      sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: ${1}" >&2
      exit 1
      ;;
  esac
  shift
done

for cmd in python3 jq; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: ${cmd} is required." >&2
    exit 1
  fi
done

python3 "${GENERATOR}"

if [[ "${POST}" == true ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "Error: gh is required for --post." >&2
    exit 1
  fi
  if ! gh api user -q .login >/dev/null 2>&1; then
    echo "Error: gh is not authenticated. Run: gh auth login" >&2
    exit 1
  fi
  if [[ -z "${ISSUE_URL}" && -f "${METADATA_FILE}" ]]; then
    ISSUE_URL="$(jq -r '.onboarding_issue_url // ""' "${METADATA_FILE}")"
  fi
  if [[ -z "${ISSUE_URL}" ]]; then
    echo "Error: --onboarding-issue-url is required with --post (or run bootstrap-issues.sh first)." >&2
    exit 1
  fi

  # Expect a URL like https://github.com/cncf/sandbox/issues/487
  repo_and_number="$(echo "${ISSUE_URL}" | sed -E 's#https://github.com/([^/]+/[^/]+)/issues/([0-9]+).*#\1 \2#')"
  repo="$(echo "${repo_and_number}" | cut -d' ' -f1)"
  number="$(echo "${repo_and_number}" | cut -d' ' -f2)"
  if [[ -z "${repo}" || -z "${number}" ]]; then
    echo "Error: could not parse repo/issue number from: ${ISSUE_URL}" >&2
    exit 1
  fi

  echo "Posting status update to ${repo}#${number}..."
  gh issue comment "${number}" -R "${repo}" --body-file "${OUTPUT_FILE}"
  echo "Posted."
fi
