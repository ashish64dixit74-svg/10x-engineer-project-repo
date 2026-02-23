"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__
from app.utils import filter_prompts_by_tags


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Checks the health status of the application.

    This endpoint returns the health status and version of the application.

    Args:
        None

    Returns:
        HealthResponse: An object containing the status and version of the application.

    Raises:
        HTTPException: If any error occurs during the process.

    Example:
        >>> response = client.get("/health")
        >>> assert response.status_code == 200
        >>> assert response.json() == {"status": "healthy", "version": "1.0.0"}
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============
# Implement GET /tags/{tag}/prompts
@app.get("/tags/{tag}/prompts", response_model=List[Prompt])
def get_prompts_by_tag(tag: str):
    """
    Fetches prompts associated with a specific tag.

    Args:
        tag (str): The tag to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts with the specified tag.

    Raises:
        HTTPException: If no prompts are found for the given tag, a 404 error is raised.
    """

    prompts = storage.get_prompts_by_tag(tag)

    if not prompts:
        raise HTTPException(status_code=404, detail="No prompts found for tag")

    return prompts

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None
):
    """Retrieve a list of prompts with optional filtering and searching.

    Args:
        collection_id (Optional[str]): An optional collection ID to filter prompts.
        search (Optional[str]): An optional search query to filter prompts based on their content.

    Returns:
        PromptList: A list of prompts that match the criteria, with metadata.

    Raises:
        Exception: If an error occurs while retrieving prompts.

    Example:
        >>> list_prompts(collection_id="123", search="example")
        PromptList(prompts=[Prompt(id="1", text="Example text.")], total=1)
    """

    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        prompts = filter_prompts_by_tags(prompts, tag_list)
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a prompt by its identifier.

    Args:
        prompt_id (str): The unique identifier of the prompt to be retrieved.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If no prompt is found with the provided identifier,
                       a 404 status code is returned.

    Example:
        >>> get_prompt("example_id")
        <Prompt object>

        >>> get_prompt("non_existent_id")
        HTTPException(status_code=404, detail="Prompt not found")
    
    """
    prompt = storage.get_prompt(prompt_id)

    # Return 404 if prompt is None
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt

# Implemented POST /prompts/{prompt_id}/tags
@app.post("/prompts/{prompt_id}/tags", response_model=Prompt)
def add_tags(prompt_id: str, payload: dict):
    """
    Adds tags to an existing prompt.

    Args:
        prompt_id (str): The unique identifier of the prompt.
        payload (dict): A dictionary containing the tags to be added.

    Returns:
        Prompt: The updated prompt object with the newly added tags.

    Raises:
        HTTPException: If the tags format is invalid (not a list).
        HTTPException: If the specified prompt is not found in storage.
    """

    tags = payload.get("tags")

    if not isinstance(tags, list):
        raise HTTPException(status_code=400, detail="Invalid tags format")

    try:
        updated = storage.add_tags_to_prompt(prompt_id, tags)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return updated

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    This endpoint receives prompt data, validates the existence of the specified
    collection (if any), and creates a new prompt in storage.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt.
            This includes optional collection identifier.

    Returns:
        Prompt: The newly created prompt object.

    Raises:
        HTTPException: If the specified collection does not exist.

    Example:
        >>> create_prompt(prompt_data)
        Prompt(id=123, title='Sample Prompt', collection_id=1)
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    data = prompt_data.model_dump()

    # Ensure tags is always a list
    if data.get("tags") is None:
        data["tags"] = []

    prompt = Prompt(**data)
    return storage.create_prompt(prompt)
  #  prompt = Prompt(**prompt_data.model_dump())
  #  return storage.create_prompt(prompt)

@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Update an existing prompt with new data.

    Args:
        prompt_id (str): The identifier of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found with status code 404.
        HTTPException: If the collection_id is provided and not found with status code 400.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        tags=prompt_data.tags if prompt_data.tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)



# Implemented Prompt Endpoint for partial updates.
@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Partially updates an existing prompt with new data provided.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): An object containing the fields to update in the prompt.

    Raises:
        HTTPException: If the prompt does not exist (404) or if the specified collection is not found (400).

    Returns:
        Prompt: The updated prompt object.
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        tags=prompt_data.tags if prompt_data.tags is not None else existing.tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)

@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt with the specified ID.

    Args:
        prompt_id (str): The unique identifier of the prompt to be deleted.

    Returns:
        None: If the prompt is successfully deleted.

    Raises:
        HTTPException: If the prompt with the given ID is not found, an
            HTTPException with a 404 status code is raised.

    Example:
        >>> delete_prompt(prompt_id="12345")
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None

# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Retrieve a list of all collections.

    This endpoint retrieves all collections available in the storage and returns
    them in a structured format.

    Args:
        None

    Returns:
        CollectionList: An object containing a list of collections and the total
        number of collections.

    Raises:
        HTTPException: If there is an error accessing the storage.

    Example:
        >>> response = client.get("/collections")
        >>> collections = response.json()
        >>> print(collections)
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieves a collection by its ID.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found, it raises a 404 error with the message "Collection not found".

    Example:
        >>> get_collection("12345")
        Collection(id='12345', name='Sample Collection', ...)

    """
    # Retrieve the collection using the provided collection_id.
    collection = storage.get_collection(collection_id)
    if not collection:
        # If the collection is not found, raise a 404 error.
        raise HTTPException(status_code=404, detail="Collection not found")
    # Return the fetched collection.
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Creates a new collection in the storage.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection, encapsulated in a CollectionCreate model.

    Returns:
        Collection: The newly created collection object.

    Raises:
        ValidationError: If the collection_data does not match the expected schema.

    Example:
        >>> collection_data = CollectionCreate(name="New Collection")
        >>> create_collection(collection_data)
        Collection(id=123, name="New Collection")
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Deletes a collection and all its associated prompts.

    This endpoint deletes a specified collection and all prompts associated with it.
    If the collection does not exist, an HTTP 404 error is raised.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Returns:
        None

    Raises:
        HTTPException: If the collection with the given collection_id is not found.

    Example:
        >>> delete_collection('123e4567-e89b-12d3-a456-426614174000')
    """

   # Retrieve all prompts associated with the collection_id
    prompts = storage.get_prompts_by_collection(collection_id)
    # Delete each prompt related to this collection
    for prompt in prompts:
        storage.delete_prompt(prompt.id)
    
    # Delete the collection
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    return None


