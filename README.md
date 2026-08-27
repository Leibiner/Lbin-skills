<div align="center">

# Lbin-skills

一个按目录生长的 skills 仓库。

<p>
  <img src="https://img.shields.io/badge/%E6%8A%80%E8%83%BD-1-2563eb" />
  <img src="https://img.shields.io/badge/%E7%BB%93%E6%9E%84-%E7%9B%AE%E5%BD%95%E5%8C%96-7c3aed" />
  <img src="https://img.shields.io/badge/%E6%89%A9%E5%B1%95-%E6%8C%81%E7%BB%AD%E5%A2%9E%E9%95%BF-10b981" />
</p>

</div>

> 这里不堆大杂烩，只收能复用、能维护、能继续长出来的 skill。

## 封面

| 当前主线 | 组织方式 | 后续扩展 |
|---|---|---|
| 微信公众号文章导出 | 每个 skill 一个独立目录 | 直接在首页索引里补一行 |

## 目录

| Skill | 作用 | 状态 | 入口 |
|---|---|---|---|
| [wechat-article-downloader](#wechat-article-downloader) | 导出可访问的微信公众号文章，保留原始图片链接、代码块和校验材料。 | active | [SKILL.md](./wechat-article-downloader/SKILL.md) |

## 结构

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

## 约定

- 新 skill 独立一个目录
- 目录内保留 `SKILL.md`
- 辅助文件按需放进 `agents/`、`scripts/`、`references/`、`assets/`
- 临时抓取和中间产物放 `work/`
- 最终交付放 `outputs/`

## Skills

### wechat-article-downloader

导出可访问的微信公众号文章，保留源数据、图片链接和代码块，并用 PDF 做校验。

<details open>
<summary>适用范围</summary>

- 单篇文章导出
- 公众号文章批量整理
- 保留图片源 URL
- 保留代码块、表格、列表和层级标题
- 生成 PDF 作为校验基线

</details>

<details>
<summary>边界</summary>

- 只处理用户能正常访问的页面
- 不绕过登录、验证码、反爬或付费限制
- 不做水印去除
- 不把临时抓取内容混进最终交付物

</details>

<details>
<summary>入口</summary>

- [wechat-article-downloader/SKILL.md](./wechat-article-downloader/SKILL.md)
- [wechat-article-downloader/agents/openai.yaml](./wechat-article-downloader/agents/openai.yaml)
- [wechat-article-downloader/scripts/validate_export.py](./wechat-article-downloader/scripts/validate_export.py)

</details>
