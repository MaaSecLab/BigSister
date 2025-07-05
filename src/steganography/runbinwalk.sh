# runbinwalk.sh
#
# Wrapper for binwalk to scan or extract embedded data from files.
#
# Usage:
#   runbinwalk.sh [options] <file>
#
# Options:
#   -e, --extract           Extract embedded files (binwalk -e)
#   -d, --output-dir DIR    Directory to extract into (default: <file>.extracted)
#   -h, --help              Display help and exit
#

set -euo pipefail

PROGRAM_NAME=$(basename "$0")
BINWALK=${BINWALK_PATH:-binwalk}
EXTRACT=false
OUTDIR=""
FILE=""

usage() {
  cat <<EOF
Usage: ${PROGRAM_NAME} [options] <file>

Options:
  -e, --extract           Extract embedded files (binwalk -e)
  -d, --output-dir DIR    Directory to extract into (default: <file>.extracted)
  -h, --help              Display this help message and exit

Examples:
  # Scan only
  ${PROGRAM_NAME} secret.bin

  # Extract into default dir
  ${PROGRAM_NAME} --extract secret.bin

  # Extract into custom dir
  ${PROGRAM_NAME} -e -d extracted/ secret.bin
EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--extract)
      EXTRACT=true
      shift
      ;;
    -d|--output-dir)
      if [[ $# -lt 2 ]]; then
        echo "Error: --output-dir requires a directory argument." >&2
        usage
      fi
      OUTDIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      ;;
    *)
      if [[ -z "$FILE" ]]; then
        FILE="$1"
        shift
      else
        echo "Error: Multiple files specified: '$FILE' and '$1'." >&2
        usage
      fi
      ;;
  esac
done

# Validate file
if [[ -z "${FILE}" ]]; then
  echo "Error: No file specified." >&2
  usage
fi
if [[ ! -f "${FILE}" ]]; then
  echo "Error: File not found: ${FILE}" >&2
  exit 2
fi

if [[ "${EXTRACT}" == false ]]; then
  echo "== Binwalk scan for '${FILE}' =="
  "${BINWALK}" "${FILE}"
  exit 0
fi

# Extraction mode
if [[ -z "${OUTDIR}" ]]; then
  OUTDIR="${FILE}.extracted"
fi

echo "== Binwalk extract for '${FILE}' =="
echo "Output directory: ${OUTDIR}"

mkdir -p "${OUTDIR}"
"${BINWALK}" -e -C "${OUTDIR}" "${FILE}"

echo "Extraction complete. Check directory: ${OUTDIR}"
