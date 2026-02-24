# Agent Development Guidelines
This document provides essential guidelines for agents working in the eastlake-science-fair repository.

## Environment Setup

### Development Environment
- Python 3.14 with numpy and ollama packages
- Code quality tools: black (formatter), mypy (type checker)
- Nix for environment management
- Required system libraries: libffi, openssl

### Supported Ollama Vision Models
- `llama4:scout`: Multi-modal model for image analysis and facial expression recognition
- `qwen-vl:8b`: Vision-language model for comprehensive image understanding
- `qwen3-vl-8b-MAX:latest`: Enhanced vision-language model with advanced processing

## Code Style Guidelines

### Build/Lint/Test Commands
```bash
# Activate Nix environment
nix-shell

# Run all tests
pytest

# Run a single test
pytest -k test_name

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=.

# Format code
black .

# Type check
mypy .
```

### Import Organization
1. Standard library imports first (alphabetically)
2. Third-party imports second (grouped by package)
3. Local imports last
4. Separate groups with blank lines
5. Use `from config import ImageConfig`, `from utils import`, etc.

### Formatting and Types
- Use 4 spaces for indentation (no tabs)
- Follow PEP 8 standard
- Use black for automatic formatting (max 88 characters line length)
- Always use type hints for function signatures
- Use snake_case for functions/variables, CamelCase for classes
- Use `Optional[Type]` or `Type | None` for optional parameters
- Use `Union[TypeA, TypeB]` for union types

### Naming Conventions
- `snake_case` for functions, variables, constants: `my_function()`, `CONSTANT_NAME`
- `CamelCase` for classes: `class ClassName:`
- `lowercase_with_underscores` for module names
- `lowercase_with_underscores` for file names (e.g., `utils.py`, `main.py`)
- Use descriptive names, avoid single-letter variables unless in loops

### Error Handling
- Use context managers with `with` statements for file operations
- Catch specific exceptions, not bare `except`
- Use logging instead of print for errors
- Validate file existence and types before operations
- Handle Ollama API connection errors gracefully
- Check `stream.response` attribute for text output

### Code Organization
- Separate concerns: group related functions together
- Limit function length to 50 lines or less
- Use classes for state when needed
- Minimize global variables, prefer local variables
- Write tests first for new features

### Testing Guidelines
- Write tests for all new features
- Test edge cases: empty input, invalid types, boundary conditions
- Mock external dependencies (Ollama API, file operations)
- Test error paths and exception handling
- Aim for 80%+ test coverage

## Development Workflow

### Before Making Changes
1. Review existing code patterns and conventions
2. Check if related tests exist
3. Understand Ollama API interactions and error handling

### When Making Changes
1. Follow existing code style and patterns
2. Run `black .` to ensure proper formatting
3. Run `pytest` or `pytest -k test_name` to verify changes
4. Run `mypy .` to ensure type correctness
5. Commit clear, descriptive messages

### After Making Changes
1. Verify tests still pass
2. Check code quality tools results
3. Update documentation if new features are added

## Project Architecture

### Core Modules
- **config.py**: Global configuration with Ollama settings and image paths
- **utils.py**: Utility functions (file operations, directory traversal, logging)
- **main.py**: Basic image processing with qwen3 model (free response)
- **main2.py**: Image processing with llama4 model (free response)
- **multipleChoice.py**: Multiple choice queries with qwen3 model (choice response)
- **multipleChoice2.py**: Multiple choice queries with llama4 model (choice response)
- **create_analysis_table.py**: Generate analysis tables from results

### Directory Structure
- **log/**: Execution logs with timestamp identification
- **results/**: Individual result files with model_name/timestamp-q*.txt format
- **../Q2**: Main image directory (.jpg files)
- **../Q2/MC**: Prompt directory (.txt files)

### File Naming Convention
- Result files: `{question_num}_{model}_{timestamp}_{type}.txt`
  - Type: "free" for main.py/main2.py, "choice" for multipleChoice files
  - Example: `q01_llama4:scout_20260221_123456_free.txt`

## Common Code Patterns

### File Operations
```python
from pathlib import Path

# Use context managers for file operations
with open('file.txt', 'r') as f:
    content = f.read()

# Validate file existence
if os.path.isfile(path) and path.suffix in ('.jpg', '.txt'):
    process_file(path)
```

### Ollama API Interactions
```python
from ollama import Client

# Create client instance
client = Client(host='http://10.0.26.32:11434')

# Handle API responses with error checking
try:
    stream = client.generate(model='llama4:scout', prompt=text, images=[image_path])
    response_content = str(stream.response)

    # Process response and write to results
    write_result_file(image_path, response_content, 'llama4:scout', prompt)
except Exception as e:
    logging.error(f"API call failed: {e}")
```

### Logging Pattern
```python
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create log directory and write execution log
log_messages = ["Starting task...", "Processing images..."]
write_log_file(config, log_messages)
```

### Directory Setup
```python
# Create log and results directories
Path(config.directories.log_directory).mkdir(parents=True, exist_ok=True)
Path(config.directories.results_directory).mkdir(parents=True, exist_ok=True)

# Get unique result filename
result_file = get_unique_filename(image_path, 'llama4:scout', 'free')
# Creates: {question_num}_{model}_{timestamp}_{type}.txt
```

## Project-Specific Notes

### Running Experiments
- Ensure Ollama service is running at http://10.0.26.32:11434
- Use `main.py` for qwen3-vl-8b-MAX:latest with free responses
- Use `main2.py` for llama4:scout with free responses
- Use `multipleChoice.py` for qwen3-vl-8b-MAX:latest with choice responses
- Use `multipleChoice2.py` for llama4:scout with choice responses

### Analysis
- Run `python3 create_analysis_table.py` to generate comparison tables
- Results stored in `results/` with unique timestamp identification
- Log files stored in `log/` with execution timestamps

### Configuration
- Main image directory: `../Q2`
- Prompt directory: `../Q2/MC`
- Default model for main scripts: `qwen3-vl-8b-MAX:latest`
- Alternative model for comparison: `llama4:scout`