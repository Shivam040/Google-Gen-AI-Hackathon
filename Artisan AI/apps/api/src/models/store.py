# apps/api/src/models/store.py
# Fields: id, display_name, owner_user_id, contact_email, region, craft_types[],
#         languages[], bio, social_handles{}, is_verified.
# Use: validate API in/out, Firestore writes (stores/{storeId}).

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator


class StoreProfile(BaseModel):
    """Represents an artisan's store/brand on the platform."""
    id: str

    display_name: str = Field(..., min_length=2, max_length=100)
    owner_user_id: str

    contact_email: Optional[EmailStr] = None
    region: Optional[str] = Field(default=None, description="e.g., UP, Uttarakhand, Kashmir")

    craft_types: List[str] = Field(
        default_factory=list,
        description='e.g., ["block printing", "bidriware", "woodwork"]'
    )
    languages: List[str] = Field(
        default_factory=lambda: ["en"],
        description="Supported storefront languages (BCP47/ISO codes)"
    )

    bio: Optional[str] = Field(default=None, max_length=1000)
    social_handles: Dict[str, str] = Field(
        default_factory=dict,
        description='Map of social handles/links, e.g., {"instagram":"@myshop","youtube":"https://..."}'
    )

    is_verified: bool = False

    # Optional fields typically filled by backend (Firestore timestamps)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # ---------- Normalizers (Pydantic v2) ----------
    @field_validator("craft_types", mode="before")
    @classmethod
    def _norm_craft_types(cls, v):
        if not v:
            return []
        return [str(x).strip() for x in v if str(x).strip()]

    @field_validator("languages", mode="before")
    @classmethod
    def _norm_languages(cls, v):
        if not v:
            return ["en"]
        out = []
        for code in v:
            c = str(code).strip().lower()
            if c:
                out.append(c)
        return out or ["en"]

    @field_validator("social_handles", mode="before")
    @classmethod
    def _norm_handles(cls, v):
        if not v:
            return {}
        d = {}
        for k, val in dict(v).items():
            key = str(k).strip().lower()
            if not key:
                continue
            sval = str(val).strip()
            if not sval:
                continue
            # Allow @handles or full URLs; keep as-is
            d[key] = sval
        return d
