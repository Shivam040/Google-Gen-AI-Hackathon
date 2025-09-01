# src/v1/models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductIn(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    materials: List[str] = []
    region: Optional[str] = None
    attributes: dict = {}

class ProductOut(ProductIn):
    id: str
    popularity: int = 0
