import os
from object3d import Object3D

# Constants (User-Configurable)
OBJECT_TYPE = 0  # Define different object types
OBJECT_TEXTURE_TYPE = 0 #define different object textures
ERROR_TYPE = 0  # Define different error types
NUM_IMAGES = 10
FILE_PATH = r'Your output path'
LIGTH_TYPE = 3

def main():
    # Ensure the render output directory exists
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)

    # Initialize the 3D object with type and error type
    obj3d = Object3D(object_type=OBJECT_TYPE, render_path=FILE_PATH, object_error=ERROR_TYPE,lighting_type=LIGHT_TYPE)
    
    # Generate the specified number of images
    obj3d.generate_images(NUM_IMAGES)

if __name__ == "__main__":
    main()
