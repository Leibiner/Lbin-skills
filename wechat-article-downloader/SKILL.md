---
name: wechat-article-downloader
description: "Export one or all accessible, user-authorized WeChat Official Account publications to verified Markdown files with source image URLs, preserved code blocks, PDF references, and validation. Prefer Chrome first, then fall back to another available external browser if Chrome is unavailable or blocked. Batch exports use valid publication records as the output unit. Do not use for login bypass, anti-bot bypass, or watermark removal."
---

# Wechat Article Downloader

Use this skill when the user asks to download, archive, or convert a WeChat article into a reusable Markdown document.

## Outcome

For a single-article request, produce one title-named Markdown file under the task's outputs directory. For a batch request from a publication-list page, produce one title-named Markdown file per valid publication record, not per child article detail URL. A merged publication record can contain multiple child articles; fetch each child detail page, then place the child articles in their original order in the same publication-record Markdown file. Deleted or otherwise unreadable publication records are skipped by default and may be listed in a manifest or report. Each file should contain:

- article title, author, source URL, and useful metadata
- the source article's heading hierarchy, lists, tables, links, and paragraph order
- complete fenced code blocks, including terminal commands and alignment-sensitive text diagrams
- Markdown image references pointing to the article's original image URLs
- no local image directory, Base64 image data, assets folder, or generic article.md name when a title is available

Generate a PDF from the source article as the completeness and visual reference. The PDF is a QA baseline; do not use PDF OCR as the primary Markdown source when the original HTML is available.

## Boundaries

- Work only with pages the user can access. Reuse an already logged-in Chrome session through the chrome:control-chrome capability when available.
- When the user provides a WeChat article or publication download link, open it in Chrome first. If Chrome is unavailable, blocked, or cannot complete the page, switch to another available external browser and continue there. Do not use the in-app/internal browser for WeChat article access or extraction.
- If the page is not accessible or the session is not logged in, stop and ask the user to open or authenticate the article. Do not bypass login, CAPTCHA, anti-bot controls, paywalls, or access restrictions.
- Do not remove or obscure third-party watermarks. If the user owns the image or has authorization, use the supplied unwatermarked originals instead.
- Keep raw HTML/JSON and temporary renders under work/; keep only user-facing deliverables under outputs/.

## Workflow

1. Resolve the article detail URL in Chrome first, then in another available external browser if needed. An appmsgpublish list page is not the article body; open the individual article before extracting content. Do not use the in-app/internal browser for this workflow.
2. For a list or batch request, enumerate publication records and their visible article detail anchors from the current page. Use links whose href starts with https://mp.weixin.qq.com/s/. Keep the parent record and child detail URLs together: one list row may contain multiple child article links. The output count is the number of valid publication records; child detail URL counts are internal fetch/QA data and must not appear in the final report unless the user explicitly asks for debugging details.
3. Handle pagination as an asynchronous UI operation. Click the visible “下一页” control, wait for the list to refresh, and verify the page signature or article set changed. The URL may remain unchanged. Stop when “下一页” is absent or disabled, or when a page signature repeats. Record page number, title, URL, and source row for a resumable manifest. Deduplicate by detail URL.
4. Determine record validity before export. A record is valid when at least one child detail page is accessible and contains a real article body. Mark deleted, unavailable, empty, or access-blocked records as skipped; do not create a fake Markdown body for them. Process each unique child detail URL sequentially or with a small bounded concurrency. Open the individual article, capture its rendered article or page payload, and prefer the article container (#js_content) or a saved payload.html field over a list response. Record title, author, date, parent record identity, source URL, and raw HTML/JSON.
5. Extract image sources in document order. Prefer data-src, data-original, or equivalent source attributes over lazy-load placeholder src values. Reject 1x1 SVG placeholders. Preserve each source URL exactly, including its query string.
6. Create the PDF from the source HTML. Use the PDF skill and bundled PDF runtime. Embed the source images, render the PDF, and inspect representative pages for missing text, broken tables, clipped content, and image failures. For batches, keep or remove per-article PDFs according to the user's request, but use the PDF as the QA baseline for every Markdown file.
7. Build Markdown from the source HTML, not from PDF OCR. Use YAML front matter, the article title as the H1, and the article's original section order. Do not add the reference-template Excerpt block.
8. Restore every preformatted block as a fenced Markdown block. Preserve line breaks and indentation. Use bash for shell commands and text for diagrams or conversation examples. A styled monospace block with white-space: pre-wrap is also a code block for this purpose.
9. Write images as direct Markdown URLs, for example ![image](https://...). Do not download a local copy unless the user explicitly chooses a local/offline package. Explain that source URLs can expire or reject external access.
10. Clean conversion artifacts only: remove Excerpt, &#x20;, accidental &nbsp;, leaked 1x1 SVG tails, and extraction-only backslash escapes. Do not remove article meaning or code characters.
11. Use a title-based Windows-safe filename. Replace invalid filename characters such as /, \, :, *, ?, ", <, >, and | with spaces or a short safe separator. Do not call the final file article.md.
12. Run scripts/validate_export.py with the bundled Python runtime. Compare normalized Markdown content and every code line against the PDF, verify even fence markers, verify image references, and compare image URLs to the captured source list when available.

## Counting and grouping

- `publication record count`: the number shown by the account's publication list, after pagination and deduplication of list records.
- `valid publication count`: publication records that have at least one readable child article; this is the batch output count.
- `child detail count`: unique `/s/` article URLs discovered inside those records; this is an implementation and QA metric only and is normally omitted from user-facing results.
- Never describe `child detail count` as the number of exported publications. A merged record may contain multiple child details, but it still produces one publication-record Markdown file.
- A skipped record can be reported with its title, URL, and reason, but it must not be included among the valid Markdown outputs.

## Final report

For a batch, report only these primary numbers unless the user requests technical diagnostics:

```text
发表记录总数：N
有效发表记录：M
跳过记录：K
Markdown 文件：M
```

The skipped count must include deleted, empty, unavailable, and access-blocked publication records. Do not include attempted, readable, or unique child detail page counts in the normal final report.

## QA acceptance criteria

Do not deliver until all of these are true:

- PDF text and Markdown content have no missing normalized lines.
- Every Markdown code block is closed; command and diagram blocks are not split by headings or prose.
- Every local image reference resolves, or every image reference is an intentional source URL.
- The ordered Markdown source image URLs match the captured source URLs when a source list is available.
- The PDF renders without clipped text, broken tables, blank images, or placeholder SVGs.

For the reusable PDF/Markdown checks, read and run scripts/validate_export.py. Final delivery should link the single Markdown file for a single-article request, or link the output directory/manifest for a batch request, and state the external-image availability caveat.
