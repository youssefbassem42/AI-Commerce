#!/usr/bin/env python3
"""
RAG Pipeline Playground

Validates the complete Knowledge Base pipeline using existing project services.
Place PDF files in resources/testing/ and run:
    python scripts/rag_playground.py

Environment variables:
    RAG_PLAYGROUND_DEBUG=true   Enable verbose object dumps
    RAG_STORE_ID=my-store       Override default store ID
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DEBUG = os.getenv("RAG_PLAYGROUND_DEBUG", "false").lower() in ("true", "1", "yes")
STORE_ID = os.getenv("RAG_STORE_ID", "playground-store")
ORG_ID = os.getenv("RAG_ORG_ID", "playground-org")
RESOURCES_DIR = PROJECT_ROOT / "resources" / "testing"

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("rag_playground")


class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def cprint(color: str, *args: Any, **kwargs: Any) -> None:
    print(f"{color}", end="")
    print(*args, **kwargs)
    print(f"{Color.RESET}", end="")
    sys.stdout.flush()


def print_header(text: str) -> None:
    width = 72
    print()
    cprint(Color.CYAN + Color.BOLD, "━" * width)
    cprint(Color.CYAN + Color.BOLD, f"  {text}")
    cprint(Color.CYAN + Color.BOLD, "━" * width)
    print()


def print_success(text: str) -> None:
    cprint(Color.GREEN, f"  ✔ {text}")


def print_warning(text: str) -> None:
    cprint(Color.YELLOW, f"  ⚠ {text}")


def print_error(text: str) -> None:
    cprint(Color.RED, f"  ✘ {text}")


def print_info(text: str) -> None:
    cprint(Color.BLUE, f"  ℹ {text}")


def print_label(label: str, value: Any, color: str = "") -> None:
    if color:
        print(f"  {label}: ", end="")
        cprint(color, str(value))
    else:
        print(f"  {label}: {value}")


def debug_dump(label: str, obj: Any) -> None:
    if not DEBUG:
        return
    cprint(Color.MAGENTA + Color.DIM, f"\n  ── DEBUG [{label}] ──")
    try:
        if hasattr(obj, "model_dump"):
            text = json.dumps(obj.model_dump(), default=str, indent=2, ensure_ascii=False)
        elif hasattr(obj, "dict"):
            text = json.dumps(obj.dict(), default=str, indent=2, ensure_ascii=False)
        elif isinstance(obj, (list, tuple)):
            text = json.dumps(obj, default=str, indent=2, ensure_ascii=False)
        elif isinstance(obj, dict):
            text = json.dumps(obj, default=str, indent=2, ensure_ascii=False)
        else:
            text = str(obj)
        for line in text.splitlines():
            cprint(Color.MAGENTA + Color.DIM, f"  │ {line}")
    except Exception:
        cprint(Color.MAGENTA + Color.DIM, f"  │ {obj}")
    cprint(Color.MAGENTA + Color.DIM, "  ─────────────────────")


def _patch_settings() -> None:
    """Workaround for production bug: client.py reads settings.MONGO_URI
    but Settings nests it under MONGO_SETTINGS."""
    from app.core.config import settings
    for attr, nested in [("MONGO_URI", "MONGO_URI"), ("MONGO_DB", "MONGO_DB")]:
        if not hasattr(settings, attr):
            val = getattr(settings.MONGO_SETTINGS, nested)
            object.__setattr__(settings, attr, val)
            logger.info("Patched settings.%s -> %s", attr, val)


def _estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


async def step1_load_pdfs() -> list[Path]:
    print_header("STEP 1: Load PDFs")

    pdf_files = sorted(RESOURCES_DIR.glob("*.pdf"))
    if not pdf_files:
        print_warning(f"No PDFs found in {RESOURCES_DIR}")
        print_info("Place PDF files in resources/testing/ and re-run.")
        print_info(f"Creating directory: {RESOURCES_DIR}")
        RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
        return []

    print_success(f"Found {len(pdf_files)} PDF(s) in {RESOURCES_DIR}")
    print()

    pdfs_info = []
    for f in pdf_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        pages = "?"
        try:
            from pdfminer.pdfpage import PDFPage
            with open(f, "rb") as fh:
                pages = sum(1 for _ in PDFPage.get_pages(fh))
        except ImportError:
            try:
                import PyPDF2
                with open(f, "rb") as fh:
                    reader = PyPDF2.PdfReader(fh)
                    pages = len(reader.pages)
            except ImportError:
                pass
        except Exception:
            pass

        info = {"path": f, "size_mb": size_mb, "pages": pages}
        pdfs_info.append(info)
        print_label("Filename", f.name, Color.BOLD)
        print_label("  Size", f"{size_mb:.2f} MB")
        print_label("  Pages", str(pages))

    return pdfs_info


async def step2_process_documents(
    pdfs: list[dict],
    knowledge_repo,
    extractor_factory,
    pipeline,
) -> list[dict]:
    print_header("STEP 2: Document Processing")

    from app.application.knowledge.processing.processor import DocumentProcessor
    from app.domain.knowledge.entities.knowledge_document import KnowledgeDocument
    from app.domain.knowledge.value_objects import DocumentMetadata, DocumentVersion
    from bson import ObjectId

    processor = DocumentProcessor(
        repository=knowledge_repo,
        extractor_factory=extractor_factory,
        pipeline=pipeline,
    )

    results = []
    for pdf_info in pdfs:
        path = pdf_info["path"]
        cprint(Color.BOLD, f"\n  ── Processing: {path.name} ──")

        doc_id = str(ObjectId())
        doc = KnowledgeDocument(
            id=doc_id,
            store_id=STORE_ID,
            title=path.stem,
            description=f"Playground upload: {path.name}",
            source_url=None,
            metadata=DocumentMetadata(
                source_type="upload",
                mime_type="application/pdf",
                tags=["playground"],
            ),
            versions=[DocumentVersion(version_number=1, is_current=True)],
        )
        created = await knowledge_repo.create(doc)
        debug_dump("Created Document", created)

        start = time.perf_counter()
        try:
            updated = await processor.process(created, str(path))
            elapsed = time.perf_counter() - start
            debug_dump("Processed Document", updated)

            result = {
                "doc_id": doc_id,
                "document": updated,
                "path": path,
                "elapsed": elapsed,
            }
            results.append(result)

            print_success(f"Extracted text length: {updated.char_count:,} chars")
            print_label("  Word count", f"{updated.word_count:,}")
            print_label("  Language", updated.language)
            print_label("  Estimated tokens", f"{updated.estimated_tokens:,}")
            print_label("  Processing time", f"{elapsed:.2f}s")
        except Exception as e:
            elapsed = time.perf_counter() - start
            print_error(f"Processing failed: {e}")
            debug_dump("Processing Error", e)
            continue

    return results


async def step3_chunk_documents(
    processed_docs: list[dict],
    chunk_repo,
    knowledge_repo,
) -> list[dict]:
    print_header("STEP 3: Chunking")

    from app.application.knowledge.chunking.chunking_service import ChunkingService, ChunkingConfig
    from app.application.knowledge.chunking.config import ChunkingConfig as ChunkConfig

    chunking_service = ChunkingService(
        chunk_repository=chunk_repo,
        knowledge_repository=knowledge_repo,
    )

    config = ChunkConfig(chunk_size=1000, overlap=200, strategy="recursive")

    all_results = []
    for entry in processed_docs:
        doc = entry["document"]
        cprint(Color.BOLD, f"\n  ── Chunking: {doc.title} ──")

        try:
            start = time.perf_counter()
            result = await chunking_service.chunk_document(doc, config)
            elapsed = time.perf_counter() - start
            debug_dump("ChunkingResult", result)

            all_results.append({"doc_id": entry["doc_id"], "result": result, "elapsed": elapsed})

            chunk_sizes = [len(c.content) for c in result.chunks]
            avg_size = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
            largest = max(chunk_sizes) if chunk_sizes else 0
            smallest = min(chunk_sizes) if chunk_sizes else 0

            print_success(f"Strategy: {result.strategy}")
            print_label("  Chunk size", str(result.chunk_size))
            print_label("  Overlap", str(result.overlap))
            print_label("  Total chunks", str(result.chunk_count))
            print_label("  Avg chunk size", f"{avg_size:.0f} chars")
            print_label("  Largest chunk", f"{largest} chars")
            print_label("  Smallest chunk", f"{smallest} chars")
            print_label("  Chunking time", f"{elapsed:.2f}s")

            preview_count = min(3, len(result.chunks))
            print()
            for i in range(preview_count):
                c = result.chunks[i]
                preview = c.content[:150].replace("\n", " ")
                print_label(f"  Chunk [{i + 1}]", f"{preview}...")

            if len(result.chunks) > preview_count:
                last = result.chunks[-1]
                preview = last.content[:150].replace("\n", " ")
                print_label(f"  Chunk [{len(result.chunks)}] (last)", f"{preview}...")

        except Exception as e:
            print_error(f"Chunking failed: {e}")
            debug_dump("Chunking Error", e)

    return all_results


async def step4_generate_embeddings(
    chunk_results: list[dict],
    provider,
) -> list[dict]:
    print_header("STEP 4: Embedding Generation")

    from app.application.dto.ai_dto import EmbeddingRequest

    all_embeddings = []
    for entry in chunk_results:
        chunks = entry["result"].chunks
        texts = [c.content for c in chunks]
        cprint(Color.BOLD, f"\n  ── Embedding {len(texts)} chunks ──")

        if not texts:
            print_warning("No chunks to embed")
            continue

        try:
            start = time.perf_counter()
            request = EmbeddingRequest(input=texts, model="gemini-embedding-001")
            response = await provider.embeddings(request)
            elapsed = time.perf_counter() - start
            debug_dump("EmbeddingResponse", response)

            dim = len(response.embeddings[0]) if response.embeddings else 0
            all_embeddings.append({
                "doc_id": entry["doc_id"],
                "chunks": chunks,
                "embeddings": response.embeddings,
                "elapsed": elapsed,
            })

            print_success(f"Model: gemini-embedding-001")
            print_label("  Embedding dimension", str(dim))
            print_label("  Embedding count", str(len(response.embeddings)))
            print_label("  Generation time", f"{elapsed:.2f}s")
            print_label("  Storage status", "In-memory (ready for vector store)")

        except Exception as e:
            print_error(f"Embedding generation failed: {e}")
            debug_dump("Embedding Error", e)

    return all_embeddings


async def step5_insert_vectors(
    embedding_results: list[dict],
    vector_store,
) -> list[dict]:
    print_header("STEP 5: Vector Store Insertion")

    from app.infrastructure.vectorstore.base import VectorRecord

    collection_name = f"kb_{STORE_ID}"

    exists = await vector_store.collection_exists(collection_name)
    if exists:
        print_info(f"Recreating collection '{collection_name}' (old vector size)")
        await vector_store.delete_collection(collection_name)
    print_info(f"Creating collection '{collection_name}'")
    await vector_store.create_collection(
        collection_name=collection_name,
        vector_size=3072,
        distance="Cosine",
    )

    all_inserted = []
    for entry in embedding_results:
        cprint(Color.BOLD, f"\n  ── Inserting vectors for doc {entry['doc_id'][:8]}... ──")

        points = []
        for chunk, emb in zip(entry["chunks"], entry["embeddings"]):
            points.append(VectorRecord(
                id=chunk.id,
                vector=emb,
                payload={
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "content": chunk.content[:2000],
                    "chunk_index": chunk.chunk_index,
                    "store_id": STORE_ID,
                    "organization_id": ORG_ID,
                    "language": chunk.metadata.get("language", "en"),
                    "source_type": chunk.metadata.get("source_type", ""),
                },
            ))

        try:
            inserted = await vector_store.upsert(collection_name, points)
            all_inserted.append(inserted)
            print_success(f"Collection: {collection_name}")
            print_label("  Inserted vectors", str(inserted))
            print_label("  Namespace", collection_name)
            print_label("  Organization ID", ORG_ID)
            print_label("  Store ID", STORE_ID)
            print_label("  Index status", "Active")
        except Exception as e:
            print_error(f"Vector insertion failed: {e}")
            debug_dump("Vector Insert Error", e)

    return all_inserted


async def step6_generate_summary(
    knowledge_repo,
    summary_repo,
    provider,
) -> Optional[dict]:
    print_header("STEP 6: Business Summary Generation")

    from app.application.knowledge.generation.service import BusinessSummaryGenerationService
    from app.application.knowledge.generation.config import GenerationConfig

    gen_service = BusinessSummaryGenerationService(
        knowledge_repository=knowledge_repo,
        summary_repository=summary_repo,
        provider=provider,
    )

    config = GenerationConfig(model="gemini-2.5-flash", temperature=0.3, max_tokens=4096)

    try:
        start = time.perf_counter()
        summary = await gen_service.generate(STORE_ID, config)
        elapsed = time.perf_counter() - start
        debug_dump("BusinessSummary", summary)

        tokens = _estimate_tokens(summary.summary)

        print_success("Business overview generated")
        print_label("  Summary length", f"{len(summary.summary):,} chars")
        print_label("  Estimated tokens", str(tokens))
        print_label("  Prompt tokens", "N/A (computed by LLM provider)")
        print_label("  Completion tokens", "N/A (computed by LLM provider)")
        print_label("  Execution time", f"{elapsed:.2f}s")

        print()
        preview = summary.summary[:500].replace("\n", " ")
        print_label("Preview", f"{preview}...")

        return {"summary": summary, "elapsed": elapsed}

    except Exception as e:
        print_warning(f"Summary generation skipped: {e}")
        debug_dump("Summary Error", e)
        return None


async def step7_semantic_search(
    query: str,
    retriever,
) -> Optional[dict]:
    print_header(f"STEP 7: Semantic Search — \"{query}\"")

    from app.application.knowledge.retrieval.config import RetrievalConfig, RetrievalFilters

    config = RetrievalConfig(
        top_k=5,
        score_threshold=0.0,
        use_hybrid=False,
        use_mmr=False,
        rerank=False,
        embedding_model="gemini-embedding-001",
        collection_prefix="kb",
    )
    filters = RetrievalFilters(
        organization_id=ORG_ID,
        store_id=STORE_ID,
    )

    try:
        start = time.perf_counter()
        result = await retriever.search(query=query, filters=filters, config=config)
        elapsed = time.perf_counter() - start
        debug_dump("SearchResult", result)

        print_success(f"Found {result.total_count} result(s) in {elapsed:.2f}ms")
        print_label("  Strategy", result.strategy)
        print_label("  Latency", f"{result.latency_ms:.1f}ms")

        for i, r in enumerate(result.results[:5]):
            print()
            print_label(f"  Result [{i + 1}]", "")
            print_label("    Chunk ID", r.chunk_id[:24] + "...")
            print_label("    Document ID", r.document_id[:24] + "...")
            print_label("    Document title", r.document_title)
            print_label("    Score", f"{r.score:.4f}")
            print_label("    Rank", str(r.rank))
            preview = r.content[:200].replace("\n", " ")
            print_label("    Preview", f"{preview}...")
            if r.metadata:
                meta_str = json.dumps(r.metadata, default=str)
                print_label("    Metadata", meta_str[:200])

        return {"result": result, "elapsed": elapsed}

    except Exception as e:
        print_error(f"Search failed: {e}")
        debug_dump("Search Error", e)
        return None


async def step8_build_rag_prompt(
    query: str,
    retriever,
    summary_data: Optional[dict],
) -> Optional[dict]:
    print_header("STEP 8: RAG Prompt Construction")

    from app.application.knowledge.retrieval.config import RetrievalConfig, RetrievalFilters
    from app.application.rag.prompt import build_rag_messages
    from app.application.rag.dedup import deduplicate_chunks

    config = RetrievalConfig(
        top_k=5, score_threshold=0.0, use_hybrid=False,
        use_mmr=False, rerank=False,
        embedding_model="gemini-embedding-001",
    )
    filters = RetrievalFilters(organization_id=ORG_ID, store_id=STORE_ID)

    try:
        retrieval_result = await retriever.search(query=query, filters=filters, config=config)
        chunks = deduplicate_chunks(retrieval_result.results)
    except Exception as e:
        print_warning(f"Retrieval failed for prompt: {e}")
        chunks = []

    summary_text = None
    summary_version = None
    if summary_data:
        summary_text = summary_data["summary"].summary
        summary_version = summary_data["summary"].version_number

    MAX_CHUNK_CHARS = 2000
    MAX_CHUNKS_IN_CONTEXT = 10
    chunks_context_lines = []
    for i, c in enumerate(chunks[:MAX_CHUNKS_IN_CONTEXT]):
        snippet = c.content[:MAX_CHUNK_CHARS]
        chunks_context_lines.append(
            f"\n### Retrieved Knowledge Chunk [{i + 1}]\n"
            f"**Source:** {c.document_title}\n"
            f"{snippet}\n"
        )
    chunks_context = "\n".join(chunks_context_lines)

    system_content, user_content, raw_system_prompt = build_rag_messages(
        user_message=query,
        chunks_context=chunks_context,
        business_summary_context=summary_text,
        business_summary_version=summary_version,
    )

    from app.application.rag.prompt import RAG_SYSTEM_PROMPT, CONTEXT_PLACEHOLDER

    print()
    print_label("SYSTEM PROMPT (base rules)", "")
    print(f"{RAG_SYSTEM_PROMPT}\n")
    print("=" * 70)
    print()

    if summary_text:
        print_label("BUSINESS SUMMARY", "")
        print(f"{summary_text}\n")
        print("=" * 70)
        print()

    print_label("RETRIEVED CONTEXT", "")
    print(f"{chunks_context}\n")
    print("=" * 70)
    print()

    print_label("CONTEXT PLACEHOLDER", "")
    print(f"{CONTEXT_PLACEHOLDER}\n")
    print("=" * 70)
    print()

    print_label("USER PROMPT (question)", "")
    print(f"{user_content}\n")
    print("=" * 70)
    print()

    print_label("FINAL PROMPT SENT TO MODEL", "")
    full_prompt = (
        f"System: {system_content}\n\n"
        f"---\n\n"
        f"User: {user_content}"
    )
    print(f"{full_prompt}\n")

    return {
        "system_content": system_content,
        "user_content": user_content,
        "chunks": chunks,
    }


async def step9_chat_completion(
    rag_prompt_data: Optional[dict],
    chat_service,
) -> Optional[dict]:
    print_header("STEP 9: Chat Completion")

    from app.application.dto.ai_dto import ChatRequest, MessageDTO

    if not rag_prompt_data:
        print_warning("No RAG prompt data available, skipping chat")
        return None

    system_content = rag_prompt_data["system_content"]
    user_content = rag_prompt_data["user_content"]

    messages = [
        MessageDTO(role="system", content=system_content),
        MessageDTO(role="user", content=user_content),
    ]

    request = ChatRequest(
        messages=messages,
        model="gemini-2.5-flash",
        temperature=0.3,
        max_tokens=1024,
    )

    try:
        start = time.perf_counter()
        response = await chat_service.chat(request=request)
        elapsed = time.perf_counter() - start
        debug_dump("ChatResponse", response)

        provider_name = response.provider
        model_name = response.model
        usage = response.usage
        response_text = response.message.content
        if isinstance(response_text, list):
            response_text = " ".join(str(item) for item in response_text)

        print_success(f"Provider: {provider_name}")
        print_label("  Model", model_name)
        print_label("  Execution time", f"{elapsed:.2f}s")
        print_label("  Prompt tokens", str(usage.prompt_tokens))
        print_label("  Completion tokens", str(usage.completion_tokens))
        print_label("  Cost", f"${usage.cost:.6f}")

        print()
        print_label("Response", "")
        print(f"{response_text}\n")

        return {
            "response": response,
            "response_text": response_text,
            "elapsed": elapsed,
        }

    except Exception as e:
        print_error(f"Chat completion failed: {e}")
        debug_dump("Chat Error", e)
        return None


async def step10_interactive_mode(
    retriever,
    chat_service,
    summary_data: Optional[dict],
) -> None:
    print_header("STEP 10: Interactive Mode")

    from app.application.knowledge.retrieval.config import RetrievalConfig, RetrievalFilters
    from app.application.rag.prompt import build_rag_messages
    from app.application.rag.dedup import deduplicate_chunks
    from app.application.dto.ai_dto import ChatRequest, MessageDTO

    print_info("Type your questions below. Type 'exit' to quit.")
    print()

    while True:
        try:
            question = input(f"{Color.GREEN}>>{Color.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print_info("Exiting interactive mode.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print_info("Exiting interactive mode.")
            break

        config = RetrievalConfig(top_k=5, score_threshold=0.0, embedding_model="gemini-embedding-001")
        filters = RetrievalFilters(organization_id=ORG_ID, store_id=STORE_ID)

        try:
            retrieval_start = time.perf_counter()
            retrieval_result = await retriever.search(query=question, filters=filters, config=config)
            retrieval_elapsed = time.perf_counter() - retrieval_start
            chunks = deduplicate_chunks(retrieval_result.results)
        except Exception as e:
            print_warning(f"Retrieval failed: {e}")
            chunks = []
            retrieval_elapsed = 0

        print()
        print_label("Retrieved chunks", str(len(chunks)))
        for i, c in enumerate(chunks[:3]):
            print_label(f"  Chunk [{i + 1}] score", f"{c.score:.4f}")

        summary_text = None
        summary_version = None
        if summary_data:
            summary_text = summary_data["summary"].summary
            summary_version = summary_data["summary"].version_number

        chunks_context_lines = []
        for i, c in enumerate(chunks[:10]):
            snippet = c.content[:2000]
            chunks_context_lines.append(
                f"\n### Retrieved Knowledge Chunk [{i + 1}]\n"
                f"**Source:** {c.document_title}\n"
                f"{snippet}\n"
            )
        chunks_context = "\n".join(chunks_context_lines)

        system_content, user_content, _ = build_rag_messages(
            user_message=question,
            chunks_context=chunks_context,
            business_summary_context=summary_text,
            business_summary_version=summary_version,
        )

        print_label("Final prompt", f"({_estimate_tokens(system_content + user_content)} estimated tokens)")

        messages = [
            MessageDTO(role="system", content=system_content),
            MessageDTO(role="user", content=user_content),
        ]

        request = ChatRequest(
            messages=messages,
            model="gemini-2.5-flash",
            temperature=0.3,
            max_tokens=1024,
        )

        try:
            chat_start = time.perf_counter()
            response = await chat_service.chat(request=request)
            chat_elapsed = time.perf_counter() - chat_start

            response_text = response.message.content
            if isinstance(response_text, list):
                response_text = " ".join(str(item) for item in response_text)

            print()
            print_label("Provider", response.provider)
            print_label("Model", response.model)
            print_label("Execution time", f"{chat_elapsed:.2f}s")
            print_label("Prompt tokens", str(response.usage.prompt_tokens))
            print_label("Completion tokens", str(response.usage.completion_tokens))
            print_label("Cost", f"${response.usage.cost:.6f}")
            print()
            print_label("Answer", "")
            print(f"{response_text}\n")

        except Exception as e:
            print_error(f"Chat failed: {e}")
            debug_dump("Interactive Chat Error", e)


async def main() -> None:
    print()
    cprint(Color.CYAN + Color.BOLD, "╔══════════════════════════════════════════════════════════╗")
    cprint(Color.CYAN + Color.BOLD, "║        RAG Pipeline Playground — AI Commerce           ║")
    cprint(Color.CYAN + Color.BOLD, "╚══════════════════════════════════════════════════════════╝")

    _patch_settings()

    if not RESOURCES_DIR.exists():
        RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
        print_info(f"Created {RESOURCES_DIR}")
        print_info("Place PDF files there and re-run.")

    pdfs = await step1_load_pdfs()
    if not pdfs:
        return

    from app.infrastructure.mongodb.client import MongoClientManager
    from app.infrastructure.qdrant.provider import QdrantProvider
    from app.infrastructure.providers.factory import LLMProviderFactory
    from app.infrastructure.mongodb.repositories.knowledge_repository import KnowledgeRepository
    from app.infrastructure.mongodb.repositories.chunk_repository import ChunkRepository
    from app.infrastructure.mongodb.repositories.business_summary_repository import (
        BusinessSummaryRepository,
    )
    from app.infrastructure.knowledge.extractors import ExtractorFactory
    from app.application.knowledge.processing.pipeline import ProcessingPipeline
    from app.application.knowledge.retrieval.service import RetrieverService
    from app.application.knowledge.retrieval.reranker import LLMCrossEncoderReRanker
    from app.application.services.chat_service import ChatService

    await MongoClientManager.connect()
    print_success("MongoDB connected")

    vector_store: Optional[QdrantProvider] = None
    qdrant_connected = False
    try:
        vector_store = QdrantProvider()
        await vector_store.connect()
        qdrant_connected = True
        print_success("Qdrant connected")
    except Exception as e:
        print_warning(f"Qdrant connection failed: {e}")
        print_info("Vector store steps (5, 7, 8) will be skipped.")
        print_info("Start Qdrant: docker run -p 6333:6333 qdrant/qdrant")

    factory = LLMProviderFactory()
    provider = factory.get_provider(os.getenv("RAG_LLM_PROVIDER", "gemini"))
    print_success(f"LLM Provider: {os.getenv('RAG_LLM_PROVIDER', 'gemini')}")

    reranker = LLMCrossEncoderReRanker(provider=provider)
    retriever = RetrieverService(
        vector_store=vector_store or QdrantProvider(),
        llm_provider=provider,
        reranker=reranker,
    )
    chat_service = ChatService(provider_factory=LLMProviderFactory())

    knowledge_repo = KnowledgeRepository()
    chunk_repo = ChunkRepository()
    summary_repo = BusinessSummaryRepository()

    try:
        processed = await step2_process_documents(
            pdfs, knowledge_repo, ExtractorFactory(), ProcessingPipeline(),
        )
        if not processed:
            print_warning("No documents were processed successfully. Exiting.")
            return

        chunked = await step3_chunk_documents(processed, chunk_repo, knowledge_repo)

        embedded = await step4_generate_embeddings(chunked, provider)

        if qdrant_connected:
            await step5_insert_vectors(embedded, vector_store)
        else:
            print_header("STEP 5: Vector Store Insertion (skipped — Qdrant unavailable)")

        summary_data = await step6_generate_summary(knowledge_repo, summary_repo, provider)

        search_queries = [
            "What products does this business sell?",
            "What are the refund policies?",
            "How long is shipping?",
            "What payment methods are supported?",
        ]
        for q in search_queries:
            if qdrant_connected:
                await step7_semantic_search(q, retriever)
            else:
                print_header(f"STEP 7: Semantic Search — \"{q}\" (skipped — Qdrant unavailable)")

        rag_data = await step8_build_rag_prompt(
            "What are your shipping options and return policy?",
            retriever,
            summary_data,
        )

        await step9_chat_completion(rag_data, chat_service)

        await step10_interactive_mode(retriever, chat_service, summary_data)

    finally:
        if qdrant_connected and vector_store is not None:
            await vector_store.disconnect()
        MongoClientManager.disconnect()
        print_success("Connections closed")


if __name__ == "__main__":
    asyncio.run(main())
