# apps/api/src/v1/endpoints/recs.py
# Purpose: Personalized recs & search (MVP).
# Routes:
#   GET  /v1/recs/user/{user_id}?k=12&category_hint=...
#   GET  /v1/recs/similar/{product_id}?k=12
#   GET  /v1/recs/popular?k=12
#   POST /v1/recs/search  {query, k}

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field

from ...services.recs_service import (
    get_recs_for_user,
    similar_items,
    popular_products,
    search_semantic,
)

router = APIRouter(prefix="/v1/recs", tags=["recs"])


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    k: int = Field(12, ge=1, le=100, description="number of results")


@router.get("/user/{user_id}")
def recs_for_user(
    user_id: str,
    k: int = Query(12, ge=1, le=100),
    category_hint: Optional[str] = Query(None, description="e.g., 'woodwork', 'textile'"),
):
    items = get_recs_for_user(user_id, k=k, category_hint=category_hint)
    return {"ok": True, "items": items}


@router.get("/similar/{product_id}")
def recs_similar(product_id: str, k: int = Query(12, ge=1, le=100)):
    items = similar_items(product_id, k=k)
    return {"ok": True, "items": items}


@router.get("/popular")
def recs_popular(k: int = Query(12, ge=1, le=100)):
    items = popular_products(k=k)
    return {"ok": True, "items": items}


@router.post("/search")
def recs_search(body: SearchRequest = Body(...)):
    items = search_semantic(body.query, k=body.k)
    return {"ok": True, "items": items}


# # endpoints/recs.py

# # Purpose: Personalized recs & search.
# # Routes: GET /user/{user_id}?k=12, POST /search (query + filters).
# # Uses: services.recs_service.

# from fastapi import APIRouter
# from ...services.recs_service import get_recs_for_user

# router = APIRouter()

# @router.get("/user/{user_id}")
# def recs(user_id: str, k: int = 12, category_hint: str | None = None):
#     return {"items": get_recs_for_user(user_id, k=k, category_hint=category_hint)}
