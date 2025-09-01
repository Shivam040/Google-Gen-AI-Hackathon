# Worker/src/consumers/pull_content_requested.py
from __future__ import annotations

import os
import sys
import json
import base64
import signal

from google.cloud import pubsub_v1, storage
from google.api_core.exceptions import (
    Forbidden,
    NotFound,
    BadRequest,
    ServiceUnavailable,
    DeadlineExceeded,
)

# Business logic handler
from ..handlers.handle_content_requested import handle as handle_content


# ------------------------------------------------------------------------------
# Environment / fail-fast
# ------------------------------------------------------------------------------
PROJECT = os.getenv("GCP_PROJECT")
SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "content.requested-pull")
BUCKET = os.getenv("GCS_BUCKET")
SA_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print(f"[worker] GCP_PROJECT={PROJECT}", file=sys.stderr)
print(f"[worker] PUBSUB_SUBSCRIPTION={SUBSCRIPTION}", file=sys.stderr)
print(f"[worker] GCS_BUCKET={BUCKET}", file=sys.stderr)
print(f"[worker] GOOGLE_APPLICATION_CREDENTIALS={SA_PATH}", file=sys.stderr)

if not PROJECT:
    sys.exit("[worker] Missing GCP_PROJECT")
if not BUCKET:
    sys.exit("[worker] Missing GCS_BUCKET")
if not SA_PATH or not os.path.exists(SA_PATH):
    sys.exit("[worker] Missing/invalid GOOGLE_APPLICATION_CREDENTIALS")

# Verify bucket exists & is accessible (fail-fast)
try:
    _storage_client = storage.Client(project=PROJECT)
    if _storage_client.lookup_bucket(BUCKET) is None:
        sys.exit(f"[worker] GCS bucket '{BUCKET}' not found in project {PROJECT}")
except Forbidden:
    sys.exit(f"[worker] No permission to access bucket '{BUCKET}'")

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def _decode(msg_bytes: bytes) -> dict:
    """Decode either raw JSON bytes or {message:{data: base64json}} envelope."""
    # raw json
    try:
        return json.loads(msg_bytes.decode())
    except Exception:
        pass
    # envelope form
    try:
        env = json.loads(msg_bytes.decode())
        data = env.get("message", {}).get("data")
        if data:
            return json.loads(base64.b64decode(data).decode())
    except Exception:
        pass
    raise ValueError("Unrecognized message format")

def _callback(message: pubsub_v1.subscriber.message.Message):
    try:
        payload = _decode(message.data)
        handle_content(payload)  # your business logic
        message.ack()
    except (NotFound, BadRequest, Forbidden) as e:
        # Permanent error (bad config/input). Mark job failed in handler if needed, then ACK.
        print(f"[worker] permanent error: {e}", file=sys.stderr)
        message.ack()
    except (ServiceUnavailable, DeadlineExceeded, ConnectionError) as e:
        # Transient error: let Pub/Sub retry.
        print(f"[worker] transient error, will retry: {e}", file=sys.stderr)
        message.nack()
    except Exception as e:
        # Unknown; to avoid infinite loops, prefer ACK (or send to DLQ via max-attempts on sub).
        print(f"[worker] unexpected error: {e}", file=sys.stderr)
        message.ack()

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    subscriber = pubsub_v1.SubscriberClient()
    path = subscriber.subscription_path(PROJECT, SUBSCRIPTION)
    print(f"[worker] Listening on {path}", file=sys.stderr)
    future = subscriber.subscribe(path, callback=_callback)

    def stop(*_):
        future.cancel()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    try:
        future.result()
    finally:
        subscriber.close()

if __name__ == "__main__":
    main()


# # Worker/src/consumers/pull_content_requested.py
# import os, json, base64, signal
# from google.cloud import pubsub_v1
# from ..handlers.handle_content_requested import handle as handle_content  # your handler


# # Worker/src/consumers/pull_content_requested.py
# import os, sys
# from google.cloud import storage
# from google.api_core.exceptions import NotFound, Forbidden

# PROJECT = os.getenv("GCP_PROJECT")
# BUCKET  = os.getenv("GCS_BUCKET")
# SA_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# print(f"[worker] GCP_PROJECT={PROJECT}", file=sys.stderr)
# print(f"[worker] GCS_BUCKET={BUCKET}", file=sys.stderr)
# print(f"[worker] GOOGLE_APPLICATION_CREDENTIALS={SA_PATH}", file=sys.stderr)

# if not PROJECT:
#     print("[worker] Missing GCP_PROJECT", file=sys.stderr)
#     sys.exit(1)
# if not BUCKET:
#     print("[worker] Missing GCS_BUCKET", file=sys.stderr)
#     sys.exit(1)
# if not SA_PATH or not os.path.exists(SA_PATH):
#     print("[worker] Missing/invalid GOOGLE_APPLICATION_CREDENTIALS", file=sys.stderr)
#     sys.exit(1)

# # verify bucket exists and we can access it
# try:
#     client = storage.Client(project=PROJECT)
#     if client.lookup_bucket(BUCKET) is None:
#         print(f"[worker] GCS bucket '{BUCKET}' not found in project {PROJECT}", file=sys.stderr)
#         sys.exit(1)
# except Forbidden:
#     print(f"[worker] No permission to access bucket '{BUCKET}'", file=sys.stderr)
#     sys.exit(1)



# PROJECT = os.getenv("GCP_PROJECT", "artisan-ai-472217")
# SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "content.requested-pull")

# def _decode(msg_bytes: bytes):
#     # If you published raw JSON bytes: {"type": "...", ...}
#     try:
#         return json.loads(msg_bytes.decode())
#     except Exception:
#         pass
#     # If you published Pub/Sub-style envelope with base64 data
#     try:
#         env = json.loads(msg_bytes.decode())
#         data = env.get("message", {}).get("data")
#         if data:
#             return json.loads(base64.b64decode(data).decode())
#     except Exception:
#         pass
#     raise ValueError("Unrecognized message format")

# def _callback(message: pubsub_v1.subscriber.message.Message):
#     try:
#         payload = _decode(message.data)
#         handle_content(payload)  # <- your business logic
#         message.ack()
#     except Exception as e:
#         print("ERROR:", e)
#         message.nack()

# def main():
#     subscriber = pubsub_v1.SubscriberClient()
#     path = subscriber.subscription_path(PROJECT, SUBSCRIPTION)
#     print("Listening on", path)
#     future = subscriber.subscribe(path, callback=_callback)

#     # graceful stop
#     def stop(*_):
#         future.cancel()
#     signal.signal(signal.SIGINT, stop); signal.signal(signal.SIGTERM, stop)

#     try:
#         future.result()
#     finally:
#         subscriber.close()

# if __name__ == "__main__":
#     main()
