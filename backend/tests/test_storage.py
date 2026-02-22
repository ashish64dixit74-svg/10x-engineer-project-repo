import pytest
from datetime import datetime
from app.models import Prompt, Collection
from app.storage import Storage
from app.models import generate_id, get_current_time

@pytest.fixture
def storage():
    """Fixture to provide a fresh Storage instance for each test."""
    return Storage()

@pytest.fixture
def prompt_data():
    """Fixture to provide a valid prompt data."""
    return {
        "id": generate_id(),
        "title": "Valid Title",
        "content": "Valid content for a prompt.",
        "description": "A descriptive text.",
        "collection_id": None,
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    }

@pytest.fixture
def collection_data():
    """Fixture to provide valid collection data."""
    return {
        "id": generate_id(),
        "name": "Valid Collection",
        "description": "A valid description for a collection.",
        "created_at": get_current_time()
    }

def test_create_and_get_prompt(storage, prompt_data):
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)
    retrieved_prompt = storage.get_prompt(prompt.id)
    assert retrieved_prompt == prompt

def test_get_all_prompts_empty(storage):
    assert storage.get_all_prompts() == []

def test_get_all_prompts(storage, prompt_data):
    prompt1 = Prompt(**prompt_data)
    storage.create_prompt(prompt1)

    prompt_data2 = prompt_data.copy()
    prompt_data2["id"] = generate_id()
    prompt2 = Prompt(**prompt_data2)
    storage.create_prompt(prompt2)
    result = storage.get_all_prompts()
    assert len(result) == 2
    assert sorted(p.id for p in result) == sorted([prompt1.id, prompt2.id])
   

def test_update_prompt(storage, prompt_data):
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)

    updated_data = prompt_data.copy()
    updated_data["content"] = "Updated content."
    updated_prompt = Prompt(**updated_data)

    storage.update_prompt(prompt.id, updated_prompt)
    retrieved_prompt = storage.get_prompt(prompt.id)
    assert retrieved_prompt.content == "Updated content."

def test_delete_prompt(storage, prompt_data):
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)

    assert storage.delete_prompt(prompt.id) is True
    assert storage.get_prompt(prompt.id) is None

def test_create_and_get_collection(storage, collection_data):
    collection = Collection(**collection_data)
    storage.create_collection(collection)
    retrieved_collection = storage.get_collection(collection.id)
    assert retrieved_collection == collection

def test_get_all_collections_empty(storage):
    assert storage.get_all_collections() == []

def test_get_all_collections(storage, collection_data):
    collection1 = Collection(**collection_data)
    storage.create_collection(collection1)

    collection_data2 = collection_data.copy()
    collection_data2["id"] = generate_id()
    collection2 = Collection(**collection_data2)
    storage.create_collection(collection2)
    result = storage.get_all_collections()
    assert len(result) == 2
    assert sorted(c.id for c in result) == sorted([collection1.id, collection2.id])

def test_delete_collection(storage, collection_data):
    collection = Collection(**collection_data)
    storage.create_collection(collection)

    assert storage.delete_collection(collection.id) is True
    assert storage.get_collection(collection.id) is None

def test_get_prompts_by_collection(storage, prompt_data, collection_data):
    collection = Collection(**collection_data)
    storage.create_collection(collection)

    prompt_data["collection_id"] = collection.id
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)

    prompts = storage.get_prompts_by_collection(collection.id)
    assert prompts == [prompt]

def test_clear_storage(storage, prompt_data, collection_data):
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)

    collection = Collection(**collection_data)
    storage.create_collection(collection)

    storage.clear()
    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []

def test_edge_cases_overwriting_id(storage, prompt_data):
    prompt_id = generate_id()
    prompt_data["id"] = prompt_id
    prompt = Prompt(**prompt_data)
    storage.create_prompt(prompt)

    new_prompt_data = prompt_data.copy()
    new_prompt_data["content"] = "Different content."
    new_prompt = Prompt(**new_prompt_data)

    storage.create_prompt(new_prompt)
    retrieved_prompt = storage.get_prompt(prompt_id)
    assert retrieved_prompt == new_prompt

def test_edge_cases_non_existing_ids(storage):
    assert storage.get_prompt("non_existing_id") is None
    assert storage.delete_prompt("non_existing_id") is False
    assert storage.get_collection("non_existing_id") is None
    assert storage.delete_collection("non_existing_id") is False