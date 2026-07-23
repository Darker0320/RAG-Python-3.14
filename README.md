# ML — Python Documentation RAG System

Cleans, chunks, and embeds the official Python 3.14 documentation into a [Milvus](https://milvus.io/) vector database, then serves a RAG (Retrieval-Augmented Generation) chat API on top of it: hybrid (dense + sparse) search, cross-encoder reranking, and LLM answer generation via an OpenAI-compatible endpoint.

## Project Structure

```
ML/
├── main/
│   └── main.py                  # Ingestion entry point: cleaned docs → create collection → chunk/embed → insert → build index → load
├── clean_doc/
│   ├── python-3.14-markdown/    # Raw Python 3.14 documentation (Markdown)
│   ├── cleaned_docs/            # Cleaned Markdown output
│   ├── clean.py                 # Cleans Markdown: strips link noise, HTML comments, heading anchors, etc. while preserving code blocks
│   ├── process_markdown.py      # Splits by headings (MarkdownHeaderTextSplitter) + recursive splitting, then embeds each chunk
│   └── embedding/
│       └── embedding.py         # BGE-M3 (FlagEmbedding) dense + sparse (lexical) vector generation
├── vectorDB/
│   ├── conf/
│   │   └── schema.json          # Milvus collection fields (dense_embedding, sparse_embedding, text, source_file, title, chunk_index, header_path, metadata)
│   ├── milvus_manager/
│   │   └── milvus_manager.py    # Milvus client initialization
│   ├── tools/
│   │   ├── create.py            # Creates the collection + AUTOINDEX (dense, COSINE) / SPARSE_INVERTED_INDEX (sparse, IP) based on schema.json
│   │   ├── insert.py            # Batch-inserts chunked data into the collection
│   │   ├── load_collection.py   # Loads the collection into memory for querying
│   │   └── search.py            # RAGRetriever: hybrid_search (dense+sparse, RRF ranking) and cross_rerank (BGE reranker)
│   └── test/
│       ├── test_tool_create.py
│       ├── test_tool_insert.py
│       └── test_tool_search.py
├── RAG/
│   ├── main.py                  # Flask API: /health and /chat endpoints
│   ├── conf/
│   │   └── model.json           # LLM backend URLs (ollama, vllm)
│   ├── generation/
│   │   └── gen_context.py       # Formats reranked chunks into context + builds the final grounded prompt
│   └── LLM/
│       └── openai.py            # OpenAI-compatible client that sends the prompt to the configured LLM backend
└── select_milvus_cli.py         # Standalone interactive CLI for testing dense-only search against Milvus
```

## Data Processing Pipeline (Ingestion)

1. **Clean documents** (`clean_doc/clean.py`)
   Cleans the raw Markdown under `python-3.14-markdown/` and writes the output to `cleaned_docs/`, removing documentation-site noise (heading anchor links, HTML comments, image/link syntax, etc.) while preserving headings, lists, tables, and code blocks.

   ```bash
   python clean_doc/clean.py --source clean_doc/python-3.14-markdown --output clean_doc/cleaned_docs
   ```

2. **Chunk and embed** (`clean_doc/process_markdown.py`)
   First splits by `#`/`##`/`###` headings, then further splits with `RecursiveCharacterTextSplitter` (chunk_size=1200, overlap=150). Each chunk is prefixed with a `Section: ...` header before being passed to `embedding.py`, which uses `BAAI/bge-m3` (via `FlagEmbedding`, on CUDA) to generate both a 1024-dimensional **dense** vector and a **sparse** (lexical weight) vector for hybrid retrieval.

3. **Create collection and load into Milvus** (`vectorDB/tools/`)
   Creates a collection based on `vectorDB/conf/schema.json`, builds an AUTOINDEX/COSINE index on `dense_embedding` and a SPARSE_INVERTED_INDEX/IP index on `sparse_embedding`, batch-inserts the chunked data, flushes it, and loads the collection so it's ready for querying.

4. **One-shot ingestion run** (`main/main.py`)
   Reads every `.md` file in each subfolder under `cleaned_docs/`, cleans and chunks each one to produce dense+sparse embedding data, then creates the collection, inserts the data, builds the indexes, and loads the collection.

   ```bash
   python main/main.py
   ```

## Query / Chat Pipeline (RAG/)

`RAG/main.py` exposes a Flask API that answers questions grounded in the ingested documentation:

1. **`POST /chat`** — accepts `{"message": "..."}`.
2. **Hybrid search** (`vectorDB/tools/search.py: RAGRetriever.hybrid_search`) — embeds the query with BGE-M3, runs parallel dense (COSINE) and sparse (IP) `AnnSearchRequest`s against Milvus, and fuses results with `RRFRanker`.
3. **Cross-encoder rerank** (`RAGRetriever.cross_rerank`) — re-scores the top candidates with `BAAI/bge-reranker-v2-m3` and keeps the top 5.
4. **Context + prompt construction** (`RAG/generation/gen_context.py`) — formats the reranked chunks (title, section/header path, source file, text) into context, then builds a grounded prompt instructing the LLM to answer only from that context.
5. **LLM generation** (`RAG/LLM/openai.py`) — sends the prompt to an OpenAI-compatible endpoint (backend selected via `RAG/conf/model.json`, currently `ollama` → `qwen3.6:35b`) and returns the generated answer.

   ```bash
   python RAG/main.py
   # Flask server on http://localhost:8080

   curl -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "How do I use asyncio.TaskGroup?"}'
   ```

`GET /health` returns a simple liveness check.

## Requirements

- Python 3.10+
- CUDA-capable GPU (embedding, sparse encoding, and reranking models run on `cuda`)
- [Milvus](https://milvus.io/docs/install_standalone-docker.md) running at `http://localhost:19530` (credentials `root:Milvus`)
- An OpenAI-compatible LLM endpoint reachable at the URL configured in `RAG/conf/model.json` (e.g. [Ollama](https://ollama.com/) at `http://localhost:11434/v1`, or vLLM)
- Python packages: `pymilvus`, `langchain-text-splitters`, `FlagEmbedding`, `sentence-transformers`, `torch`, `flask`, `openai`

## Configuration Notes

- The collection name is hardcoded to `python3_14` (see `main/main.py`, `RAG/main.py`).
- Vector dimension is 1024 (matching `bge-m3` dense output), defined in `vectorDB/conf/schema.json`; the collection also stores a `sparse_embedding` field for hybrid search.
- Milvus connection details are hardcoded in `vectorDB/milvus_manager/milvus_manager.py` — edit `server_url` and `token` there if you need to change them.
- The LLM backend used by `/chat` is selected by the `tool` argument passed to `send_request_to_openai` (currently hardcoded to `"ollama"` in `RAG/main.py`); backend URLs live in `RAG/conf/model.json`.
- `select_milvus_cli.py` is a standalone dense-only search CLI (uses `sentence-transformers` directly) useful for quickly sanity-checking what's stored in Milvus, independent of the hybrid search + rerank pipeline used by the Flask API.
