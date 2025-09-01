# apps/api/src/repos/storage.py
import os, uuid, re
from datetime import timedelta, datetime
from typing import Optional, Dict
import os
from pathlib import Path
from typing import Optional

# Accept common truthy strings
_FFLAG = os.getenv("FIREBASE_ONLY", "false").strip().lower()
FIREBASE_ONLY = _FFLAG in {"1", "true", "yes", "y"}
# apps/api/src/repos/storage.py


PUBLIC_BASE = os.getenv("PUBLIC_URL_PREFIX", "http://localhost:8080/static")
LOCAL_ROOT  = os.getenv("UPLOAD_LOCAL_ROOT", "/app/static")  # bind-mounted
# Lazy globals
_client = None
_bucket = None
_settings = None

_slug_re = re.compile(r"[^a-z0-9\-]+")


def _slug(s: str) -> str:
    s = (s or "file").lower().strip().replace(" ", "-")
    return _slug_re.sub("", s)


def write_bytes(path: str, data: bytes, content_type: Optional[str] = None) -> str:
    full = Path(LOCAL_ROOT) / path
    full.parent.mkdir(parents=True, exist_ok=True)
    with open(full, "wb") as f:
        f.write(data)
    return f"{PUBLIC_BASE}/{path}"


def _ensure_gcs():
    """Initialize GCS client/bucket once, with helpful errors."""
    global _client, _bucket, _settings
    if _client and _bucket and _settings:
        return

    # Defer imports so module can load without GCS installed
    from ..core.config import get_settings
    from google.cloud import storage as gcs  # type: ignore

    _settings = get_settings()

    if not _settings.gcp_project:
        raise RuntimeError(
            "GCS requested but GCP_PROJECT is empty. "
            "Set GCP_PROJECT or run with FIREBASE_ONLY=true."
        )
    if not _settings.gcs_bucket:
        raise RuntimeError(
            "GCS requested but GCS_BUCKET is empty. "
            "Set GCS_BUCKET or run with FIREBASE_ONLY=true."
        )

    _client = gcs.Client(project=_settings.gcp_project)
    _bucket = _client.bucket(_settings.gcs_bucket)


# ---------- READ/WRITE HELPERS (you already had these) ----------

def write_text(path: str, text: str, content_type: Optional[str] = None) -> str:
    """
    Writes text to GCS (or returns a no-op URI in MVP).
    Returns gs://... when GCS is used, or firebase://... when FIREBASE_ONLY.
    """
    if FIREBASE_ONLY:
        return f"firebase://{path}"

    _ensure_gcs()
    blob = _bucket.blob(path)
    blob.upload_from_string(text, content_type=content_type or "text/markdown; charset=utf-8")
    return f"gs://{_settings.gcs_bucket}/{path}"


def signed_url(path: str, minutes: int = 60) -> Optional[str]:
    """Signed GET URL for viewing (browser-safe)."""
    if FIREBASE_ONLY:
        return None
    _ensure_gcs()
    blob = _bucket.blob(path)
    return blob.generate_signed_url(expiration=timedelta(minutes=minutes))


# ---------- NEW: PUBLIC URL + SIGNED PUT FOR BROWSER UPLOAD ----------

def public_url(path: str) -> str:
    """
    Browser-viewable HTTP URL for an object (works if bucket allows public read).
    If your bucket isn't public, prefer signed_url(...) when rendering.
    """
    if FIREBASE_ONLY:
        # front-end should replace with a local placeholder
        return "/placeholder-640x360.png"
    _ensure_gcs()
    return f"https://storage.googleapis.com/{_settings.gcs_bucket}/{path}"


def _object_name(filename: str) -> str:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    base = _slug((filename or "image").rsplit("/", 1)[-1])
    return f"uploads/{ts}-{uuid.uuid4().hex[:8]}-{base}"


def signed_put_url(filename: str, content_type: str = "application/octet-stream") -> Dict[str, Optional[str]]:
    """
    Generate a V4 signed PUT URL so the browser can upload directly to GCS.
    Returns:
      {
        "upload_url": str | None,   # None in FIREBASE_ONLY
        "public_url": str,          # browser-viewable URL for the saved object
        "object_name": str          # gs path without prefix
      }
    """
    if FIREBASE_ONLY:
        return {
            "upload_url": None,
            "public_url": "/placeholder-640x360.png",
            "object_name": "placeholder"
        }

    _ensure_gcs()
    from google.cloud import storage as gcs  # type: ignore

    name = _object_name(filename)
    blob = _bucket.blob(name)

    upload_url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="PUT",
        content_type=content_type or "application/octet-stream",
    )
    return {
        "upload_url": upload_url,
        "public_url": public_url(name),
        "object_name": name,
    }

