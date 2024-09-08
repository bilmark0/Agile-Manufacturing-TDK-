import bpy
import random

class ErrorApplier:
    def apply_error(self, obj, error_type):
        """Applies an error to the object based on the specified error type."""
        if error_type == 0:  # Example: Coloring random faces
            polygons_list = list(obj.data.polygons)

            red_material = bpy.data.materials.get("Red") or bpy.data.materials.new(name="Red")
            red_material.diffuse_color = (1, 0, 0, 1)

            blue_material = bpy.data.materials.get("Blue") or bpy.data.materials.new(name="Blue")
            blue_material.diffuse_color = (0, 0, 1, 1)

            obj.data.materials.clear()

            # Randomly assign materials to faces
            selected_faces_red = random.sample(polygons_list, min(3, len(polygons_list)))
            remaining_faces = [f for f in polygons_list if f not in selected_faces_red]
            selected_faces_blue = random.sample(remaining_faces, min(3, len(remaining_faces)))

            for face in selected_faces_red:
                obj.data.materials.append(red_material)
                obj.data.polygons[face.index].material_index = len(obj.data.materials) - 1

            for face in selected_faces_blue:
                obj.data.materials.append(blue_material)
                obj.data.polygons[face.index].material_index = len(obj.data.materials) - 1
        else:
            print("Unsupported error type.")
            return None
