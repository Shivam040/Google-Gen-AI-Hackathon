# apps/api/src/v1/endpoints/products.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Tuple, Literal, Dict, Any
import os
from fastapi import APIRouter, Body, Query, HTTPException, status
from pydantic import ValidationError
import base64, mimetypes, uuid

from ...models.product import Product, GenerateRequest
# NEW: import quick-text models
from ...models.product import QuickTextRequest, QuickTextResponse  # <-- add these
from ...repos import firestore as fs
from ...repos import storage
from ...services.content_service import request_generation, generate_story_sync
# NEW: import the template helpers
from ...services.text_templates import compose_short_description, compose_quick_history

# Use any object that already exists in your bucket
PLACEHOLDER_IMAGE_PATH = os.getenv(
    "PLACEHOLDER_IMAGE_PATH",
    "uploads/Pottery_1.jpg",   # <-- your existing file
)

router = APIRouter(prefix="/v1/products", tags=["products"])


# ------------------------------ helpers ---------------------------------
def _parse_ts(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    s2 = s.strip()
    if s2.endswith("Z"):
        s2 = s2[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s2)
    except ValueError:
        try:
            dt = datetime.fromisoformat(s2.split(".")[0] + "+00:00")
        except Exception:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid cursor_ts format")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _normalize_images(data: Dict[str, Any]) -> None:
    imgs = data.get("images")
    if imgs is None:
        return
    if isinstance(imgs, (tuple, set)):
        imgs = list(imgs)
    if isinstance(imgs, list):
        data["images"] = [str(u) for u in imgs if u]


def _coerce_to_absolute_urls(data: Dict[str, Any]) -> None:
    """
    - Convert '/something' or 'something' to absolute HTTP via storage.public_url(...)
    - Map any placeholder-y value to the configured placeholder image
    """
    imgs = data.get("images") or []
    fixed: list[str] = []
    for u in imgs:
        if not u:
            continue
        s = str(u)

        # treat classic placeholders
        if s.startswith("/placeholder-") or s == "placeholder" or "placeholder" in s:
            fixed.append(storage.public_url(PLACEHOLDER_IMAGE_PATH))
            continue

        # already absolute?
        if s.startswith("http://") or s.startswith("https://"):
            fixed.append(s)
            continue

        # relative path -> absolute URL
        fixed.append(storage.public_url(s.lstrip("/")))

    if fixed:
        data["images"] = fixed


def _ensure_image(data: Dict[str, Any]) -> None:
    """Guarantee at least one absolute image URL."""
    imgs = data.get("images")
    if not isinstance(imgs, list) or len(imgs) == 0:
        data["images"] = [storage.public_url(PLACEHOLDER_IMAGE_PATH)]


def _coerce_placeholders_to_urls(data: Dict[str, Any]) -> None:
    """
    Upgrade any relative placeholders (e.g. '/placeholder-640x360.png')
    to absolute HTTP URLs so Pydantic URL validation passes.
    """
    imgs = data.get("images") or []
    fixed: list[str] = []
    for u in imgs:
        if not u:
            continue
        if isinstance(u, str) and u.startswith("/placeholder-"):
            fixed.append(storage.public_url(u.lstrip("/")))
        else:
            fixed.append(str(u))
    if fixed:
        data["images"] = fixed


# ----------------------------- Create/Upsert -----------------------------
@router.post(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Upserted"}, 400: {}, 422: {}, 500: {}},
)
def upsert_product(product_id: str, body: dict = Body(..., embed=False)):
    """
    Accept raw dict to keep URLs as plain strings. If an image arrives as a base64
    data URI, store it and replace with a short URL before validating with Product.
    This avoids Pydantic Url errors and keeps Firestore clean.
    """
    try:
        # Work on a mutable copy
        data: Dict[str, Any] = dict(body) if isinstance(body, dict) else {}

        # --- Ingest any data:image/...;base64,... into storage -> URL ---
        imgs = data.get("images") or []
        if isinstance(imgs, (tuple, set)):
            imgs = list(imgs)

        processed: list[str] = []
        for u in imgs:
            if isinstance(u, str) and u.startswith("data:image/"):
                header, b64 = u.split(",", 1)
                ctype = header.split(";")[0].split(":")[1]        # e.g. image/png
                ext = (mimetypes.guess_extension(ctype) or ".jpg").lstrip(".")
                path = f"products/{product_id}/{uuid.uuid4().hex}.{ext}"
                raw = base64.b64decode(b64)
                url = storage.write_bytes(path, raw, content_type=ctype)  # http(s)://...
                processed.append(url)
            elif u:
                processed.append(str(u))
        if processed:
            data["images"] = processed

        # Normalize + upgrade placeholders to absolute URLs
        _normalize_images(data)
        _coerce_to_absolute_urls(data)

        # Ensure at least one absolute image BEFORE validation (in case schema requires one)
        _ensure_image(data)

        # Validate request (now only absolute URLs remain)
        Product.model_validate(data)

        # Finalize
        data["id"] = product_id
        fs.save_product(product_id, data)
        return {"ok": True, "product_id": product_id, "data": data}

    except ValidationError as ve:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(ve))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# (optional) PUT alias for idempotent upserts
