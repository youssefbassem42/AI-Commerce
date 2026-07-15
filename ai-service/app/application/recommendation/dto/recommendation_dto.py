from datetime import datetime
from typing import List
from pydantic import BaseModel

class RecommendationDTO(BaseModel):
    id: str
    conversation_id: str
    customer_id: str
    recommended_product_ids: List[str]
    store_id: str
    accepted: bool
    rationale: str
    created_at: datetime

class BundleSuggestionDTO(BaseModel):
    id: str
    store_id: str
    title: str
    product_ids: List[str]
    total_price: float
    discount_percentage: float
    status: str
    created_at: datetime
    updated_at: datetime
