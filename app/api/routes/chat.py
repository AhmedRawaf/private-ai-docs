from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.core.config import get_settings
from app.db.session import get_session


router = APIRouter(tags=["chat"])
settings = get_settings()


class ChatRequest(BaseModel):
    workspace_id: Optional[str] = Field(
        default=None,
        description="Workspace ID.",
    )
    session_id: Optional[str] = None
    message: str
    top_k: int = 5
    bilingual: bool = False


class Citation(BaseModel):
    document_id: str
    filename: str
    page_number: Optional[int]
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]


def _require_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return None


@router.post("/v1/chat", response_model=ChatResponse)
def chat_with_documents(
    payload: ChatRequest,
    x_api_key: str = Header(..., alias="X-API-Key"),
    x_workspace_id: str = Header(..., alias="X-Workspace-Id"),
    session: Session = Depends(get_session),
) -> ChatResponse:
    _require_api_key(x_api_key)

    workspace_id = payload.workspace_id or x_workspace_id
    if workspace_id != x_workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="workspace_id in body must match X-Workspace-Id header if provided.",
        )

    if not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    # Placeholder answer until RAG pipeline is wired in.
    return ChatResponse(
        answer="RAG pipeline is not yet initialized in this skeleton.",
        citations=[],
    )

