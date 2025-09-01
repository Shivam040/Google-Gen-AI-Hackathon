Got it. When your \$300 free credits land (i.e., you can enable billing), run this one-time setup to get your full async flow (GCS + Pub/Sub + optional Vertex) working.

# 0) Pick variables (replace if you use different names)

```bash
export PROJECT=artisan-ai-472217
export REGION=asia-south1
export BUCKET=${PROJECT}-generated         # e.g. artisan-ai-472217-generated
export TOPIC_CONTENT=content.requested
export SUB_PULL=content.requested-pull
export SA_EMAIL=$(jq -r .client_email apps/api/service-account.json)  # your service account from the key you’re mounting
```

# 1) Link billing to the project

UI path (easiest): Google Cloud Console → Billing → Link billing account to project **\$PROJECT**.

CLI (if you want):

```bash
gcloud config set project $PROJECT
gcloud beta billing accounts list                    # find BILLING_ACCOUNT_ID
gcloud beta billing projects link $PROJECT \
  --billing-account=YOUR_BILLING_ACCOUNT_ID
```

# 2) Enable required APIs (one time)

```bash
gcloud services enable \
  storage.googleapis.com \
  pubsub.googleapis.com \
  firestore.googleapis.com \
  aiplatform.googleapis.com
```

> Firestore must already be created in **Native mode** (Console → Firestore → “Create database”, region close to your app).

# 3) Create your GCS bucket

```bash
gcloud storage buckets create gs://$BUCKET \
  --location=$REGION --uniform-bucket-level-access
```

# 4) Grant IAM to your service account

```bash
# Storage (write & read objects)
gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
  --member="serviceAccount:$SA_EMAIL" --role="roles/storage.objectCreator"
gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
  --member="serviceAccount:$SA_EMAIL" --role="roles/storage.objectViewer"

# Pub/Sub publish (API) + subscribe (Worker)
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" --role="roles/pubsub.publisher"
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" --role="roles/pubsub.subscriber"

# (Optional if you’ll call Vertex from this SA)
gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" --role="roles/aiplatform.user"
```

# 5) Pub/Sub resources (topic + pull subscription)

```bash
gcloud pubsub topics create $TOPIC_CONTENT
gcloud pubsub subscriptions create $SUB_PULL --topic=$TOPIC_CONTENT
# (optional) add DLQ to prevent infinite retries
gcloud pubsub topics create ${TOPIC_CONTENT}.dlq
gcloud pubsub subscriptions update $SUB_PULL \
  --dead-letter-topic=projects/$PROJECT/topics/${TOPIC_CONTENT}.dlq \
  --max-delivery-attempts=5
```

# 6) Set envs when running API & Worker

API container:

```bash
# Git Bash example
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" \
docker run -p 8080:8080 \
  -e GCP_PROJECT=$PROJECT \
  -e GCS_BUCKET=$BUCKET \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
  -v "$PWD/apps/api/service-account.json":/app/service-account.json:ro \
  artisan-api
```

Worker (local):

```bash
export GCP_PROJECT=$PROJECT
export GCS_BUCKET=$BUCKET
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/../api/service-account.json"
python -m src.consumers.pull_content_requested
```

# 7) Quick end-to-end test

Create a product:

```bash
curl -s -X POST http://localhost:8080/v1/products/p1 \
  -H 'content-type: application/json' \
  -d '{"title":"Sheesham Box","category":"woodwork","is_active":true}' | jq
```

Publish an async job:

```bash
curl -s -X POST 'http://localhost:8080/v1/products/p1/generate?mode=event' \
  -H 'content-type: application/json' \
  -d '{"langs":["en"],"tone":"friendly"}' | jq
```

Watch the worker logs (it should process the message). Verify artifacts:

```bash
# GCS
gcloud storage ls gs://$BUCKET/stories/p1/**

# Firestore (Console → Data) — check stories/marketing_assets docs exist
```

# 8) If you also want sync generation with Vertex

* Keep `FIREBASE_ONLY=false` in API env.
* Ensure `aiplatform.googleapis.com` enabled and SA has `roles/aiplatform.user`.
* Your `content_service.py` calls Vertex and writes to `gs://$BUCKET/...`.

# 9) Safety tips

* Add fail-fast checks in the worker (you already did): print `GCP_PROJECT`, `GCS_BUCKET`, SA path, and verify bucket at startup.
* Use DLQ + `max-delivery-attempts` on the subscription to avoid infinite retry loops.
* Prefer deterministic IDs for Firestore/GCS writes so retries are idempotent.

Once billing is enabled, running steps **2 → 7** gets you fully operational.