@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def upsert_product_put(product_id: str, body: dict = Body(..., embed=False)):
    return upsert_product(product_id, body)


# -------------------------- Partial update (PATCH) -----------------------
@router.patch(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Not found"}},
)
def update_product(product_id: str, patch: dict = Body(..., embed=False)):
    try:
        if not fs.get_product(product_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
        _normalize_images(patch)
        _coerce_placeholders_to_urls(patch)
        fs.update_product_fields(product_id, patch)
        return {"ok": True, "product_id": product_id, "patched": patch}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# ------------------------------- Read single -----------------------------
@router.get("/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: str):
    try:
        doc = fs.get_product(product_id)
        if not doc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# -------------------------- List + pagination ----------------------------
@router.get("/", status_code=status.HTTP_200_OK)
def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(24, ge=1, le=100),
    cursor_ts: Optional[str] = Query(None, description="ISO ts from previous next.ts"),
    cursor_id: Optional[str] = Query(None, description="Doc id from previous next.id"),
    include_inactive: bool = Query(False, description="Include soft-deleted items"),
):
    try:
        ts_parsed = _parse_ts(cursor_ts) if cursor_ts else None
        cursor: Optional[Tuple[datetime, str]] = (
            (ts_parsed, cursor_id) if (ts_parsed and cursor_id) else None
        )
        out = fs.list_products(
            category=category,
            limit=limit,
            cursor=cursor,
            include_inactive=include_inactive,
        )
        nxt = out.get("next")
        if nxt:
            ts, pid = nxt
            ts_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
            out["next"] = {"ts": ts_str, "id": pid}
        else:
            out["next"] = None
        return out
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# --------------------------- Popularity counter --------------------------
@router.post("/{product_id}/popularity", status_code=status.HTTP_200_OK)
def bump_popularity(product_id: str, delta: int = Query(1)):
    try:
        if not fs.get_product(product_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
        new_val = fs.bump_popularity(product_id, delta=delta)
        return {"ok": True, "product_id": product_id, "popularity": new_val}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# --------------------------- Generate content ----------------------------
@router.post("/{product_id}/generate", status_code=status.HTTP_200_OK)
def generate_content(
    product_id: str,
    req: GenerateRequest = Body(...),
    mode: Literal["sync", "event"] = Query("sync"),
):
    try:
        prod = fs.get_product(product_id)
        if not prod:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")

        if mode == "event":
            msg_id = request_generation(product_id, req.langs, req.tone, actor={"via": "api"})
            return {"ok": True, "published": msg_id, "mode": "event"}

        pointers = generate_story_sync(product_id, prod, req.tone, req.langs)
        return {"ok": True, "items": pointers, "mode": "sync"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"generation: {e}")


# ---------------------- Quick description / history ----------------------
@router.post("/{product_id}/quicktext", response_model=QuickTextResponse, status_code=status.HTTP_200_OK)
def quicktext(product_id: str, req: QuickTextRequest = Body(default_factory=QuickTextRequest)):
    """
    Build a short description + compact history from existing product fields,
    optionally applying client-side patches. Does not save unless persist=True.
    """
    try:
        stored = fs.get_product(product_id) or {}

        # Normalize any images arriving in the patch so template functions see absolute URLs if needed.
        patch = dict(req.patch or {})
        if patch:
            _normalize_images(patch)
            _coerce_to_absolute_urls(patch)

        merged = {**stored, **patch}

        description = compose_short_description(merged) if req.mode in ("both", "description") else None
        story       = compose_quick_history(merged)     if req.mode in ("both", "story")        else None

        if req.persist:
            to_save = dict(merged)
            if description is not None:
                to_save["description"] = description
            if story is not None:
                to_save["story"] = story
            fs.save_product(product_id, to_save)

        return QuickTextResponse(
            id=product_id,
            description=description,
            story=story,
            used_fields={
                "title": merged.get("title"),
                "materials": merged.get("materials"),
                "category": merged.get("category"),
                "region": merged.get("region"),
                "artisan_name": merged.get("artisan_name"),
                "attributes": merged.get("attributes"),
                "provenance": merged.get("provenance"),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"quicktext: {e}")


# ------------------------ Hard delete disabled (soft) --------------------
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: str):
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        "Hard delete disabled. Use PATCH { is_active: false } instead.",
    )


# # apps/api/src/v1/endpoints/products.py
# from __future__ import annotations

# from datetime import datetime, timezone
# from typing import Optional, Tuple, Literal, Dict, Any
# import os
# from fastapi import APIRouter, Body, Query, HTTPException, status
# from pydantic import ValidationError
# import base64, mimetypes, uuid

# from ...models.product import Product, GenerateRequest
# from ...repos import firestore as fs
# from ...repos import storage
# from ...services.content_service import request_generation, generate_story_sync
# # Use any object that already exists in your bucket
# PLACEHOLDER_IMAGE_PATH = os.getenv(
#     "PLACEHOLDER_IMAGE_PATH",
#     "uploads/Pottery_1.jpg",   # <-- your existing file
# )

# router = APIRouter(prefix="/v1/products", tags=["products"])


# # ------------------------------ helpers ---------------------------------
# def _parse_ts(s: Optional[str]) -> Optional[datetime]:
#     if not s:
#         return None
#     s2 = s.strip()
#     if s2.endswith("Z"):
#         s2 = s2[:-1] + "+00:00"
#     try:
#         dt = datetime.fromisoformat(s2)
#     except ValueError:
#         try:
#             dt = datetime.fromisoformat(s2.split(".")[0] + "+00:00")
#         except Exception:
#             raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid cursor_ts format")
#     if dt.tzinfo is None:
#         dt = dt.replace(tzinfo=timezone.utc)
#     return dt


# def _normalize_images(data: Dict[str, Any]) -> None:
#     imgs = data.get("images")
#     if imgs is None:
#         return
#     if isinstance(imgs, (tuple, set)):
#         imgs = list(imgs)
#     if isinstance(imgs, list):
#         data["images"] = [str(u) for u in imgs if u]

# def _coerce_to_absolute_urls(data: Dict[str, Any]) -> None:
#     """
#     - Convert '/something' or 'something' to absolute HTTP via storage.public_url(...)
#     - Map any placeholder-y value to the configured placeholder image
#     """
#     imgs = data.get("images") or []
#     fixed: list[str] = []
#     for u in imgs:
#         if not u:
#             continue
#         s = str(u)

#         # treat classic placeholders
#         if s.startswith("/placeholder-") or s == "placeholder" or "placeholder" in s:
#             fixed.append(storage.public_url(PLACEHOLDER_IMAGE_PATH))
#             continue

#         # already absolute?
#         if s.startswith("http://") or s.startswith("https://"):
#             fixed.append(s)
#             continue

#         # relative path -> absolute URL
#         fixed.append(storage.public_url(s.lstrip("/")))

#     if fixed:
#         data["images"] = fixed

# def _ensure_image(data: Dict[str, Any]) -> None:
#     """Guarantee at least one absolute image URL."""
#     imgs = data.get("images")
#     if not isinstance(imgs, list) or len(imgs) == 0:
#         data["images"] = [storage.public_url(PLACEHOLDER_IMAGE_PATH)]



# def _coerce_placeholders_to_urls(data: Dict[str, Any]) -> None:
#     """
#     Upgrade any relative placeholders (e.g. '/placeholder-640x360.png')
#     to absolute HTTP URLs so Pydantic URL validation passes.
#     """
#     imgs = data.get("images") or []
#     fixed: list[str] = []
#     for u in imgs:
#         if not u:
#             continue
#         if isinstance(u, str) and u.startswith("/placeholder-"):
#             fixed.append(storage.public_url(u.lstrip("/")))
#         else:
#             fixed.append(str(u))
#     if fixed:
#         data["images"] = fixed


# # ----------------------------- Create/Upsert -----------------------------
# @router.post(
#     "/{product_id}",
#     status_code=status.HTTP_200_OK,
#     responses={200: {"description": "Upserted"}, 400: {}, 422: {}, 500: {}},
# )
# def upsert_product(product_id: str, body: dict = Body(..., embed=False)):
#     """
#     Accept raw dict to keep URLs as plain strings. If an image arrives as a base64
#     data URI, store it and replace with a short URL before validating with Product.
#     This avoids Pydantic Url errors and keeps Firestore clean.
#     """
#     try:
#         # Work on a mutable copy
#         data: Dict[str, Any] = dict(body) if isinstance(body, dict) else {}

#         # --- Ingest any data:image/...;base64,... into storage -> URL ---
#         imgs = data.get("images") or []
#         if isinstance(imgs, (tuple, set)):
#             imgs = list(imgs)

#         processed: list[str] = []
#         for u in imgs:
#             if isinstance(u, str) and u.startswith("data:image/"):
#                 header, b64 = u.split(",", 1)
#                 ctype = header.split(";")[0].split(":")[1]        # e.g. image/png
#                 ext = (mimetypes.guess_extension(ctype) or ".jpg").lstrip(".")
#                 path = f"products/{product_id}/{uuid.uuid4().hex}.{ext}"
#                 raw = base64.b64decode(b64)
#                 url = storage.write_bytes(path, raw, content_type=ctype)  # http(s)://...
#                 processed.append(url)
#             elif u:
#                 processed.append(str(u))
#         if processed:
#             data["images"] = processed

#         # Normalize + upgrade placeholders to absolute URLs
#         _normalize_images(data)
#         _coerce_to_absolute_urls(data)

#         # Ensure at least one absolute image BEFORE validation (in case schema requires one)
#         _ensure_image(data)

#         # Validate request (now only absolute URLs remain)
#         Product.model_validate(data)

#         # Finalize
#         data["id"] = product_id
#         fs.save_product(product_id, data)
#         return {"ok": True, "product_id": product_id, "data": data}

#     except ValidationError as ve:
#         raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(ve))
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# # (optional) PUT alias for idempotent upserts
# @router.put("/{product_id}", status_code=status.HTTP_200_OK)
# def upsert_product_put(product_id: str, body: dict = Body(..., embed=False)):
#     return upsert_product(product_id, body)


# # -------------------------- Partial update (PATCH) -----------------------
# @router.patch(
#     "/{product_id}",
#     status_code=status.HTTP_200_OK,
#     responses={404: {"description": "Not found"}},
# )
# def update_product(product_id: str, patch: dict = Body(..., embed=False)):
#     try:
#         if not fs.get_product(product_id):
#             raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
#         _normalize_images(patch)
#         _coerce_placeholders_to_urls(patch)
#         fs.update_product_fields(product_id, patch)
#         return {"ok": True, "product_id": product_id, "patched": patch}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# # ------------------------------- Read single -----------------------------
# @router.get("/{product_id}", status_code=status.HTTP_200_OK)
# def get_product(product_id: str):
#     try:
#         doc = fs.get_product(product_id)
#         if not doc:
#             raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
#         return doc
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# # -------------------------- List + pagination ----------------------------
# @router.get("/", status_code=status.HTTP_200_OK)
# def list_products(
#     category: Optional[str] = Query(None, description="Filter by category"),
#     limit: int = Query(24, ge=1, le=100),
#     cursor_ts: Optional[str] = Query(None, description="ISO ts from previous next.ts"),
#     cursor_id: Optional[str] = Query(None, description="Doc id from previous next.id"),
#     include_inactive: bool = Query(False, description="Include soft-deleted items"),
# ):
#     try:
#         ts_parsed = _parse_ts(cursor_ts) if cursor_ts else None
#         cursor: Optional[Tuple[datetime, str]] = (
#             (ts_parsed, cursor_id) if (ts_parsed and cursor_id) else None
#         )
#         out = fs.list_products(
#             category=category,
#             limit=limit,
#             cursor=cursor,
#             include_inactive=include_inactive,
#         )
#         nxt = out.get("next")
#         if nxt:
#             ts, pid = nxt
#             ts_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
#             out["next"] = {"ts": ts_str, "id": pid}
#         else:
#             out["next"] = None
#         return out
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# # --------------------------- Popularity counter --------------------------
# @router.post("/{product_id}/popularity", status_code=status.HTTP_200_OK)
# def bump_popularity(product_id: str, delta: int = Query(1)):
#     try:
#         if not fs.get_product(product_id):
#             raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
#         new_val = fs.bump_popularity(product_id, delta=delta)
#         return {"ok": True, "product_id": product_id, "popularity": new_val}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"firestore: {e}")


# # --------------------------- Generate content ----------------------------
# @router.post("/{product_id}/generate", status_code=status.HTTP_200_OK)
# def generate_content(
#     product_id: str,
#     req: GenerateRequest = Body(...),
#     mode: Literal["sync", "event"] = Query("sync"),
# ):
#     try:
#         prod = fs.get_product(product_id)
#         if not prod:
#             raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")

#         if mode == "event":
#             msg_id = request_generation(product_id, req.langs, req.tone, actor={"via": "api"})
#             return {"ok": True, "published": msg_id, "mode": "event"}

#         pointers = generate_story_sync(product_id, prod, req.tone, req.langs)
#         return {"ok": True, "items": pointers, "mode": "sync"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"generation: {e}")


# # ------------------------ Hard delete disabled (soft) --------------------
# @router.delete("/{product_id}", status_code=status.HTTP_200_OK)
# def delete_product(product_id: str):
#     raise HTTPException(
#         status.HTTP_400_BAD_REQUEST,
#         "Hard delete disabled. Use PATCH { is_active: false } instead.",
#     )

