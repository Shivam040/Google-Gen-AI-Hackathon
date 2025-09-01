# apps/api/src/v1/endpoints/uploads.py
from __future__ import annotations

from fastapi import APIRouter, Body, Query, HTTPException, status
from pydantic import BaseModel, Field
from ...repos import storage

router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

# ---- Schemas ----
class SignRequest(BaseModel):
    filename: str = Field(..., min_length=1)
    content_type: str = Field(
        "application/octet-stream",
        alias="contentType",
        description="MIME type of the file (e.g., image/png)",
    )

class SignResponse(BaseModel):
    upload_url: str | None
    public_url: str
    object_name: str

# ---- POST (preferred) ----
@router.post("/sign", response_model=SignResponse, status_code=status.HTTP_200_OK)
def sign_upload(body: SignRequest = Body(...)):
    try:
        out = storage.signed_put_url(body.filename, body.content_type)
        return out
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"sign: {e}")

# ---- GET (back-compat) ----
@router.get("/signed-url", response_model=SignResponse)
def get_signed_url(
    filename: str = Query(..., min_length=1),
    contentType: str = Query("application/octet-stream"),
):
    # Reuse the POST handler for consistent behavior
    return sign_upload(SignRequest(filename=filename, contentType=contentType))


# # apps/api/src/v1/endpoints/uploads.py
# from fastapi import APIRouter, Query
# from ...repos.storage import signed_put_url


# router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

# @router.get("/signed-url")
# def get_signed_url(
#     filename: str = Query(..., min_length=1),
#     contentType: str = Query("application/octet-stream"),
# ):
#     return signed_put_url(filename, contentType)
