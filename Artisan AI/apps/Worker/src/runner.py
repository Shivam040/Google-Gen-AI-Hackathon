# apps/worker/src/runner.py
import base64
import json
import logging
from fastapi import FastAPI, Request, HTTPException

from .handlers.handle_content_requested import handle as handle_content

# Optional: include if you added the marketing handler
try:
    from .handlers.handle_marketing_requested import handle as handle_marketing
except Exception:  # handler may not exist yet in your repo
    handle_marketing = None  # type: ignore

app = FastAPI(title="artisan-worker")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _decode_pubsub_message(envelope: dict) -> dict:
    """
    Pub/Sub push format:
    {
      "message": {
        "data": "<base64-encoded-bytes>",
        "attributes": {...},
        "messageId": "...", "publishTime": "..."
      },
      "subscription": "..."
    }
    We publish base64-encoded JSON. Decode and return the dict payload.
    """
    msg = envelope.get("message")
    if not msg or "data" not in msg:
        raise HTTPException(status_code=400, detail="Bad Pub/Sub push: missing message.data")

    try:
        raw = base64.b64decode(msg["data"])
        return json.loads(raw.decode("utf-8"))
    except Exception as e:
        logger.exception("Failed to decode Pub/Sub message")
        raise HTTPException(status_code=400, detail=f"Invalid message data: {e}")

@app.post("/_pubsub")
async def pubsub_push(request: Request):
    envelope = await request.json()
    payload = _decode_pubsub_message(envelope)

    event_type = payload.get("type")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing event 'type' in payload")

    logger.info("Received event type=%s", event_type)

    if event_type == "content.requested":
        handle_content(payload)
    elif event_type == "marketing.asset.requested" and handle_marketing:
        handle_marketing(payload)
    else:
        logger.info("Ignoring unknown or unsupported event type: %s", event_type)

    # 200 OK lets Pub/Sub mark delivery successful
    return {"ok": True}
