# apps/api/src/models/events.py
# Envelope for Pub/Sub/Kafka style events.
# - Strong typing for common fields
# - UTC timestamps in ISO-8601 Z format
# - Backward-compatible factory: envelope()

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4
from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_serializer


def _now_utc_iso() -> datetime:
    # store as aware datetime; serializer below emits Z-ISO
    return datetime.now(timezone.utc).replace(microsecond=0)


class EventEnvelope(BaseModel):
    # core metadata
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=_now_utc_iso)

    # required type + payload
    type: str
    data: Dict[str, Any]

    # optional context
    source: str = Field(default="api", description="emitter (api|worker|web|script)")
    actor: Optional[Dict[str, Any]] = Field(default=None, description="who triggered the event")
    schema_version: str = Field(default="1.0")
    idempotency_key: Optional[str] = Field(
        default=None,
        description="set to dedupe at consumer; same key = same logical event",
    )

    @field_serializer("occurred_at")
    def _serialize_dt(self, dt: datetime, _info):
        # Emit as RFC3339 with Z (e.g., 2025-09-19T13:30:00Z)
        return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ---- Convenience factory (backward compatible with your old `envelope()` name) ----
def make_event(
    event_type: str,
    data: Dict[str, Any],
    *,
    source: str = "api",
    actor: Optional[Dict[str, Any]] = None,
    idempotency_key: Optional[str] = None,
) -> EventEnvelope:
    return EventEnvelope(
        type=event_type,
        data=data,
        source=source,
        actor=actor,
        idempotency_key=idempotency_key,
    )


# Back-compat aliases so existing imports keep working if you used older names
Event = EventEnvelope
def envelope(event_type: str, data: Dict[str, Any], actor: Optional[Dict[str, Any]] = None) -> EventEnvelope:
    return make_event(event_type, data, source="api", actor=actor)
