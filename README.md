# ML — Python Documentation RAG Retrieval System

Cleans, chunks, and embeds the official Python 3.14 documentation, then loads it into a [Milvus](https://milvus.io/) vector database to build a knowledge base for RAG (Retrieval-Augmented Generation) queries.

## Project Structure

```
ML/
├── main/
│   └── main.py                  # End-to-end entry point: cleaned docs → create collection → chunk/embed → insert → build index → load
├── clean_doc/
│   ├── python-3.14-markdown/    # Raw Python 3.14 documentation (Markdown)
│   ├── cleaned_docs/            # Cleaned Markdown output
│   ├── clean.py                 # Cleans Markdown: strips link noise, HTML comments, heading anchors, etc. while preserving code blocks
│   ├── process_markdown.py      # Splits by headings (MarkdownHeaderTextSplitter) + recursive splitting, then calls embedding
│   └── embedding/
│       └── embedding.py         # Generates vectors using Ollama's bge-m3 model
└── vectorDB/
    ├── conf/
    │   └── schema.json          # Milvus collection field definitions (embedding, text, source_file, title, chunk_index, header_path, metadata)
    ├── milvus_manager/
    │   └── milvus_manager.py    # Milvus client initialization and retrieval
    ├── tools/
    │   ├── create.py            # Creates the collection and index (IVF_FLAT, L2) based on schema.json
    │   ├── insert.py            # Writes chunked data into the collection
    │   └── load_collection.py   # Loads the collection into memory for querying
    └── test/
        ├── test_tool_create.py
        └── test_tool_insert.py
```

## Data Processing Pipeline

1. **Clean documents** (`clean_doc/clean.py`)
   Cleans the raw Markdown under `python-3.14-markdown/` and writes the output to `cleaned_docs/`, removing documentation-site noise (heading anchor links, HTML comments, image/link syntax, etc.) while preserving headings, lists, tables, and code blocks.

   ```bash
   python clean_doc/clean.py --source clean_doc/python-3.14-markdown --output clean_doc/cleaned_docs
   ```

2. **Chunk and embed** (`clean_doc/process_markdown.py`)
   First splits by `#`/`##`/`###` headings, then further splits with `RecursiveCharacterTextSplitter` (chunk_size=1200, overlap=150). Each chunk is prefixed with a `Section: ...` header before being passed to `embedding.py`, which calls a local Ollama instance (`bge-m3` model) to generate a 1024-dimensional vector.

3. **Create collection and load into Milvus** (`vectorDB/tools/`)
   Creates a collection and an IVF_FLAT/L2 index based on `vectorDB/conf/schema.json`, batch-inserts the chunked data, flushes it, and loads the collection so it's ready for querying.

4. **One-shot run** (`main/main.py`)
   Reads every `.md` file in each subfolder under `cleaned_docs/`, cleans and chunks each one to produce embedding data, then creates the collection, inserts the data, builds the index, and loads the collection.

   ```bash
   python main/main.py
   ```

## Requirements

- Python 3.10+
- [Milvus](https://milvus.io/docs/install_standalone-docker.md) running at `http://localhost:19530` (credentials `root:Milvus`)
- [Ollama](https://ollama.com/) running at `http://localhost:11434`, with the `bge-m3` model pulled:

  ```bash
  ollama pull bge-m3
  ```

- Python packages: `pymilvus`, `langchain-ollama`, `langchain-text-splitters`

## Configuration Notes

- The collection name is hardcoded to `python3_14` (see `main/main.py`).
- The vector dimension is 1024 (matching `bge-m3` output), defined in `vectorDB/conf/schema.json`.
- Milvus connection details are hardcoded in `vectorDB/milvus_manager/milvus_manager.py` — edit the `server_url` and `token` there if you need to change them.
