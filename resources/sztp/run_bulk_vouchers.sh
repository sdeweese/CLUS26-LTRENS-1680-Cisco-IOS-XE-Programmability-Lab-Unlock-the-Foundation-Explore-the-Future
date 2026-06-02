#!/usr/bin/env bash
set -uo pipefail

usage() {
  cat << 'EOF'
Usage:
  ./run_bulk_vouchers.sh [options]

Optional:
  --serial-source FILE         Serial source file (default: serials.txt)
  -p, --pinned-cert-file FILE     Pinned domain cert PEM file (default: pinned-domain-cert.pem)
      --platform VALUE            Platform value (default: XE)
  -o, --output-dir DIR            Output directory for per-serial files
                                  (default: vouchers/api_generated)
      --python CMD                Python command (default: .venv/bin/python)
      --script FILE               Script path (default: masa_ov_request.py)
      --dry-run                   Do not send API request; only print request details
  -h, --help                      Show this help

Notes:
  - For live API calls, MASA_API_TOKEN must be set in the environment.
  - Serials are extracted from either a plain serial list or a markdown pod table.
  - For markdown tables, vouchers are saved under subfolders based on table headers.
  - One VCJ file is written per serial number.
EOF
}

platform="XE"
serial_source="serials.txt"
#serial_source="pod-devices-table.md"
pinned_cert_file="pinned-domain-cert.pem"
output_dir="vouchers/api_generated"
python_cmd=".venv/bin/python"
script_path="masa_ov_request.py"
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --serial-source)
      serial_source="${2:-}"
      shift 2
      ;;
    -p|--pinned-cert-file)
      pinned_cert_file="${2:-}"
      shift 2
      ;;
    --platform)
      platform="${2:-}"
      shift 2
      ;;
    -o|--output-dir)
      output_dir="${2:-}"
      shift 2
      ;;
    --python)
      python_cmd="${2:-}"
      shift 2
      ;;
    --script)
      script_path="${2:-}"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -f "$serial_source" ]]; then
  echo "Error: serial source file not found: $serial_source" >&2
  exit 1
fi

if [[ ! -f "$pinned_cert_file" ]]; then
  echo "Error: pinned cert file not found: $pinned_cert_file" >&2
  exit 1
fi

if [[ ! -f "$script_path" ]]; then
  echo "Error: script not found: $script_path" >&2
  exit 1
fi

if [[ $dry_run -eq 0 ]]; then
  token="${MASA_API_TOKEN:-}"
  if [[ -z "$token" ]]; then
    echo "Error: MASA_API_TOKEN is not set for live API calls." >&2
    exit 1
  fi

  # Catch common placeholder/mistyped values early.
  case "$token" in
    YOUR_CORRECT_ORG_TOKEN|YOUR_TOKEN|CHANGE_ME|TOKEN|token)
      echo "Error: MASA_API_TOKEN appears to be a placeholder value." >&2
      exit 1
      ;;
  esac

  if [[ "$token" =~ [[:space:]] ]]; then
    echo "Error: MASA_API_TOKEN contains whitespace; re-export it as a single token string." >&2
    exit 1
  fi
fi

mkdir -p "$output_dir"

mapfile -t serial_entries < <(
  "$python_cmd" - "$serial_source" << 'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
entries = []
header_cols = []
table_mode = False

def normalize_header(text):
  text = text.strip().upper()
  text = re.sub(r"[^A-Z0-9_-]+", "_", text)
  return text.strip("_")

for line in src.read_text(encoding="utf-8").splitlines():
  raw = line.strip()
  if not raw:
    continue
  # Ignore inline comments for plain-text serial files.
  plain = raw.split("#", 1)[0].strip()
  if not plain:
    continue

  # Markdown pod table format: | Pod | cat9300x | cat9300 | cat9350 |
  if plain.startswith("|"):
    table_mode = True
    cols = [c.strip() for c in plain.strip("|").split("|")]

    # Header row: capture group names from columns after first (Pod)
    if "POD" in plain.upper() and len(cols) >= 4:
      header_cols = [normalize_header(c) for c in cols[1:4]]
      continue

    if "-----" in plain:
      continue

    if len(cols) >= 4:
      data_cols = cols[1:4]
      if not header_cols:
        # Fallback if header row was not found.
        header_cols = [f"COL{i+1}" for i in range(len(data_cols))]
      for idx, value in enumerate(data_cols):
        if re.fullmatch(r"[A-Z0-9]{8,20}", value):
          group = header_cols[idx] if idx < len(header_cols) else "UNGROUPED"
          entries.append((value, group))
    continue

  # Plain serial file format: one serial per line, or comma/space separated.
  for value in re.split(r"[\s,]+", plain):
    if re.fullmatch(r"[A-Z0-9]{8,20}", value):
      entries.append((value, ""))

seen = set()
for sn, group in entries:
  if sn not in seen:
    seen.add(sn)
    print(f"{sn}\t{group}")
PY
)

if [[ ${#serial_entries[@]} -eq 0 ]]; then
  echo "Error: no serial numbers were found in $serial_source" >&2
  exit 1
fi

total=0
success=0
failed=0

for entry in "${serial_entries[@]}"; do
  sn="${entry%%$'\t'*}"
  group="${entry#*$'\t'}"

  target_dir="$output_dir"
  if [[ -n "$group" ]]; then
    target_dir="$output_dir/$group"
  fi

  mkdir -p "$target_dir"

  total=$((total + 1))
  out_file="$target_dir/${sn}.vcj"

  cmd=(
    "$python_cmd" "$script_path"
    "$sn"
    --platform "$platform"
    --pinned-domain-cert-file "$pinned_cert_file"
    --output "$out_file"
  )
  if [[ $dry_run -eq 1 ]]; then
    cmd+=(--dry-run)
  fi

  if [[ -n "$group" ]]; then
    echo "[$total] Requesting voucher for $sn ($group)"
  else
    echo "[$total] Requesting voucher for $sn"
  fi
  if "${cmd[@]}"; then
    success=$((success + 1))
  else
    failed=$((failed + 1))
    echo "Failed for $sn" >&2
  fi
done

echo "Completed. total=$total success=$success failed=$failed"
[[ $failed -eq 0 ]]
