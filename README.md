<div align="center">

# Lbin-skills

Codex skills collection for my own use.

[![Skills](https://img.shields.io/badge/Skills-1-blue)](#skills)
[![Codex](https://img.shields.io/badge/Codex-Skills-black)](https://github.com/KKKKhazix/khazix-skills)

</div>

---

## 目录

| Skill | 作用 | 入口 |
|---|---|---|
| [wechat-article-downloader](#wechat-article-downloader) | 导出可访问的微信公众号文章，保留原始图片链接、代码块和校验材料。 | [SKILL.md](./wechat-article-downloader/SKILL.md) |

## 安装方式

把每个 skill 放在独立目录里，目录内保留 `SKILL.md`。需要额外材料时，再按需加入 `agents/`、`scripts/`、`references/`、`assets/`。

```text
Lbin-skills/
  README.md
  wechat-article-downloader/
    SKILL.md
    agents/
    scripts/
```

## Skills

### wechat-article-downloader

这个 skill 用来处理用户有权限访问的微信公众号文章，目标是把页面内容整理成可复用的 Markdown，并保留可追溯的原始信息。

适合下面这类需求：

- 单篇文章导出
- 公众号文章批量整理
- 保留图片源 URL
- 保留代码块、表格、列表和层级标题
- 生成 PDF 作为校验基线

它的约束也比较明确：

- 只处理用户能正常访问的页面
- 不绕过登录、验证码、反爬或付费限制
- 不做水印去除
- 不把临时抓取内容混进最终交付物

入口文件： [wechat-article-downloader/SKILL.md](./wechat-article-downloader/SKILL.md)
