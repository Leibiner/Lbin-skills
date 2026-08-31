#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${HOME}/.claude"
TARGET_DIR="${CLAUDE_DIR}/skills/intent-compiler"
SETTINGS="${CLAUDE_DIR}/settings.json"

mkdir -p "${CLAUDE_DIR}/skills" "${CLAUDE_DIR}/hooks"
rm -rf "${TARGET_DIR}"
cp -R "${ROOT_DIR}" "${TARGET_DIR}"

python3 - "${SETTINGS}" <<'PY'
import json
import os
import sys

settings_path = sys.argv[1]
os.makedirs(os.path.dirname(settings_path), exist_ok=True)

if os.path.exists(settings_path):
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {}

hooks = settings.setdefault("hooks", {})
entries = hooks.setdefault("UserPromptSubmit", [])
command = "bash ~/.claude/skills/intent-compiler/scripts/user-prompt-submit.sh"

exists = any(
    isinstance(entry, dict)
    and any(
        isinstance(h, dict) and h.get("command") == command
        for h in entry.get("hooks", [])
    )
    for entry in entries
)

if not exists:
    entries.append({
        "hooks": [{
            "type": "command",
            "command": command,
            "timeout": 3000
        }]
    })

with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY

chmod +x "${TARGET_DIR}/scripts/intent-router.py" "${TARGET_DIR}/scripts/user-prompt-submit.sh" "${TARGET_DIR}/scripts/install.sh"

echo "Intent Compiler installed."
echo "Skill: ${TARGET_DIR}"
echo "Hook:  UserPromptSubmit"
echo "Restart Claude Code or start a new session to verify."
