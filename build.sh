#!/usr/bin/env bash
# Rebuild the entire Tudor eDiscovery corpus from scratch.
#
# The build is seeded and deterministic: with the default configuration it
# reproduces byte-for-byte identical natives, load files and hash values.
#
# Usage:
#   ./build.sh                                  # default ~2,000 documents
#   ./build.sh --routine 2000 --noise 3000      # scale volumes up
set -euo pipefail

cd "$(dirname "$0")"

if ! python3 -c "import faker, docx, openpyxl, reportlab, PIL" 2>/dev/null; then
    echo "Installing dependencies ..."
    pip install -r requirements.txt
fi

exec python3 -m generator.build "$@"
