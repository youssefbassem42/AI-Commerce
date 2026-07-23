import logging
from typing import Optional

logger = logging.getLogger(__name__)

CANONICAL_FIELDS: dict[str, set[str]] = {
    "product": {
        "title",
        "name",
        "description",
        "price",
        "sku",
        "inventory_quantity",
        "stock",
        "images",
        "category_id",
        "vendor",
        "product_type",
        "tags",
        "weight",
        "status",
        "handle",
        "external_id",
    },
    "order": {
        "email",
        "total",
        "subtotal",
        "currency",
        "line_items",
        "financial_status",
        "fulfillment_status",
        "shipping",
        "billing",
        "notes",
        "tags",
        "customer_id",
    },
    "customer": {
        "email",
        "first_name",
        "last_name",
        "phone",
        "addresses",
        "city",
        "country",
        "zip",
        "state",
        "total_spent",
        "orders_count",
        "note",
        "tags",
    },
    "category": {
        "name",
        "title",
        "description",
        "parent_id",
        "image",
        "sort_order",
        "handle",
    },
}

FIELD_SYNONYMS: dict[str, set[str]] = {
    "title": {"name", "headline", "label"},
    "price": {"cost", "amount", "unit_price", "sale_price"},
    "sku": {"sku", "barcode", "upc", "ean", "isbn"},
    "inventory_quantity": {"stock", "quantity", "inventory", "qty", "stock_level"},
    "description": {"desc", "body_html", "body", "summary", "details"},
    "image": {"images", "photo", "picture", "media", "thumbnail"},
    "email": {"e_mail", "mail", "email_address"},
    "phone": {"telephone", "phone_number", "tel", "mobile"},
    "first_name": {"firstname", "given_name", "forename"},
    "last_name": {"lastname", "surname", "family_name"},
    "address": {"addresses", "location", "shipping_address", "billing_address"},
    "tags": {"tag", "labels", "categories", "collections"},
    "handle": {"slug", "url_handle", "permalink"},
    "external_id": {"id", "source_id", "origin_id", "remote_id"},
}


class EntityDetectionResult:
    def __init__(
        self,
        entity_type: Optional[str],
        confidence: float,
        matched_fields: list[str],
    ):
        self.entity_type = entity_type
        self.confidence = confidence
        self.matched_fields = matched_fields


class EntityDetector:
    """Compare external schema field names against canonical field names.

    The detector scores each entity type by:
      - exact match (weight 1.0)
      - substring match (weight 0.6)
      - synonym match (weight 0.4)
    """

    EXACT_WEIGHT = 1.0
    SUBSTRING_WEIGHT = 0.6
    SYNONYM_WEIGHT = 0.4

    def detect(
        self, external_fields: set[str], entity_type_hint: Optional[str] = None
    ) -> EntityDetectionResult:
        candidates = [entity_type_hint] if entity_type_hint else list(CANONICAL_FIELDS.keys())
        best_type: Optional[str] = None
        best_score = 0.0
        best_matched: list[str] = []

        external_lower = {f.lower().replace("-", "_") for f in external_fields}

        for candidate in candidates:
            canonical = CANONICAL_FIELDS.get(candidate, set())
            score = 0.0
            matched: list[str] = []
            for ext_field in external_lower:
                score_contribution, match = self._score_field(ext_field, canonical)
                if score_contribution > 0:
                    score += score_contribution
                    if match:
                        matched.append(match)
            if score > best_score:
                best_score = score
                best_type = candidate
                best_matched = matched

        if best_type is None or best_score < 0.5:
            return EntityDetectionResult(
                entity_type=None,
                confidence=0.0,
                matched_fields=[],
            )

        max_possible = len(CANONICAL_FIELDS.get(best_type, set())) * self.EXACT_WEIGHT
        confidence = min(round(best_score / max_possible, 4), 1.0) if max_possible > 0 else 0.0

        return EntityDetectionResult(
            entity_type=best_type,
            confidence=confidence,
            matched_fields=list(set(best_matched)),
        )

    def _score_field(self, ext_field: str, canonical_set: set[str]) -> tuple[float, Optional[str]]:
        cleaned = ext_field.replace(" ", "_").strip()
        if cleaned in canonical_set:
            return self.EXACT_WEIGHT, cleaned
        for canon in canonical_set:
            if canon in cleaned or cleaned in canon:
                return self.SUBSTRING_WEIGHT, canon
        for canon in canonical_set:
            synonyms = FIELD_SYNONYMS.get(canon, set())
            if cleaned in synonyms:
                return self.SYNONYM_WEIGHT, canon
        return 0.0, None