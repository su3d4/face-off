"""Utility functions for file operations and directory traversal."""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Literal, get_args, List, Tuple, Generator
from config import ImageConfig


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

    with open(prompt_path, "r", encoding="utf-8") as file:
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


def create_log_directory(config) -> Path:
    """
    Create log directory if it doesn't exist.

    Args:
        config: Application configuration containing directory settings

    Returns:
        Path object for log directory
    """
    log_dir = Path(config.directories.log_directory)
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def create_results_directory(config) -> Path:
    """
    Create results directory if it doesn't exist.

    Args:
        config: Application configuration containing directory settings

    Returns:
        Path object for results directory
    """
    results_dir = Path(config.directories.results_directory)
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def get_unique_filename(image_path: Path, model: str, response_type: str) -> Path:
    """
    Generate a unique filename for results including model name and timestamp.

    Args:
        image_path: Path to the input image file
        model: Name of the model used
        response_type: Type of response ("free" for main.py/main2.py, "choice" for multipleChoice files)

    Returns:
        Unique Path object for result file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = create_results_directory(ImageConfig())

    if response_type == "free":
        question_part = image_path.stem
        result_file = results_dir / f"{question_part}_{model}_{timestamp}_free.txt"
    else:
        question_part = image_path.stem
        result_file = results_dir / f"{question_part}_{model}_{timestamp}_choice.txt"

    return result_file


def write_log_file(config, messages: list) -> None:
    """
    Write messages to a log file.

    Args:
        config: Application configuration containing directory settings
        messages: List of messages to write to log file
    """
    log_dir = create_log_directory(config)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"execution_{timestamp}.log"

    with open(log_file, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(f"{message}\n")

    logging.info(f"Log file written: {log_file}")


def write_result_file(
    image_path: Path, response: str, model: str, prompt: str
) -> None:
    """
    Write result to results directory with unique filename.

    Args:
        image_path: Path to the input image file
        response: Model response content
        model: Name of the model used
        prompt: Prompt used for processing
    """
    result_file = get_unique_filename(image_path, model, "free")

    with open(result_file, "w", encoding="utf-8") as file:
        file.write(f"# Image Analysis Results\n")
        file.write(f"Image: {image_path}\n")
        file.write(f"Model: {model}\n")
        file.write(f"Prompt: {prompt}\n")
        file.write(f"\n--- Response ---\n")
        file.write(f"{response}\n")
        file.write(f"\n{'='*60}\n")

    logging.info(f"Result file written: {result_file}")


def write_multiple_choice_result(
    prompt_file: Path, response: str, model: str
) -> None:
    """
    Write multiple choice result to results directory with unique filename.

    Args:
        prompt_file: Path to the prompt file used
        response: Model response content
        model: Name of the model used
    """
    result_file = get_unique_filename(prompt_file, model, "choice")

    with open(result_file, "w", encoding="utf-8") as file:
        file.write(f"# Multiple Choice Analysis Results\n")
        file.write(f"Prompt File: {prompt_file}\n")
        file.write(f"Model: {model}\n")
        file.write(f"\n--- Response ---\n")
        file.write(f"{response}\n")
        file.write(f"\n{'='*60}\n")

    logging.info(f"Multiple choice result file written: {result_file}")
