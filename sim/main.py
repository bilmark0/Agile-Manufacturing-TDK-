import os
import sys
sys.path.append("./")
from object3d import Object3D

# Constants (User-Configurable)
OBJECT_TYPE = 0  # Define different object types
OBJECT_TEXTURE_TYPE = 1 #define different object textures
OBJECT_LIGHTING_TYPE = 3 #define lighting type for the images
ERROR_TYPE = 3  # Define different error types
NUM_IMAGES = 5
FILE_PATH = r'C:\temp'
RES_X = 380
RES_Y = 240

def main():
    # Ensure the render output directory exists
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)

    # Initialize the 3D object with type and error type
    obj3d = Object3D(object_type=OBJECT_TYPE, object_error=ERROR_TYPE, render_path=FILE_PATH, texture_type=OBJECT_TEXTURE_TYPE, lighting_type=OBJECT_LIGHTING_TYPE)
    
    # Generate the specified number of images
    obj3d.generate_images(NUM_IMAGES, RES_X, RES_Y)

if __name__ == "__main__":
    main()
