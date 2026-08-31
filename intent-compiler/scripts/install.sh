#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${HOME}/.claude"
TARGET_DIR="${CLAUDE_DIR}/skills/intent-compiler"
SETTINGS="${CLAUDE_DIR}/settings.json"

mkdir -p "${CLAUDE_DIR}/skills"
rm -rf "${TARGET_DIR}"
cp -R "${ROOT_DIR}" "${TARGET_DIR}"

python3 - "${SETTINGS}" <<'PY'
import json
import os
import sys

path = sys.argv[1]
settings = {}
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        settings = json.load(f)

hooks = settings.setdefault("hooks", {})
entries = hooks.setdefault("UserPromptSubmit", [])
command = "bash ~/.claude/skills/intent-compiler/scripts/user-prompt-submit.sh"

for entry in entries:
    if not isinstance(entry, dict):
        continue
    if any(isinstance(h, dict) and h.get("command") == command for h in entry.get("hooks", [])):
        break
else:
    entries.append({
        "hooks": [{
            "type": "command",
            "command": command,
            "timeout": 3000
        }]
    })

os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY

chmod +x "${TARGET_DIR}/scripts/"*.sh "${TARGET_DIR}/scripts/intent-router.py"

echo "Installed intent-compiler to ${TARGET_DIR}"
echo "Registered UserPromptSubmit hook. Start a new Claude Code session to use it."
