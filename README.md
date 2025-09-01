# Google Gen AI Hackathon


awesome—here’s a **submission-ready scoring matrix** you can paste into your form/README. It mirrors the hackathon rubric and shows exactly how you’ll hit each criterion.

# 📊 Evaluation Scoring Matrix (artisan-ai)

| Criterion                   |  Weight | What judges look for                                 | Our evidence (repo/files)                                                                                                                                                                                                                                                                                | Demo proof (what you’ll show)                                                                                                                                    | Risks & mitigations                                                                                            | Target score |
| --------------------------- | :-----: | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | :----------: |
| **Technical merit**         | **40%** | Smart use of Google GenAI, clean code, scalable arch | **AI tools:** `/docs/architecture/ai_tools.md`; **API:** `apps/api/src` (FastAPI, services/\*); **Worker:** `apps/worker/src` (handlers, Pub/Sub); **Infra:** `infra/terraform` (Cloud Run, Pub/Sub, Firestore, GCS); **Schemas:** `data/schemas/*.avsc`; **Security:** `/docs/architecture/security.md` | Postman/curl: `POST /v1/products/{id}` → `POST /v1/products/{id}/generate` → worker writes `gs://.../content/...md` & Firestore `stories` doc; logs in Cloud Run | Cold starts / quota: set min instances for API; pre-warm; use Vertex rate limits with backoff; DLQs on Pub/Sub |   **32/40**  |
| **User experience**         | **10%** | Simple flow; AI feels seamless                       | **UX flow:** `apps/web` scaffold (optional); **Endpoints:** `products`, `marketing`, `recs`; **Docs:** `/docs/user_guides/artisan_onboarding.md`                                                                                                                                                         | Quick screencast: artisan adds product → clicks “Generate” → multilingual story appears; show a generated social post                                            | If frontend unfinished, demo via Postman + console screen share; provide screenshots in README                 |   **8/10**   |
| **Alignment with cause**    | **15%** | Solves the stated problem; community impact          | **Story/impact:** `README.md` (Problem → Solution → Impact); **Provenance:** `models/story.py`, Firestore; **Low commission** noted in docs                                                                                                                                                              | Slide with before/after: time to create listing (60→5 min), languages (1→10+), forecasted earnings uplift                                                        | Add 2–3 real artisan personas/use-cases in README to humanize impact                                           |   **13/15**  |
| **Innovation & creativity** | **20%** | Novel ideas; potential to change behavior            | **Unique features:** `services/voice_service.py` (dialect narration), `ml/pipelines/*` (festival forecasting), `services/pricing_service.py` (empowerment pricing), “Community Labs” note in docs                                                                                                        | Play TTS sample of dialect narration; show festival feature SQL & pipeline graph (even if mocked)                                                                | If TTS/dialect not fully ready, include 30-sec audio sample & describe path to production                      |   **16/20**  |
| **Market feasibility**      | **15%** | Real market; path to adoption                        | **Go-to-market:** section in `README.md`; **Dashboards:** `data/bq/views/*` + Looker plan; **Integrations:** `payment_service.py` stubs (Stripe/Razorpay)                                                                                                                                                | Slide: TAM (7M+ artisans), early pipeline (NGOs, Ministries), pilot plan (district→state)                                                                        | Add 1–2 LOIs (letters of intent) from a local NGO/collective if possible                                       |   **12/15**  |

**Projected total: 81/100** (competitive for Top-100)

---

## 🧪 Demo script (90 seconds)

1. **Create product**
   `POST /v1/products/SH001` (title, materials, region, images)

2. **Generate content (multi-lang + tone)**
   `POST /v1/products/SH001/generate` (langs: `["en","hi"]`, tone: `narrative`)
   → show Pub/Sub message in logs
   → show `gs://.../content/SH001_hi.md` + Firestore `stories/SH001_hi`

3. **Create marketing post**
   `POST /v1/marketing/SH001/post?lang=hi&channel=instagram`
   → show Firestore `marketing_assets/SH001_hi_instagram`

4. **Recommendations (stub now, vector later)**
   `GET /v1/recs/user/demo?k=6` → returns similar crafts

