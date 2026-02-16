"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
 """
    Storage class for managing in-memory representations of prompts and collections.
    
    This class allows for CRUD operations (Create, Read, Update, Delete) on
    prompt and collection objects, which are stored in separate dictionaries.
    Persistence is not provided. Data is lost when the application stops.
    
    Attributes:
        _prompts (Dict[str, Prompt]): A dictionary storing prompts with their IDs.
        _collections (Dict[str, Collection]): A dictionary storing collections with their IDs.
    """
def __init__(self):
 self._prompts: Dict[str, Prompt] = {}
 self._collections: Dict[str, Collection] = {}
    
# ============== Prompt Operations ==============

def create_prompt(self, prompt: Prompt) -> Prompt:
    """
    Adds a new prompt to the storage.

    Args:
        prompt (Prompt): The prompt to be added.

    Returns:
        Prompt: The prompt instance added to the storage.
    """
    self._prompts[prompt.id] = prompt
    return prompt

def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
    """
    Retrieves a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Optional[Prompt]: The prompt with the specified ID or None if not found.
    """
    return self._prompts.get(prompt_id)

def get_all_prompts(self) -> List[Prompt]:
    """
    Retrieves all prompts from storage.

    Returns:
        List[Prompt]: A list of all stored prompts.
    """
    return list(self._prompts.values())

def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
    """
        Updates an existing prompt with new data.

        Args:
            prompt_id (str): The ID of the prompt to be updated.
            prompt (Prompt): The prompt data to update.

        Returns:
            Optional[Prompt]: The updated prompt, or None if the ID does not exist.
        """
    if prompt_id not in self._prompts:
        return None
    self._prompts[prompt_id] = prompt
    return prompt

def delete_prompt(self, prompt_id: str) -> bool:
    """
        Deletes a prompt from storage.
        Args:
            prompt_id (str): The ID of the prompt to be deleted.

        Returns:
            bool: True if the prompt was deleted, False if it did not exist.
        """
    if prompt_id in self._prompts:
        del self._prompts[prompt_id]
        return True
    return False

# ============== Collection Operations ==============

def create_collection(self, collection: Collection) -> Collection:
    """
        Adds a new collection to the storage.

        Args:
            collection (Collection): The collection to be added.

        Returns:
            Collection: The collection instance added to the storage.
    """
    self._collections[collection.id] = collection
    return collection

def get_collection(self, collection_id: str) -> Optional[Collection]:
    """
        Retrieves a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection with the specified ID or None if not found.
    """
    return self._collections.get(collection_id)

def get_all_collections(self) -> List[Collection]:
    """
        Retrieves all collections from storage.

        Returns:
            List[Collection]: A list of all stored collections.
    """
    return list(self._collections.values())

def delete_collection(self, collection_id: str) -> bool:
    """
        Deletes a collection from storage.

        Args:
            collection_id (str): The ID of the collection to be deleted.

        Returns:
            bool: True if the collection was deleted, False if it did not exist.
    """
    if collection_id in self._collections:
        del self._collections[collection_id]
        return True
    return False

def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
    """
        Retrieves prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts associated with the given collection ID.
    """
    return [p for p in self._prompts.values() if p.collection_id == collection_id]

# ============== Utility ==============

def clear(self):
    """
        Clears all stored prompts and collections from memory.

        This operation will delete all data and cannot be undone. Used mostly for resetting storage during tests or application restart.
    """
    self._prompts.clear()
    self._collections.clear()


# Global storage instance
storage = Storage()
