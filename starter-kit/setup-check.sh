#!/usr/bin/env bash
# Setup check — verify your environment is ready for the hackathon.
# Run: bash setup-check.sh

set -euo pipefail

PASS="\033[92mPASS\033[0m"
FAIL="\033[91mFAIL\033[0m"
WARN="\033[93mWARN\033[0m"

passed=0
failed=0

check() {
    if eval "$2" >/dev/null 2>&1; then
        echo -e "  $PASS  $1"
        ((passed++))
    else
        echo -e "  $FAIL  $1"
        echo "        $3"
        ((failed++))
    fi
}

warn() {
    if eval "$2" >/dev/null 2>&1; then
        echo -e "  $PASS  $1"
        ((passed++))
    else
        echo -e "  $WARN  $1 (optional)"
        echo "        $3"
    fi
}

echo ""
echo "  HACKATHON SETUP CHECK"
echo "  =========================================="
echo ""

# Python
check "Python 3.11+" \
    "python3 -c 'import sys; assert sys.version_info >= (3, 11)'" \
    "Install Python 3.11+: https://python.org/downloads"

# Key packages
check "pdfplumber installed" \
    "python3 -c 'import pdfplumber'" \
    "Run: pip install pdfplumber"

check "pydantic installed" \
    "python3 -c 'import pydantic'" \
    "Run: pip install pydantic"

check "anthropic SDK installed" \
    "python3 -c 'import anthropic'" \
    "Run: pip install anthropic"

warn "pymupdf installed" \
    "python3 -c 'import fitz'" \
    "Run: pip install pymupdf (needed for vision/rendering fallback)"

# API key
check "ANTHROPIC_API_KEY is set" \
    "test -n \"\${ANTHROPIC_API_KEY:-}\"" \
    "Run: export ANTHROPIC_API_KEY=sk-ant-..."

# Sample PDF
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PDF_PATH="$SCRIPT_DIR/../Sample-Enhanced-Memo.pdf"

check "Sample PDF present" \
    "test -f \"$PDF_PATH\"" \
    "Download Sample-Enhanced-Memo.pdf to the repo root"

if [ -f "$PDF_PATH" ]; then
    SIZE=$(wc -c < "$PDF_PATH" | tr -d ' ')
    check "Sample PDF size looks right (~1.1 MB)" \
        "test $SIZE -gt 1000000 -a $SIZE -lt 2000000" \
        "File is ${SIZE} bytes — expected ~1,127,443. You may have the wrong file."
fi

# Schemas importable
check "schemas.py importable" \
    "cd \"$SCRIPT_DIR\" && python3 -c 'from schemas import CreditMemo'" \
    "Check that starter-kit/schemas.py exists and has no syntax errors"

# Validator runs
check "validate.py runs" \
    "cd \"$SCRIPT_DIR\" && python3 validate.py sample-output.json >/dev/null 2>&1" \
    "Check that starter-kit/validate.py and sample-output.json exist"

echo ""
echo "  ------------------------------------------"
echo -e "  Passed: $passed  |  Failed: $failed"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "  \033[92mYou're ready to build.\033[0m"
    echo ""
else
    echo -e "  \033[93mFix the items above, then re-run this script.\033[0m"
    echo ""
fi
