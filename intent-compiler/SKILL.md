---
name: intent-compiler
description: "Silently turn a user's vague or incomplete natural-language request into a clear, context-aware, executable task. Use when a request contains ambiguity, missing requirements, unclear scope, or when the user wants their intent understood and refined before execution. Do not use merely to rewrite polished prompts."
argument-hint: "[debug|preview|off] [request]"
---

# Intent Compiler

将用户自然语言中的**意图**编译成明确、可执行、可验证的任务。这个 Skill 是一个独立 Skill，不负责管理、路由或编排其他 Skill。

## Invocation

本 Skill 同时支持 Claude Code 的直接 Skill 调用和自动相关调用。Claude Code 会根据 `description` 判断何时自动加载；用户也可以直接输入 `/intent-compiler`。Skill 参数通过 `$ARGUMENTS` 传入。

首先判断 `$ARGUMENTS` 是否以以下控制词开头：

- `debug`：Debug 模式。
- `preview`：Preview 模式。
- `off`：本次会话关闭 Intent Compiler；不要继续编译当前请求。
- 其他内容：视为用户要编译的请求。

如果用户通过 `/intent-compiler` 调用但没有参数，则使用当前对话中最近一条尚未完成的用户请求；如果没有明确目标，直接询问用户要处理什么。

## Core behavior

默认采用 **silent mode**：不要把内部编译过程、完整 Task Specification 或最终 Compiled Prompt 展示给用户。完成理解后，直接继续当前任务；只有存在会实质改变结果的歧义时才向用户澄清。

核心原则：

```text
用户原话
  ↓
理解真正目标
  ↓
发现已有上下文
  ↓
判断关键歧义
  ↓
必要时最小澄清
  ↓
内部形成 Task Specification
  ↓
编译成 Executable Prompt
  ↓
直接执行 / 研究 / 写作 / 讨论
  ↓
验证
```

## Three modes

### Silent mode

默认模式。内部完成 Intent Analysis、Context Discovery、Task Compilation 和 Quality Gate，然后直接执行。

不要展示：

- 内部推理过程
- 完整 Task Specification
- Compiled Prompt
- 内部评分

除非用户明确要求查看。

### Preview mode

当 `$ARGUMENTS` 以 `preview` 开头时：

1. 去掉 `preview` 后，将剩余内容作为用户请求；若为空，使用当前对话中最近一条尚未完成的用户请求。
2. 正常执行 Intent Analysis、Context Discovery、Ambiguity Gate 和 Task Compilation。
3. 如果存在 Critical 缺失信息，先进行最小澄清；不要假装可以编译。
4. 生成最终 `Compiled Prompt`。
5. **只展示编译结果，不执行任务。**

输出结构：

```markdown
## Compiled Prompt

<最终准备交给执行 Agent 的任务指令>

## Task Summary
- Objective: ...
- Scope: ...
- Constraints: ...
- Acceptance Criteria: ...
- Validation: ...

## Decision
PREVIEW ONLY — not executed.
```

Compiled Prompt 必须是一个可以直接交给 Agent 执行的完整任务指令，而不是对用户原话的简单改写，也不是内部思维过程。

### Debug mode

当 `$ARGUMENTS` 以 `debug` 开头时：

1. 去掉 `debug` 后，将剩余内容作为用户请求；若为空，使用当前对话中最近一条尚未完成的用户请求。
2. 执行完整 Intent Analysis、Context Discovery、Ambiguity Gate、Task Compilation 和 Quality Gate。
3. 如果存在 Critical 缺失信息，明确指出阻塞点并提出最小澄清问题；不要虚构结果。
4. 如果信息足够，生成最终 `Compiled Prompt`。
5. **只展示分析和编译结果，不执行任务。**

输出结构：

```markdown
## Intent
<用户真正想达成的目标>

## Task Type
<execute / research / write / discuss + subtype>

## Context
<与任务相关的已知上下文>

## Ambiguities
<关键歧义；没有则写“无”>

## Assumptions
<采用的合理默认；没有则写“无”>

## Scope
<本次任务范围>

## Non-goals
<明确不做的内容>

## Constraints
<关键约束>

## Acceptance Criteria
<完成标准>

## Validation
<验证方式>

## Task Quality
| Dimension | Status |
| --- | --- |
| Goal | PASS / BLOCKED |
| Context | PASS / BLOCKED |
| Scope | PASS / BLOCKED |
| Constraints | PASS / BLOCKED |
| Acceptance | PASS / BLOCKED |
| Validation | PASS / BLOCKED |

## Compiled Prompt
<最终准备交给执行 Agent 的任务指令>

## Decision
DEBUG ONLY — not executed.
```

不要输出模型的隐藏 Chain-of-Thought。Debug 只展示可审计的结构化决策、依据、假设和最终任务，不展示隐式推理过程。

### Off mode

当 `$ARGUMENTS` 以 `off` 开头时，不执行 Intent Compilation。告诉用户当前请求不会经过本 Skill，然后停止，不继续执行该 Skill 的任务。

`off` 是 Skill 级显式控制，不修改 Claude Code 全局设置。

## When to use

优先在以下情况使用：

