from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship


class Workspace(SQLModel, table=True):
    __tablename__ = "workspace"

    id: str = Field(primary_key=True, index=True, max_length=64)
    name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )

    documents: list["Document"] = Relationship(back_populates="workspace")


class Document(SQLModel, table=True):
    __tablename__ = "document"

    id: str = Field(primary_key=True, index=True, max_length=64)
    workspace_id: str = Field(foreign_key="workspace.id", index=True)
    filename: str = Field(max_length=512)
    content_type: str | None = Field(default=None, max_length=128)
    num_pages: int | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )

    workspace: Workspace | None = Relationship(back_populates="documents")
    chunks: list["DocumentChunk"] = Relationship(back_populates="document")


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunk"

    id: int | None = Field(default=None, primary_key=True)
    document_id: str = Field(
        foreign_key="document.id", index=True, nullable=False
    )
    workspace_id: str = Field(
        foreign_key="workspace.id", index=True, nullable=False
    )
    chunk_index: int = Field(nullable=False)
    page_number: int | None = Field(default=None)
    text: str = Field(nullable=False)

    document: Document | None = Relationship(back_populates="chunks")
    vectors: list["FaissVector"] = Relationship(back_populates="chunk")


class FaissVector(SQLModel, table=True):
    __tablename__ = "faiss_vector"

    id: int | None = Field(default=None, primary_key=True)
    workspace_id: str = Field(
        foreign_key="workspace.id", index=True, nullable=False
    )
    chunk_id: int = Field(
        foreign_key="document_chunk.id", nullable=False
    )
    vector_id: int = Field(index=True, nullable=False)

    chunk: DocumentChunk | None = Relationship(back_populates="vectors")

