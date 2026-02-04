from __future__ import annotations

import os
import uuid
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    UploadFile,
)
from fastapi import status
from sqlmodel import Session

from app.core.config import get_settings
from app.db.session import get_session
from app.db.models import Document, DocumentChunk, Workspace


router = APIRouter(tags=["documents"])
settings = get_settings()


def _require_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> str:
    # NOTE: This is kept simple; in a full implementation we'd use a shared dependency module.
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key


@router.post(
    "/v1/documents/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    x_workspace_id: str = Header(..., alias="X-Workspace-Id"),
    _: str = Depends(_require_api_key),
    session: Session = Depends(get_session),
) -> dict:
    # Simple workspace id sanitation
    if "/" in x_workspace_id or "\\" in x_workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid workspace id",
        )
    workspace_id = x_workspace_id

    # Ensure workspace exists
    workspace = session.get(Workspace, workspace_id)
    if workspace is None:
        workspace = Workspace(id=workspace_id)
        session.add(workspace)
        session.commit()

    # Store original file
    doc_id = uuid.uuid4().hex
    ext = os.path.splitext(file.filename or "")[1].lower() or ".bin"
    storage_dir = os.path.join(
        "data", "storage", workspace_id, doc_id
    )
    os.makedirs(storage_dir, exist_ok=True)
    stored_path = os.path.join(storage_dir, f"original{ext}")

    with open(stored_path, "wb") as out_f:
        content = await file.read()
        out_f.write(content)

    # Placeholder: in the next step, real extraction + chunking + FAISS will be wired here.
    document = Document(
        id=doc_id,
        workspace_id=workspace_id,
        filename=file.filename or f"{doc_id}{ext}",
        content_type=file.content_type,
        num_pages=None,
    )
    session.add(document)
    session.commit()

    # For now, we do not create chunks or vectors in this initial skeleton.
    return {
        "document_id": doc_id,
        "workspace_id": workspace_id,
        "num_pages": 0,
        "num_chunks": 0,
    }

