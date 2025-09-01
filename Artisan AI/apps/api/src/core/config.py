# apps/api/src/core/config.py
from __future__ import annotations

from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- App ----
    env: str = Field("dev", env="ENV")
    allow_origins: str = Field("*", env="ALLOW_ORIGINS")  # comma-separated

    # ---- GCP Project/Regions ----
    gcp_project: str = Field("", env="GCP_PROJECT")
    gcp_region: str = Field("asia-south1", env="GCP_REGION")
    vertex_location: str = Field("asia-south1", env="VERTEX_LOCATION")

    # ---- Buckets ----
    gcs_bucket: str = Field("", env="GCS_BUCKET")

    # ---- Pub/Sub topics ----
    pubsub_topic_content: str = Field("content.requested", env="PUBSUB_TOPIC_CONTENT")
    pubsub_topic_marketing: str = Field("marketing.asset.requested", env="PUBSUB_TOPIC_MARKETING")

    # Back-compat (old env names)
    TOPIC_CONTENT_REQUESTED: str = Field("content.requested", env="TOPIC_CONTENT_REQUESTED")
    TOPIC_MARKETING_REQUESTED: str = Field("marketing.asset.requested", env="TOPIC_MARKETING_REQUESTED")

    # ---- Firestore collections ----
    firestore_collection_products: str = Field("products", env="FIRESTORE_COLL_PRODUCTS")
    firestore_collection_stories: str = Field("stories", env="FIRESTORE_COLL_STORIES")
    firestore_collection_marketing: str = Field("marketing_assets", env="FIRESTORE_COLL_MARKETING")

    # ---- Vertex AI (Gemini) ----
    vertex_model: str = Field("gemini-1.5-pro", env="VERTEX_MODEL")

    # ---- Feature flags ----
    firebase_only: bool = Field(False, env="FIREBASE_ONLY")

    # ---- Credentials (optional convenience) ----
    google_application_credentials: str = Field("/app/service-account.json", env="GOOGLE_APPLICATION_CREDENTIALS")

    # Pydantic v2 settings (replaces class Config)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Convenience helper
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allow_origins.split(",") if o.strip()]


@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    # prefer explicit PUBSUB_TOPIC_*; fall back to legacy names if set
    if s.TOPIC_CONTENT_REQUESTED and s.TOPIC_CONTENT_REQUESTED != s.pubsub_topic_content:
        s.pubsub_topic_content = s.TOPIC_CONTENT_REQUESTED
    if s.TOPIC_MARKETING_REQUESTED and s.TOPIC_MARKETING_REQUESTED != s.pubsub_topic_marketing:
        s.pubsub_topic_marketing = s.TOPIC_MARKETING_REQUESTED
    return s


# Back-compat import style: from core.config import settings
settings = get_settings()