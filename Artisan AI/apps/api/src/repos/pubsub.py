# apps/api/src/services/pubsub.py: For calling:
#from ..services import pubsub
# from ..models.events import EventEnvelope

# envelope = EventEnvelope(type="content.generated", data={"product_id": "SH001"}).model_dump()
# msg_id = pubsub.publish("content.generated", envelope)

from __future__ import annotations

import json
from typing import Dict, Optional, Any

from google.cloud import pubsub_v1
from ..core.config import get_settings
from ..models.events import EventEnvelope, make_event

_settings = get_settings()
_publisher = pubsub_v1.PublisherClient()
_topic_cache: Dict[str, str] = {}


def _topic_path(topic_name: str) -> str:
    """Memoize topic path resolution."""
    if topic_name not in _topic_cache:
        _topic_cache[topic_name] = _publisher.topic_path(_settings.gcp_project, topic_name)
    return _topic_cache[topic_name]


def publish(topic_name: str, payload: Dict[str, Any], *, attrs: Optional[Dict[str, str]] = None) -> str:
    """
    Publish a pre-built payload to a specific Pub/Sub topic.
    - `topic_name`: e.g. "content.requested" | "content.generated" | "marketing.asset.requested"
    - `payload`: dict (will be json-encoded)
    - `attrs`: optional message attributes (string-only values)
    Returns Pub/Sub message_id.
    """
    topic_path = _topic_path(topic_name)
    data = json.dumps(payload).encode("utf-8")
    future = _publisher.publish(topic_path, data, **(attrs or {}))
    return future.result()


def publish_event(
    event_type: str,
    data: Dict[str, Any],
    *,
    source: str = "api",
    actor: Optional[Dict[str, Any]] = None,
    idempotency_key: Optional[str] = None,
    topic_name: Optional[str] = None,
) -> str:
    """
    Build an EventEnvelope and publish it.
    - If `topic_name` is provided, publish there.
    - Otherwise, route by convention:
        * content.*   → _settings.pubsub_topic_content
        * marketing.* → _settings.pubsub_topic_marketing
        * else        → use event_type as topic name (advanced/manual routing)
    """
    ev: EventEnvelope = make_event(
        event_type,
        data,
        source=source,
        actor=actor,
        idempotency_key=idempotency_key,
    )

    # Routing
    if topic_name:
        topic = topic_name
    elif event_type.startswith("content."):
        topic = _settings.pubsub_topic_content
        # If caller passed ".generated" in the type, keep that in attributes;
        # topic stays the base (common pattern).
    elif event_type.startswith("marketing."):
        topic = _settings.pubsub_topic_marketing
    else:
        # Fallback: treat the event_type as the topic name (advanced/manual)
        topic = event_type

    # Helpful attributes for filters & diagnostics (must be str values)
    attrs = {
        "type": ev.type,
        "event_id": ev.event_id,
        "source": ev.source,
        "schema_version": ev.schema_version,
    }
    if ev.idempotency_key:
        attrs["idempotency_key"] = ev.idempotency_key

    return publish(topic, ev.model_dump(), attrs=attrs)



