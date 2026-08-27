<div align="center">

# Lbin-skills

Codex skills collection for my own use.

[![Skills](https://img.shields.io/badge/Skills-1-blue)](#skills)
[![Codex](https://img.shields.io/badge/Codex-Skills-black)](https://github.com/KKKKhazix/khazix-skills)
[![Layout](https://img.shields.io/badge/Layout-Indexed%20Skills-7c3aed)](#目录)

</div>

<br>

> A compact index of reusable Codex skills, each kept in its own folder with its own instructions and supporting files.

## 目录

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

## Skills

### wechat-article-downloader

> Extract WeChat Official Account articles into verified Markdown, while preserving source image URLs and code blocks.

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

## Adding more skills

1. Create a new folder beside `wechat-article-downloader/`
2. Add a `SKILL.md` in that folder
3. Add supporting files only when the skill really needs them
4. Register the new skill in the table above
