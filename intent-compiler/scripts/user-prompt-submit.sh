#!/usr/bin/env bash
set -euo pipefail

# Claude Code executes this script from an arbitrary working directory.
# Resolve the companion router relative to this file so installation remains portable.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/intent-router.py"
