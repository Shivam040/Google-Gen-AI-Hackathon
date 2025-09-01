# apps/api/src/models/marketing.py
# Fields: product_id, lang, channel, post_text, hashtags[], best_time.
# Use: generated assets + scheduling.

from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator

# Allowed channels for validation/autocomplete
Channel = Literal["instagram", "facebook", "whatsapp", "x", "youtube"]

class MarketingRequest(BaseModel):
    product_id: str
    lang: str = Field("en", description="ISO code, e.g., en, hi, bn")
    channel: Channel = Field("instagram", description="instagram|facebook|whatsapp|x|youtube")
    # Optional user-provided tags to merge with defaults (service will cap/unique)
    extra_tags: Optional[List[str]] = Field(default=None, description="Additional hashtags (with or without #)")

class MarketingAsset(BaseModel):
    product_id: str
    lang: str
    channel: Channel
    post_text: str = Field(..., max_length=2200, description="Final caption/text for the post")
    hashtags: List[str] = Field(default_factory=list, description="Normalized list of hashtags (with #)")
    best_time_iso: Optional[str] = Field(
        default=None,
        description="ISO-8601 datetime (UTC) recommended publish time, e.g., 2025-09-19T13:30:00Z",
    )
    image_uri: Optional[HttpUrl] = Field(
        default=None,
        description="(Optional) Link to generated marketing image in GCS or CDN",
    )

    @field_validator("hashtags")
    @classmethod
    def _normalize_hashtags(cls, v: List[str]) -> List[str]:
        """Ensure each tag starts with '#', remove empties/dupes, cap to 10 for safety."""
        seen = set()
        norm: List[str] = []
        for tag in v or []:
            t = tag.strip()
            if not t:
                continue
            if not t.startswith("#"):
                t = f"#{t}"
            # very light cleanup: collapse internal spaces
            t = "#"+t[1:].replace(" ", "")
            if t not in seen:
                seen.add(t)
                norm.append(t)
            if len(norm) >= 10:
                break
        return norm