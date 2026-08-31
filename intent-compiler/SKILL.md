---
name: intent-compiler
description: "Silently turn a user's vague or incomplete natural-language request into a clear, context-aware, executable task. Use when a request contains ambiguity, missing requirements, unclear scope, or when the user wants their intent understood and refined before execution. Do not use merely to rewrite polished prompts."
---

# Intent Compiler

将用户自然语言中的**意图**编译成明确、可执行、可验证的任务。这个 Skill 是一个独立 Skill，不负责管理、路由或编排其他 Skill。

## Core behavior

默认采用 **silent mode**：不要把内部编译过程、完整 Task Specification 或“优化后的 Prompt”展示给用户。完成理解后，直接继续当前任务；只有存在会实质改变结果的歧义时才向用户澄清。

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
直接执行 / 研究 / 写作 / 讨论
  ↓
验证
```

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

如果关键维度仍然缺失，并且无法从上下文推断，回到 Clarification；否则直接执行。

## Execution policy

编译完成后**不要要求用户复制或确认“优化后的 Prompt”**。

根据任务类型直接：

- 执行代码任务。
- 进行研究。
- 完成写作。
- 回答讨论问题。

如果用户只是要求优化需求，而不是执行任务，则输出编译后的需求；否则默认直接继续完成用户真正想要的工作。

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

## Debug mode

如果用户明确要求查看 Intent Compiler 的内部结果，例如：

```text
/intent debug 帮我优化这个项目
```

可以展示：

- Intent
- Task Type
- Context
- Ambiguities
- Assumptions
- Scope
- Acceptance Criteria
- Validation
- Decision

Debug mode 仅用于观察和调试，不改变正常执行策略。

## Explicit controls

如果用户明确要求：

- `/intent`：对当前请求执行一次 Intent Compilation。
- `/intent debug`：显示编译结果，不隐藏 Task Specification。
- `/intent off`：停止本次会话中的 Intent Compiler 行为，直到用户再次明确启用。

这些命令属于 Skill 的显式控制方式，不需要 Hook。

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

## References

- `references/clarification.md`：澄清策略。
- `references/task-schema.md`：Task Specification 说明。
- `schema/task.schema.json`：Task Specification Schema。
- `schema/clarification.schema.json`：澄清 Schema。
- `tests/test-cases.md`：行为测试用例。
