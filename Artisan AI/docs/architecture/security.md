# Security Architecture – artisan-ai

## Overview
The platform runs on **Google Cloud Run** (API + Worker) with an event-driven backbone (Pub/Sub). Data lives in Firestore, BigQuery, and Cloud Storage. AI workloads run on Vertex AI.

## Security Layers
- **Identity & Access Management (IAM):**
  - API service account → `roles/pubsub.publisher`
  - Worker service account → `roles/pubsub.subscriber`, `roles/datastore.user`, `roles/aiplatform.user`
  - Least-privilege roles only

- **Ingress & Authentication:**
  - API: public HTTPS with Firebase Auth
  - Worker: private HTTPS; only Pub/Sub push SA can invoke
  - All services served over TLS 1.2+ by default

- **Secrets & Config:**
  - API keys (Stripe, Razorpay) stored in Secret Manager
  - No secrets in repo; mounted at runtime

- **Event Security:**
  - Pub/Sub schema validation for all topics
  - Dead-letter topics + retry policies
  - Idempotency keys in event envelopes

- **Data Protection:**
  - Uniform bucket-level access for GCS
  - Firestore & BigQuery encrypted at rest
  - CMEK ready if required

- **Observability:**
  - Structured JSON logs with trace IDs
  - OpenTelemetry traces across API → Worker → Vertex AI
  - Error Reporting + uptime checks enabled
