import bpy
import random
import math

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
        
        
        if error_type == 1: # Generating chamfer on a random edge, for circular disk surfaces
            def cutter_cube():#Generates a cube to the desired spot
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                z_location = obj.dimensions.z/2
                r = 0.5 + random.randrange(5, 13)/100
                rot_angle = math.radians(random.randrange(45,90))
                bpy.ops.mesh.primitive_cube_add(size = 1, location = (r*math.cos(rot_angle),r*math.sin(rot_angle),z_location ))
                cube = bpy.context.active_object
                cube.scale.x *=0.4
                cube.scale.z *=0.25
                cut_angle = 45 + random.randrange(-15, 15)
                cube.rotation_euler.y = math.radians(cut_angle)
                cube.rotation_euler.z = rot_angle
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                return cube
            
            cube = cutter_cube()
            bpy.context.view_layer.objects.active = obj
            
            self.boolean_diff(obj, cube)
            bpy.data.objects.remove(cube)
            
            self.rotate_obj(obj)

        if error_type == 2: # Generating a V shaped cut on one of the surfaces
            def cutter_cube():#Generates a cube to the desired spot
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                z_location = obj.dimensions.z/2
                rot_angle = math.radians(random.randrange(0,90))
                bpy.ops.mesh.primitive_cube_add(size = 0.5, location = (0,0,z_location))
                cube = bpy.context.active_object
                cube.location.z += cube.dimensions.z * random.randrange(63,69)/100
                cube.location.x += random.randrange(0,45)/100
                cube.rotation_euler.y = math.radians(45)
                cube.rotation_euler.z = rot_angle
                cube.scale.y *= 10
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                return cube

            cube = cutter_cube()
            bpy.context.view_layer.objects.active = obj

            self.boolean_diff(obj, cube)
            bpy.data.objects.remove(cube)

            obj.rotation_euler.x = math.radians(random.randrange(-90, 180, 90))
            obj.rotation_euler.z = math.radians(random.randrange(-155,-25)) 
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        if error_type == 3: #use only to generate a champfer into a cube
            def cutter_cube():#Generates a cube to the desired spot
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                z_location = obj.dimensions.z/2
                r = 0.5 + random.randrange(5, 13)/100
                bpy.ops.mesh.primitive_cube_add(size = 1, location = (r,0,z_location ))
                cube = bpy.context.active_object
                cube.scale.x *=0.5
                cube.scale.z *=0.25
                cube.scale.y *= 2
                cut_angle = 45 + random.randrange(-15, 15)
                cube.rotation_euler.y = math.radians(cut_angle)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                return cube
            
            cube = cutter_cube()
            bpy.context.view_layer.objects.active = obj

            self.boolean_diff(obj, cube)
            bpy.data.objects.remove(cube)
            
            """Applies random rotation to the object."""
            obj.rotation_euler.x = math.radians(random.randrange(0, 360, 90))
            obj.rotation_euler.z = math.radians(random.randrange(-155,-25)) 
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        if error_type == 4: #creates a V shaped cut on the surface of a sphere
            def cutter_cube():#Generates a cube to the desired spot
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                z_location = obj.dimensions.z/2
                rot_angle = math.radians(random.randrange(0,90))
                bpy.ops.mesh.primitive_cube_add(size = 0.5, location = (0,0,z_location))
                cube = bpy.context.active_object
                cube.location.z += cube.dimensions.z * random.randrange(63,70)/100
                cube.rotation_euler.y = math.radians(45)
                cube.rotation_euler.z = rot_angle
                cube.scale.y *= 10
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                return cube

            cube = cutter_cube()
            bpy.context.view_layer.objects.active = obj

            self.boolean_diff(obj, cube)
            bpy.data.objects.remove(cube)

            obj.rotation_euler.x = math.radians(random.randrange(0,360))
            obj.rotation_euler.y = math.radians(random.randrange(0,360))
            obj.rotation_euler.z = math.radians(random.randrange(0,360))
            obj.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
        else:
            print("Unsupported error type.")
            return None
    
    def boolean_diff(self, obj, diff):
        """Applies a boolean difference modifier between obj and diff."""
        bool_mod = obj.modifiers.new(obj.name + '_bool', 'BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.solver = 'FAST'
        bool_mod.object = diff
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    def rotate_obj(self, obj):
        """Applies random rotation to the object."""
        obj.rotation_euler.x = math.radians(random.randrange(0, 360, 90))
        obj.rotation_euler.z = math.radians(random.randrange(-155,-25)) 
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
