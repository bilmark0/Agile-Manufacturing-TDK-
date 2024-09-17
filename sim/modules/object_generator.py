import bpy
import math

class ObjectGenerator:
    def create_object(self, object_type):
        """Creates and returns a new object based on the specified type."""
        if object_type == 0:  # Example: Cube
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.selected_objects[0]
            obj.name = "GeneratedObject"
            return obj
        
        if object_type == 1: #6 way cross for champfer
            bpy.ops.import_mesh.stl(filepath=".\\3D_models\\6WAYS_CROSS.stl", directory=".\\3D_models\\", files=[{"name":"6WAYS_CROSS.stl", "name":"6WAYS_CROSS.stl"}])
            obj = bpy.context.active_object

            # Shade flat
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = math.radians(30)

            obj.scale *= 1/obj.dimensions.x 
            return obj

        else:
            print("Unsupported object type.")
            return None
