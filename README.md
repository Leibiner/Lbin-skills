<div align="center">

# Lbin-skills

我的 skills 仓库。

[![Skills](https://img.shields.io/badge/Skills-1-blue)](#skills)
[![Layout](https://img.shields.io/badge/Layout-Indexed%20Skills-7c3aed)](#目录)

</div>

<br>

> 一个可持续扩展的技能索引仓库，每个 skill 都放在独立目录里。

## Skills

| Skill | 作用 | 状态 | 入口 |
|---|---|---|---|
| [wechat-article-downloader](#wechat-article-downloader) | 导出可访问的微信公众号文章，保留原始图片链接、代码块和校验材料。 | active | [SKILL.md](./wechat-article-downloader/SKILL.md) |

## 快速概览

```text
Lbin-skills/
  README.md
  wechat-article-downloader/
    SKILL.md
    agents/
    scripts/
    work/
    outputs/
```

## Conventions

- 新 skill 独立一个目录
- 目录内保留 `SKILL.md`
- 需要辅助文件时再加 `agents/`、`scripts/`、`references/`、`assets/`
- 临时产物放 `work/`
- 最终交付放 `outputs/`

### wechat-article-downloader

导出可访问的微信公众号文章，保留源数据、图片链接和代码块，并用 PDF 做校验。

<details open>
<summary>Scope</summary>

- 单篇文章导出
- 公众号文章批量整理
- 保留图片源 URL
- 保留代码块、表格、列表和层级标题
- 生成 PDF 作为校验基线

</details>

<details>
<summary>Boundaries</summary>

- 只处理用户能正常访问的页面
- 不绕过登录、验证码、反爬或付费限制
- 不做水印去除
- 不把临时抓取内容混进最终交付物

</details>

<details>
<summary>Entry</summary>

- [wechat-article-downloader/SKILL.md](./wechat-article-downloader/SKILL.md)
- [wechat-article-downloader/agents/openai.yaml](./wechat-article-downloader/agents/openai.yaml)
- [wechat-article-downloader/scripts/validate_export.py](./wechat-article-downloader/scripts/validate_export.py)

</details>
