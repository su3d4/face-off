"""Multiple choice prompt and image queries for facial expression recognition with llama4 model."""

import logging
from pathlib import Path

from ollama import Client
from config import create_app_config
from utils import find_files, read_prompt_file, write_multiple_choice_result, write_log_file

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_images_with_prompts(
    image_paths: list, prompt_files: list, model: str
) -> dict:
    """
    Process images with associated multiple choice prompts using a model.

    Args:
        image_paths: List of image file paths paired with prompts
        prompt_files: List of prompt file paths paired with images
        model: Name of the Ollama model to use

    Returns:
        Dictionary mapping image paths to responses
    """
    if not image_paths or not prompt_files:
        logger.warning("No images or prompts provided for processing")
        return {}

    if len(image_paths) != len(prompt_files):
        logger.error(
            f"Mismatch between images ({len(image_paths)}) and prompts ({len(prompt_files)})"
        )
        return {}

    # Create client instance
    client = Client(host=create_app_config().ollama.host)
    config = create_app_config()
    write_log_file(
        config,
        [
            "Starting multiple choice query processing with alternative model...",
            f"Using model: {model}",
            f"Image-prompt pairs: {len(image_paths)}",
        ],
    )

    log_messages = [
        "Starting multiple choice query processing with alternative model...",
        f"Using model: {model}",
        f"Image-prompt pairs: {len(image_paths)}",
    ]

    results = {}

    for image_path, prompt_file_path in zip(image_paths, prompt_files):
        logger.info(
            f"Processing: {image_path.name} with prompt: {prompt_file_path.name}"
        )
        log_messages.append(
            f"Processing: {image_path.name} with prompt: {prompt_file_path.name}"
        )

        try:
            # Read prompt content
            prompt_text = read_prompt_file(prompt_file_path)
            logger.debug(f"Prompt content: {prompt_text[:100]}...")

            # Make API call
            stream = client.generate(
                model=model, prompt=prompt_text, images=[image_path]
            )

            response_content = str(stream.response)
            results[str(image_path)] = response_content

            # Write result to file
            write_multiple_choice_result(
                config, prompt_file_path, response_content, model
            )
            log_messages.append(f"✓ Processed {image_path.name} successfully")

            logger.info(f"Response generated for {image_path.name}")

        except FileNotFoundError as e:
            error_msg = f"✗ File not found: {e}"
            logger.error(error_msg)
            log_messages.append(error_msg)
        except Exception as e:
            error_msg = f"✗ Error processing {image_path.name}: {e}"
            logger.error(error_msg)
            log_messages.append(error_msg)

    logger.info("Multiple choice processing completed")
    log_messages.append(f"Completed processing. Generated {len(results)} responses")
    write_log_file(config, log_messages)

    return results


def main() -> None:
    """Main function to process multiple choice queries using llama4 model."""
    config = create_app_config()

    logger.info(
        "Starting multiple choice query processing pipeline with alternative model..."
    )

    # Find all images in the configured directory
    try:
        image_paths = find_files(
            config.image.image_directory, config.image.image_extensions
        )
        logger.info(
            f"Found {len(image_paths)} images in {config.image.image_directory}"
        )
    except ValueError as e:
        logger.error(f"Failed to load images: {e}")
        return

    # Find all prompt files in the configured directory
    try:
        prompt_paths = find_files(
            config.image.prompt_directory, config.image.prompt_extensions
        )
        logger.info(
            f"Found {len(prompt_paths)} prompts in {config.image.prompt_directory}"
        )
    except ValueError as e:
        logger.error(f"Failed to load prompts: {e}")
        return

    if image_paths and prompt_paths:
        # Create paired requests dictionary
        # Ensure prompt files correspond to images - for now, use existing file structure
        pairs = {}
        for image_path in image_paths:
            # Try to find matching prompt file (e.g., image.jpg pairs with question.txt)
            stem = image_path.stem
            matching_prompt = None
            for prompt_path in prompt_paths:
                if prompt_path.stem == stem:
                    matching_prompt = prompt_path
                    break
            if matching_prompt:
                pairs[image_path] = matching_prompt

        if not pairs:
            logger.warning("No valid image-prompt pairs found")
            return

        logger.info(f"Processing {len(pairs)} image-prompt pairs")

        # Process using the llama4 scout model for comparison
        results = process_images_with_prompts(
            list(pairs.keys()), list(pairs.values()), config.ollama.model_llama4_scout
        )

        logger.info(f"Completed processing. Generated {len(results)} responses")

        # Print results
        print(f"\n{'='*60}")
        print("SUMMARY OF RESULTS (llama4:scout)")
        print(f"{'='*60}\n")
        for image_path, response in results.items():
            print(f"Image: {Path(image_path).name}")
            print(f"Response: {response}")
            print(f"{'-'*60}\n")
    else:
        logger.warning("No images or prompts found")


if __name__ == "__main__":
    main()
