"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4

def generate_id() -> str:
    """
    Generate a unique identifier as a string.

    Returns:
        str: A unique identifier using UUID4.

    Example:
        >>> generate_id()
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """
    Generate current Date time.

    Returns:
        datetime: Current date.

    Example:
        >>> get_current_time()
        '19:10:00'
    """
    return datetime.utcnow()



# ============== Prompt Models ==============
class PromptBase(BaseModel):
    """Represents a basic prompt model.

    Attributes:
        title (str): The title of the prompt. Must be between 1 and 200 characters.
        content (str): The content of the prompt. Must be at least 1 character long.
        description (Optional[str]): An optional description for the prompt. Maximum 500 characters.
        collection_id (Optional[str]): The ID of the collection this prompt belongs to, if applicable.

    Example:
        example_prompt = PromptBase(
            title="Sample Title",
            content="Sample content for the prompt.",
            description="An optional description for clarity.",
            collection_id="12345"
        )
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    pass



class PromptUpdate(PromptBase):
    pass


class Prompt(PromptBase):
    """Represents a fully detailed prompt model including metadata.

    Attributes:
        id (str): A unique identifier for the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp when the prompt was last updated.

    Example:
        example_prompt = Prompt(
            id='f47ac10b-58cc-4372-a567-0e02b2c3d479',
            created_at=datetime(2023, 10, 20, 12, 0, 0),
            updated_at=datetime(2023, 10, 21, 12, 0, 0),
            title='Sample Title',
            content='Sample content for the prompt.'
        )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Represents a basic collection model.

    Attributes:
        name (str): The name of the collection. Must be between 1 and 100 characters.
        description (Optional[str]): An optional description for the collection. Maximum 500 characters.

    Example:
        example_collection = CollectionBase(
            name="Sample Collection",
            description="An optional description for the collection."
        )
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

# Note: Existing comments have been retained as they do not conflict with the new docstring.


class CollectionCreate(CollectionBase):
    pass


# ============== Collection Models ==============
class CollectionBase(BaseModel):
    """Represents a basic collection model.

    Attributes:
        name (str): The name of the collection. Must be between 1 and 100 characters.
        description (Optional[str]): An optional description for the collection. Maximum 500 characters.

    Example:
        example_collection = CollectionBase(
            name="Sample Collection",
            description="An optional description for the collection."
        )
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    """Represents a fully detailed collection model.

    Attributes:
        id (str): A unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.

    Example:
        example_collection = Collection(
            id='f47ac10b-58cc-4372-a567-0e02b2c3d479',
            created_at=datetime(2023, 10, 20, 12, 0, 0),
            name='Sample Collection',
            description='An optional description for the collection.'
        )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """
    Represents a list of prompts along with a total count.

    Attributes:
        prompts (List[Prompt]): A list of prompt objects.
        total (int): The total number of prompts.

    Example:
        >>> prompt_list = PromptList(
        ...     prompts=[Prompt(id='1', created_at=datetime.now(), updated_at=datetime.now(), title='Example', content='Example content')],
        ...     total=1
        ... )
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """
    Represents a list of collections along with a total count.

    Attributes:
        collections (List[Collection]): A list of collection objects.
        total (int): The total number of collections.

    Example:
        >>> collection_list = CollectionList(
        ...     collections=[Collection(id='1', created_at=datetime.now(), name='Sample Collection')],
        ...     total=1
        ... )
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """
    Represents the health status of the service.

    Attributes:
        status (str): Current status of the service, typically 'healthy' or 'unhealthy'.
        version (str): The current version of the service.

    Example:
        >>> health_response = HealthResponse(
        ...     status='healthy',
        ...     version='1.0.0'
        ... )
    """
    status: str
    version: str

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """
    Represents a list of prompts along with a total count.

    Attributes:
        prompts (List[Prompt]): A list of prompt objects.
        total (int): The total number of prompts.

    Example:
        >>> prompt_list = PromptList(
        ...     prompts=[Prompt(id='1', created_at=datetime.now(), updated_at=datetime.now(), title='Example', content='Example content')],
        ...     total=1
        ... )
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """
    Represents a list of collections along with a total count.

    Attributes:
        collections (List[Collection]): A list of collection objects.
        total (int): The total number of collections.

    Example:
        >>> collection_list = CollectionList(
        ...     collections=[Collection(id='1', created_at=datetime.now(), name='Sample Collection')],
        ...     total=1
        ... )
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """
    Represents the health status of the service.

    Attributes:
        status (str): Current status of the service, typically 'healthy' or 'unhealthy'.
        version (str): The current version of the service.

    Example:
        >>> health_response = HealthResponse(
        ...     status='healthy',
        ...     version='1.0.0'
        ... )
    """
    status: str
    version: str
