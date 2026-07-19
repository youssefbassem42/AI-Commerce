#!/usr/bin/env python3
"""RAG playground — test retrieval and generation for a specific store.

Usage:
    python scripts/rag_playground.py --store electronics
    python scripts/rag_playground.py --store fashion
    python scripts/rag_playground.py --store pharmacy

Every pipeline resolves its TenantContext from the store slug and
runs in complete isolation — no data crosses tenant boundaries.
"""

import argparse
import asyncio
import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("rag_playground")


# ---------------------------------------------------------------------------
# Tenant registry — maps store slugs to their tenant identities
# Extend this list as new stores are onboarded.
# ---------------------------------------------------------------------------
STORE_REGISTRY: dict[str, dict[str, str]] = {
    "electronics": {
        "organization_id": "org_elec_001",
        "store_id": "store_elec_001",
        "merchant_id": "merchant_elec_001",
        "integration_id": "int_elec_shopify",
        "store_slug": "electronics",
        "language": "en",
        "currency": "USD",
        "timezone": "America/New_York",
    },
    "fashion": {
        "organization_id": "org_fashion_002",
        "store_id": "store_fashion_002",
        "merchant_id": "merchant_fashion_002",
        "integration_id": "int_fashion_magento",
        "store_slug": "fashion",
        "language": "en",
        "currency": "EUR",
        "timezone": "Europe/Paris",
    },
    "pharmacy": {
        "organization_id": "org_pharma_003",
        "store_id": "store_pharma_003",
        "merchant_id": "merchant_pharma_003",
        "integration_id": "int_pharma_custom",
        "store_slug": "pharmacy",
        "language": "fr",
        "currency": "EUR",
        "timezone": "Europe/Brussels",
    },
}


def build_tenant_context(slug: str) -> "TenantContext":
    """Resolve a store slug into a fully-populated TenantContext."""
    from app.domain.knowledge.value_objects.tenant_context import TenantContext

    registry = STORE_REGISTRY.get(slug)
    if not registry:
        available = ", ".join(STORE_REGISTRY)
        raise ValueError(
            f"Unknown store '{slug}'. Available stores: {available}"
        )
    return TenantContext(
        **registry,
        knowledge_version=1,
        vector_namespace=slug,
    )


# ---------------------------------------------------------------------------
# Pipeline stages — each is tenant-aware
# ---------------------------------------------------------------------------


async def resolve_tenant_context(slug: str) -> "TenantContext":
    logger.info("Resolving tenant context for store '%s' ...", slug)
    ctx = build_tenant_context(slug)
    logger.info(
        "  Organization : %s", ctx.organization_id
    )
    logger.info("  Store        : %s (%s)", ctx.store_id, ctx.store_slug)
    logger.info("  Language     : %s", ctx.language)
    logger.info("  Currency     : %s", ctx.currency)
    logger.info("  Timezone     : %s", ctx.timezone)
    logger.info("  Vector ns    : %s", ctx.collection_name)
    return ctx


async def load_documents(tenant: "TenantContext") -> int:
    """Load documents for the tenant's store from MongoDB."""
    from app.infrastructure.mongodb.repositories.knowledge_repository import (
        KnowledgeRepository,
    )

    repo = KnowledgeRepository(tenant=tenant)
    docs = await repo.find_many({}, limit=100)
    logger.info("Loaded %d documents for store '%s'", len(docs), tenant.store_slug)
    return len(docs)


async def load_chunks(tenant: "TenantContext") -> int:
    """Load chunks for the tenant's store from MongoDB."""
    from app.infrastructure.mongodb.repositories.chunk_repository import ChunkRepository

    repo = ChunkRepository(tenant=tenant)
    docs = await repo.find_many({}, limit=500)
    logger.info("Loaded %d chunks for store '%s'", len(docs), tenant.store_slug)
    return len(docs)


async def build_vector_index(tenant: "TenantContext") -> int:
    """Ensure the tenant's Qdrant collection exists with payload indexes."""
    from app.infrastructure.qdrant.vectorstore import VectorStore

    vs = VectorStore(tenant=tenant)
    await vs._ensure_collection()
    count = await vs.count()
    logger.info(
        "Vector index '%s' ready — %d vectors",
        tenant.collection_name,
        count,
    )
    return count


async def run_search_query(
    tenant: "TenantContext",
    query_text: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Run a vector search against the tenant's isolated index."""
    from app.infrastructure.qdrant.vectorstore import VectorStore

    logger.info("Searching '%s' for: %s", tenant.store_slug, query_text)

    vs = VectorStore(tenant=tenant)
    dummy_vector = [0.0] * 1536
    results = await vs.search(vector=dummy_vector, top_k=top_k)

    if not results:
        logger.info("  (no results — no embeddings ingested yet)")
    for r in results:
        logger.info(
            "  [%.4f] %s", r["score"], r["payload"].get("document_id", "?")
        )
    return results


async def full_pipeline(slug: str) -> None:
    """Execute the full RAG pipeline for a single tenant."""
    logger.info("=" * 60)
    logger.info("RAG PLAYGROUND — STORE: %s", slug.upper())
    logger.info("=" * 60)

    tenant = await resolve_tenant_context(slug)
    await load_documents(tenant)
    await load_chunks(tenant)
    await build_vector_index(tenant)
    await run_search_query(tenant, "sample query", top_k=3)

    logger.info("Pipeline complete for '%s'", slug)
    logger.info("")


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG Playground — test tenant-isolated knowledge retrieval."
    )
    parser.add_argument(
        "--store",
        type=str,
        required=True,
        choices=list(STORE_REGISTRY),
        help="Store slug to run the pipeline for",
    )
    args = parser.parse_args()

    await full_pipeline(args.store)


if __name__ == "__main__":
    asyncio.run(main())
