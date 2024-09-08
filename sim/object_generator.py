import bpy

class ObjectGenerator:
    def create_object(self, object_type):
        """Creates and returns a new object based on the specified type."""
        if object_type == 0:  # Example: Cube
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.selected_objects[0]
            obj.name = "GeneratedObject"
            return obj
        else:
            print("Unsupported object type.")
            return None
