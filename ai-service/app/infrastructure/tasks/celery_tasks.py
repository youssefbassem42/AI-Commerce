import asyncio
import time
import logging
from typing import List, Dict, Any
from app.core.celery_app import celery_app
from app.infrastructure.providers.factory import LLMProviderFactory
from app.application.dto.ai_dto import EmbeddingRequest, ChatRequest, MessageDTO
from app.infrastructure.repositories.conversation_repository import ConversationRepository
from app.core.model_registry import ModelRegistry

logger = logging.getLogger("ai_service")

def _run_async(coro):
    """Helper to run async coroutines synchronously in Celery worker processes."""
    return asyncio.run(coro)

@celery_app.task(name="ai.generate_embeddings")
def generate_embeddings_task(texts: List[str], model: str) -> List[List[float]]:
    """
    Generate embeddings for a list of texts in the background.
    """
    async def _async_run():
        model_info = ModelRegistry.get_model_info(model)
        if not model_info:
            raise ValueError(f"Model '{model}' not found in registry.")
            
        factory = LLMProviderFactory()
        provider = factory.get_provider(model_info.provider)
        
        request = EmbeddingRequest(input=texts, model=model)
        response = await provider.embeddings(request)
        return response.embeddings

    logger.info(f"Triggering background embedding generation for {len(texts)} items using {model}")
    return _run_async(_async_run())

@celery_app.task(name="ai.summarize_conversation")
def summarize_conversation_task(conversation_id: str, model: str = "gpt-4o-mini") -> str:
    """
    Generate a summary of a conversation and update its metadata in MongoDB.
    """
    async def _async_run():
        repo = ConversationRepository()
        conversation = await repo.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation '{conversation_id}' not found.")
            
        messages = conversation.get("messages", [])
        if not messages:
            return "No messages to summarize."

        # Compile message text
        text_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, list):
                content_str = " ".join([str(c) for c in content])
            else:
                content_str = str(content)
            text_parts.append(f"{role.capitalize()}: {content_str}")
        
        full_transcript = "\n".join(text_parts)
        
        # Call Chat Service / Provider to summarize
        model_info = ModelRegistry.get_model_info(model)
        if not model_info:
            raise ValueError(f"Model '{model}' not found in registry.")
            
        factory = LLMProviderFactory()
        provider = factory.get_provider(model_info.provider)
        
        prompt = f"Please provide a concise summary of the following conversation transcript:\n\n{full_transcript}"
        request = ChatRequest(
            messages=[MessageDTO(role="user", content=prompt)],
            model=model
        )
        response = await provider.chat(request)
        summary = response.message.content
        
        # Save summary to conversation metadata
        metadata = conversation.get("metadata", {})
        metadata["summary"] = summary
        metadata["summarized_at"] = time.time()
        
        await repo.collection.update_one(
            {"conversation_id": conversation_id},
            {"$set": {"metadata": metadata}}
        )
        return summary

    logger.info(f"Triggering background summarization for conversation: {conversation_id}")
    return _run_async(_async_run())
