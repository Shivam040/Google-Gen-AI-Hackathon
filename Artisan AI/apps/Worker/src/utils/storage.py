# Worker/src/utils/storage.py
from __future__ import annotations

import os
import sys
import json
import uuid
from typing import Tuple, Optional
from urllib.parse import urlparse

from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden

# ------------------------------------------------------------------------------
# Client + config
# ------------------------------------------------------------------------------
PROJECT = os.getenv("GCP_PROJECT")
BUCKET_ENV = os.getenv("GCS_BUCKET")

_client = storage.Client(project=PROJECT)

def _ensure_bucket_or_die() -> storage.Bucket:
    if not BUCKET_ENV:
        raise SystemExit("[worker.storage] GCS_BUCKET not set")
    try:
        bucket = _client.lookup_bucket(BUCKET_ENV)
    except Forbidden:
        raise SystemExit(f"[worker.storage] No permission to access bucket '{BUCKET_ENV}'")
    if bucket is None:
        raise SystemExit(f"[worker.storage] Bucket '{BUCKET_ENV}' not found in project {PROJECT}")
    return bucket

# Resolve once at import; fail fast if misconfigured.
_DEFAULT_BUCKET = _ensure_bucket_or_die()

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def _parse_gs_uri(gs_or_key: str) -> Tuple[storage.Bucket, str]:
    """
    Accepts either:
      - 'gs://bucket/path/to/file.ext'  -> use that bucket/key
      - 'path/to/file.ext'              -> use env bucket + that key
    """
    if gs_or_key.startswith("gs://"):
        u = urlparse(gs_or_key)
        if not u.netloc or not u.path:
            raise ValueError(f"Invalid GCS URI: {gs_or_key}")
        bucket = _client.bucket(u.netloc)
        key = u.path.lstrip("/")
        return bucket, key

    # treat as key under default bucket
    return _DEFAULT_BUCKET, gs_or_key.lstrip("/")

def _normalize_uri(bucket: storage.Bucket, key: str) -> str:
    return f"gs://{bucket.name}/{key}"

def _pick_key(prefix: str, ext: Optional[str]) -> str:
    rid = uuid.uuid4().hex
    if ext and not ext.startswith("."):
        ext = f".{ext}"
    return f"{prefix.rstrip('/')}/{rid}{ext or ''}"

# ------------------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------------------
def write_text(gs_or_key: str, text: str, *, content_type: str = "text/markdown") -> str:
    """
    Write text to GCS. If gs_or_key is a key (no gs://), uses env bucket.
    Returns the gs:// URI.
    """
    bucket, key = _parse_gs_uri(gs_or_key)
    blob = bucket.blob(key)
    blob.upload_from_string(text, content_type=content_type)
    return _normalize_uri(bucket, key)

def write_json(gs_or_key: str, obj, *, indent: Optional[int] = None) -> str:
    data = json.dumps(obj, ensure_ascii=False, indent=indent)
    return write_text(gs_or_key, data, content_type="application/json; charset=utf-8")

def write_bytes(gs_or_key: str, data: bytes, *, content_type: Optional[str] = None) -> str:
    bucket, key = _parse_gs_uri(gs_or_key)
    blob = bucket.blob(key)
    if content_type:
        blob.content_type = content_type
    blob.upload_from_string(data)
    return _normalize_uri(bucket, key)

def read_text(gs_uri: str) -> str:
    bucket, key = _parse_gs_uri(gs_uri)
    blob = bucket.blob(key)
    if not blob.exists():
        raise NotFound(f"GCS object not found: {gs_uri}")
    return blob.download_as_text()

def exists(gs_uri: str) -> bool:
    bucket, key = _parse_gs_uri(gs_uri)
    return bucket.blob(key).exists()

# Convenience: allocate a new unique key under a prefix in the default bucket.
def new_key(prefix: str, *, ext: Optional[str] = None) -> str:
    key = _pick_key(prefix, ext)
    return _normalize_uri(_DEFAULT_BUCKET, key)


# from google.cloud import storage
# from urllib.parse import urlparse

# client = storage.Client()

# def write_text(gs_uri: str, text: str):
#     u = urlparse(gs_uri)
#     bucket = client.bucket(u.netloc)
#     blob = bucket.blob(u.path.lstrip("/"))
#     blob.upload_from_string(text, content_type="text/markdown")
#     return f"gs://{bucket.name}/{blob.name}"
