---
name: intent-compiler
description: "Convert natural-language requests into clear, executable, and verifiable tasks. Use project context first, infer non-critical details, ask only the minimum critical clarification questions, then execute without requiring the user to write or copy an optimized prompt."
---

# Intent Compiler

把用户的自然语言需求编译成 Claude Code 可执行、可验证的任务。这个 skill 的目标不是把 Prompt 写长，而是减少歧义、补齐关键上下文、控制范围，并让 Claude 在信息足够时直接执行。

## Outcome

对每个用户请求，完成以下判断：

1. 用户真正想达成什么结果。
2. 当前请求属于执行、讨论、研究还是写作。
3. 当前项目和会话已经提供了哪些上下文。
4. 哪些信息可以从项目中发现或合理推断。
5. 哪些缺失信息会实质改变结果，必须向用户确认。
6. 信息足够时直接执行，不要求用户复制所谓“优化后的 Prompt”。
7. 执行后验证结果，而不是以“文件已修改”作为完成标准。

## Decision model

内部将请求划分为以下模式：

- `execute`：明确要求执行代码、测试、重构、配置、自动化等任务。
- `clarify`：存在会显著影响结果的关键歧义。
- `discuss`：用户主要在询问概念、原因、方案或观点。
- `research`：需要搜索、调研、比较或收集外部资料。
- `write`：主要目标是生成、改写、润色或组织内容。

任务类型可进一步划分为：

`coding`、`debugging`、`testing`、`refactoring`、`research`、`writing`、`analysis`、`architecture`、`automation`、`ui_ux`、`general`。

## Information policy

把缺失信息分为三类：

### Critical

缺失后无法可靠判断用户真正要的结果，或者不同答案会导致明显不同的实现。

**必须澄清。**

### Important

对方案有影响，但可以通过当前项目、现有代码、文档、约定或合理默认值得到。

**优先自行获取或推断。**

### Optional

不影响主要结果，只影响偏好、表现形式或次要细节。

**不要为了“完整”而询问。**

## Clarification rules

需要澄清时：

1. 一次只问真正阻塞任务的问题。
2. 优先使用选择题。
3. 问题必须能直接回答。
4. 不询问 Claude Code 可以通过仓库、文件或工具自行获得的信息。
5. 不因为 Prompt 看起来不够漂亮而追问。
6. 用户回答后，将原始需求、回答和已发现上下文合并，不要求用户重新描述完整需求。

推荐形式：

> 你说的“优化”主要是指哪一类？
>
> A. UI/交互
> B. 性能
> C. 业务逻辑
> D. 测试
> E. 全部

## Context discovery

软件工程任务优先检查当前可用上下文，例如：

- `CLAUDE.md`
- `AGENTS.md`
- `README*`
- 项目目录结构
- package / build / dependency 配置
- 相关源码
- 现有测试
- Git 状态和 diff
- 已有文档和配置

不要让用户重复提供可以从项目中发现的信息。

## Internal task specification

执行非平凡任务前，内部形成任务规格。字段定义见 `schema/task.schema.json`：

- `objective`：最终目标。
- `context`：已知事实和项目上下文。
- `scope`：本次要处理的范围。
- `non_goals`：明确不做什么。
- `constraints`：技术、业务和兼容性限制。
- `assumptions`：合理推断和默认值。
- `acceptance_criteria`：完成标准。
- `validation`：验证方式。

除非用户明确要求，否则不要把内部 Task Specification 当作 Prompt 让用户复制。

## Execution policy

信息足够时：

1. 先理解现状。
2. 再确定最小正确变更。
3. 执行任务。
4. 运行适合的测试、构建、lint、类型检查或其他验证。
5. 检查 diff 和副作用。
6. 汇报结果。

不要把“解释怎么做”误当成“已经做完”。

## Research policy

研究类请求应先定义研究问题，然后收集和比较资料。优先一手来源，并区分事实、推断和建议。研究任务没有明确要求时，不要擅自进入代码实施。

## Writing policy

写作类请求优先利用已有上下文和用户既定目标。缺少真正影响成稿方向的信息时再澄清；否则采用合理默认值直接完成。

## Scope control

用户请求决定主范围。不要把“修一个 Bug”擅自扩大成架构重写，也不要把“调研一下”扩大成完整产品实现。只有当扩大范围是完成目标的必要条件时才扩大，并在最终结果中说明。

## Verification

任务完成必须尽可能验证：

- 功能结果
- 自动化测试
- 构建或类型检查
- 运行结果
- 关键输出
- Git diff

如果某项无法验证，明确说明未验证项。

## Final response

执行完成后简洁报告：

1. 做了什么。
2. 关键决策或假设。
3. 做了哪些验证。
4. 还有什么已知限制。

不要暴露隐藏推理过程。

## Companion files

- `scripts/intent-router.py`：轻量本地 Router，不调用 LLM。
- `scripts/user-prompt-submit.sh`：Claude Code `UserPromptSubmit` Hook 入口。
- `schema/task.schema.json`：标准 Task Specification Schema。
- `agents/openai.yaml`：Skill 的 Agent UI 元数据。
- `references/installation.md`：安装和配置说明。
