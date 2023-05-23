from PIL import Image

def crop_image(image_path, x1, y1, x2, y2, output_path):
    # Open the image
    image = Image.open(image_path)

    # Crop the image
    cropped_image = image.crop((x1, y1, x2, y2))

    # Save the cropped image
    cropped_image.save(output_path)

    print("Image cropped and saved successfully.")

# Example usage
image_path = "countdown.png"

COUNTDOWN_TIMER = (960, 445, 990, 480)
x1 = 375  # Starting X-coordinate
y1 = 835  # Starting Y-coordinate
x2 = 400   # Ending X-coordinate
y2 = 855  # Ending Y-coordinate
output_path = "cropped_image.png"

crop_image(image_path, *COUNTDOWN_TIMER, output_path)
