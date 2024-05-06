import numpy as np
from PIL import Image, ImageFilter
import random
import math
import os

# just for more easily naming the images to have a lot of test images
def count_files_in_folder():
    # Get the current directory where the script is located
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Count the number of files in the directory
    file_count = len([name for name in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, name))])
    
    return file_count

# I thought it could be useful, but now I'm not so sure
def create_proxy(image_path, scale_down_factor):
    image = Image.open(image_path)
    width, height = image.size

    # Ensure image is a square
    size = max(width, height)
    image = image.resize((size, size), Image.LANCZOS)

    # Create a blurred version of the image
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))

    # Create a scaled down version of the image
    scaled_size = int(size / scale_down_factor)
    scaled_down_image = image.resize((scaled_size, scaled_size), Image.LANCZOS)

    # Create a new image with the blurred background
    combined_image = blurred_image.copy()
    # Calculate position to place the scaled down image (centered)
    top_left_x = (size - scaled_size) // 2
    top_left_y = (size - scaled_size) // 2
    combined_image.paste(scaled_down_image, (top_left_x, top_left_y))

    return combined_image

# written by chat mostly, i have no idea what it does
def warp_image(image_path, bulge_factor=1.8, bulge_exponent=2, scale_down_factor=1.5):
    combined_image = create_proxy(image_path, scale_down_factor)
    img_array = np.array(combined_image)
    new_img_array = np.zeros_like(img_array)

    size = combined_image.size[0]
    center_x, center_y = size / 2, size / 2

    # Process each pixel in the image
    for i in range(size):
        for j in range(size):
            norm_x = (i - center_x) / center_x
            norm_y = (j - center_y) / center_y
            r = math.sqrt(norm_x**2 + norm_y**2)

            if r <= 1.0:  # Only process pixels within the unit circle
                theta = math.atan2(norm_y, norm_x)
                # Adjust radius using a customizable bulge factor and exponent
                adjusted_r = r * (1 - bulge_factor * r**bulge_exponent)
                
                if adjusted_r < 0:
                    adjusted_r = 0  # Avoid negative radius values

                # Calculate new pixel positions based on adjusted radius
                proj_x = center_x + adjusted_r * math.cos(theta) * center_x
                proj_y = center_y + adjusted_r * math.sin(theta) * center_y

                # Ensure projected coordinates are within image bounds
                proj_x = min(max(int(proj_x), 0), size - 1)
                proj_y = min(max(int(proj_y), 0), size - 1)

                new_img_array[j, i] = img_array[proj_y, proj_x]

    warped_image = Image.fromarray(new_img_array)
    return warped_image

if __name__ == "__main__":
    # just place holder variable names, i kinda don't know what they do
    stretchFactor = 6.5
    bge = stretchFactor/4
    bf = (bge*stretchFactor) / 100
    
    image_folder = "image_assets/"
    
    # actual running the thing
    warped_image = warp_image(image_folder + "earthView1.png", bulge_factor=-bf, bulge_exponent=bge, scale_down_factor=1.01)
    imgName = "newGrid" + str(count_files_in_folder()) + ".png"
    warped_image.save(imgName)
