"""Utility functions for PromptLab"""

import re
from typing import List

from app.models import Prompt


def sort_prompts_by_date(
    prompts: List[Prompt], descending: bool = True
) -> List[Prompt]:
    """Sort prompts by creation date."""
    return sorted(
        prompts,
        key=lambda prompt: prompt.created_at,
        reverse=descending,
    )


def filter_prompts_by_collection(
    prompts: List[Prompt], collection_id: str
) -> List[Prompt]:
    """Filter prompts by collection ID."""
    return [
        prompt
        for prompt in prompts
        if prompt.collection_id == collection_id
    ]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description."""
    query_lower = query.lower()

    return [
        prompt
        for prompt in prompts
        if query_lower in prompt.title.lower()
        or (
            prompt.description
            and query_lower in prompt.description.lower()
        )
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate prompt content.

    Rules:
    - Must not be empty
    - Must not be whitespace
    - Must be at least 10 characters
    """
    stripped = content.strip() if content else ""
    return len(stripped) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables in {{variable}} format."""
    pattern = r"\{\{(\w+)\}\}"
    return re.findall(pattern, content)


def filter_prompts_by_tags(
    prompts: List[Prompt], tags: List[str]
) -> List[Prompt]:
    """Filter prompts that contain ALL specified tags (case-insensitive)."""
    normalized_tags = {tag.lower() for tag in tags}

    filtered_prompts: List[Prompt] = []

    for prompt in prompts:
        prompt_tags = {tag.lower() for tag in prompt.tags}
        if normalized_tags.issubset(prompt_tags):
            filtered_prompts.append(prompt)

    return filtered_prompts