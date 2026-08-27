from __future__ import annotations

import argparse
import html
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


def normalize(value: str) -> str:
    value = html.unescape(value)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u00a0", " ").replace("\ufeff", "").replace("\u200b", "")
    value = (
        value.replace("\\[", "[")
        .replace("\\]", "]")
        .replace("\\.", ".")
    )
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*([,.;:!?()\[\]{}/])\s*", r"\1", value)
    value = re.sub(r'"\s+', '"', value)
    value = re.sub(r'\s+"', '"', value)
    return value.strip()


def compact(value: str) -> str:
    return re.sub(r"\s+", "", normalize(value))


def is_fence(line: str) -> bool:
    marker = chr(96) * 3
    stripped = line.lstrip()
    return stripped.startswith(marker) or stripped.startswith("~~~")


def markdown_content_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    source_lines = markdown.splitlines()
    index = 0
    if source_lines and source_lines[0].strip() == "---":
        index = 1
        while index < len(source_lines) and source_lines[index].strip() != "---":
            index += 1
        index += 1

    in_code = False
    for raw in source_lines[index:]:
        line = raw.strip()
        if is_fence(raw):
            in_code = not in_code
            continue
        if not line or line == "---":
            continue
        if re.fullmatch(r"!\[[^\]]*\]\([^)]*\)", line):
            continue
        if re.fullmatch(r"\[[^\]]+\]:\s*\S+", line):
            continue
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"^>\s?", "", line)
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^\d+\.\s+", "", line)
        line = line.replace("**", "").replace("__", "").replace(chr(96), "")
        if line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                lines.extend(normalize(cell) for cell in cells if normalize(cell))
            continue
        value = normalize(line)
        if value:
            lines.append(value)
    return lines


def code_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    in_code = False
    for raw in markdown.splitlines():
        if is_fence(raw):
            in_code = not in_code
            continue
        if in_code:
            value = normalize(raw)
            if value:
                lines.append(value)
    return lines


def fence_stats(markdown: str) -> tuple[int, int, bool]:
    markers = 0
    blocks = 0
    in_code = False
    fence_char = ""
    backtick = chr(96)
    for raw in markdown.splitlines():
        stripped = raw.lstrip()
        if stripped.startswith(backtick * 3):
            token_char = backtick
        elif stripped.startswith("~~~"):
            token_char = "~"
        else:
            continue
        markers += 1
        if not in_code:
            in_code = True
            fence_char = token_char
            blocks += 1
        elif token_char == fence_char:
            in_code = False
            fence_char = ""
    return blocks, markers, in_code


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a Markdown export against its PDF.")
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--md", required=True, type=Path)
    parser.add_argument(
        "--expected-image-urls",
        type=Path,
        help="Optional text file containing source image URLs, one per line, in document order.",
    )
    parser.add_argument("--expected-pages", type=int)
    parser.add_argument("--expected-images", type=int)
    args = parser.parse_args()

    reader = PdfReader(str(args.pdf))
    pdf_text = normalize("\n".join(page.extract_text() or "" for page in reader.pages))
    markdown = args.md.read_text(encoding="utf-8")
    md_lines = markdown_content_lines(markdown)
    checked_code_lines = code_lines(markdown)
    code_blocks, fence_markers, unclosed = fence_stats(markdown)

    pdf_compact = compact(pdf_text)
    missing = sorted({line for line in md_lines if compact(line) not in pdf_compact})
    missing_code = sorted(
        {line for line in checked_code_lines if compact(line) not in pdf_compact}
    )
    image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown)
    missing_local_images = [
        ref for ref in image_refs
        if not ref.startswith(("http://", "https://")) and not (args.md.parent / ref).is_file()
    ]

    expected_urls = None
    image_url_order_match = "not_checked"
    if args.expected_image_urls:
        expected_urls = [
            line.strip()
            for line in args.expected_image_urls.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        actual_urls = [ref for ref in image_refs if ref.startswith(("http://", "https://"))]
        image_url_order_match = actual_urls == expected_urls

    print(f"pdf_pages={len(reader.pages)}")
    print(f"pdf_embedded_images={sum(len(page.images) for page in reader.pages)}")
    print(f"md_code_blocks={code_blocks}")
    print(f"md_code_fence_markers={fence_markers}")
    print(f"md_code_lines={len(checked_code_lines)}")
    print(f"md_image_refs={len(image_refs)}")
    print(f"missing_md_lines_in_pdf={len(missing)}")
    print(f"missing_code_lines_in_pdf={len(missing_code)}")
    print(f"missing_local_image_files={len(missing_local_images)}")
    print(f"image_url_order_match={image_url_order_match}")

    failures: list[str] = []
    if unclosed or fence_markers % 2:
        failures.append("Markdown code fences are not balanced")
    if missing:
        failures.append("Markdown contains lines not found in the PDF")
    if missing_code:
        failures.append("Markdown contains code lines not found in the PDF")
    if missing_local_images:
        failures.append("Markdown contains missing local image files")
    if expected_urls is not None and image_url_order_match is not True:
        failures.append("Markdown image URLs differ from the expected source list")
    if args.expected_pages is not None and len(reader.pages) != args.expected_pages:
        failures.append("PDF page count differs from expected")
    if args.expected_images is not None:
        actual_images = sum(len(page.images) for page in reader.pages)
        if actual_images != args.expected_images:
            failures.append("PDF image count differs from expected")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
