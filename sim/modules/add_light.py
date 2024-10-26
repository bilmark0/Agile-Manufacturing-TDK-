import os
import bpy


class AddLight():
    def remove_existing_lights(self):
        # Remove all lights from the scene
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def remove_existing_hdri(self):
        # Clear existing nodes from the World node tree (HDRI map)
        world = bpy.context.scene.world
        if world and world.use_nodes:
            nodes = world.node_tree.nodes
            nodes.clear()

    def add_light(self, light_type):
        # Remove any existing lights before adding a new one
        self.remove_existing_lights()

        if light_type == 0:
            # Create a point light
            light_data = bpy.data.lights.new(name="Point Light", type='POINT')
            light_object = bpy.data.objects.new(name="Point Light", object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            light_object.location = (0, 0, 10)
        elif light_type == 1:
            # Create a sun light
            light_data = bpy.data.lights.new(name="Sun Light", type='SUN')
            light_object = bpy.data.objects.new(name="Sun Light", object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            light_object.location = (0, 0, 10)
        elif light_type == 2:
            # Create an area light
            light_data = bpy.data.lights.new(name="Area Light", type='AREA')
            light_object = bpy.data.objects.new(name="Area Light", object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            light_object.location = (0, 0, 10)
        elif light_type == 3:
            # Remove existing HDRI maps before adding a new one
            self.remove_existing_hdri()
            # Call HDRI map addition logic
            hdri_path=r".\modules\hdri_maps\bank_vault_8k.hdr"
            hdri_path_n = os.path.abspath(hdri_path)
            self.add_hdri(hdri_path_n)# Update with actual path to HDRI file

    def add_hdri(self, hdri_path):
        # Check current working directory
        print("Current working directory:", os.getcwd())

        # Check if HDRI path exists
        if not os.path.exists(hdri_path):
            print(f"Error: HDRI file does not exist at path: {hdri_path}")
            return

        # Set the rendering engine to 'CYCLES'
        bpy.context.scene.render.engine = 'CYCLES'

        # Get the World node tree and clear any existing nodes
        world = bpy.context.scene.world
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links
        
        # Clear all nodes
        nodes.clear()

        # Add a background shader
        background_node = nodes.new(type='ShaderNodeBackground')

        # Add an environment texture node and set the HDRI path
        env_texture_node = nodes.new(type='ShaderNodeTexEnvironment')
        
        try:
            env_texture_node.image = bpy.data.images.load(hdri_path)
            print(f"Successfully loaded HDRI from: {hdri_path}")
        except Exception as e:
            print(f"Failed to load HDRI image: {e}")
            return

        # Connect the environment texture to the background shader
        links.new(env_texture_node.outputs['Color'], background_node.inputs['Color'])

        # Add a world output node and connect the background shader to it
        world_output_node = nodes.new(type='ShaderNodeOutputWorld')
        links.new(background_node.outputs['Background'], world_output_node.inputs['Surface'])

        # Update the scene
        bpy.context.scene.world = world
        bpy.context.view_layer.update()

        # Only set the scene world shading if the active space is a 3D view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.use_scene_world_render = False
                        break
                