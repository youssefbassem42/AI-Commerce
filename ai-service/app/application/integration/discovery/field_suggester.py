import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

SYNONYM_MAP: dict[str, list[str]] = {
    "title": ["name", "headline", "label", "product_name", "item_name"],
    "description": ["desc", "body_html", "body", "summary", "details", "description_html"],
    "price": ["cost", "amount", "unit_price", "sale_price", "price_amount", "regular_price"],
    "sku": ["sku", "barcode", "upc", "ean", "isbn", "code"],
    "inventory_quantity": ["stock", "quantity", "inventory", "qty", "stock_level", "available_quantity"],
    "weight": ["mass", "weight_grams", "weight_ounces"],
    "image": ["images", "photo", "picture", "thumbnail", "image_url", "featured_image"],
    "tags": ["tag", "labels", "category_ids"],
    "vendor": ["brand", "manufacturer", "supplier", "seller"],
    "product_type": ["type", "category", "product_category", "item_type"],
    "handle": ["slug", "url_handle", "permalink", "custom_url"],
    "external_id": ["id", "source_id", "origin_id", "remote_id", "legacy_id"],
    "email": ["e_mail", "mail", "email_address", "contact_email"],
    "phone": ["telephone", "phone_number", "tel", "mobile", "cell"],
    "first_name": ["firstname", "given_name", "forename", "fname"],
    "last_name": ["lastname", "surname", "family_name", "lname"],
    "total": ["total_price", "order_total", "grand_total", "total_amount"],
    "subtotal": ["subtotal_price", "sub_total", "subtotal_amount"],
    "currency": ["currency_code", "currency_iso", "monetary_currency"],
    "notes": ["note", "comment", "customer_note", "internal_note"],
    "status": ["state", "order_status", "fulfillment_status", "shipping_status"],
}


@dataclass
class SuggestedMapping:
    source: str
    target: str
    confidence: float
    transformer: Optional[str] = None

    def __hash__(self):
        return hash((self.source, self.target))


class FieldSuggester:
    """Suggest field mappings by name similarity."""

    EXACT_SCORE = 1.0
    SYNONYM_SCORE = 0.7
    SUBSTRING_SCORE = 0.5

    def suggest(
        self, external_fields: set[str], entity_type: str
    ) -> list[SuggestedMapping]:
        from app.application.integration.discovery.entity_detector import CANONICAL_FIELDS

        canonical = CANONICAL_FIELDS.get(entity_type, set())
        results: list[SuggestedMapping] = []

        if not canonical:
            return self._suggest_identity_mappings(external_fields)

        for ext_field in external_fields:
            ext_clean = ext_field.lower().replace("-", "_").strip()

            best_match: Optional[str] = None
            best_confidence = 0.0
            transformer_hint: Optional[str] = None

            for canon in canonical:
                if ext_clean == canon:
                    if self.EXACT_SCORE > best_confidence:
                        best_confidence = self.EXACT_SCORE
                        best_match = canon
                    continue

                if ext_clean in SYNONYM_MAP.get(canon, []):
                    score = self.SYNONYM_SCORE
                    if score > best_confidence:
                        best_confidence = score
                        best_match = canon
                    continue

                if canon in ext_clean or ext_clean in canon:
                    if self.SUBSTRING_SCORE > best_confidence:
                        best_confidence = self.SUBSTRING_SCORE
                        best_match = canon
                    continue

            if best_match:
                if best_match in ("price", "cost", "amount"):
                    transformer_hint = "string_to_decimal"
                elif "date" in best_match:
                    transformer_hint = "iso_date"
                results.append(
                    SuggestedMapping(
                        source=ext_field,
                        target=best_match,
                        confidence=best_confidence,
                        transformer=transformer_hint,
                    )
                )

        return results

    @staticmethod
    def _suggest_identity_mappings(external_fields: set[str]) -> list[SuggestedMapping]:
        """For unknown entity types create identity mappings so raw data is preserved."""
        id_field = None
        for candidate in ("id", "external_id", "source_id", "remote_id"):
            if candidate in external_fields or candidate.replace("_", "") in {f.replace("_", "") for f in external_fields}:
                id_field = candidate
                break
        results: list[SuggestedMapping] = []
        for f in external_fields:
            results.append(
                SuggestedMapping(
                    source=f,
                    target=f,
                    confidence=1.0,
                    transformer=None,
                )
            )
            if f == id_field:
                results.append(
                    SuggestedMapping(
                        source=f,
                        target="external_id",
                        confidence=0.8,
                        transformer=None,
                    )
                )
        return results