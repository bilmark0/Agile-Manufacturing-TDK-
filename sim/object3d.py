import bpy
import random
import math
from modules.object_generator import ObjectGenerator
from modules.texture_applier import TextureApplier
from modules.error_applier import ErrorApplier

class Object3D:
    def __init__(self, object_type, object_error, texture_type, render_path):
        self.object_type = object_type
        self.object_error = object_error
        self.texture_type = texture_type
        self.render_path = render_path
        self.object_generator = ObjectGenerator()
        self.texture_applier = TextureApplier()
        self.error_applier = ErrorApplier()

    def place_object_rnd(self, error_range):
        # clear all
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

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
            bpy.context.active_object.rotation_euler[2] = math.radians(random.randint(0, 179))
            return obj
        else:
            return None

    def render_image(self, render_num, res_x, res_y):
        """Render a single image."""
        # Place the object
        obj = self.place_object_rnd(error_range=5)
        if obj is None:
            print("Error no object placed")
            return None

        # Apply texture to the object
        self.texture_applier.apply_texture(obj, self.texture_type)

        # Generate error on the object
        self.error_applier.apply_error(obj, self.object_error)

        # Render the image
        bpy.context.scene.render.filepath = f"{self.render_path}/image_{render_num}.png"
        bpy.context.scene.render.resolution_x = res_x
        bpy.context.scene.render.resolution_y = res_y
        bpy.ops.render.render(write_still=True)

        # Remove the object after rendering
        bpy.data.objects.remove(obj)
        bpy.data.objects.remove(bpy.data.objects["Plane"])

    def generate_images(self, num_images, res_x, res_y):
        """Generate multiple images."""
        for i in range(num_images):
            self.render_image(i, res_x, res_y)
