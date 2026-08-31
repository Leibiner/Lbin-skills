# Intent Compiler 安装

## 目标

Intent Compiler 分为两个部分：

1. `SKILL.md`：定义意图理解、澄清、任务规格和执行策略。
2. `UserPromptSubmit` Hook：保证每次用户提交 Prompt 时，都把轻量 Intent Compiler 上下文注入当前 Claude Code 会话。

**仅安装 Skill 不会强制它参与每一次对话；要实现自动触发，必须安装 Hook。**

## 一键安装

从仓库进入 `intent-compiler` 目录后执行：

```bash
bash scripts/install.sh
```

安装脚本会：

- 复制 Skill 到 `~/.claude/skills/intent-compiler/`
- 合并 `~/.claude/settings.json`
- 注册 `UserPromptSubmit` Hook
- 不覆盖已有的其他 Hook 配置
- 重复执行不会重复添加同一个 Hook

安装完成后重新启动 Claude Code 或开始新会话。

## 验证 Router

```bash
echo '{"prompt":"把这个项目的测试体系完善一下"}' | \
  python3 ~/.claude/skills/intent-compiler/scripts/intent-router.py
```

输出应包含 `hookSpecificOutput.additionalContext`。

## 验证 Claude Code 自动触发

安装 Hook 后，在任意项目直接输入：

```text
帮我把这个项目的测试体系完善一下
```

Hook 会在 Claude Code 处理用户 Prompt 前注入 Intent Compiler 上下文。Claude 随后根据当前项目和会话上下文判断是否需要澄清，并在信息足够时直接执行。

## 卸载

```bash
bash ~/.claude/skills/intent-compiler/scripts/uninstall.sh
```

## 当前设计边界

V1 Router 不调用外部 LLM，只做低成本预路由；真正的意图理解、上下文发现、关键歧义判断、澄清和任务执行由 Claude Code 完成。

这样可以避免每个 Prompt 都额外调用一次模型，也避免 Compiler 故障阻塞 Claude Code。

## 下一阶段

V1.5：增加 `/intent` 调试入口、clarification state 和测试集。

V2：可选增加独立 LLM Compiler，将自然语言编译成 `task.schema.json` 定义的结构化任务，再交给 Claude Code 执行。
