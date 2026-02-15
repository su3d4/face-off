# Agent Development Guidelines
This document provides guidelines for agents working in the eastlake-science-fair repository.

## Environment Setup

### Development Environment
This project uses Nix for environment management. The environment includes:
- Python 3.14 with numpy and ollama packages
- Code quality tools: black (formatter), mypy (type checker)
- Required system libraries: libffi, openssl

### Run tests
To run all tests or specific tests, use the following commands:

```bash
# Run all tests
pytest

# Run a single test
pytest -k test_name

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=.
```

## Code Style Guidelines

### Import Organization
1. **Standard library imports first** - Organize imports alphabetically
2. **Third-party imports second** - Group by package
3. **Local imports last** - Place at the end of the file
4. **Separate import groups** with blank lines
5. **Use relative imports** for local module imports when appropriate

Example:
```python
import os
from pathlib import Path

import ollama
from some_library import SomeClass
```

### Indentation and Formatting
1. **Use 4 spaces for indentation** (no tabs)
2. **Follow PEP 8 standard** for Python code
3. **Use black** for automatic formatting:
   ```bash
   black .
   ```
4. **Line length**: Maximum 88 characters

### Variable and Function Naming
1. **CamelCase for classes**: `class ClassName:`
2. **snake_case for functions and variables**: `def my_function():`
3. **snake_case for constants**: `CONSTANT_NAME = 42`
4. **Descriptive names**: Avoid single-letter variables unless in loops
5. **Type annotations** for function parameters and return values

### Type Hints
1. **Always use type hints** for all function signatures
2. **Optional types**: Use `Optional[Type]` for optional parameters
3. **Union types**: Use `Union[TypeA, TypeB]` or `TypeA | TypeB`
4. **Complex types**: Use `TypedDict` for dictionary types

### Error Handling
1. **Use context managers** with `with` statements for file operations
2. **Handle Exceptions specifically**: Catch specific exceptions, not bare except
3. **Use meaningful error messages**: Provide context in error prints
4. **Log errors appropriately**: Use logging instead of print for errors
5. **Validate inputs**: Check file existence, type conversion, etc.

### Comments
1. **Document complex logic**: Explain non-obvious code sections
2. **Comment temporary fixes**: Mark TODO, FIXME, HACK with descriptions
3. **Avoid comments for code**: Use meaningful names instead
4. **Follow existing style**: Match comment style with the codebase

### Code Organization
1. **Separate concerns**: Group related functions together
2. **Limit function length**: Keep functions focused and concise
3. **Use classes for state**: When state is needed
4. **Avoid global variables**: Minimize global state, prefer local variables
5. **Separate configuration**: Define constants and settings separately

### Python Conventions
1. **Use f-strings** for string formatting: `f"Value: {var}"`
2. **Use list comprehensions** for simple transformations
3. **Use ** operator for exponentiation: `x ** 2`
4. **Use meaningful docstrings**: Describe function purpose and parameters
5. **Follow PEP 484** for type hinting

### Testing Guidelines
1. **Write tests for new features**
2. **Test edge cases**: Empty input, invalid types, boundary conditions
3. **Mock external dependencies**: Use mocks for API calls, file operations
4. **Test error paths**: Verify exception handling
5. **Maintain test coverage**: Aim for 80%+ coverage

### Documentation Requirements
1. **Document public API**: Functions, classes, and key modules
2. **Use docstrings** in Google, NumPy, or reStructuredText format
3. **Include examples** for complex functions
4. **Document parameters** with types and descriptions
5. **Document return values** including types
6. **Document side effects** where applicable

## Development Workflow

### Before Making Changes
1. **Review existing code**: Understand patterns and conventions
2. **Check related tests**: Ensure tests cover related functionality
3. **Update documentation**: Update AGENTS.md if adding new conventions

### When Making Changes
1. **Follow existing style**: Match the codebase's conventions
2. **Write tests first**: Write tests for new features
3. **Run linters**: Pass code quality checks before committing
4. **Run tests**: Ensure all tests pass locally
5. **Commit messages**: Use clear, descriptive commit messages

### After Making Changes
1. **Update AGENTS.md**: Add or update guidelines if needed
2. **Review test coverage**: Ensure new code is tested
3. **Update documentation**: Document new features or changes

## Common Code Patterns

