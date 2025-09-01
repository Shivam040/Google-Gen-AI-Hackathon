# ---------- Build/runtime image ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    TZ=Asia/Kolkata

WORKDIR /app

# Dev-only: copy SA key (use a secret/Workload Identity in prod)
COPY service-account.json /app/service-account.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json

# App configuration (dev defaults)
ENV GCP_PROJECT=artisan-ai-472217
ENV ALLOW_ORIGINS=http://localhost:5173
ENV FIREBASE_ONLY=true

# If you have pyproject.toml or requirements.txt, copy first to leverage cache
COPY pyproject.toml /app/

# Install deps (pin versions for reproducibility)
RUN pip install --no-cache-dir \
    fastapi==0.115.2 \
    uvicorn[standard]==0.30.6 \
    pydantic==2.8.2 \
    pydantic-settings==2.4.0 \
    python-dotenv==1.0.1 \
    google-cloud-firestore==2.16.0 \
    google-cloud-pubsub==2.21.5 \
    google-cloud-storage==2.18.2 \
    google-genai==0.3.0 \
    vertexai
# NOTE: When you enable billing and flip FIREBASE_ONLY=false,
#       add Vertex AI client:
# RUN pip install --no-cache-dir google-cloud-aiplatform==1.70.0

# App code
COPY src /app/src
ENV PYTHONPATH=/app

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', 8080))" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]