5. **Security & scale slide**
   Cloud Run + Pub/Sub + Firestore diagram (from `/docs/architecture/security.md`)

---

## ✅ Submission checklist (one-pager)

* **Problem → Solution → Impact** (3 bullets each)
* **Architecture** (1 diagram + 5 bullets)
* **AI Utilization Table** (from `/docs/architecture/ai_tools.md`)
* **Demo link** (screen recording or live URL)
* **Security highlights** (TLS, IAM, SA roles, Secret Manager, Pub/Sub schemas)
* **Roadmap** (Vector Search, Dialogflow CX, Pipelines)
* **Impact metrics** (time saved, languages covered, expected earnings uplift)

---

If you want, I can also generate a **templated README section** with these exact pieces so you can copy-paste into your repo right now.




# artisan-ai Documentation by Folder

---

## apps/api/src

### services/

* **content\_service.py**: Wraps Vertex AI (Gemini) for product descriptions, tone control, and multilingual output. Stores generated content in Cloud Storage, versions in Firestore, and publishes `content.generated` events.
* **translation\_service.py**: Uses Google Translation API to localize artisan stories and product descriptions. Updates Firestore localized fields and emits `content.translated` events.
* **marketing\_service.py**: Generates social posts, taglines, and hashtags. Pulls trend features from BigQuery to suggest best posting times and themes.
* **recs\_service.py**: Provides personalized recommendations via hybrid search (Vertex Vector Search embeddings + Firestore filters). Returns tailored slates to buyers.
* **pricing\_service.py**: Computes festival-aware pricing recommendations. Uses BigQuery demand features, stores audit logs in `pricing_decisions` table.
* **voice\_service.py**: Manages dialect-aware narration workflows. Integrates Speech-to-Text, Text-to-Speech, and Dialogflow CX to create authentic artisan voice assistants.
* **payment\_service.py**: Integrates with Stripe/Razorpay for secure artisan payouts and buyer payments.

### middleware/

* **cors.py**: Configures cross-origin requests for frontend apps.
* **auth.py**: Handles Firebase Auth and API key-based authentication.
* **error\_handlers.py**: Custom exception and error response mappers for consistency.

### v1/endpoints/

* **products.py**: CRUD endpoints for artisan products.
* **stories.py**: APIs to fetch/create artisan stories and narratives.
* **marketing.py**: Endpoints to request social content and campaign suggestions.
* **pricing.py**: Provides recommended prices and demand forecasts.
* **recs.py**: Buyer product recommendations API.
* **orders.py**: Endpoints for cart, checkout, order placement.
* **auth.py**: Login, logout, token refresh endpoints.

---

## apps/worker/src

### events/

* **pubsub\_consumer.py**: Subscribes to GCP Pub/Sub topics, dispatches events to handlers.
* **kafka\_consumer.py**: Optional Confluent Kafka consumer for external integrations.
* **publisher.py**: Publishes standardized events back to Pub/Sub.

### handlers/

* **handle\_content\_requested.py**: Processes `content.requested` → calls Vertex AI → stores → publishes `content.generated`.
* **handle\_marketing\_requested.py**: Generates posts from `marketing.asset.requested`.
* **handle\_pricing\_refresh.py**: Runs pricing pipeline on schedule or demand.
* **handle\_order\_events.py**: Listens to `order.placed` and triggers downstream workflows.

### utils/

* **vertex.py**: Helper utilities for Vertex AI API calls.
* **storage.py**: GCS upload/download and signed URL helpers.
* **tracing.py**: OpenTelemetry tracing utilities for event pipelines.

---

## apps/web (Next.js)

