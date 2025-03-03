import cloudinary.uploader
from asgiref.sync import sync_to_async
import logging

# Set up logging
logger = logging.getLogger(__name__)

from asgiref.sync import sync_to_async
import cloudinary.uploader
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Synchronous function for image upload to Cloudinary
def sync_upload_image(image, folder):
    try:
        # Cloudinary image upload with specific transformations
        response = cloudinary.uploader.upload(
            image,
            folder=folder,
            format='png',  # Ensuring the format is PNG
            transformation=[{
                "width": 385,  # Resize the image to fit within 500x500
                "height": 330,
                "crop": "fit",  # Ensure the image fits the dimensions
            }]
        )
        logger.info(f"Image uploaded successfully: {response['secure_url']}")
       
        return response
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise Exception(f"Failed to upload image: {str(e)}")

# Asynchronous function that calls the synchronous upload function
async def upload_image(image, folder):
    try:
        # Using sync_to_async to run the synchronous upload function in an async context
        response = await sync_to_async(sync_upload_image)(image, folder)
       
        return response
    except Exception as e:
        logger.error(f"Error in async image upload: {str(e)}")
        raise Exception(f"Failed to upload image asynchronously: {str(e)}")
    


async def get_image_urls(result, photo_1, photo_2):
    """
    Function to safely extract image URLs from the upload result based on the presence of photo_1 and photo_2.
    
    Parameters:
    - result: The list containing the upload responses.
    - photo_1: The first photo file, if present.
    - photo_2: The second photo file, if present.
    
    Returns:
    - photo_1_url: The URL for photo_1 if uploaded, or None.
    - photo_2_url: The URL for photo_2 if uploaded, or None.
    """
    if photo_1 and photo_2:
        # If both photo_1 and photo_2 are present
        photo_1_url = result[0]['secure_url'] if result else None
        photo_2_url = result[1]['secure_url'] if result else None
    elif photo_1:
        # If only photo_1 is present
        photo_1_url = result[0]['secure_url'] if result else None
        photo_2_url = None
    elif photo_2:
        # If only photo_2 is present
        photo_1_url = None
        photo_2_url = result[0]['secure_url'] if result else None
    else:
        # If neither photo_1 nor photo_2 is present
        photo_1_url = None
        photo_2_url = None

    return photo_1_url, photo_2_url

