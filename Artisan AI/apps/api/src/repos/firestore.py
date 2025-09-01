# apps/api/src/repos/firestore.py
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

from google.api_core.retry import Retry
from google.api_core import exceptions as gexc
from google.api_core.exceptions import FailedPrecondition, InvalidArgument
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP, Increment
from google.oauth2 import service_account

from ..core.config import get_settings

# -------------------------------------------------------------------
# Client bootstrap
# -------------------------------------------------------------------
_settings = get_settings()

def _make_client() -> firestore.Client:
    """
    Create a Firestore client that:
      - Uses emulator if FIRESTORE_EMULATOR_HOST is present.
      - Uses explicit service-account if GOOGLE_APPLICATION_CREDENTIALS points to a file.
      - Otherwise falls back to ADC.
    """
    # Emulator: let google-cloud-firestore pick up env var
    if os.getenv("FIRESTORE_EMULATOR_HOST"):
        return firestore.Client(project=_settings.gcp_project)

    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path and os.path.exists(sa_path):
        creds = service_account.Credentials.from_service_account_file(sa_path)
        return firestore.Client(project=_settings.gcp_project, credentials=creds)

    # ADC (works in Docker if no SA is mounted)
    return firestore.Client(project=_settings.gcp_project)

_db = _make_client()

# -------------------------------------------------------------------
# Collections
# -------------------------------------------------------------------
COLL_PRODUCTS  = _settings.firestore_collection_products       # "products"
COLL_STORIES   = _settings.firestore_collection_stories        # "stories"
COLL_MARKETING = _settings.firestore_collection_marketing      # "marketing_assets"
COLL_ORDERS    = "orders"
COLL_STORES    = "stores"
COLL_USERS     = "users"

RETRY = Retry(deadline=10.0)

# -------------------------------------------------------------------
# Utils
# -------------------------------------------------------------------
def _with_timestamps(data: Dict[str, Any], *, new: bool) -> Dict[str, Any]:
    d = dict(data)
    if new:
        d.setdefault("created_at", SERVER_TIMESTAMP)
    d["updated_at"] = SERVER_TIMESTAMP
    return d

def _page_after(q: firestore.Query,
                limit: int,
                cursor: Optional[Tuple[Any, str]],
                order_field: str) -> firestore.Query:
    """
    Keyset pagination: assumes the query is ordered by (order_field desc, id asc)
    and cursor is (timestamp, id).
    """
    if cursor:
        ts, doc_id = cursor
        q = q.start_after({order_field: ts, "id": doc_id})
    return q.limit(limit)

# ---- NEW: make any payload Firestore-safe --------------------------------
def _to_firestore(v: Any) -> Any:
    """
    Recursively coerce values into Firestore-friendly primitives.
    Converts Pydantic v2 Url/AnyUrl/HttpUrl (and other exotic objects) to str.
    """
    # primitives pass through
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    # Firestore-native types
    if v is SERVER_TIMESTAMP or isinstance(v, Increment):
        return v
    if isinstance(v, datetime):
        return v
    # mappings
    if isinstance(v, dict):
        return {k: _to_firestore(vv) for k, vv in v.items()}
    # sequences
    if isinstance(v, (list, tuple, set)):
        return [_to_firestore(x) for x in v]
    # pydantic-core URL types (stringify)
    tname = type(v).__name__.lower()
    if tname in {"url", "anyurl", "httpurl"}:
        return str(v)
    # fallback: stringify any unknown object
    return str(v)

# -------------------------------------------------------------------
# PRODUCTS
# -------------------------------------------------------------------
def save_product(product_id: str, doc: Dict[str, Any]) -> None:
    """
    Create/merge a product (idempotent).
    Defaults new docs to is_active=True and stamps server timestamps.
    """
    data = {**doc}
    data.setdefault("id", product_id)
    data.setdefault("is_active", True)
    data.setdefault("created_at", SERVER_TIMESTAMP)
    data["updated_at"] = SERVER_TIMESTAMP
    data = _to_firestore(data)  # ← sanitize before write
    _db.collection(COLL_PRODUCTS).document(product_id).set(data, merge=True, retry=RETRY)

def update_product_fields(product_id: str, patch: Dict[str, Any]) -> None:
    payload = _with_timestamps(patch, new=False)
    payload = _to_firestore(payload)  # ← sanitize
    _db.collection(COLL_PRODUCTS).document(product_id).set(payload, merge=True, retry=RETRY)

def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    snap = _db.collection(COLL_PRODUCTS).document(product_id).get(retry=RETRY)
    return snap.to_dict() if snap.exists else None

def list_products_by_category(category: str, limit: int = 24) -> List[Dict[str, Any]]:
    q = (_db.collection(COLL_PRODUCTS)
         .where("category", "==", category)
         .order_by("popularity", direction=firestore.Query.DESCENDING)
         .limit(limit))
    return [d.to_dict() for d in q.stream()]

