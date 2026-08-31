#!/usr/bin/env python3
"""Lightweight, deterministic router for the Intent Compiler skill.

It deliberately does not call an LLM. Its job is only to provide coarse
routing context to Claude Code through UserPromptSubmit.
"""

import json
import re
import sys


DISCUSS = [r"^什么是", r"^为什么", r"^怎么看", r"^你觉得", r"^解释一下", r"^聊聊"]
RESEARCH = [r"查一下", r"搜索", r"研究", r"看看 github", r"帮我找", r"最新", r"对比", r"调研"]
WRITE = [r"写一篇", r"写个", r"帮我写", r"润色", r"改写", r"生成一份"]
EXECUTE = [r"修", r"修改", r"实现", r"增加", r"添加", r"删除", r"重构", r"优化", r"测试", r"部署", r"创建", r"改一下", r"处理一下"]


def match(text, patterns):
    return any(re.search(p, text, re.I) for p in patterns)


def classify(prompt):
    text = prompt.strip()
    if not text:
        return "discuss", "general", "empty"
    if text.startswith(("/", "!")):
        return "execute", "general", "command"
    if match(text, RESEARCH):
        return "research", "research", "research_pattern"
    if match(text, WRITE):
        return "write", "writing", "writing_pattern"
    if match(text, DISCUSS):
        return "discuss", "analysis", "discussion_pattern"
    if match(text, EXECUTE):
        return "execute", "general", "execution_pattern"
    return "execute", "general", "default"


def main():
    try:
        payload = json.load(sys.stdin)
        prompt = payload.get("prompt", "")
        mode, task_type, reason = classify(prompt)
        context = f"""[Lbin Intent Compiler V1]

The user's original request is authoritative. A lightweight router classified it as:
- mode: {mode}
- task_type: {task_type}
- reason: {reason}

Before acting:
1. Understand the user's actual outcome.
2. Inspect available project/conversation context.
3. Infer information that can be reliably discovered.
4. Ask only for critical missing information.
5. If sufficiently clear, execute directly.
6. Internally establish objective, scope, constraints, assumptions, acceptance criteria, and validation.
7. Do not ask the user to copy an optimized prompt.
8. Verify the result after execution.
"""
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"systemMessage": f"Lbin Intent Compiler router failed open: {exc}"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
