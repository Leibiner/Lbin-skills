import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "intent-router.py"
FIXTURES = ROOT / "tests" / "fixtures.json"


def test_router_fixtures():
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for case in fixtures:
        result = subprocess.run(
            ["python3", str(ROUTER)],
            input=json.dumps({"prompt": case["prompt"]}),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        assert f'mode: {case["expected_mode"]}' in context
        assert f'task_type: {case["expected_type"]}' in context
