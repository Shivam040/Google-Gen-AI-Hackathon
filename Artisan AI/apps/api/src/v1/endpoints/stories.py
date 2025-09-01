# endpoints/stories.py

# Purpose: Manage story versions per product/lang.
# Stores: doc in stories + GCS URI for markdown.

# apps/api/src/v1/endpoints/stories.py
# Purpose: Read story versions per product/lang (MVP read-only).
# Routes:
#   GET  /v1/stories?product_id=SH001&lang=hi  → list (filtered)
#   GET  /v1/stories/{product_id}/{lang}       → get one

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Query
from ...repos import firestore as fs
from google.cloud import firestore as gcf

router = APIRouter(prefix="/v1/stories", tags=["stories"])

# LIST (optionally filter by product_id, lang)
@router.get("")
def list_stories(
    product_id: Optional[str] = Query(None),
    lang: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
):
    if product_id:
        items = fs.list_stories(product_id, limit=limit)
        if lang:
            items = [s for s in items if s.get("lang") == lang]
        return {"ok": True, "items": items[:limit]}
    # No product_id filter: keep MVP simple (frontend usually queries per product)
    return {"ok": True, "items": []}

# GET one by composite key {product_id}_{lang}
@router.get("/{product_id}/{lang}")
def get_story(product_id: str, lang: str):
    doc_id = f"{product_id}_{lang}"
    # direct read (simple; keeps repo changes optional for MVP)
    db = gcf.Client()
    snap = db.collection("stories").document(doc_id).get()
    if not snap.exists:
        return {"ok": False, "error": "story not found"}
    data = snap.to_dict()
    data["id"] = doc_id
    return {"ok": True, "story": data}