* **app/**: App Router pages for buyer storefront and artisan dashboards.
* **components/**: UI components (ProductCard, StoryBlock, LiveBadge) using shadcn/ui.
* **lib/**: API client, Firebase Auth helpers, i18n config.
* **styles/**: Tailwind + global CSS.

---

## ml/

* **notebooks/**: Prototypes and EDA (e.g., demand forecasting, pricing experiments).
* **pipelines/**: Vertex AI Pipelines for training demand models, scheduled predictions.
* **features/**: SQL feature builders (festival calendars, regional demand signals).
* **models/**: Registry JSON for model versions and metadata.

---

## data/

* **schemas/**: Avro/Proto schemas for events (`content.generated`, `order.placed`, etc.).
* **bq/**: BigQuery datasets and SQL views (user metrics, marketing performance).

---

## infra/

* **terraform/**: Modules for provisioning Cloud Run, Firestore, BigQuery, Pub/Sub, Vertex AI.
* **envs/**: Environment-specific Terraform configs (dev, staging, prod).
* **policies/**: OPA/Conftest rules for security and compliance.

---

## services/

* **vector-store/**: ChromaDB or Vertex Vector Search proxy for embeddings.
* **data-ingestion/**: Dataflow/ETL tasks for ingesting artisan/product data to BigQuery.
* **api-gateway/**: Optional API gateway microservice (Cloud API Gateway preferred).
* **live-ar/**: WebRTC signaling service for live artisan sessions and AR previews.

---

## config/

* **settings.py**: Centralized Python config (env vars, constants).
* **agent\_configs.yaml**: Tone presets, prompt templates, content safety rules.
* **event\_topics.yaml**: Pub/Sub topic definitions.
* **environments/**: Separate YAMLs for dev, staging, prod configs.

---

## tests/

* **unit/**: Unit tests for content, marketing, recs, pricing services.
* **integration/**: API endpoint tests, Pub/Sub roundtrip tests.
* **e2e/**: Buyer checkout and artisan onboarding flow tests.
* **fixtures/**: Sample events and test data.

---

## deployment/

* **docker/**: Dockerfiles and Compose setup for local development.
* **k8s/**: Kubernetes manifests (namespace, deployments, services, configmaps, secrets).
* **scripts/**: Deployment scripts (setup.sh, deploy.sh, health\_check.sh).

---

## docs/

* **architecture/**: System design, event flows, data modeling.
* **api/**: OpenAPI specifications.
* **runbooks/**: Oncall guides, incident response checklists.
* **user\_guides/**: Artisan onboarding, best practices, live video setup.

---

## scripts/

* **setup\_dev\_env.py**: Local dev bootstrap.
* **seed\_firestore.py**: Loads sample artisan/product data.
* **backfill\_bq.py**: Rebuilds historical analytics data.
* **backup\_media\_bucket.py**: Exports media assets from GCS.

---

## Folder Docs (what each part does)

### Root

* **.env.example**: Template for required env vars (GCP project/region, API keys, emulator hosts). Duplicate as `.env` locally.
* **cloudbuild.yaml / .cloudbuild/**: CI pipelines for building & deploying `web`, `api`, `worker`, plus Terraform plan/apply.
* **pyproject.toml / package.json**: Tooling for Python (ruff/black/pytest) and JS (eslint/prettier). Root scripts for lint/test.
* **.pre-commit-config.yaml**: Hooks (format, lint, secret scan) on commit.
* **LICENSE / README.md / CODE\_OF\_CONDUCT.md / CONTRIBUTING.md / SECURITY.md**: Project meta & contribution/security policies.

### infra/terraform

* **modules/**: Reusable Terraform modules.

  * **cloud\_run\_service/**: Deploys Cloud Run service (container, concurrency, min/max instances, IAM).
  * **pubsub/**: Creates topics, subscriptions, schemas, and DLQs.
  * **firestore/**: Enables Firestore (native) and indexes (if any).
  * **bigquery/**: Datasets/tables, partitioning, retention.
  * **storage\_bucket/**: Media/generated/artifact buckets with lifecycle rules.
  * **vertex\_ai/**: Enables Vertex AI API, service accounts, and minimal policies.
  * **secret\_manager/**: Secrets and IAM bindings.
  * **scheduler/**: Scheduled jobs (cron) for batch predictions/ingestion.
  * **vpc/**: (Optional) Private networking for egress control.
* **envs/** (dev/staging/prod): Per‑environment stacks wiring modules together; `terraform.tfvars` holds env‑specific values.

### data/

* **schemas/**: Event schemas (Avro/JSON/Proto) used by Pub/Sub (and Kafka mirror). Ensures strong contracts and evolution.

  * `content.generated.avsc`, `marketing.asset.created.avsc`, `order.placed.avsc`, `pricing.updated.avsc`, `forecast.generated.avsc`.
* **bq/**: BigQuery SQL artifacts.

  * **datasets/**: Logical groupings (`core`, `ml`, `dash`).
  * **views/**: Derived tables (`v_user_metrics.sql`, `v_marketing_performance.sql`).
  * **models/**: dbt/BQML models, if used for ML-in-BQ.

### apps/web (Next.js)

* **src/app/**: App Router pages (`layout.tsx`, landing `page.tsx`, artisan dashboard route).
* **src/components/**:

  * **ui/**: Shared UI (shadcn components)
  * `ProductCard.tsx`: Product preview with price/cta.
  * `StoryBlock.tsx`: Long‑form artisan story presenter.
  * `LiveBadge.tsx`: Live session indicator.
* **src/lib/**: Client utilities.

  * `api.ts`: REST client for `apps/api`.
  * `auth.ts`: Firebase Auth helpers (token, role guard).
  * `i18n.ts`: i18next setup for multilingual UI.
* **public/**, **styles/**: Static assets and global CSS.

### apps/api/src (FastAPI)

* **main.py**: App factory; mounts routers; OpenAPI; health/live/readiness endpoints.
* **core/**:

  * `config.py`: Settings (env, project IDs, bucket names, model IDs).
  * `logging.py`: Structured logging (JSON), trace correlation.
  * `security.py`: AuthN/Z (Firebase/OIDC), API keys for webhooks.
  * `exceptions.py`: Standardized API errors.
* **middleware/**:

  * `cors.py`: CORS policy per env.
  * `auth.py`: Request auth; role checks (artisan/buyer/admin).
  * `error_handlers.py`: Maps exceptions → RFC7807 responses.
* **v1/endpoints/**:

  * `products.py`: CRUD, media upload URLs, indexing triggers.
  * `stories.py`: Create/version stories; list per product/artisan.
  * `marketing.py`: Generate posts; suggest hashtags/times.
  * `pricing.py`: Recalculate prices; retrieve audit trails.
  * `recs.py`: Personalized recommendations & search.
  * `orders.py`: Cart/checkout, payment intents, webhooks.
  * `auth.py`: Login status, token exchange.
* **models/** (Pydantic): `product.py`, `story.py`, `marketing.py`, `pricing.py`, `order.py`, `events.py` (shared event envelope).
* **repos/**: Data adapters.

  * `firestore.py`: CRUD for users/products/orders/stories.
  * `storage.py`: Signed URLs; upload/download; media metadata.
  * `bigquery.py`: Query helpers for analytics & features.
* **services/** (API highlights):

  * `content_service.py`: wraps Vertex AI (Gemini) for descriptions + tone + multilingual; stores outputs to Cloud Storage; writes version doc in Firestore; emits `content.generated`.
  * `translation_service.py`: Translation API; updates Firestore localized fields; emits `content.translated`.
  * `marketing_service.py`: Post generator + BQ trend lookup (hashtags, post times).
  * `recs_service.py`: Hybrid search (Vertex Vector Search + filters), backed by product embeddings.
  * `pricing_service.py`: Festival‑aware pricing using BigQuery features; audit logs to `pricing_decisions`.
  * `voice_service.py`: STT/TTS with Dialogflow CX for guided narration flows.
  * `payment_service.py`: Stripe/Razorpay intents and webhooks.

### apps/worker/src (Async processing)

* **runner.py**: Entrypoint that launches consumers for configured backends.
* **events/**:

  * `pubsub_consumer.py`: Subscribes to Pub/Sub, ack/nack, DLQ handling.
  * `kafka_consumer.py`: Optional Confluent consumer (bridge/mirror topics).
  * `publisher.py`: Common publish util with idempotency keys.
* **handlers/**:

  * `handle_content_requested.py`: Fetch product → call Vertex → write artifact → publish `content.generated`.
  * `handle_marketing_requested.py`: Build social copy → persist → `marketing.asset.created`.
  * `handle_pricing_refresh.py`: Trigger recalculation → persist → `pricing.updated`.
  * `handle_order_events.py`: React to `order.*` (fulfillment, emails).
* **utils/**: `vertex.py` (Vertex client), `storage.py` (GCS), `tracing.py` (OpenTelemetry).

### services/ (optional microservices)

* **vector-store/**: ChromaDB (or proxy to Vertex Vector Search). Exposes gRPC/HTTP for index/search; manages embeddings sync.
* **data-ingestion/**: Periodic ingestion to Pub/Sub & BigQuery; may run scheduled in Cloud Run Jobs/Cloud Scheduler.
* **api-gateway/**: Thin proxy if not using managed API Gateway.
* **live-ar/**: WebRTC signaling & 3D asset optimization for AR previews.

### ml/

* **notebooks/**: Exploratory analysis for demand/pricing; prototypes.
* **pipelines/**: Vertex Pipelines (Kubeflow) definitions (`demand_forecast_pipeline.py`, `training_component.yaml`).
* **features/**: SQL to compute calendar/festival/regional features (`build_calendar_features.sql`, `festival_features.sql`).
* **models/**: Registry (`registry.json`), notes, evaluation results.

### frontend/ (alt Vite React skeleton)

* If you prefer Vite over Next.js for certain surfaces. Components/services mimic `apps/web` but without SSR.

### config/

* **settings.py**: Central config loader (env → dataclass/pydantic settings).
* **agent\_configs.yaml**: Prompt presets, tones, safety thresholds.
* **event\_topics.yaml**: Source of truth for topics & subscriptions.
* **environments/**: Per‑env values merged into settings for dev/staging/prod.

### docs/

* **architecture/**: System design, event flow, data model diagrams.
* **api/**: OpenAPI spec (`openapi.yaml`).
* **runbooks/**: On‑call, incident guide, common playbooks.
* **user\_guides/**: Artisan onboarding, listing tips, live video setup.

### tests/

* **unit/**: Service‑level tests (content/marketing/recs/pricing).
* **integration/**: API endpoint tests; Pub/Sub round‑trip with emulators.
* **e2e/**: Buyer journey (browse → cart → checkout) happy path.
* **fixtures/**: Sample events and payload builders.

### deployment/

* **docker/**: Local composition and service Dockerfiles (`api.Dockerfile`, `worker.Dockerfile`, `web.Dockerfile`).
* **k8s/**: If using GKE instead of Cloud Run (Deployments/Services/ConfigMaps/Secrets).
* **scripts/**: `setup.sh` (bootstrap project), `deploy.sh` (one‑command deploy), `health_check.sh`.

### scripts/

* **setup\_dev\_env.py**: Creates local `.env`, installs hooks, pulls emulators.
* **seed\_firestore.py**: Seeds demo users/products/stories.
* **backfill\_bq.py**: Backfills analytics tables.
* **backup\_media\_bucket.py**: Snapshot media to archival bucket.



# artisan-ai /

> Production-ready monorepo scaffold for **AI‑Powered Artisan Marketplace** on **Google Cloud** (Vertex AI, Pub/Sub, Cloud Run, Firestore, BigQuery) with optional **Kafka** bridge.

```
artisan-ai/
├── .gitignore
├── .env.example
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
│
├── pnpm-workspace.yaml                 # If using pnpm; else remove
├── package.json                        # Root scripts (lint, fmt) for JS workspaces
├── pyproject.toml                      # Python toolchain config (ruff/black/uv/poetry)
├── poetry.lock                         # If using poetry; else uv.lock/requirements.txt
│
├── cloudbuild.yaml                     # Cloud Build pipeline orchestrator
├── .cloudbuild/
│   ├── build_api.yaml
│   ├── build_web.yaml
│   ├── build_worker.yaml
│   ├── terraform_plan_apply.yaml
│   └── lint_test.yaml
│
├── infra/                              # IaC: Google Cloud via Terraform
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── cloud_run_service/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── pubsub/
│   │   │   │   ├── main.tf            # topics, subs, schemas, DLQs
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── firestore/
│   │   │   ├── bigquery/
│   │   │   ├── storage_bucket/
│   │   │   ├── vertex_ai/
│   │   │   ├── secret_manager/
│   │   │   ├── scheduler/
│   │   │   └── vpc/
│   │   ├── envs/
│   │   │   ├── dev/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   ├── terraform.tfvars
│   │   │   │   └── backend.tf
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   └── README.md
│   └── policies/                       # OPA/Conftest policies (optional)
│
├── data/
│   ├── schemas/                        # Shared event schemas (JSON/Avro/Proto)
│   │   ├── content.generated.avsc
│   │   ├── marketing.asset.created.avsc
│   │   ├── order.placed.avsc
│   │   ├── pricing.updated.avsc
│   │   └── forecast.generated.avsc
│   └── bq/                             # BigQuery SQL (views, UDFs, models)
│       ├── datasets/
│       │   ├── core/
│       │   ├── ml/
│       │   └── dash/
│       ├── views/
│       │   ├── v_user_metrics.sql
│       │   └── v_marketing_performance.sql
│       └── models/                     # dbt or BQML models (optional)
│
├── apps/
│   ├── web/                            # Next.js (TypeScript) storefront + artisan console
│   │   ├── next.config.js
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── public/
│   │   └── src/
│   │       ├── app/
│   │       │   ├── layout.tsx
│   │       │   ├── page.tsx
│   │       │   └── (dash)/artisan/page.tsx
│   │       ├── components/
│   │       │   ├── ui/                 # shadcn/ui components
│   │       │   ├── ProductCard.tsx
│   │       │   ├── StoryBlock.tsx
│   │       │   └── LiveBadge.tsx
│   │       ├── lib/
│   │       │   ├── api.ts              # REST client
│   │       │   ├── auth.ts             # Firebase Auth helpers
│   │       │   └── i18n.ts             # i18next setup
│   │       └── styles/
│   │           └── globals.css
│   │
│   ├── api/                            # FastAPI core API (Cloud Run)
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── main.py                 # FastAPI app, OpenAPI
│   │       ├── core/
│   │       │   ├── config.py
│   │       │   ├── logging.py
│   │       │   ├── security.py
│   │       │   └── exceptions.py
│   │       ├── middleware/
│   │       │   ├── cors.py
│   │       │   ├── auth.py
│   │       │   └── error_handlers.py
│   │       ├── v1/
│   │       │   ├── endpoints/
│   │       │   │   ├── products.py
│   │       │   │   ├── stories.py
│   │       │   │   ├── marketing.py
│   │   │   │   ├── pricing.py
│   │       │   │   ├── recs.py
│   │       │   │   ├── orders.py
│   │       │   │   └── auth.py
│   │       │   └── dependencies.py
│   │       ├── models/                 # pydantic schemas
│   │       │   ├── product.py
│   │       │   ├── story.py
│   │       │   ├── marketing.py
│   │       │   ├── pricing.py
│   │       │   ├── order.py
│   │       │   └── events.py
│   │       ├── repos/
│   │       │   ├── firestore.py
│   │       │   ├── storage.py
│   │       │   └── bigquery.py
│   │       └── services/
│   │           ├── content_service.py      # Vertex AI (Gemini) wrapper
│   │           ├── translation_service.py  # GCP Translation API
│   │           ├── marketing_service.py    # hashtags/time via BQ features
│   │           ├── pricing_service.py      # dynamic pricing rules
│   │           ├── recs_service.py         # Vector Search + rules
│   │           ├── voice_service.py        # STT/TTS + Dialogflow CX
│   │           └── payment_service.py      # Stripe/Razorpay
│   │
│   ├── worker/                         # Async workers (Pub/Sub or Kafka)
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── runner.py               # entrypoint
│   │       ├── events/
│   │       │   ├── pubsub_consumer.py
│   │       │   ├── kafka_consumer.py   # optional (Confluent)
│   │       │   └── publisher.py
│   │       ├── handlers/
│   │       │   ├── handle_content_requested.py
│   │       │   ├── handle_marketing_requested.py
│   │       │   ├── handle_pricing_refresh.py
│   │       │   └── handle_order_events.py
│   │       └── utils/
│   │           ├── vertex.py
│   │           ├── storage.py
│   │           └.— tracing.py
│   │
│   └── admin/                          # Admin console (optionally Next.js or FastAPI)
│       ├── README.md
│       └── (later)
│
├── services/                           # Optional microservices (split out concerns)
│   ├── vector-store/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/chromadb_service.py     # or Vertex Vector Search proxy
│   ├── data-ingestion/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/ingest_to_pubsub.py     # Schedules + ETL to BigQuery
│   ├── api-gateway/
│   │   ├── Dockerfile
│   │   └── src/gateway.py              # optional (Cloud API Gateway is managed)
│   └── live-ar/
│       ├── Dockerfile
│       └── src/live_router.py          # WebRTC signaling / 3D asset prep
│
├── ml/                                 # Vertex AI pipelines + models
│   ├── notebooks/
│   │   ├── demand_forecast_eda.ipynb
│   │   └── pricing_rules_sandbox.ipynb
│   ├── pipelines/
│   │   ├── demand_forecast_pipeline.py # Kubeflow/Vertex Pipelines
│   │   └── training_component.yaml
│   ├── features/
│   │   ├── build_calendar_features.sql
│   │   └── festival_features.sql
│   └── models/
│       ├── README.md
│       └── registry.json               # model versions/URIs
│
├── frontend/                           # Alternative to Next.js (if needed): Vite React
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── pages/
│       ├── components/
│       └── services/
│
├── config/
│   ├── settings.py                     # central config (Python)
│   ├── agent_configs.yaml              # tone presets, prompts, safety
│   ├── event_topics.yaml               # list of Pub/Sub topics
│   └── environments/
│       ├── development.yaml
│       ├── staging.yaml
│       └── production.yaml
│
├── docs/
│   ├── architecture/
│   │   ├── system_design.md
│   │   ├── event_flow.md               # event-driven diagrams
│   │   └── data_modeling.md
│   ├── api/
│   │   └── openapi.yaml
│   ├── runbooks/
│   │   ├── oncall_guide.md
│   │   └── incident_checklist.md
│   └── user_guides/
│       ├── artisan_onboarding.md
│       ├── listing_best_practices.md
│       └── live_video_setup.md
│
├── tests/
│   ├── unit/
│   │   ├── test_content_service.py
│   │   ├── test_marketing_service.py
│   │   ├── test_recs_service.py
│   │   └── test_pricing_service.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   └── test_pubsub_roundtrip.py
│   ├── e2e/
│   │   └── test_buyer_checkout.py
│   └── fixtures/
│       └── sample_events.json
│
├── deployment/
│   ├── docker/
│   │   ├── docker-compose.yaml
│   │   ├── docker-compose.override.yaml
│   │   └── services/
│   │       ├── api.Dockerfile
│   │       ├── worker.Dockerfile
│   │       └── web.Dockerfile
│   ├── k8s/                            # if using GKE instead of Cloud Run
│   │   ├── namespace.yaml
│   │   ├── deployments/
│   │   │   ├── api.yaml
│   │   │   ├── worker.yaml
│   │   │   └── web.yaml
│   │   ├── services/
│   │   │   ├── api-svc.yaml
│   │   │   └── web-svc.yaml
│   │   ├── configmaps/
│   │   └── secrets/
│   └── scripts/
│       ├── setup.sh
│       ├── deploy.sh
│       └── health_check.sh
│
└── scripts/
    ├── setup_dev_env.py
    ├── seed_firestore.py
    ├── backfill_bq.py
    └── backup_media_bucket.py
```

---

## Root files

* **.env.example**: `GCP_PROJECT=...`, `REGION=asia-south1`, `FIRESTORE_EMULATOR_HOST=...`, `VERTEX_MODEL=gemini-1.5-pro`, `PUBSUB_EMULATOR_HOST=...`, `CONFLUENT_BOOTSTRAP=...` (if Kafka), payment keys, etc.
* **cloudbuild.yaml**: matrix builds for `apps/api`, `apps/web`, `apps/worker` + Terraform plan/apply with manual approval for prod.
* **.pre-commit-config.yaml**: ruff/black for Python, eslint/prettier for TS, commitlint.

## Pub/Sub topics (config/event\_topics.yaml)

* `content.requested`, `content.generated`, `content.translated`
* `marketing.asset.requested`, `marketing.asset.created`
* `product.created`, `product.updated`
* `order.placed`, `order.paid`, `order.fulfilled`
* `pricing.updated`, `forecast.generated`
* `voice.narration.uploaded`, `voice.tts.ready`

## Data schemas (data/schemas/\*.avsc)

Each event has Avro schema: `event_id`, `occurred_at`, `actor`, `type`, `data{...}` with resource references (Firestore IDs, `gs://` URIs).

## API highlights (apps/api/src)

* `services/content_service.py`: wraps Vertex AI (Gemini) for descriptions + tone + multilingual; stores outputs to Cloud Storage; writes version doc in Firestore; emits `content.generated`.
* `services/translation_service.py`: Translation API; updates Firestore localized fields; emits `content.translated`.
* `services/marketing_service.py`: Post generator + BQ trend lookup (hashtags, post times).
* `services/recs_service.py`: hybrid search (Vertex Vector Search + filters), backed by product embeddings.
* `services/pricing_service.py`: festival-aware pricing using features from BigQuery; audit logs to BQ table `pricing_decisions`.
* `services/voice_service.py`: STT/TTS with Dialogflow CX for guided narration flows.

## Worker highlights (apps/worker/src)

* `events/pubsub_consumer.py`: subscription loop with ack/nack + DLQ.
* Handlers convert `content.requested` → Vertex call → write artifact → `content.generated`.
* Optional `events/kafka_consumer.py` if using Confluent Cloud; mirror topics; Dataflow bridge recommended.

## ML (Vertex AI)

* `pipelines/demand_forecast_pipeline.py`: BigQuery → feature build → train → eval → register → batch predict; scheduled by Cloud Scheduler.
* `features/*.sql`: holiday/festival features (Diwali, Durga Puja, Onam), seasonality, regionality.

## Terraform quick list (infra/terraform)

* Enable APIs: `run.googleapis.com`, `aiplatform.googleapis.com`, `firestore.googleapis.com`, `storage.googleapis.com`, `bigquery.googleapis.com`, `pubsub.googleapis.com`, `cloudbuild.googleapis.com`, `cloudscheduler.googleapis.com`.
* Resources: Cloud Run (api/web/worker), Firestore (native), Pub/Sub (topics/subs/schemas), Storage buckets (`media`, `generated`, `ml-artifacts`), BigQuery datasets (`core`, `ml`, `dash`), Secret Manager entries, Service Accounts w/ IAM.

## Optional Kafka (Confluent Cloud)

* Keep topic names identical; use Confluent Schema Registry. Use **Dataflow KafkaIO** to bridge Kafka⇄Pub/Sub; or Confluent Pub/Sub sink/source connectors. Only adopt if you need Kafka Streams/ksqlDB ecosystem.

## Testing

* Unit tests for services and handlers; integration tests spin up emulators (Firestore/PubSub) via docker-compose; e2e covers browse→add‑to‑cart→checkout.

## MVP checklist

* [ ] Deploy Firestore, Pub/Sub, buckets, BigQuery via Terraform (dev)
* [ ] Ship `apps/api` + `apps/web` + `apps/worker` to Cloud Run (dev)
* [ ] Verify event round‑trip (request→generated)
* [ ] Enable Translation + generate localized pages (hi, bn, ta)
* [ ] Basic recs (embedding + popularity)
* [ ] Dashboard in Looker Studio over `events_*` tables

---

### Notes

* This scaffold maps 1:1 to your earlier GrantGenie.ai rigor (agents, pipelines, services) but optimized for GCP‑native execution and artisan‑commerce needs. Add or prune services as you converge on MVP scope.
