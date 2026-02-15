"""Utility functions for file operations and directory traversal."""

import os
from pathlib import Path
from typing import List, Tuple, Generator


def find_files(directory: str, extensions: Tuple[str, ...]) -> List[Path]:
    """
    Find all files in a directory with specified extensions.

    Args:
        directory: Path to search for files
        extensions: Tuple of file extensions to match (e.g., ('.jpg', '.png'))

    Returns:
        Sorted list of Path objects for matching files
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory does not exist: {directory}")

    file_paths = []
    for filename in os.listdir(directory):
        path = Path(directory) / filename
        if path.is_file() and path.suffix.lower() in extensions:
            file_paths.append(path)

    return sorted(file_paths)


def read_prompt_file(prompt_path: Path) -> str:
    """
    Read and return the content of a prompt file.

    Args:
        prompt_path: Path to the prompt file

    Returns:
        Content of the prompt file as a string

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, 'r', encoding='utf-8') as file:
        return file.read()


def validate_directory(directory: str) -> bool:
    """
    Validate that a directory exists and is accessible.

    Args:
        directory: Path to validate

    Returns:
        True if directory exists and is accessible
    """
    return os.path.isdir(directory)


def safe_join(*paths: str) -> Path:
    """
    Safely join multiple path components.

    Args:
        *paths: Path components to join

    Returns:
        Path object representing the joined path
    """
    base_dir = Path(__file__).parent.parent
    result = base_dir
    for path in paths:
        result = result / path
    return result