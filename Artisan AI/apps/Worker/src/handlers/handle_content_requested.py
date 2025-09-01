# Worker/src/handlers/handle_marketing_requested.py
from __future__ import annotations
import os, uuid, json, time
from typing import Dict, List
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from ..utils import storage  # uses GCS_BUCKET and fails fast if misconfigured

db = firestore.Client()

# 1×1 transparent PNG (valid PNG bytes)
_TRANSPARENT_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc``\x00"
    b"\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
)

def generate_mock_image(product_id: str, channel: str) -> str:
    """
    MVP: creates a tiny placeholder PNG and uploads it to GCS.
    Returns the gs:// URI.
    """
    key = f"marketing/{product_id}/{channel}/{uuid.uuid4().hex}.png"
    uri = storage.write_bytes(key, _TRANSPARENT_PNG, content_type="image/png")
    return uri

def handle(payload: Dict):
    """
    Expected payload (flat):
      {
        "type": "marketing.requested",
        "product_id": "p1",
        "lang": "en",
        "channel": "instagram"
      }
    """
    product_id: str = payload["product_id"]
    lang: str = payload.get("lang", "en")
    channel: str = payload.get("channel", "instagram")

    # (Optional) fetch product metadata for better copy
    prod = db.collection("products").document(product_id).get()
    title = (prod.to_dict() or {}).get("title", product_id)

    # Simple MVP copy
    post_text = f"Discover handcrafted beauty from {title} ✨"
    hashtags: List[str] = ["#handmade", "#supportlocal", "#artisan"]
    best_time_iso = "2025-09-19T13:30:00Z"  # TODO: compute based on audience

    image_uri = generate_mock_image(product_id, channel)

    # Deterministic doc id (product_lang_channel)
    doc_id = f"{product_id}_{lang}_{channel}"

    db.collection("marketing_assets").document(doc_id).set(
        {
            "id": doc_id,
            "product_id": product_id,
            "lang": lang,
            "channel": channel,
            "post_text": post_text,
            "hashtags": hashtags,
            "best_time_iso": best_time_iso,
            "image_uri": image_uri,
            "created_at": SERVER_TIMESTAMP,
            "updated_at": SERVER_TIMESTAMP,
        },
        merge=True,
    )

    # Return value is optional for a push/pull handler
    return {"ok": True, "doc_id": doc_id, "image_uri": image_uri}


# from google.cloud import firestore
# from ..utils.storage import write_text
# import os
# import uuid

# db = firestore.Client()
# BUCKET = os.getenv("BUCKET_GENERATED", "artisan-generated")

# def generate_mock_image(product_id: str, channel: str) -> str:
#     """
#     For MVP: just create a placeholder banner text file in GCS.
#     Later: use Vertex AI Image Generation (Imagen) or GenAI model.
#     """
#     file_name = f"marketing/{product_id}_{channel}_{uuid.uuid4().hex}.png"
#     uri = f"gs://{BUCKET}/{file_name}"
#     write_text(uri, f"IMAGE PLACEHOLDER for {product_id} on {channel}")
#     return uri

# def handle(event: dict):
#     data = event["data"]
#     product_id = data["product_id"]
#     lang = data.get("lang", "en")
#     channel = data.get("channel", "instagram")

#     # TODO: fetch product info from Firestore if needed
#     post_text = f"Discover handcrafted beauty from {product_id} ✨"
#     hashtags = ["#handmade", "#supportlocal", "#artisan"]
#     best_time_iso = "2025-09-19T13:30:00Z"

#     image_uri = generate_mock_image(product_id, channel)

#     db.collection("marketing_assets").document(f"{product_id}_{channel}").set({
#         "product_id": product_id,
#         "lang": lang,
#         "channel": channel,
#         "post_text": post_text,
#         "hashtags": hashtags,
#         "best_time_iso": best_time_iso,
#         "image_uri": image_uri,
#     }, merge=True)