- 用户需求明显模糊，例如“优化一下”“搞好一点”“处理一下”。
- 用户只描述问题，没有明确目标或验收标准。
- 用户使用口语表达，但实际任务需要结构化理解。
- 用户要求“帮我想清楚”“帮我完善需求”“帮我把这句话变成能执行的任务”。
- 当前项目上下文可以补足用户没有说出的信息。

不要为了显得专业而对已经明确的简单请求重复编译或追问。

## Intent analysis

判断用户真正需要的是：

- `execute`：实际修改、创建、测试、部署或自动化。
- `research`：搜索、调研、比较、事实收集。
- `write`：写作、改写、润色、整理。
- `discuss`：解释、分析、方案讨论。

同时判断任务类型，例如：`coding`、`debugging`、`testing`、`refactoring`、`research`、`writing`、`analysis`、`architecture`、`automation`、`ui_ux`、`general`。

不要机械依赖关键词；根据完整语境判断。

## Context discovery

在提出问题之前，先利用当前环境能够获得的上下文。

软件工程任务优先检查：

- `CLAUDE.md`
- `AGENTS.md`
- `README*`
- 项目结构
- 依赖与构建配置
- 相关源码
- 现有测试
- Git 状态与 diff
- 相关文档与配置

**可自行发现的信息不向用户询问。**

## Ambiguity gate

把信息缺口分成三类：

### Critical

缺失后可能导致完全不同的目标、范围、实现或结果。

→ 必须澄清。

### Important

有影响，但可以通过项目上下文、已有约定或合理默认值解决。

→ 自行发现或推断。

### Optional

只影响非关键偏好。

→ 不询问，采用合理默认值。

## Minimal clarification

需要澄清时：

1. 一次只解决主要阻塞点。
2. 优先提供 2～5 个选项。
3. 问题必须可以直接回答。
4. 不要求用户重新描述完整需求。
5. 用户回答后，将回答与原始请求及已有上下文合并，继续执行。

示例：

> 你说的“优化”主要指哪一类？
> A. 性能
> B. 测试
> C. 代码质量
> D. 架构
> E. 全部

## Task compilation

对于非平凡任务，在内部形成 Task Specification：

- `objective`：真正要达成的结果。
- `context`：已知事实和环境。
- `scope`：本次处理范围。
- `non_goals`：明确不处理的内容。
- `constraints`：技术、业务、兼容性等限制。
- `assumptions`：合理且可验证的默认判断。
- `acceptance_criteria`：完成标准。
- `validation`：验证方式。

Schema 见 `schema/task.schema.json`。

**Task Specification 是内部工作模型，不是要求用户填写的表单。**

然后将 Task Specification 编译成 `Compiled Prompt`。Compiled Prompt 应：

- 保留用户真实目标。
- 包含执行所需的关键上下文。
- 明确范围和约束。
- 给出可验证的完成标准。
- 不添加用户没有授权且与目标无关的工作。
- 不暴露内部推理。

## Quality gate

执行前检查：

| 维度 | 判断 |
| --- | --- |
| Goal | 是否知道要得到什么结果 |
| Context | 是否拥有完成任务所需上下文 |
| Scope | 是否知道处理边界 |
| Constraints | 是否存在关键约束 |
| Acceptance | 是否知道什么算完成 |
| Validation | 是否知道如何验证 |

如果关键维度仍然缺失，并且无法从上下文推断，回到 Clarification；否则生成 Compiled Prompt 并直接执行。

## Execution policy

Silent 模式下，编译完成后**不要要求用户复制、确认或查看 Compiled Prompt**。

根据任务类型直接：

- 执行代码任务。
- 进行研究。
- 完成写作。
- 回答讨论问题。

如果用户只是要求优化需求，而不是执行任务，则输出 Compiled Prompt；否则默认直接继续完成用户真正想要的工作。

## Scope control

不得因为编译任务而擅自扩大工作范围。

例如：

- “修登录 Bug”不等于重写认证架构。
- “优化测试”不等于重构整个项目。
- “研究 GitHub 方案”不等于自动实现产品。

只有完成目标确实需要扩大范围时才扩大，并说明原因。

## Verification

对于执行类任务，尽可能验证：

- 功能结果
- 测试
- 构建
- lint / type check
- 运行结果
- 关键输出
- Git diff

无法验证时，明确指出未验证内容。

## Anti-patterns

不要：

- 把每个 Prompt 都改写成超长 Prompt。
- 对明确需求重复询问。
- 询问可以从项目中找到的信息。
- 为了“完整”要求用户填写十几个字段。
- 把内部 Task Specification 当成用户必须确认的表单。
- 擅自扩大任务范围。
- 用关键词规则代替语义理解。
- 因为 Skill 被加载就强制展示编译过程。
- 在 Debug / Preview 模式执行实际任务。
- 把隐藏 Chain-of-Thought 当作 Debug 输出。

## References

- `references/clarification.md`：澄清策略。
- `references/task-schema.md`：Task Specification 说明。
- `schema/task.schema.json`：Task Specification Schema。
- `schema/clarification.schema.json`：澄清 Schema。
- `tests/test-cases.md`：行为测试用例。
