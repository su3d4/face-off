"""Alternative model testing for facial expression recognition."""

import logging
from pathlib import Path

from ollama import Client
from config import create_app_config
from utils import find_files, write_result_file, write_log_file

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_images_with_model(image_paths: list, model: str, prompt: str) -> None:
    """
    Process multiple images using a specified Ollama model.

    Args:
        image_paths: List of image file paths
        model: Name of the Ollama model to use
        prompt: Text prompt for image analysis
    """
    if not image_paths:
        logger.warning("No images provided for processing")
        return

    # Create client instance
    client = Client(host=create_app_config().ollama.host)
    config = create_app_config()

    logger.info(f"Processing {len(image_paths)} images with model: {model}")

    log_messages = [
        f"Starting alternative model testing with: {model}",
        f"Images to process: {len(image_paths)}",
    ]

    for i, image_path in enumerate(image_paths, 1):
        logger.info(f"Processing image {i}/{len(image_paths)}: {image_path.name}")
        log_messages.append(
            f"Processing image {i}/{len(image_paths)}: {image_path.name}"
        )

        try:
            stream = client.generate(model=model, prompt=prompt, images=[image_path])

            response_content = str(stream.response)
            print(f"\n{'='*60}")
            print(f"Image: {image_path.name}")
            print(f"{'='*60}")
            print(stream)
            print("\nModel output:")
            print(stream.response)
            print(f"{'='*60}\n")

            # Write result to file
            write_result_file(image_path, response_content, model, prompt)
            log_messages.append(f"✓ Processed {image_path.name} successfully")

        except Exception as e:
            error_msg = f"✗ Error processing {image_path.name}: {e}"
            logger.error(error_msg)
            log_messages.append(error_msg)

    logger.info("Alternative model testing completed")
    log_messages.append("Alternative model testing completed successfully")


def main() -> None:
    """Main function to process images using llama4 model."""
    config = create_app_config()
    write_log_file(
        config,
        [
            "Starting facial expression recognition with alternative model...",
            f"Log directory: {config.directories.log_directory}",
            f"Results directory: {config.directories.results_directory}",
        ],
    )

    logger.info("Starting image processing with alternative model...")
    log_messages = [
        "Starting facial expression recognition with alternative model...",
        f"Log directory: {config.directories.log_directory}",
        f"Results directory: {config.directories.results_directory}",
    ]

    # Find all images in the configured directory
    try:
        images = find_files(config.image.image_directory, config.image.image_extensions)
        logger.info(f"Found {len(images)} images in {config.image.image_directory}")
        log_messages.append(
            f"Found {len(images)} images in {config.image.image_directory}"
        )
    except ValueError as e:
        error_msg = f"Failed to load images: {e}"
        logger.error(error_msg)
        log_messages.append(error_msg)
        write_log_file(config, log_messages)
        return

    if images:
        # Process images using the llama4 scout model for comparison
        prompt = "What emotion is this face expressing?"
        process_images_with_model(images, config.ollama.model_llama4_scout, prompt)
        log_messages.append(f"Using model: {config.ollama.model_llama4_scout}")
        write_log_file(config, log_messages)
    else:
        error_msg = "No images found to process"
        logger.warning(error_msg)
        log_messages.append(error_msg)
        write_log_file(config, log_messages)


if __name__ == "__main__":
    main()
