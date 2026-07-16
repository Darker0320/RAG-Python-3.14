"""Clean the Python documentation Markdown for RAG ingestion.

Preserve headings, lists, tables, inline code, and fenced code blocks while
removing documentation-site artifacts that add noise to embeddings.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DOCS_DIR = PROJECT_DIR / "python-3.14-markdown"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "cleaned_docs"

API_DEFINITION = re.compile(
    r"^\s*\*(?:async\s+)?(?:class|function|exception|method|classmethod|"
    r"staticmethod|attribute|data|decorator|coroutine)\*\s+(.+?)\s*$",
    re.IGNORECASE,
)
HEADING_PERMALINK = re.compile(
    r'\[¶\]\(#[^\s)]*(?:\s+"Link to this (?:heading|definition)")?\)',
    re.IGNORECASE,
)
MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\((?:[^()]|\([^()]*\))*\)")
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((?:[^()]|\([^()]*\))*\)")
AUTOLINK = re.compile(r"<((?:https?|mailto):[^>]+)>")
HTML_ANCHOR = re.compile(r"</?a\b[^>]*>", re.IGNORECASE)
FENCE = re.compile(r"^\s*((?:\x60){3,}|~{3,})(.*)$")


@dataclass
class CleanStats:
    files: int = 0
    input_chars: int = 0
    output_chars: int = 0


def _strip_links(line: str) -> str:
    """Keep human-readable link text and discard embedding-noisy targets."""

    line = MARKDOWN_IMAGE.sub(
        lambda match: f"Image: {match.group(1).strip()}"
        if match.group(1).strip()
        else "",
        line,
    )
    line = MARKDOWN_LINK.sub(lambda match: match.group(1), line)
    line = AUTOLINK.sub(lambda match: match.group(1), line)
    return line


def clean_markdown(text: str) -> str:
    """Return RAG-friendly Markdown without changing code block contents."""

    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    output: list[str] = []
    in_fence = False
    fence_character = ""
    in_comment = False

    for original_line in text.split("\n"):
        line = original_line.rstrip()
        line = re.sub(r"^\s*:\s{2,}(?=(?:\x60){3,}|~{3,})", "", line)
        fence_match = FENCE.match(line)

        if in_fence:
            output.append(line)
            if fence_match and fence_match.group(1)[0] == fence_character:
                in_fence = False
                fence_character = ""
            continue

        if fence_match:
            in_fence = True
            fence_character = fence_match.group(1)[0]
            output.append(line)
            continue

        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue
        while "<!--" in line:
            before, after = line.split("<!--", 1)
            if "-->" in after:
                line = before + after.split("-->", 1)[1]
            else:
                line = before
                in_comment = True
                break

        line = HEADING_PERMALINK.sub("", line)
        line = HTML_ANCHOR.sub("", line)
        line = _strip_links(line)

        definition = API_DEFINITION.match(line)
        if definition:
            line = f"### {definition.group(1).strip()}"

        line = re.sub(r"^\s*:\s{2,}", "", line)

        heading = re.match(r"^(#{1,6})\s*(.*?)\s*#*\s*$", line)
        if heading and heading.group(2):
            line = f"{heading.group(1)} {heading.group(2).strip()}"

        output.append(line.rstrip())

    cleaned = "\n".join(output).strip()
    cleaned = re.sub(r"\n[ \t]+\n", "\n\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned + "\n" if cleaned else ""


def process_file(source_file: Path, source_root: Path, output_root: Path) -> int:
    """Clean one file, preserving its path below the documentation root."""

    output_file = output_root / source_file.relative_to(source_root)
    raw = source_file.read_text(encoding="utf-8", errors="replace")
    cleaned = clean_markdown(raw)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(cleaned, encoding="utf-8", newline="\n")
    return len(cleaned)


def clean_directory(source_root: Path, output_root: Path) -> CleanStats:

    if not source_root.is_dir():
        raise FileNotFoundError(f"找不到 Markdown 來源資料夾：{source_root}")
    if source_root.resolve() == output_root.resolve():
        raise ValueError("來源資料夾與輸出資料夾不可相同")

    files = sorted(source_root.rglob("*.md"))
    if not files:
        raise FileNotFoundError(f"來源資料夾內沒有 .md 文件：{source_root}")

    stats = CleanStats()
    for source_file in files:
        raw_size = len(
            source_file.read_text(encoding="utf-8", errors="replace")
        )
        output_size = process_file(source_file, source_root, output_root)
        stats.files += 1
        stats.input_chars += raw_size
        stats.output_chars += output_size
    return stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="清洗 Python 文件 Markdown，輸出成適合 RAG 匯入的 Markdown。"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help=f"來源資料夾（預設：{DEFAULT_DOCS_DIR.name}）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"輸出資料夾（預設：{DEFAULT_OUTPUT_DIR.name}）",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source.resolve()
    output_root = args.output.resolve()

    try:
        stats = clean_directory(source_root, output_root)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"錯誤：{exc}")
        return 1

    reduction = 0.0
    if stats.input_chars:
        reduction = (1 - stats.output_chars / stats.input_chars) * 100
    print(f"完成：已清洗 {stats.files} 個 Markdown 文件")
    print(f"輸出：{output_root}")
    print(
        f"文字量：{stats.input_chars:,} → {stats.output_chars:,}"
        f"（減少 {reduction:.1f}%）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
