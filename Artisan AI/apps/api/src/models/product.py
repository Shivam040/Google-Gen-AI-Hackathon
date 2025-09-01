# apps/api/src/models/product.py
# Fields: id, title, category, materials, region, images, base_cost, artisan_id,
# attributes{size,color,...}, provenance.
# Use: validate API in/out, Firestore writes.

from __future__ import annotations

import os
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field, field_validator

# Use storage.public_url(...) to turn relative paths into absolute HTTP URLs
from ..repos import storage

# Configurable placeholder object that already exists in your bucket
PLACEHOLDER_IMAGE_PATH = os.getenv("PLACEHOLDER_IMAGE_PATH", "uploads/Pottery_1.jpg")


class ProductIn(BaseModel):
    """Payload used to create/update a product."""
    title: str = Field(..., min_length=2, max_length=140)
    description: Optional[str] = Field(None, max_length=2000)
    category: Optional[str] = Field(None, description="e.g., pottery, weaving, woodwork")
    materials: List[str] = Field(default_factory=list)
    region: Optional[str] = Field(None, description="e.g., Saharanpur, Kutch, Channapatna")
    attributes: Dict[str, str] = Field(default_factory=dict, description="size, color, pattern, finish")

    # NOTE: strings (not HttpUrl) so we can accept data URLs and coerce relatives
    images: List[str] = Field(default_factory=list)

    artisan_id: Optional[str] = None
    base_cost: Optional[float] = Field(None, ge=0.0)
    skill_factor: Optional[float] = Field(1.0, ge=0.0, description="Relative skill/time effort 0..N")
    inventory: Optional[int] = Field(1, ge=0)
    provenance: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional provenance info (e.g., origin_story, acquired_year, lineage)",
    )

    # --- Normalizers (Pydantic v2) ---
    @field_validator("materials", mode="before")
    @classmethod
    def _norm_materials(cls, v):
        if not v:
            return []
        return [str(x).strip() for x in v if str(x).strip()]

    @field_validator("attributes", mode="before")
    @classmethod
    def _norm_attrs(cls, v):
        if not v:
            return {}
        return {str(k).strip(): str(vv).strip() for k, vv in dict(v).items() if str(k).strip()}

    @field_validator("images", mode="before")
    @classmethod
    def _images_to_absolute(cls, v):
        """
        Accepts list/tuple/set/str.
        - Keep data:image/... values (endpoint may ingest them).
        - Convert relative or placeholder-y values to absolute HTTP URLs via storage.public_url(...).
        """
        if not v:
            return []
        if isinstance(v, (set, tuple)):
            v = list(v)
        if not isinstance(v, list):
            v = [v]

        out: List[str] = []
        for u in v:
            s = str(u or "").strip()
            if not s:
                continue

            # data URLs allowed (ingested later by endpoint)
            if s.startswith("data:image/"):
                out.append(s)
                continue

            # already absolute
            if s.startswith("http://") or s.startswith("https://"):
                out.append(s)
                continue

            # treat placeholders/relatives as bucket objects -> absolute public URL
            if s.startswith("/placeholder-") or "placeholder" in s:
                out.append(storage.public_url(PLACEHOLDER_IMAGE_PATH))
            else:
                out.append(storage.public_url(s.lstrip("/")))
        return out


class ProductOut(ProductIn):
    id: str
    popularity: int = Field(0, ge=0, description="Simple counter for views/saves")
    is_active: bool = True
    created_at: Optional[str] = None  # filled by backend (Firestore server timestamp)
    updated_at: Optional[str] = None


# Back-compat alias so existing code can do: from models.product import Product
Product = ProductIn


# ---- Requests for generation ----
class GenerateRequest(BaseModel):
    langs: List[str] = Field(default_factory=lambda: ["en"])
    tone: str = Field("narrative", description="narrative|professional|playful|luxury|...")

    @field_validator("langs")
    @classmethod
    def _norm_langs(cls, v: List[str]) -> List[str]:
        out = []
        for code in v or []:
            c = str(code).strip().lower()
            if c:
                out.append(c)
        return out or ["en"]


# ---- Returned pointer to generated content assets ----
class ContentPointer(BaseModel):
    path: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    # For frontend convenience
    text: Optional[str] = None
    gcs_uri: Optional[str] = None
    url: Optional[str] = None


# apps/api/src/models/product.py  (add near your other models)
class QuickTextRequest(BaseModel):
    """
    - patch: optional partial product fields from the client *without* saving.
    - mode: what to generate.
    - persist: if true, we also update the stored product's description/story.
    """
    patch: Dict[str, Any] = Field(default_factory=dict)
    mode: Literal["both", "description", "story"] = "both"
    persist: bool = False

class QuickTextResponse(BaseModel):
    id: str
    description: Optional[str] = None
    story: Optional[str] = None
    used_fields: Dict[str, Any] = Field(default_factory=dict)
