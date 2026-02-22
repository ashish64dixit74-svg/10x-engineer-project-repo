"""
Tests for models.py

Covers:
- Model validation
- Required fields
- Field constraints
- Default values
- Serialization
- Utility functions
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    Collection,
    CollectionCreate,
    generate_id,
    get_current_time
)


# ============================================================
# Utility Function Tests
# ============================================================

def test_generate_id_returns_string():
    uid = generate_id()
    assert isinstance(uid, str)
    assert len(uid) > 0


def test_get_current_time_returns_datetime():
    now = get_current_time()
    assert isinstance(now, datetime)


# ============================================================
# Prompt Model Validation
# ============================================================

class TestPromptValidation:

    def test_prompt_create_valid(self):
        prompt = PromptCreate(
            title="Valid Title",
            content="Valid content"
        )
        assert prompt.title == "Valid Title"
        assert prompt.content == "Valid content"

    def test_prompt_missing_title(self):
        with pytest.raises(ValidationError):
            PromptCreate(content="Valid content")

    def test_prompt_missing_content(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="Valid Title")

    def test_prompt_title_min_length(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="Valid content")

    def test_prompt_title_max_length(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="A" * 201, content="Valid content")

    def test_prompt_content_min_length(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="Valid", content="")

    def test_prompt_description_max_length(self):
        with pytest.raises(ValidationError):
            PromptCreate(
                title="Valid",
                content="Valid content",
                description="A" * 501
            )


# ============================================================
# Prompt Default Values
# ============================================================

class TestPromptDefaults:

    def test_prompt_auto_generates_fields(self):
        prompt = Prompt(
            title="Valid Title",
            content="Valid content"
        )

        assert isinstance(prompt.id, str)
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)


# ============================================================
# Prompt Serialization
# ============================================================

class TestPromptSerialization:

    def test_prompt_model_dump(self):
        prompt = Prompt(
            title="Serialize Test",
            content="Serialize content"
        )

        data = prompt.model_dump()

        assert data["title"] == "Serialize Test"
        assert data["content"] == "Serialize content"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data


# ============================================================
# PromptUpdate Validation
# ============================================================

class TestPromptUpdate:

    def test_prompt_update_valid(self):
        update = PromptUpdate(
            title="Updated",
            content="Updated content"
        )
        assert update.title == "Updated"

    def test_prompt_update_requires_fields(self):
        with pytest.raises(ValidationError):
            PromptUpdate(title="Only title")


# ============================================================
# Collection Model Validation
# ============================================================

class TestCollectionValidation:

    def test_collection_create_valid(self):
        collection = CollectionCreate(name="Valid Collection")
        assert collection.name == "Valid Collection"

    def test_collection_name_required(self):
        with pytest.raises(ValidationError):
            CollectionCreate()

    def test_collection_name_min_length(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="")

    def test_collection_name_max_length(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="A" * 101)

    def test_collection_description_max_length(self):
        with pytest.raises(ValidationError):
            CollectionCreate(
                name="Valid",
                description="A" * 501
            )


# ============================================================
# Collection Default Values
# ============================================================

class TestCollectionDefaults:

    def test_collection_auto_generates_fields(self):
        collection = Collection(name="My Collection")

        assert isinstance(collection.id, str)
        assert isinstance(collection.created_at, datetime)


# ============================================================
# Collection Serialization
# ============================================================

class TestCollectionSerialization:

    def test_collection_model_dump(self):
        collection = Collection(name="Serialize Collection")

        data = collection.model_dump()

        assert data["name"] == "Serialize Collection"
        assert "id" in data
        assert "created_at" in data