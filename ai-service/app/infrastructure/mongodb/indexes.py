import logging
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT

logger = logging.getLogger(__name__)

async def setup_database_indexes(db) -> None:
    """Create all indexes on collections for fast lookup and query optimization."""
    logger.info("Initializing database indexes...")
    
    await db["conversations"].create_indexes([
        IndexModel([("customer_id", ASCENDING)]),
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("store_id", ASCENDING), ("customer_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)])
    ])
    
    await db["messages"].create_indexes([
        IndexModel([("conversation_id", ASCENDING)]),
        IndexModel([("conversation_id", ASCENDING), ("timestamp", ASCENDING)]),
        IndexModel([("timestamp", ASCENDING)])
    ])
    
    await db["knowledge_documents"].create_indexes([
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING)]),
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("title", TEXT)], name="knowledge_doc_title_text"),
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING), ("status", ASCENDING)]),
    ])
    
    await db["knowledge_chunks"].create_indexes([
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING)]),
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING), ("document_id", ASCENDING)]),
        IndexModel([("document_id", ASCENDING)]),
        IndexModel([("document_id", ASCENDING), ("chunk_index", ASCENDING)], unique=True),
        IndexModel([("embedding_id", ASCENDING)], sparse=True)
    ])

    await db["knowledge_business_summaries"].create_indexes([
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING)]),
        IndexModel([("document_id", ASCENDING)]),
        IndexModel([("document_id", ASCENDING), ("version_number", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)])
    ])

    await db["knowledge_uploads"].create_indexes([
        IndexModel([("organization_id", ASCENDING), ("store_id", ASCENDING)]),
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("checksum", ASCENDING)], unique=True),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("uploaded_by", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("store_id", ASCENDING), ("status", ASCENDING)]),
    ])
    
    await db["runtime_logs"].create_indexes([
        IndexModel([("conversation_id", ASCENDING)]),
        IndexModel([("timestamp", ASCENDING)], expireAfterSeconds=2592000), # 30 days
        IndexModel([("level", ASCENDING)])
    ])
    
    await db["prompt_history"].create_indexes([
        IndexModel([("runtimeId", ASCENDING)]),
        IndexModel([("timestamp", ASCENDING)], expireAfterSeconds=2592000),
        IndexModel([("provider", ASCENDING), ("model", ASCENDING)])
    ])
    
    await db["recommendations"].create_indexes([
        IndexModel([("conversation_id", ASCENDING)]),
        IndexModel([("customer_id", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)])
    ])
    
    await db["bundle_suggestions"].create_indexes([
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)])
    ])
    
    await db["abandoned_cart_campaigns"].create_indexes([
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("customer_id", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("store_id", ASCENDING), ("status", ASCENDING)])
    ])
    
    await db["dashboard_insights"].create_indexes([
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("calculated_at", DESCENDING)])
    ])
    
    await db["ticket_analysis"].create_indexes([
        IndexModel([("ticket_id", ASCENDING)], unique=True),
        IndexModel([("store_id", ASCENDING)]),
        IndexModel([("customer_id", ASCENDING)]),
        IndexModel([("priority", ASCENDING)]),
        IndexModel([("sentiment", ASCENDING)])
    ])
    
    logger.info("Database indexes successfully created.")
