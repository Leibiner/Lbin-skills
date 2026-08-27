<div align="center">

# Lbin-skills

把重复工作流封装成可复用 skills。

<p>
  <img src="https://img.shields.io/badge/%E6%8A%80%E8%83%BD-1-2563eb" />
  <img src="https://img.shields.io/badge/%E5%A4%8D%E7%94%A8-%E5%B7%A5%E4%BD%9C%E6%B5%81-7c3aed" />
  <img src="https://img.shields.io/badge/%E8%B0%83%E7%94%A8-%E5%8D%B3%E6%89%A7%E8%A1%8C-10b981" />
</p>

</div>

> 别把稳定流程反复手搓。能沉淀的就写成 skill，下次直接调用，少一点玄学，多一点可复现。

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
