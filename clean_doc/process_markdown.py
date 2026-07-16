import os
import sys
from pathlib import Path
from typing import Any
from langchain_text_splitters import MarkdownHeaderTextSplitter , RecursiveCharacterTextSplitter

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from clean_doc.embedding.embedding import do_embedding

headers_to_split = [
    ("#","Header_1"),
    ("##","Header_2"),
    ('###',"Header_3"),
]
mk_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split,
    strip_headers=False)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150,
    separators=["\n\n","\n","\n*","。", ";", " ", ""]
)

def mkSplitter(file_content:str) -> list:
    return mk_splitter.split_text(file_content)

def recursiveSplitter(file_content:list) -> list:
    return recursive_splitter.split_documents(file_content)

def dismantle_begM3(file: Path) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []

    file_content = file.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    split_content = mkSplitter(file_content=file_content)
    recursive_split_content = recursiveSplitter(split_content)

    for index, data in enumerate(recursive_split_content):
        chunk_metadata = data.metadata or {}
        page_content = data.page_content.strip()

        header_values = [
            chunk_metadata.get("Header_1"),
            chunk_metadata.get("Header_2"),
            chunk_metadata.get("Header_3"),
        ]

        cleaned_headers = [
            value.strip()
            for value in header_values
            if isinstance(value, str) and value.strip()
        ]

        header_path = " > ".join(cleaned_headers)

        title = cleaned_headers[-1] if cleaned_headers else ""
        embedding_text = (
            f"Section: {header_path}\n\n{page_content}"
            if header_path
            else page_content
        )

        embedding_vector = do_embedding(embedding_text)

        documents.append({
            "text": page_content,
            "embedding": embedding_vector,
            "source_file": file.name,
            "title": title,
            "chunk_index": index,
            "header_path": header_path,
            "metadata": {
                **chunk_metadata,
                "source_file": file.name,
                "title": title,
                "header_path": header_path,
            },
        })
    return documents