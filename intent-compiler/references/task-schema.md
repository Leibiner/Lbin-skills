# Task Specification

Intent Compiler 在内部将自然语言需求编译成任务规格，而不是要求用户编写 Prompt。

## Fields

| 字段 | 作用 |
| --- | --- |
| objective | 用户真正要达成的结果 |
| context | 已知事实、项目上下文 |
| scope | 本次处理范围 |
| non_goals | 明确不做的事情 |
| constraints | 技术、业务、兼容性约束 |
| assumptions | 可验证的合理默认 |
| acceptance_criteria | 什么条件算完成 |
| validation | 如何验证结果 |

## Principle

Task Specification 是 Agent 的内部工作模型。除非用户要求查看，否则不要机械输出完整 Schema。

优先执行，而不是把 Schema 变成另一份需要用户确认的 Prompt。
