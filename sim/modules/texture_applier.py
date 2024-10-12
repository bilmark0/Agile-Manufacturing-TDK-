import bpy

class TextureApplier:
    def apply_texture(self, obj, texture_type):
        # Create a new material
        material = bpy.data.materials.new(name="CustomMaterial")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Clear all nodes
        for node in nodes:
            nodes.remove(node)

        # Add Material Output node first
        material_output = nodes.new(type='ShaderNodeOutputMaterial')

        if texture_type == 0:
            # Add Principled BSDF node for basic color
            principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled_bsdf.inputs['Base Color'].default_value = (1, 1, 0, 1)  # Yellow color
            
            # Link Principled BSDF to the material output
            links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

            # Assign the material to the object
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)

        elif texture_type == 1:
            # Procedural texture nodes (as in the previous setup)
            # This part remains unchanged

            layer_weight = nodes.new(type='ShaderNodeLayerWeight')
            layer_weight.inputs[0].default_value = 0.3

            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.color_ramp.elements[0].position = 0.5

            noise_texture = nodes.new(type='ShaderNodeTexNoise')
            noise_texture.inputs['Scale'].default_value = 100.0
            noise_texture.inputs['Detail'].default_value = 2.0
            noise_texture.inputs['Roughness'].default_value = 0.5

            tex_coord = nodes.new(type='ShaderNodeTexCoord')
            links.new(tex_coord.outputs['Object'], noise_texture.inputs['Vector'])

            diffuse_bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')

            glossy_bsdf = nodes.new(type='ShaderNodeBsdfGlossy')
            glossy_bsdf.inputs['Roughness'].default_value = 0.4

            mix_shader = nodes.new(type='ShaderNodeMixShader')

            math_node = nodes.new(type='ShaderNodeMath')
            math_node.operation = 'MULTIPLY'
            math_node.inputs[1].default_value = 0.5  # Scale noise effect on roughness

            displacement = nodes.new(type='ShaderNodeDisplacement')
            displacement.inputs['Scale'].default_value = 0.1

            # Link nodes (unchanged)
            links.new(layer_weight.outputs['Facing'], color_ramp.inputs['Fac'])
            links.new(color_ramp.outputs['Color'], diffuse_bsdf.inputs['Color'])
            links.new(noise_texture.outputs['Fac'], math_node.inputs[0])
            links.new(math_node.outputs['Value'], glossy_bsdf.inputs['Roughness'])
            links.new(diffuse_bsdf.outputs['BSDF'], mix_shader.inputs[1])
            links.new(glossy_bsdf.outputs['BSDF'], mix_shader.inputs[2])
            links.new(mix_shader.outputs['Shader'], material_output.inputs['Surface'])
            links.new(noise_texture.outputs['Fac'], displacement.inputs['Height'])
            links.new(displacement.outputs['Displacement'], material_output.inputs['Displacement'])

            # Assign the material to the object
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)

        else:
            print("Unsupported texture type.")
            return None


