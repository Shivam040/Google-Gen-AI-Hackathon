# apps/api/src/services/marketing_service.py
# Purpose: Generate captions/taglines + best time/hashtags.
# Do: text generation + (later) BQ trend lookup; persist asset; emit marketing.asset.created.
# MVP: rule-based times; Gemini when available; Firebase-only placeholder otherwise.

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

from ..core.config import get_settings
from ..repos import firestore as fs, pubsub

# Optional: if you already have a pydantic model
try:
    from ..models.marketing import MarketingRequest  # type: ignore
except Exception:  # fallback type (so this file works even if model not present yet)
    from typing import TypedDict
    class MarketingRequest(TypedDict, total=False):
        product_id: str
        lang: str
        channel: str
        extra_tags: List[str]

settings = get_settings()
FIREBASE_ONLY = os.getenv("FIREBASE_ONLY", "false").lower() == "true"

DEFAULT_HASHTAGS = {
    "instagram": ["#handmade", "#supportlocal", "#craft", "#artisan", "#madeinindia"],
    "facebook":  ["#handmade", "#localbusiness", "#crafts"],
    "whatsapp":  [],
    "x":         ["#Handmade", "#Artisan"],
    "youtube":   ["#handmade", "#craft"],
}

# -------------------------------------------------------------------
# Event path (worker-based) – publish marketing.asset.requested
# -------------------------------------------------------------------
def request_marketing(req: MarketingRequest, actor: Optional[Dict[str, Any]] = None) -> str:
    """
    Publish a marketing.asset.requested event that the worker will handle.
    Compatible with your original signature.
    """
    topic = getattr(settings, "TOPIC_MARKETING_REQUESTED", None) or settings.pubsub_topic_marketing
    envelope = {
        "type": "marketing.asset.requested",
        "source": "api",
        "data": dict(req),
    }
    if actor:
        envelope["actor"] = actor
    return pubsub.publish(topic, envelope)

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def suggest_hashtags(channel: str, extra: Optional[List[str]] = None) -> List[str]:
    base = DEFAULT_HASHTAGS.get(channel.lower(), DEFAULT_HASHTAGS["instagram"]).copy()
    if extra:
        for tag in extra:
            t = tag if tag.startswith("#") else f"#{tag}"
            if t not in base:
                base.append(t)
    return base[:8]  # cap to something reasonable for MVP

def suggest_best_time(now: Optional[datetime] = None) -> str:
    """
    Naive MVP: next 19:00 IST (13:30 UTC). Replace later with BigQuery-derived stats.
    """
    now = now or datetime.now(timezone.utc)
    target = now.astimezone(timezone.utc).replace(hour=13, minute=30, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target.isoformat()

# -------------------------------------------------------------------
# Sync path (API does generation now) – Firebase-only safe
# -------------------------------------------------------------------
def _mock_caption(product: Dict[str, Any], lang: str, channel: str) -> str:
    mats = ", ".join(product.get("materials", []))
    region = product.get("region") or ""
    title = product.get("title") or ""
    return (
        f"{title} — handcrafted with love.\n"
        f"Materials: {mats}. Region: {region}.\n"
        f"Discover the story behind this piece and support local artisans. "
        f"(lang={lang}, channel={channel})"
    )

def _gen_caption_vertex(product: Dict[str, Any], lang: str, channel: str) -> str:
    # Uses Vertex AI only when FIREBASE_ONLY is false
    import vertexai
    from vertexai.generative_models import GenerativeModel

    vertexai.init(project=settings.gcp_project, location=settings.vertex_location)
    model = GenerativeModel(settings.vertex_model)
    prompt = (
        f"Write a concise social post for {channel}. Language '{lang}'. "
        f"Handcrafted item titled '{product.get('title','')}'. "
        f"Materials: {', '.join(product.get('materials', []))}. "
        f"Region: {product.get('region','')}. "
        f"Provide: caption (≤120 words), 6-10 hashtags, and a clear CTA."
    )
    resp = model.generate_content(prompt)
    return (resp.text or "").strip()

def create_marketing_asset_sync(
    product: Dict[str, Any],
    lang: str,
    channel: str,
    extra_tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Generates a caption now (no worker):
      - FIREBASE_ONLY=true  → mock caption
      - else               → Vertex AI (Gemini)
    Persists Firestore doc and emits marketing.asset.created.
    """
    if FIREBASE_ONLY:
        caption = _mock_caption(product, lang, channel)
    else:
        caption = _gen_caption_vertex(product, lang, channel)

    tags = suggest_hashtags(channel, extra_tags)
    best_time_iso = suggest_best_time()

    key = f"{product['id']}_{lang}_{channel}"
    doc = {
        "product_id": product["id"],
        "lang": lang,
        "channel": channel,
        "post_text": caption,
        "hashtags": tags,
        "best_time_iso": best_time_iso,
        # "image_uri": ...  # add when you render images
    }
    fs.save_marketing_asset(key, doc)

    # Emit created event (best-effort)
    try:
        env = {
            "type": "marketing.asset.created",
            "source": "api",
            "data": {"product_id": product["id"], "lang": lang, "channel": channel, "doc_id": key},
        }
        pubsub.publish(
            (getattr(settings, "TOPIC_MARKETING_CREATED", None) or settings.pubsub_topic_marketing).replace(
                ".requested", ".created"
            ),
            env,
        )
    except Exception:
        pass

    return doc

# Backwards/endpoint-friendly alias (used by your router already)
def create_post(product: Dict[str, Any], lang: str, channel: str, extra_tags: Optional[List[str]] = None) -> Dict[str, Any]:
    return create_marketing_asset_sync(product, lang, channel, extra_tags)

