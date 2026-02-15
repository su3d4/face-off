"""Basic image processing with Ollama for facial expression recognition."""
import logging

from ollama import Client
from config import create_app_config
from utils import find_files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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

    logger.info(f"Processing {len(image_paths)} images with model: {model}")

    for i, image_path in enumerate(image_paths, 1):
        logger.info(f"Processing image {i}/{len(image_paths)}: {image_path.name}")
        try:
            stream = client.generate(
                model=model,
                prompt=prompt,
                images=[image_path]
            )

            logger.info(f"Response for {image_path.name}:")
            print(f"\n{'='*60}")
            print(f"Image: {image_path.name}")
            print(f"{'='*60}")
            print(stream)
            print("\nModel output:")
            print(stream.response)
            print(f"{'='*60}\n")

        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")


def main() -> None:
    """Main function to process images using default Ollama configuration."""
    config = create_app_config()

    logger.info("Starting image processing pipeline...")

    # Find all images in the configured directory
    try:
        images = find_files(config.image.image_directory, config.image.image_extensions)
        logger.info(f"Found {len(images)} images in {config.image.image_directory}")
    except ValueError as e:
        logger.error(f"Failed to load images: {e}")
        return

    if images:
        # Process images using the qwen3 model
        prompt = 'What emotion is this face expressing?'
        process_images_with_model(
            images,
            config.ollama.model_qwen3_vl,
            prompt
        )
    else:
        logger.warning("No images found to process")


if __name__ == "__main__":
    main()
