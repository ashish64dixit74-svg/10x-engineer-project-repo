"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
        Args:
            prompts (List[Prompt]): The list of prompts to sort.
            descending (bool): Sort order flag. True for descending, False for ascending.

        Returns:
            List[Prompt]: The sorted list of prompts.

        Raises:
            ValueError: If prompts is not a list of Prompt objects.

        Example:
            >>> prompts = [Prompt(id=1, created_at="2023-10-01"), Prompt(id=2, created_at="2023-11-01")]
            >>> sort_prompts_by_date(prompts)
            [Prompt(id=2, created_at="2023-11-01"), Prompt(id=1, created_at="2023-10-01")]
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        collection_id (str): The collection identifier to filter by.

    Returns:
        List[Prompt]: A list of prompts belonging to the specified collection.

    Example:
        >>> prompts = [Prompt(id=1, collection_id="123"), Prompt(id=2, collection_id="456")]
        >>> filter_prompts_by_collection(prompts, "123")
        [Prompt(id=1, collection_id="123")]
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts based on a query string.

    Args:
        prompts (List[Prompt]): The list of prompts to search within.
        query (str): The search query string.

    Returns:
        List[Prompt]: A list of prompts that match the search query.

    Example:
        >>> prompts = [Prompt(title="Hello World"), Prompt(title="Goodbye")]  
        >>> search_prompts(prompts, "hello")
        [Prompt(title="Hello World")]
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters
    
    Args:
        content (str): The prompt content string to validate.

    Returns:
        bool: True if the content is valid, False otherwise.

    Example:
        >>> validate_prompt_content("   ")
        False
        >>> validate_prompt_content("Valid content here.")
        True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
        Variables are in the format {{variable_name}}.

        Args:
            content (str): The prompt content string to extract variables from.

        Returns:
            List[str]: A list of variable names found in the content.

        Example:
            >>> extract_variables("Hello {{name}}, today is {{day}}.")
            ['name', 'day']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
