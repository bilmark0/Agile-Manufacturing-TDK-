import bpy
import random
import math
import os
import sys
sys.path.append("./modules")
from modules.object_generator import ObjectGenerator
from modules.texture_applier import TextureApplier
from modules.error_applier import ErrorApplier
from modules.add_light import AddLight
from modules.gpu_renderer import GPURenderer

class Object3D:
    def __init__(self, object_type, object_error, render_path, texture_type=0, lighting_type=0):
        self.object_type = object_type
        self.object_error = object_error
        self.texture_type = texture_type
        self.render_path = render_path
        self.lighting_type = lighting_type
        self.object_generator = ObjectGenerator()
        self.texture_applier = TextureApplier()
        self.error_applier = ErrorApplier()
        self.add_light = AddLight()
        self.gpu_renderer = GPURenderer()
        self.gpu_renderer.set_gpu_rendering()
        
    def setup_camera(self):
        """Set up the camera in the scene."""
        # Remove any existing cameras
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                bpy.data.objects.remove(obj, do_unlink=True)

        # Add a new camera
        bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(math.radians(75), 0, 0))
        camera = bpy.context.object
        camera.name = "Camera"

        # Set the camera as the active camera
        bpy.context.scene.camera = camera

        camera.data.lens = 30

        # Debug: Confirm the camera is set
        if bpy.context.scene.camera is None:
            print("Error: No camera set in the scene.")
        else:
            print(f"Camera '{bpy.context.scene.camera.name}' set as active camera.")

    def place_object_rnd(self, error_range):
        # Clear all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Set up the camera
        self.setup_camera()

        """Randomly place the object within the scene."""
        placement = random.randint(-error_range, error_range), random.randint(-error_range, error_range), 0
        
        # Create a new plane
        bpy.ops.mesh.primitive_plane_add(size=80)  # Adjust size as needed
        plane = bpy.context.selected_objects[0]
        plane.name = "Plane"
        plane.location = (placement[0], placement[1], placement[2] - 1)

        # Create and assign white material to the plane
        plane_material = bpy.data.materials.new(name="PlaneMaterial")
        plane_material.diffuse_color = (1, 1, 1, 1)  # White color (RGBA)
        plane.data.materials.append(plane_material)

        # Create and place the object
        obj = self.object_generator.create_object(self.object_type)
        if obj is not None:
            obj.location = placement
            #bpy.context.active_object.rotation_euler[2] = math.radians(random.randint(0, 179))
            return obj
        else:
            return None

    def render_image(self, render_num, res_x, res_y):
        """Render a single image."""
        # Place the object
        obj = self.place_object_rnd(error_range=0)
        if obj is None:
            print("Error: no object placed")
            return None

        # Apply texture to the object
        self.texture_applier.apply_texture(obj, self.texture_type)

        # Generate error on the object
        self.error_applier.apply_error(obj, self.object_error)

        # Add HDRI map or other lighting
        self.add_light.add_light(self.lighting_type)

        # Render the image
        bpy.context.scene.render.filepath = f"{self.render_path}/image_{render_num}_{self.object_error}_{self.object_type}.png"
        bpy.context.scene.render.resolution_x = res_x
        bpy.context.scene.render.resolution_y = res_y

        # Ensure the camera is set as active before rendering
        if bpy.context.scene.camera is None:
            print("Error: No active camera in the scene. Cannot render.")
            return

        bpy.ops.render.render(write_still=True)

        # Remove the object after rendering
        bpy.data.objects.remove(obj)
        bpy.data.objects.remove(bpy.data.objects["Plane"])

    def generate_images(self, num_images, res_x, res_y):
        """Generate multiple images."""
        for i in range(num_images):
            self.render_image(i, res_x, res_y)
