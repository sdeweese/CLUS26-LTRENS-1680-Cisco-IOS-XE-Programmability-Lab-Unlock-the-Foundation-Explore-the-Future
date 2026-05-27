#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

DEVICE="c9300x-lab"
TESTBED="${SCRIPT_DIR}/testbed.yaml"
WRITE_MEMORY="--write-memory"

usage() {
  cat <<'EOF'
Usage:
  ./run_pyats.sh [--device NAME] [--testbed PATH] [--no-write-memory]

Examples:
  ./run_pyats.sh
  ./run_pyats.sh --device c9300x-lab
  ./run_pyats.sh --testbed /home/auto/pyats/testbed.yaml --no-write-memory
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --device)
      DEVICE="$2"
      shift 2
      ;;
    --testbed)
      TESTBED="$2"
      shift 2
      ;;
    --no-write-memory)
      WRITE_MEMORY=""
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 2
      ;;
  esac
done

if [[ ! -f "${TESTBED}" ]]; then
  echo "ERROR: testbed file not found: ${TESTBED}"
  exit 2
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Creating virtual environment at ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

if ! python -c "import pyats,unicon,genie" >/dev/null 2>&1; then
  echo "Installing required packages: pyats unicon genie"
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install pyats unicon genie
fi

cd "${SCRIPT_DIR}"

CMD=(python3 enable_netconf_atomic_pyats.py --testbed "${TESTBED}" --device "${DEVICE}")
if [[ -n "${WRITE_MEMORY}" ]]; then
  CMD+=("${WRITE_MEMORY}")
fi

echo "Running: ${CMD[*]}"
"${CMD[@]}"
