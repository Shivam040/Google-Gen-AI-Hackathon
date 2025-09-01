#!/usr/bin/env python3
"""
Seed Firestore with a few demo docs:
- users/{usr_...}
- stores/{store_...}
- products/{SH001, SH002, SH003}

Usage:
  export GOOGLE_CLOUD_PROJECT=<your-project>   # or set GCP_PROJECT
  python scripts/seed_firestore.py
"""

from datetime import datetime
from google.cloud import firestore

db = firestore.Client()

TS = firestore.SERVER_TIMESTAMP

def upsert(col, doc_id, data):
    db.collection(col).document(doc_id).set(data, merge=True)
    print(f"✓ {col}/{doc_id}")

def seed_users():
    upsert("users", "usr_admin", {
        "email": "admin@example.com",
        "role": "admin",
        "locale": "en-IN",
        "created_at": TS,
    })
    upsert("users", "usr_artisan1", {
        "email": "artisan@example.com",
        "role": "artisan",
        "store_id": "store_001",
        "locale": "hi-IN",
        "created_at": TS,
    })
    upsert("users", "usr_buyer1", {
        "email": "buyer@example.com",
        "role": "buyer",
        "locale": "en-IN",
        "created_at": TS,
    })

def seed_store():
    upsert("stores", "store_001", {
        "display_name": "Saharanpur Woodcrafts",
        "owner_user_id": "usr_artisan1",
        "contact_email": "owner@crafts.in",
        "region": "UP",
        "craft_types": ["woodwork"],
        "languages": ["en","hi"],
        "bio": "Family of artisans crafting Sheesham wood items.",
        "social_handles": {"instagram": "@saharanpur_wood"},
        "is_verified": False,
        "created_at": TS,
    })

def seed_products():
    upsert("products", "SH001", {
        "title": "Sheesham Wood Jewelry Box",
        "description": "Hand-crafted box with brass inlay.",
        "category": "woodwork",
        "materials": ["Sheesham wood","brass inlay"],
        "region": "Saharanpur",
        "attributes": {"size":"M","finish":"natural"},
        "images": ["https://example.com/box.jpg"],
        "artisan_id": "usr_artisan1",
        "base_cost": 1200.0,
        "skill_factor": 1.2,
        "inventory": 5,
        "popularity": 3,
        "is_active": True,
        "created_at": TS,
        "updated_at": TS,
    })

    upsert("products", "SH002", {
        "title": "Handloom Pashmina Shawl",
        "category": "textile",
        "materials": ["pashmina wool"],
        "region": "Kashmir",
        "images": ["https://example.com/shawl.jpg"],
        "artisan_id": "usr_artisan1",
        "base_cost": 3500.0,
        "skill_factor": 1.4,
        "inventory": 8,
        "popularity": 5,
        "is_active": True,
        "created_at": TS,
        "updated_at": TS,
    })

    upsert("products", "SH003", {
        "title": "Terracotta Diyas (Set of 8)",
        "category": "clay",
        "materials": ["terracotta"],
        "region": "Kutch",
        "images": ["https://example.com/diya.jpg"],
        "artisan_id": "usr_artisan1",
        "base_cost": 240.0,
        "skill_factor": 1.1,
        "inventory": 40,
        "popularity": 2,
        "is_active": True,
        "created_at": TS,
        "updated_at": TS,
    })

def main():
    print("Seeding Firestore…")
    seed_users()
    seed_store()
    seed_products()
    print("Done.")

if __name__ == "__main__":
    main()
