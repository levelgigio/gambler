import pytesseract
from PIL import Image

def identify_character(image_path):
    # Load the image
    image = Image.open(image_path)

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Apply OCR to extract text from the image
    text = pytesseract.image_to_string(image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

    # Extract the first character from the OCR result
    # character = text.strip()[0] if text.strip() else None

    return text

# Provide the path to the image containing the character
image_path = 'cropped_image.png'
character = identify_character(image_path)

if character:
    print(f"The image contains the character: {character}")
else:
    print("No character was identified in the image.")
