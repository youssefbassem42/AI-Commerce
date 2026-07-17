from app.core.knowledge_settings import knowledge_settings
from app.infrastructure.mongodb.client import get_mongodb


def get_collection(name: str):
    """Retrieve collection reference dynamically."""
    return get_mongodb()[name]


def get_conversations_collection():
    return get_collection("conversations")


def get_messages_collection():
    return get_collection("messages")


def get_knowledge_documents_collection():
    return get_collection(knowledge_settings.documents_collection)


def get_knowledge_chunks_collection():
    return get_collection(knowledge_settings.chunks_collection)


def get_knowledge_business_summaries_collection():
    return get_collection(knowledge_settings.summaries_collection)


def get_knowledge_uploads_collection():
    return get_collection(knowledge_settings.uploads_collection)


def get_runtime_logs_collection():
    return get_collection("runtime_logs")


def get_prompt_history_collection():
    return get_collection("prompt_history")


def get_recommendations_collection():
    return get_collection("recommendations")


def get_bundle_suggestions_collection():
    return get_collection("bundle_suggestions")


def get_abandoned_cart_campaigns_collection():
    return get_collection("abandoned_cart_campaigns")


def get_dashboard_insights_collection():
    return get_collection("dashboard_insights")


def get_ticket_analysis_collection():
    return get_collection("ticket_analysis")
