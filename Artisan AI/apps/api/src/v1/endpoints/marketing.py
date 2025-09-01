# apps/api/src/v1/endpoints/marketing.py
# Purpose: Queue or directly generate social posts & suggestions.
# Routes:
#   POST /v1/marketing/{product_id}/post   → generate (mode=sync|event)
#   GET  /v1/marketing/suggest             → helper (hashtags + best_time)

from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, Body, Query
from ...repos import firestore as fs
from ...models.marketing import MarketingRequest
from ...services.marketing_service import (
    request_marketing,
    create_post,            # sync generation path (Firebase-only safe)
    suggest_hashtags,
    suggest_best_time,
)

router = APIRouter(prefix="/v1/marketing", tags=["marketing"])

@router.post("/{product_id}/post")
def marketing_post(
    product_id: str,
    lang: str = Query("en"),
    channel: str = Query("instagram"),
    mode: str = Query("sync", regex="^(sync|event)$"),
    extra_tags: Optional[List[str]] = Body(default=None),
):
    """
    mode=sync  → generate caption now (mock in Firebase-only; Gemini when enabled)
    mode=event → publish 'marketing.asset.requested' for worker to process later
    """
    prod = fs.get_product(product_id)
    if not prod:
        return {"ok": False, "error": "product not found"}

    if mode == "event":
        op = request_marketing(
            MarketingRequest(product_id=product_id, lang=lang, channel=channel, extra_tags=extra_tags or []),
            actor={"via": "api", "role": "artisan"},
        )
        return {"ok": True, "queued": True, "op_id": op, "mode": "event"}

    # mode == "sync"
    doc = create_post(prod, lang, channel, extra_tags)
    return {"ok": True, "doc": doc, "mode": "sync"}

@router.get("/suggest")
def suggest(channel: str = Query("instagram")):
    return {"hashtags": suggest_hashtags(channel), "best_time": suggest_best_time()}


# # endpoints/marketing.py

# # Purpose: Queue social posts & suggestions.
# # Routes: POST /{product_id}/post (lang, channel), GET /suggest (hashtags, times).
# # Uses: services.marketing_service.

# from fastapi import APIRouter, Body
# from ...models.marketing import MarketingRequest
# from ...services.marketing_service import request_marketing, suggest_hashtags, suggest_best_time

# router = APIRouter()

# @router.post("/{product_id}/post")
# def create_post(product_id: str, lang: str = "en", channel: str = "instagram"):
#     op = request_marketing(MarketingRequest(product_id=product_id, lang=lang, channel=channel), actor={"role":"artisan"})
#     return {"queued": True, "op_id": op}

# @router.get("/suggest")
# def suggest(channel: str = "instagram"):
#     return {"hashtags": suggest_hashtags(channel), "best_time": suggest_best_time()}
