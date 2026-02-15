"""Global configuration module for Ollama-based image recognition tasks."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class OllamaConfig:
    """Configuration for Ollama API interactions."""
    host: str = os.getenv('OLLAMA_HOST', 'http://10.0.26.32:11434')
    model_qwen3_vl: str = 'qwen3-vl-8b-MAX:latest'
    model_llama4_scout: str = 'llama4:scout'


@dataclass
class ImageConfig:
    """Configuration for image processing."""
    image_directory: str = os.getenv('IMAGE_PATH', '../Q2')
    prompt_directory: str = os.getenv('PROMPT_PATH', '../Q2/MC')
    image_extensions: tuple = ('.jpg', '.jpeg')
    prompt_extensions: tuple = ('.txt',)


@dataclass
class AppConfig:
    """Main application configuration."""
    ollama: OllamaConfig
    image: ImageConfig


def create_app_config() -> AppConfig:
    """Create and return application configuration."""
    return AppConfig(
        ollama=OllamaConfig(),
        image=ImageConfig()
    )


# Global configuration instance
config = create_app_config()