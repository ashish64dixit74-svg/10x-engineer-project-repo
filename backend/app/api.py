"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


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
    """
    Health check endpoint.

    This endpoint returns the current status and version of the service.

    Args:
        None

    Returns:
        HealthResponse: An object containing the health status and current version of the application.
            - status (str): The health status of the service (e.g., "healthy").
            - version (str): The current version of the application.

    Raises:
        HTTPException: This function currently does not raise any exceptions.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Lists prompts optionally filtered by collection ID or search query.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts by. If None, no collection filtering is applied.
        search (Optional[str]): A search query string to filter prompts. If None, no search filtering is applied.

    Returns:
        PromptList: A list of prompts with metadata, filtered and sorted.

    Raises:
        ValueError: If the sorting function encounters an unexpected error.
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """
    Retrieve a specific prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier for the prompt.

    Returns:
        Prompt: A Prompt object containing the details of the prompt.

    Raises:
        HTTPException: If no prompt is found with the given identifier, a 404 error is raised.
    """
    prompt = storage.get_prompt(prompt_id)
    
    # Return 404 if prompt is None
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return prompt

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """
    Create a new prompt entry.

    This endpoint allows for the creation of a new prompt, and optionally associates it
    with an existing collection by its ID.

    Args:
        prompt_data (PromptCreate): An object containing the data necessary to create a new prompt.
            - title (str): The title of the prompt.
            - content (str): The main content of the prompt.
            - description (Optional[str]): Detailed description of the prompt.
            - collection_id (Optional[str]): The ID of the collection to which this prompt belongs.

    Returns:
        Prompt: An object representing the newly created prompt.
            - id (str): Unique identifier for the prompt.
            - title (str): The title of the prompt.
            - content (str): The main content of the prompt.
            - description (Optional[str]): Detailed description of the prompt.
            - collection_id (Optional[str]): The ID of the collection to which the prompt is associated.

    Raises:
        HTTPException: If the collection_id is provided but does not correspond to an existing collection,
        a 400 error is raised with the message "Collection not found".
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Update an existing prompt with new data.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt, including
            optional fields such as title, content, description, and
            collection_id.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found (404) or the collection
        is not found (400).
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
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # Fixed: Updated to get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)

# Implemented Prompt Endpoint for partial updates.

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Update an existing prompt with the given `prompt_id` using the provided `prompt_data`.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The data to update the prompt with.
            Fields include:
            - title (Optional[str]): The new title for the prompt.
            - content (Optional[str]): The new content of the prompt.
            - description (Optional[str]): The new description of the prompt.
            - collection_id (Optional[str]): The ID of the collection this prompt belongs to.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt with the given `prompt_id` is not found (404).
        HTTPException: If the specified collection is not found (400).
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Create updated prompt only with fields provided
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)

@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """
    Delete a specific prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier for the prompt to be deleted.

    Returns:
        None: This endpoint returns no content upon successful deletion.

    Raises:
        HTTPException: If no prompt is found with the given identifier, a 404 error is raised.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None

# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """
    Retrieve a list of all collections.

    This endpoint provides a summary of all available collections including the total count.

    Args:
        None

    Returns:
        CollectionList: An object containing a list of collections.
            - collections (List[Collection]): A list of collection objects.
            - total (int): The total number of collections.

    Raises:
        HTTPException: This function currently does not raise any exceptions.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """
    Retrieve a collection by its ID.

    Args:
        collection_id (str): The ID of the collection to retrieve from the database.

    Returns:
        Collection: The collection object that matches the provided ID.

    Raises:
        HTTPException: If no collection is found with the given ID, an HTTP 404 error is raised.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """
    Create a new collection entry.

    This endpoint allows for the creation of a new collection using the provided data.

    Args:
        collection_data (CollectionCreate): An object containing the data necessary to create a new collection.
            - name (str): The name of the collection.
            - description (Optional[str]): An optional description of the collection.

    Returns:
        Collection: An object representing the newly created collection.
            - id (str): Unique identifier for the collection.
            - name (str): The name of the collection.
            - description (Optional[str]): A description of the collection.

    Raises:
        HTTPException: This function currently does not raise any exceptions.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Deletes a collection and all associated prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None: This endpoint returns HTTP 204 status indicating the
        collection was successfully deleted or raises an exception if not.

    Raises:
        HTTPException: If the collection does not exist, an HTTP 404 error
        is raised with the message "Collection not found".

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

