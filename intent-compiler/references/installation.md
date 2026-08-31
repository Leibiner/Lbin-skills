# Intent Compiler 安装

## Skill

把 `intent-compiler/` 目录复制到 Claude Code 的个人 skills 目录：

```text
~/.claude/skills/intent-compiler/
```

保持目录结构不变。

## Hook

在 `~/.claude/settings.json` 的 `hooks.UserPromptSubmit` 中加入：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/intent-compiler/scripts/user-prompt-submit.sh",
            "timeout": 3000
          }
        ]
      }
    ]
  }
}
```

如果已有 `UserPromptSubmit` 配置，应合并而不是覆盖原配置。

## 本地测试 Router

```bash
echo '{"prompt":"把这个项目的登录功能优化一下"}' | \
  python3 ~/.claude/skills/intent-compiler/scripts/intent-router.py
```

应输出 JSON，并包含 `hookSpecificOutput.additionalContext`。

## 当前边界

V1 的 Router 是确定性规则，不调用外部 LLM。它只负责粗分类和注入行为上下文；真正的意图理解、项目上下文分析、澄清和任务规格生成由 Claude Code 完成。

后续 V1.5 可增加结构化 `/intent` 调试入口和 clarification state；V2 再考虑独立 LLM Compiler。
