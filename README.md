# Eastlake Science Fair - Image Recognition Project

A Python-based AI-assisted science fair project focusing on facial expression recognition using Ollama service on NixOS.

## Project Overview

This project demonstrates facial expression recognition capabilities using various AI models (llama4:scout, qwen-vl:8b, and qwen3-vl-8b-MAX) via the Ollama API. The system processes images and multiple choice queries to analyze emotions and facial expressions.

## Environment Setup

This project uses Nix for environment management. The environment includes:
- Python 3.14 with numpy and ollama packages
- Code quality tools: black (formatter), mypy (type checker)
- Required system libraries: libffi, openssl

### Supported Ollama Vision Models
- **llama4:scout**: Multi-modal model for image analysis and facial expression recognition
- **qwen-vl:8b**: Vision-language model for comprehensive image understanding
- **qwen3-vl-8b-MAX:latest**: Enhanced vision-language model with advanced processing

### Quick Start

```bash
# Activate Nix environment
nix-shell

# Run image processing
python main.py

# Run multiple choice queries
python multipleChoice.py

# Check model availability
ollama list

# Pull vision models
ollama pull llama4:scout
ollama pull qwen-vl:8b
ollama pull qwen3-vl-8b-MAX:latest

# Format code
black .

# Type check
mypy src/

# Run tests
pytest
```

## Project Structure

```
src/
 ├── config.py          # Global configuration for Ollama and image paths
 ├── utils.py           # Utility functions for file operations and directory traversal
 ├── main.py            # Basic image processing with qwen3 model (http://10.0.26.32:11434)
 ├── main2.py           # Image processing with llama4 model (comparison)
 ├── multipleChoice.py  # Multiple choice queries with qwen3 model
 ├── multipleChoice2.py # Multiple choice queries with llama4 model
 ├── AGENTS.md          # Agent development guidelines
 └── README.md          # This file
 ```

### Vision Models
- **llama4:scout**: Multi-modal model for image analysis and facial expression recognition
- **qwen-vl:8b**: Vision-language model for comprehensive image understanding
- **qwen3-vl-8b-MAX:latest**: Enhanced vision-language model with advanced processing