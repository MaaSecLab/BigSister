#!/usr/bin/env bash
#
# runsteghide.sh
#
# Wrapper script for Steghide to inspect and extract hidden data from files.
#
# Usage:
#   runsteghide.sh [options] <stego-file>
#
# Options:
#   -p, --passphrase PASS   Passphrase for encrypted data (if required)
#   -o, --output-dir DIR    Directory to extract files into (default: current directory)
#   -i, --info              Show Steghide info only; do not attempt extraction
#   -h, --help              Display this help message and exit
#

set -euo pipefail

PROGRAM_NAME=$(basename "$0")
STEGHIDE=${STEGHIDE_PATH:-steghide}
PASS=""
OUTDIR="."
INFO_ONLY=false

usage() {
  cat <<EOF
Usage: ${PROGRAM_NAME} [options] <stego-file>

Options:
  -p, --passphrase PASS   Passphrase for encrypted data (if required)
  -o, --output-dir DIR    Directory to extract files into (default: current directory)
  -i, --info              Show Steghide info only; do not attempt extraction
  -h, --help              Display this help message and exit

Examples:
  # Show embedded file info:
  ${PROGRAM_NAME} --info secret.jpg

  # Extract with passphrase:
  ${PROGRAM_NAME} -p hunter2 secret.jpg

  # Extract into a specific directory:
  ${PROGRAM_NAME} -o extracted/ secret.jpg
EOF
  exit 1
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--passphrase)
      [[ $# -lt 2 ]] && { echo "Error: --passphrase requires an argument." >&2; usage; }
      PASS="$2"; shift 2;;
    -o|--output-dir)
      [[ $# -lt 2 ]] && { echo "Error: --output-dir requires an argument." >&2; usage; }
      OUTDIR="$2"; shift 2;;
    -i|--info)
      INFO_ONLY=true; shift;;
    -h|--help)
      usage;;
    --) shift; break;;
    -*)
      echo "Unknown option: $1" >&2; usage;;
    *)
      STEGO_FILE="$1"; shift;;
  esac
done

# Validate
[[ -z "${STEGO_FILE:-}" ]] && { echo "Error: No stego file specified." >&2; usage; }
[[ ! -f "$STEGO_FILE" ]] && { echo "Error: File not found: $STEGO_FILE" >&2; exit 2; }

# Info mode
if [[ "$INFO_ONLY" = true ]]; then
  echo "== Steghide Info for '$STEGO_FILE' =="
  if [[ -n "$PASS" ]]; then
    echo "(using passphrase)"
    # pipe passphrase to avoid any interactive prompt
    printf "%s\n" "$PASS" | "$STEGHIDE" info -p "$PASS" "$STEGO_FILE"
  else
    # no passphrase: just run info directly
    "$STEGHIDE" info "$STEGO_FILE"
  fi
  exit 0
fi

# Extraction mode
echo "== Extracting hidden data from '$STEGO_FILE' =="
echo "Output directory: $OUTDIR"
mkdir -p "$OUTDIR"
pushd "$OUTDIR" >/dev/null

if [[ -n "$PASS" ]]; then
  # pipe passphrase and use -p and -sf flags
  printf "%s\n" "$PASS" \
    | "$STEGHIDE" extract -p "$PASS" -sf "$STEGO_FILE"
else
  # send an empty line and use -sf
  printf "\n" \
    | "$STEGHIDE" extract -sf "$STEGO_FILE"
fi

popd >/dev/null
echo "Extraction complete. Files (if any) are in '$OUTDIR'."

