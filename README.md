<div align="center">

# Lbin-skills

> 我的可复用 AI Skills 集合。

<p>
  不同类型、不同用途的 Skills 持续沉淀于此。
</p>

<p>
  <img src="https://img.shields.io/badge/Skills-2-2563eb" />
  <img src="https://img.shields.io/badge/Reusable-Workflows-7c3aed" />
  <img src="https://img.shields.io/badge/Status-Active-10b981" />
</p>

</div>

> 别把稳定流程反复手搓。能沉淀的就写成 Skill，下次直接调用，少一点玄学，多一点可复现。

## 安装

### 一键安装全部 Skills

将仓库中的 Skill 自动复制到 Claude Code 的个人 Skills 目录：

```bash
git clone https://github.com/Leibiner/Lbin-skills.git /tmp/Lbin-skills && mkdir -p ~/.claude/skills && for d in /tmp/Lbin-skills/*/; do [ -f "$d/SKILL.md" ] && cp -R "$d" ~/.claude/skills/; done && rm -rf /tmp/Lbin-skills
```

安装后可直接检查：

```bash
ls ~/.claude/skills
```

> 当前仓库的 Skill 均按 Claude Code 个人 Skills 目录组织。部分 Skill 可能还需要额外配置，例如 Hook；请以对应 Skill 目录中的安装说明为准。

## Skills

当前收录的 Skills：

| Skill | 类型 | 简介 | 状态 |
|---|---|---|---|
| [`wechat-article-downloader`](./wechat-article-downloader/) | Content | 导出可访问的微信公众号文章，保留图片、代码块和校验材料。 | 🟢 Active |
| [`intent-compiler`](./intent-compiler/) | Agent | 将自然语言需求转换成明确、可执行、可验证的任务。 | 🟢 Active |

---

### 📰 wechat-article-downloader

**微信公众号文章下载 / 整理 / 校验**

> 将可访问的微信公众号文章整理为结构化内容，尽可能保留原始图片链接、代码块、表格和文档结构，并使用 PDF 进行校验。

<details>
<summary><strong>适用场景</strong></summary>

- 单篇文章导出
- 公众号文章批量整理
- 保留图片源 URL
- 保留代码块、表格、列表和层级标题
- 生成 PDF 作为校验基线

</details>

<details>
<summary><strong>处理边界</strong></summary>

- 只处理用户能正常访问的页面
- 不绕过登录、验证码、反爬或付费限制
- 不做水印去除
- 不把临时抓取内容混进最终交付物

</details>

<details>
<summary><strong>文件入口</strong></summary>

| 文件 | 用途 |
|---|---|
| [`SKILL.md`](./wechat-article-downloader/SKILL.md) | Skill 主定义 |
| [`agents/openai.yaml`](./wechat-article-downloader/agents/openai.yaml) | Agent 配置 |
| [`scripts/validate_export.py`](./wechat-article-downloader/scripts/validate_export.py) | 导出结果校验 |

</details>

---

### 🧠 intent-compiler

**自然语言需求编译 / 任务澄清 / 执行准备**

> 将用户自然语言需求转换成 Claude Code 可执行、可验证的任务。优先利用当前项目和会话上下文，只澄清真正阻塞执行的关键问题，信息足够后直接执行并验证。

<details>
<summary><strong>适用场景</strong></summary>

- 模糊需求澄清
- Coding / Debugging / Testing / Refactoring
- Research / Analysis / Architecture
- Writing / Automation / UI/UX
- 将自然语言转换为结构化 Task Specification

</details>

<details>
<summary><strong>核心组成</strong></summary>

| 组件 | 作用 |
|---|---|
| `UserPromptSubmit` Hook | 在 Claude Code 处理用户请求前注入编译上下文 |
| Router | 本地规则分类，不调用 LLM |
| Task Schema | 统一 objective、scope、constraints、acceptance criteria、validation |
| Skill | 负责上下文发现、澄清、执行和验证策略 |
| Fail-open | Router 异常时不阻塞原始请求 |

</details>

<details>
<summary><strong>文件入口</strong></summary>

| 文件 | 用途 |
|---|---|
| [`SKILL.md`](./intent-compiler/SKILL.md) | Skill 主定义 |
| [`agents/openai.yaml`](./intent-compiler/agents/openai.yaml) | Agent 配置 |
| [`schema/task.schema.json`](./intent-compiler/schema/task.schema.json) | Task Schema |
| [`scripts/intent-router.py`](./intent-compiler/scripts/intent-router.py) | 本地 Router |
| [`scripts/user-prompt-submit.sh`](./intent-compiler/scripts/user-prompt-submit.sh) | Claude Code Hook |
| [`references/installation.md`](./intent-compiler/references/installation.md) | 安装与配置说明 |

</details>

> `intent-compiler` 除了 Skill 本身，还包含 Hook 与 Router 配置，因此安装后请继续阅读它自己的安装说明。

## Repository Structure

```text
Lbin-skills/
├── README.md
│
├── wechat-article-downloader/
│   ├── SKILL.md
│   ├── agents/
│   ├── scripts/
│   ├── work/
│   └── outputs/
│
└── intent-compiler/
    ├── SKILL.md
    ├── agents/
    ├── scripts/
    ├── schema/
    └── references/
```

## Skill Convention

每个 Skill 独立一个目录，并至少包含：

```text
skill-name/
└── SKILL.md
```

根据 Skill 的实际需求，可以增加：

| 目录 | 用途 |
|---|---|
| `agents/` | Agent 配置 |
| `scripts/` | 可执行脚本 |
| `schema/` | 数据结构 / Schema |
| `references/` | 参考资料、安装说明 |
| `assets/` | 静态资源 |
| `work/` | 临时文件和中间产物 |
| `outputs/` | 最终交付物 |

## Status

- 🟢 `Active` — 当前稳定可用
- 🟡 `Experimental` — 实验中
- 🔴 `Deprecated` — 不再推荐使用

## Philosophy

不要重复手工完成稳定的工作流。

如果一个工作流值得重复使用，就把它沉淀成 Skill。

## License

暂未指定 License。