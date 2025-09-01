# apps/api/src/main.py
# FastAPI app entrypoint: routers, middleware, OpenAPI, health probes.

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings

# Routers (they already include their own /v1/... prefixes & tags)
from .v1.endpoints import products, marketing, recs, uploads  # <-- added uploads

# ---- App init ----
settings = get_settings()

app = FastAPI(
    title="Artisan AI API",
    version="0.1.0",
    description="Backend for AI-powered artisan marketplace (Firestore-first; Vertex/GCS optional).",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---- Middleware ----
origins = settings.cors_origins() or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # e.g. ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Routers ----
app.include_router(products.router)
app.include_router(marketing.router)
app.include_router(recs.router)
app.include_router(uploads.router)  # <-- register uploads endpoints

# ---- Health/Liveness/Readiness ----
@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/livez")
def live():
    return {"ok": True, "env": settings.env}

@app.get("/readyz")
def ready():
    # place quick dependency checks here later (e.g., Firestore ping)
    return {"ok": True}
