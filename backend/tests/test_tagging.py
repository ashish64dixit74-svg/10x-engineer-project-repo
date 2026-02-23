import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.storage import storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    storage.clear()


def create_prompt(title="Test", content="This is valid content."):
    response = client.post(
        "/prompts",
        json={
            "title": title,
            "content": content
        }
    )
    assert response.status_code == 201
    return response.json()


def test_add_tags_to_prompt():
    prompt = create_prompt()
    prompt_id = prompt["id"]

    response = client.post(
        f"/prompts/{prompt_id}/tags",
        json={"tags": ["ai", "ml"]}
    )

    assert response.status_code == 200
    data = response.json()

    assert "tags" in data
    assert set(data["tags"]) == {"ai", "ml"}


def test_prevent_duplicate_tags():
    prompt = create_prompt()
    prompt_id = prompt["id"]

    client.post(f"/prompts/{prompt_id}/tags", json={"tags": ["python"]})
    response = client.post(f"/prompts/{prompt_id}/tags", json={"tags": ["python"]})

    data = response.json()
    assert data["tags"].count("python") == 1


def test_get_prompts_by_tag():
    p1 = create_prompt("P1", "Some valid content here.")
    p2 = create_prompt("P2", "Another valid content here.")

    client.post(f"/prompts/{p1['id']}/tags", json={"tags": ["python"]})
    client.post(f"/prompts/{p2['id']}/tags", json={"tags": ["python"]})

    response = client.get("/tags/python/prompts")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2


def test_filter_prompts_by_multiple_tags():
    p1 = create_prompt("P1", "Content 1 valid.")
    p2 = create_prompt("P2", "Content 2 valid.")
    p3 = create_prompt("P3", "Content 3 valid.")

    client.post(f"/prompts/{p1['id']}/tags", json={"tags": ["ai", "ml"]})
    client.post(f"/prompts/{p2['id']}/tags", json={"tags": ["ml"]})
    client.post(f"/prompts/{p3['id']}/tags", json={"tags": ["ai"]})

    response = client.get("/prompts?tags=ai,ml")
    assert response.status_code == 200

    data = response.json()
    returned_ids = {prompt["id"] for prompt in data["prompts"]}

    # Only prompt with BOTH ai and ml should be returned
    assert p1["id"] in returned_ids
    assert p2["id"] not in returned_ids
    assert p3["id"] not in returned_ids