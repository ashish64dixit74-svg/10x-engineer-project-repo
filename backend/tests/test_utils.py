# tests/test_utils.py

import pytest
from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
)
from app.models import generate_id, get_current_time


@pytest.fixture
def prompt_factory():
    def _create(**overrides):
        now = get_current_time()
        base = {
            "id": generate_id(),
            "title": "Sample Title",
            "content": "Sample content",
            "description": "Sample description",
            "collection_id": None,
            "created_at": now,
            "updated_at": now,
        }
        base.update(overrides)
        return Prompt(**base)
    return _create


# ------------------ SORT TESTS ------------------

def test_sort_prompts_by_date_normal_case(prompt_factory):
    p1 = prompt_factory(created_at=datetime(2022, 1, 1))
    p2 = prompt_factory(created_at=datetime(2023, 1, 1))

    sorted_prompts = sort_prompts_by_date([p1, p2])
    assert sorted_prompts[0].created_at >= sorted_prompts[1].created_at


@pytest.mark.parametrize("descending", [True, False])
def test_sort_prompts_by_date_edge_cases(prompt_factory, descending):
    p1 = prompt_factory(created_at=datetime(2022, 1, 1))
    p2 = prompt_factory(created_at=datetime(2023, 1, 1))

    sorted_prompts = sort_prompts_by_date([p1, p2], descending)
    assert len(sorted_prompts) == 2


def test_sort_prompts_by_date_empty():
    assert sort_prompts_by_date([]) == []


# ------------------ FILTER TESTS ------------------

def test_filter_prompts_by_collection(prompt_factory):
    p1 = prompt_factory(collection_id="123")
    p2 = prompt_factory(collection_id="456")

    filtered = filter_prompts_by_collection([p1, p2], "123")

    assert len(filtered) == 1
    assert filtered[0].collection_id == "123"


def test_filter_prompts_by_collection_empty():
    assert filter_prompts_by_collection([], "123") == []


# ------------------ SEARCH TESTS ------------------

def test_search_prompts(prompt_factory):
    p1 = prompt_factory(title="Test Prompt", description="Something")
    p2 = prompt_factory(title="Another", description="Example")

    results = search_prompts([p1, p2], "test")

    assert len(results) == 1
    assert "Test" in results[0].title


def test_search_prompts_edge_cases(prompt_factory):
    p1 = prompt_factory(title="Title", description=None)
    p2 = prompt_factory(title="Another", description="description")

    assert len(search_prompts([p1, p2], "")) == 2
    assert len(search_prompts([p1, p2], "nonexistent")) == 0


# ------------------ VALIDATION TESTS ------------------

def test_validate_prompt_content():
    assert validate_prompt_content("Valid content") is True
    assert validate_prompt_content("  ") is False
    assert validate_prompt_content("") is False


# ------------------ VARIABLE EXTRACTION ------------------

@pytest.mark.parametrize("input_content, expected", [
    ("{{name}}", ["name"]),
    ("{{}}", []),
    ("No variables here", []),
    ("{{var1}} and {{var2}}", ["var1", "var2"]),
    ("Hello, {{name}}! Your account {{number}} is ready.", ["name", "number"]),
])
def test_extract_variables(input_content, expected):
    assert extract_variables(input_content) == expected


def test_extract_variables_empty():
    assert extract_variables("") == []


def test_extract_variables_special_characters():
    assert extract_variables("{{var!}}") == []