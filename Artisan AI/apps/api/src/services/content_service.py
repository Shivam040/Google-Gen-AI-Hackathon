# apps/api/src/services/content_service.py
from __future__ import annotations

import os
from typing import List, Dict, Any

from ..core.config import get_settings
from ..repos import pubsub, firestore as fs, storage
from ..models.events import EventEnvelope
from ..models.product import ContentPointer

settings = get_settings()
FIREBASE_ONLY = os.getenv("FIREBASE_ONLY", "false").lower() == "true"

# Prefer Google AI (google.genai) when an API key is present.
_GENAI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
_DEFAULT_MODEL = "gemini-2.5-pro"


# --------------------------------------------------------------------
# (1) Async / event path — publish "content.requested"
# --------------------------------------------------------------------
def request_generation(
    product_id: str,
    langs: List[str],
    tone: str,
    actor: Dict[str, Any] | None = None,
) -> str:
    topic_requested = getattr(settings, "TOPIC_CONTENT_REQUESTED", None) or settings.pubsub_topic_content
    envelope = EventEnvelope(
        type="content.requested",
        data={"product_id": product_id, "langs": langs, "tone": tone},
        source="api",
    ).model_dump()
    if actor:
        envelope["actor"] = actor
    return pubsub.publish(topic_requested, envelope)


# --------------------------------------------------------------------
# (2) Sync path — immediate generation
# --------------------------------------------------------------------
def _mock_text(product: dict, tone: str, lang: str) -> str:
    mats = ", ".join(product.get("materials", []) or [])
    region = product.get("region") or "—"
    title = product.get("title") or "Untitled"
    return (
        f"# {title}\n\n"
        f"({lang}, {tone})\n\n"
        f"Materials: {mats or '—'}\n"
        f"Region: {region}\n\n"
        f"_Placeholder story generated in Firebase-only mode._"
    )


def _build_prompt(product: dict, tone: str, lang: str) -> str:
    mats = ", ".join(product.get("materials", []) or [])
    region = product.get("region") or "—"
    title = product.get("title") or product.get("name") or "Untitled"
    return (
        "You help artisans describe their handmade products.\n"
        f"Write a **{tone.lower()}** product story in language code '{lang}'. "
        "Output in Markdown, about 150 words. Be specific and warm. "
        "Include a short title as the first Markdown heading (# Title).\n\n"
        f"- Title: {title}\n"
        f"- Materials: {mats or 'unspecified'}\n"
        f"- Region: {region}\n"
        "- Avoid making up facts. Keep it respectful and authentic."
    )


def _generate_with_genai(prompt: str, model: str) -> str:
    """Generate text via google.genai (Google AI API, API key path)."""
    try:
        import google.generativeai as genai
    except ModuleNotFoundError as e:
        raise RuntimeError("google-genai not installed. Add `google-genai`.") from e

    if not _GENAI_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY / GOOGLE_GENAI_API_KEY is not set.")

    genai.configure(api_key=_GENAI_API_KEY)
    genai_model = genai.GenerativeModel(model)
    response = genai_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7, max_output_tokens=512, top_p=0.95, top_k=40
        ),
    )

    if getattr(response, "text", None):
        return response.text.strip()

    parts: list[str] = []
    for cand in getattr(response, "candidates", []) or []:
        content = getattr(cand, "content", None)
        if content:
            for part in getattr(content, "parts", []) or []:
                if getattr(part, "text", None):
                    parts.append(part.text)
    return "\n".join(parts).strip()


def _generate_with_vertex(prompt: str, model: str | None = None) -> str:
    """Generate via Vertex AI SDK (ADC/service account)."""
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, GenerationConfig
    except ModuleNotFoundError as e:
        raise RuntimeError("Vertex SDK not installed. Add `google-cloud-aiplatform`.") from e

    project = getattr(settings, "gcp_project", None) or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = getattr(settings, "vertex_location", None) or os.getenv("VERTEX_LOCATION") or "us-central1"
    model_id = model or os.getenv("VERTEX_MODEL", _DEFAULT_MODEL)

    if not project:
        raise RuntimeError("GCP_PROJECT / GOOGLE_CLOUD_PROJECT not set.")

    vertexai.init(project=project, location=location)
    vertex_model = GenerativeModel(model_id)
    cfg = GenerationConfig(temperature=0.7, top_p=0.95, top_k=40, max_output_tokens=1024)

    response = vertex_model.generate_content(prompt, generation_config=cfg)

    if getattr(response, "text", None):
        return response.text.strip()

    parts: list[str] = []
    for cand in getattr(response, "candidates", []) or []:
        content = getattr(cand, "content", None)
        if content:
            for part in getattr(content, "parts", []) or []:
                if getattr(part, "text", None):
                    parts.append(part.text)

    text = "\n".join(parts).strip()
    if not text:
        raise RuntimeError("Vertex response had no text content.")
    return text


def generate_story_sync(product_id: str, product: dict, tone: str, langs: List[str]) -> list[dict]:
    """
    Generates one Markdown story per language and returns a list of ContentPointer dicts.
    Each pointer includes:
      - path: object path (e.g. 'content/<id>_<lang>.md')
      - meta.url: browser URL (http/https) to view the file
      - meta.text: the generated markdown (for immediate UI display)
    """
    results: list[dict] = []

    # Choose a generated-topic name robustly
    topic_requested = getattr(settings, "TOPIC_CONTENT_REQUESTED", None) or settings.pubsub_topic_content
    topic_generated = getattr(settings, "TOPIC_CONTENT_GENERATED", None)
    if not topic_generated:
        topic_generated = topic_requested.replace(".requested", ".generated") if ".requested" in topic_requested else f"{topic_requested}.generated"

    for lang in langs:
        prompt = _build_prompt(product, tone, lang)
        text = ""

        # Try Google AI via API key
        if _GENAI_API_KEY:
            try:
                text = _generate_with_genai(prompt, _DEFAULT_MODEL)
                print(f"✅ Google GenAI ok for {lang}")
            except Exception as e:
                print(f"❌ Google GenAI failed for {lang}: {e}")

        # Fallback: Vertex (service account)
        if not text:
            try:
                text = _generate_with_vertex(prompt, _DEFAULT_MODEL)
                print(f"✅ Vertex ok for {lang}")
            except Exception as e:
                print(f"❌ Vertex failed for {lang}: {e}")

        # Final fallback: mock
        if not text:
            text = _mock_text(product, tone, lang)
            print(f"⚠️ Using mock content for {lang}")

        # Persist
        path = f"content/{product_id}_{lang}.md"
        gcs_uri = storage.write_text(path, text, content_type="text/markdown; charset=utf-8")
        http_url = storage.public_url(path)

        fs.save_story(
            product_id,
            lang,
            {"gcs_uri": gcs_uri, "http_url": http_url, "tone": tone, "version": 1, "approved": True},
        )

        # Notify (best-effort)
        try:
            env = EventEnvelope(
                type="content.generated",
                data={
                    "product_id": product_id,
                    "lang": lang,
                    "tone": tone,
                    "gcs_path": path,
                    "http_url": http_url,
                },
            ).model_dump()
            pubsub.publish(topic_generated, env)
        except Exception as e:
            print(f"⚠️ publish content.generated failed: {e}")

        # Return pointer (with immediate text for UI)
        results.append(
            ContentPointer(
                path=path,
                meta={"lang": lang, "tone": tone},  # keep light
                text=text,          # <-- frontend reads first.text
                gcs_uri=gcs_uri,    # <-- frontend reads first.gcs_uri
                url=http_url,       # optional convenience
            ).model_dump()
        )

    return results

