"""In-memory storage for PromptLab."""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, get_current_time


class Storage:
    """Manages in-memory storage of prompts and collections."""

    def __init__(self) -> None:
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}

    # ============== Internal Helpers ==============

    @staticmethod
    def _delete_item(store: Dict[str, object], item_id: str) -> bool:
        """Delete item from a dictionary store safely."""
        if item_id in store:
            del store[item_id]
            return True
        return False

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        return self._delete_item(self._prompts, prompt_id)

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [
            prompt
            for prompt in self._prompts.values()
            if prompt.collection_id == collection_id
        ]

    def add_tags_to_prompt(self, prompt_id: str, tags: List[str]) -> Prompt:
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError("Prompt not found")

        normalized_tags = {tag.lower() for tag in tags}
        existing_tags = {tag.lower() for tag in prompt.tags}

        prompt.tags = list(existing_tags.union(normalized_tags))
        prompt.updated_at = get_current_time()

        self._prompts[prompt_id] = prompt
        return prompt

    def get_prompts_by_tag(self, tag: str) -> List[Prompt]:
        normalized_tag = tag.lower()
        return [
            prompt
            for prompt in self._prompts.values()
            if normalized_tag in {t.lower() for t in prompt.tags}
        ]

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        return self._delete_item(self._collections, collection_id)

    # ============== Utility ==============

    def clear(self) -> None:
        """Clear all stored prompts and collections."""
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()