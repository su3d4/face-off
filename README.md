# Eastlake Science Fair - Image Recognition Project

A Python-based AI-assisted science fair project focusing on facial expression recognition using Ollama service.

## Project Overview

This project demonstrates facial expression recognition capabilities using various AI models (qwen3-vl-8b-MAX and llama4:scout) via the Ollama API. The system processes images and multiple choice queries to analyze emotions and facial expressions.

## Project Structure

```
src/
├── config.py          # Global configuration for Ollama and image paths
├── utils.py           # Utility functions for file operations and directory traversal
├── main.py            # Basic image processing with qwen3 model
├── main2.py           # Image processing with llama4 model (comparison)
├── multipleChoice.py  # Multiple choice queries with qwen3 model
├── multipleChoice2.py # Multiple choice queries with llama4 model
├── AGENTS.md          # Agent development guidelines
└── README.md          # This file
```