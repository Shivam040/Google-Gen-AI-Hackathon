# apps/api/src/services/recs_service.py
# Purpose: Recommendations & semantic search (MVP → Firestore popularity/category).
# Later: Vertex Vector Search (embeddings) + re-rank (availability, margin, etc).

from __future__ import annotations

from typing import List, Optional, Dict, Any
from google.cloud import firestore
from ..core.config import get_settings

_settings = get_settings()
_db = firestore.Client(project=_settings.gcp_project)

COLL_PRODUCTS = _settings.firestore_collection_products  # "products"


def _to_out(doc: firestore.DocumentSnapshot) -> Dict[str, Any]:
    d = doc.to_dict() or {}
    d["id"] = doc.id
    return d


def popular_products(k: int = 12) -> List[Dict[str, Any]]:
    """
    Top-K products by popularity. Tries to prefer active products.
    NOTE: If you add `where("is_active", "==", True)` with order_by(popularity),
    Firestore may require a composite index (is_active ↑, popularity ↓).
    """
    # Try active-only (best). If it fails due to index, fall back gracefully.
    try:
        q = (
            _db.collection(COLL_PRODUCTS)
            .where("is_active", "==", True)
            .order_by("popularity", direction=firestore.Query.DESCENDING)
            .limit(k)
        )
        snaps = q.stream()
        items = [_to_out(s) for s in snaps]
        if items:
            return items
    except Exception:
        pass  # likely missing composite index; fall back without filter

    q = (
        _db.collection(COLL_PRODUCTS)
        .order_by("popularity", direction=firestore.Query.DESCENDING)
        .limit(k)
    )
    snaps = q.stream()
    return [_to_out(s) for s in snaps]


def similar_by_category(category: str, k: int = 12) -> List[Dict[str, Any]]:
    """
    Recommend within the same category, ordered by popularity.
    Requires composite index: (category ↑, popularity ↓) if you haven’t added it yet.
    """
    q = (
        _db.collection(COLL_PRODUCTS)
        .where("category", "==", category)
        .order_by("popularity", direction=firestore.Query.DESCENDING)
        .limit(k)
    )
    snaps = q.stream()
    return [_to_out(s) for s in snaps]


def similar_items(product_id: str, k: int = 12) -> List[Dict[str, Any]]:
    """
    Fetch the product and suggest similar by category; fallback to popular.
    """
    snap = _db.collection(COLL_PRODUCTS).document(product_id).get()
    if snap.exists:
        prod = snap.to_dict() or {}
        cat = prod.get("category")
        if cat:
            items = similar_by_category(cat, k=k)
            # optional: remove the same item if present
            return [it for it in items if it.get("id") != product_id]
    return popular_products(k=k)


def get_recs_for_user(
    user_id: str,
    k: int = 12,
    category_hint: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    MVP: if we have a category hint (e.g., last viewed), use it; else popular.
    Later: use user profile, browsing history, embeddings.
    """
    if category_hint:
        items = similar_by_category(category_hint, k=k)
        if items:
            return items
    return popular_products(k=k)


# ----------- Placeholder for semantic search (upgrade later) ----------------
def search_semantic(query: str, k: int = 12) -> List[Dict[str, Any]]:
    """
    Placeholder: returns popular products.
    Later:
      - Generate embeddings via Vertex AI Text Embeddings
      - Query Vertex Vector Search / matching index
      - Re-rank with business rules (availability, margin, recency)
    """
    return popular_products(k=k)