### File Operations
```python
# Use context managers for file operations
with open('file.txt', 'r') as f:
    content = f.read()
```

### API Calls
```python
# Always handle responses and errors
try:
    response = client.call_api(params)
    if response.success:
        return response.data
except Exception as e:
    logger.error(f"API call failed: {e}")
    raise
```

### Configuration Loading
```python
# Load from environment or config file
config = load_config()
# Use typed configuration object
```

### Directory Traversal and File Handling
```python
# Read files from directory with filtering
directory = '../Q2'  # image directory
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    if os.path.isfile(path) and filename.endswith('.jpg'):
        process_file(path)

# Sort file lists for consistent processing
file_list.sort()

# Read all files and batch process
file_list = []
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_list.append(os.path.join(directory, filename))
```

### API Client Usage
```python
# Create client instance once and reuse
client = Client(host='http://10.0.26.32:11434')

# Prepare image and prompt arrays
images = []
prompts = []

# Make batch API calls
for image_path, prompt_text in zip(image_paths, prompts):
    response = client.generate(
        model='model-name',
        prompt=prompt_text,
        images=[image_path]
    )
    process_response(response.response)
```

## Project-Specific Notes

### Environment-Sensitive Code
- This project interacts with Ollama API (http://10.0.26.32:11434)
- Ensure Ollama service is running before executing scripts
- Handle connection errors gracefully

### File Structure
- **main.py**: Basic image processing with Ollama
- **main2.py**: Alternative model testing
- **multipleChoice.py**: Multiple choice prompt and image queries
- **shell.nix**: Nix environment configuration
- Test files should follow naming convention: `test_*.py`

## Continuous Integration

If CI/CD is configured, ensure:
1. All tests pass
2. Code passes black formatting
3. Code passes mypy type checking
4. Test coverage meets requirements

## Codebase Specific Patterns

### Batch Processing with Ollama API
- **Multi-model testing**: Scripts like main.py and main2.py demonstrate pattern of iterating through images and sending each to different models (qwen3-vl-8b-MAX:latest vs llama4:scout)
- **Batch file operations**: Use list comprehensions to collect file paths, then sort for deterministic ordering
- **Client isolation**: Create client instance at module level for reuse across multiple API calls

### Image and Prompt Directory Structure
- Main image directory: `../Q2` (contains .jpg files)
- Prompt directory: `../Q2/MC` (contains .txt files with prompts)
- Scripts should locate and process these standard directory paths for consistency

### Response Handling
- Check `stream.response` attribute for text output from Ollama API
- Print both full stream and response for debugging and documentation
- Handle model variations - use appropriate model names for different task requirements

### Error Handling Patterns
- Validate file existence before reading: `if os.path.isfile(path)`
- Check file extensions with `filename.endswith('.jpg')` or `['.jpg', '.txt']`
- Handle potential connection errors when Ollama service is unavailable

## Project Architecture

### Science Fair Project Context
This is an AI-assisted science fair project focusing on facial expression recognition. The project includes:
- **Experimental trials**: F1, F2, MC (multiple choice) - face analysis sessions
- **Novel data sets**: Separate evaluation trials with new questions/exercises
- **Multi-session organization**: Each session generates JSON logs (F1-chat.json, MC1-chat.json, etc.)
- **Documented trials**: PDF reports for F1, F2, MC, MC2 sessions and novel data

### Chat Session Workflow
The project uses Ollama chat sessions to:
1. Process multiple-choice questions with image inputs (F1, F2, MC series)
2. Generate JSON responses with detailed analysis and emotion detection
3. Track responses through chat.json files in the project root
4. Produce summary reports (Score Summary.pdf, Tests Summary.pdf, etc.)

### Ollama Model Configuration
- Project uses `opencode.json` configuration at repository root for model definitions
- Multiple model providers configured: local Ollama and Ollama (taiko) with different API endpoints
- Models available: gpt-oss, qwen3-coder, glm-4.7-flash variants, requiring proper model selection
- Modelfile examples exist in `../modelfiles/` directory showing context parameter settings

### Data Organization Patterns
- **Session data**: chat.json files store full chat history and API responses
- **PDF documentation**: Trial results and analysis documents (all in main project root, not src/)
- **Excel/ODS datasets**: Test data in TestData.xlsx and TestDataMC.ods formats
- **Nested structure**: src/ directory for Python scripts, main directory for experimental data