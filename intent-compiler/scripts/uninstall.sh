#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${HOME}/.claude/skills/intent-compiler"
SETTINGS="${HOME}/.claude/settings.json"
COMMAND="bash ~/.claude/skills/intent-compiler/scripts/user-prompt-submit.sh"

python3 - "${SETTINGS}" "${COMMAND}" <<'PY'
import json
import os
import sys

path, command = sys.argv[1:]
if not os.path.exists(path):
    raise SystemExit(0)

with open(path, "r", encoding="utf-8") as f:
    settings = json.load(f)

entries = settings.get("hooks", {}).get("UserPromptSubmit", [])
filtered = []
for entry in entries:
    if not isinstance(entry, dict):
        filtered.append(entry)
        continue
    hooks = entry.get("hooks", [])
    remaining = [h for h in hooks if not (isinstance(h, dict) and h.get("command") == command)]
    if remaining:
        entry["hooks"] = remaining
        filtered.append(entry)

if "hooks" in settings and "UserPromptSubmit" in settings["hooks"]:
    settings["hooks"]["UserPromptSubmit"] = filtered

with open(path, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY

rm -rf "${TARGET_DIR}"
echo "Intent Compiler uninstalled."