def list_products(
    category: Optional[str] = None,
    limit: int = 24,
    cursor: Optional[Tuple[Any, str]] = None,
    include_inactive: bool = False,
) -> Dict[str, Any]:
    """
    Dev-safe list. Prefer ordering by updated_at desc, id asc.
    Falls back if index/field issues occur.
    Returns {"items":[...], "next": (ts, id) | None}
    """
    base = _db.collection(COLL_PRODUCTS)
    if not include_inactive:
        base = base.where("is_active", "==", True)  # ✅ apply to base
    if category:
        base = base.where("category", "==", category)

    try:
        # Primary path: order by updated_at desc, then id asc (stable)
        q = (base
             .order_by("updated_at", direction=firestore.Query.DESCENDING)
             .order_by("id"))
        q = _page_after(q, limit, cursor, "updated_at")
        docs = list(q.stream())
    except (FailedPrecondition, InvalidArgument):
        # Index missing or some docs missing updated_at → fallback
        q = base.limit(limit) if cursor is None else _page_after(base, limit, cursor, "updated_at")
        docs = list(q.stream())

    items = [d.to_dict() | {"id": d.id} for d in docs]
    next_cursor = None
    if docs:
        last = docs[-1]
        ts = last.get("updated_at") or last.get("created_at")
        next_cursor = (ts, last.id)
    return {"items": items, "next": next_cursor}

def bump_popularity(product_id: str, delta: int = 1) -> int:
    ref = _db.collection(COLL_PRODUCTS).document(product_id)
    ref.update({"popularity": Increment(int(delta)), "updated_at": SERVER_TIMESTAMP})
    snap = ref.get()
    return int(snap.get("popularity") or 0)

# -------------------------------------------------------------------
# STORIES
# -------------------------------------------------------------------
def save_story(product_id: str, lang: str, data: Dict[str, Any]) -> None:
    doc_id = f"{product_id}_{lang}"
    base = {
        "id": doc_id,
        "product_id": product_id,
        "lang": lang,
        "tone": data.get("tone", "narrative"),
        "gcs_uri": data.get("gcs_uri") or data.get("uri"),
        "version": int(data.get("version", 1)),
        "approved": bool(data.get("approved", True)),
        "approved_by": data.get("approved_by"),
    }
    payload = _with_timestamps(base, new=True)
    payload = _to_firestore(payload)  # ← sanitize
    _db.collection(COLL_STORIES).document(doc_id).set(payload, merge=True, retry=RETRY)

def list_stories(product_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    q = (_db.collection(COLL_STORIES)
         .where("product_id", "==", product_id)
         .order_by("created_at", direction=firestore.Query.DESCENDING)
         .limit(limit))
    return [d.to_dict() for d in q.stream()]

# -------------------------------------------------------------------
# MARKETING
# -------------------------------------------------------------------
def save_marketing_asset(key: str, data: Dict[str, Any]) -> None:
    payload = _with_timestamps({"id": key, **data}, new=True)
    payload = _to_firestore(payload)  # ← sanitize
    _db.collection(COLL_MARKETING).document(key).set(payload, merge=True, retry=RETRY)

def list_marketing_assets(
    product_id: Optional[str] = None,
    channel: Optional[str] = None,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    q = _db.collection(COLL_MARKETING)
    if product_id:
        q = q.where("product_id", "==", product_id)
    if channel:
        q = q.where("channel", "==", channel)
    q = q.order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit)
    return [d.to_dict() for d in q.stream()]

# -------------------------------------------------------------------
# ORDERS / STORES / USERS
# -------------------------------------------------------------------
def create_order(order_id: str, data: Dict[str, Any]) -> None:
    ref = _db.collection(COLL_ORDERS).document(order_id)
    payload = _with_timestamps({**data, "id": order_id, "status": data.get("status", "pending")}, new=True)
    payload = _to_firestore(payload)  # ← sanitize
    try:
        ref.set(payload, merge=True, retry=RETRY)
    except gexc.AlreadyExists:
        pass

def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    snap = _db.collection(COLL_ORDERS).document(order_id).get(retry=RETRY)
    return snap.to_dict() if snap.exists else None

def list_orders_for_user(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    q = (_db.collection(COLL_ORDERS)
         .where("user_id", "==", user_id)
         .order_by("created_at", direction=firestore.Query.DESCENDING)
         .limit(limit))
    return [d.to_dict() for d in q.stream()]

def save_store(store_id: str, data: Dict[str, Any]) -> None:
    payload = _with_timestamps({**data, "id": store_id}, new=True)
    payload = _to_firestore(payload)  # ← sanitize
    _db.collection(COLL_STORES).document(store_id).set(payload, merge=True, retry=RETRY)

def get_store(store_id: str) -> Optional[Dict[str, Any]]:
    snap = _db.collection(COLL_STORES).document(store_id).get(retry=RETRY)
    return snap.to_dict() if snap.exists else None

def save_user(user_id: str, data: Dict[str, Any]) -> None:
    payload = _with_timestamps({**data, "id": user_id}, new=True)
    payload = _to_firestore(payload)  # ← sanitize
    _db.collection(COLL_USERS).document(user_id).set(payload, merge=True, retry=RETRY)

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    snap = _db.collection(COLL_USERS).document(user_id).get(retry=RETRY)
    return snap.to_dict() if snap.exists else None



