"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


def generate_id() -> str:
    """Generate a unique identifier string."""
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC time."""
    return datetime.utcnow()


# ============== Prompt Models ==============


class PromptBase(BaseModel):
    """Base model for a prompt."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a prompt (tags optional)."""

    tags: Optional[List[str]] = None


class PromptUpdate(PromptBase):
    """Model for updating a prompt (tags optional)."""

    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    """Complete prompt model including metadata and tags."""

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# ============== Collection Models ==============


class CollectionBase(BaseModel):
    """Base model for a collection."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a collection."""
    pass


class Collection(CollectionBase):
    """Complete collection model including metadata."""

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)


# ============== Response Models ==============


class PromptList(BaseModel):
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    status: str
    version: str