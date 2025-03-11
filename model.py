import moderngl as mgl
import numpy as np
import glm

from vbo import BodyPart


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

        # Handle texture assignment
        if isinstance(tex_id, str):  # If tex_id is a string (e.g., 'cat')
            self.textures = self.app.mesh.texture.textures.get(tex_id, {})
        else:  # If tex_id is an integer (e.g., 0, 1, 2)
            self.textures = {tex_id: self.app.mesh.texture.textures[tex_id]}

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        if isinstance(self.textures, dict):
            for i, (mat_name, tex) in enumerate(self.textures.items()):
                tex.use(location=i)
                self.program[f"u_texture_{i}"] = i
        elif self.tex_id in self.app.mesh.texture.textures:
            self.app.mesh.texture.textures[self.tex_id].use(location=0)
            self.program["u_texture_0"] = 0

        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
       super().__init__(app, vao_name, tex_id, pos, rot, scale)
       self.on_init()
       
    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
    def on_init(self):
        
        
        #texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        #mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        #light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        


class Cat(BaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat', pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), render_mode="", part_to_render=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.parts = {}
        self.render_mode = render_mode  # 'all' or 'single'
        self.part_to_render = part_to_render  # Specific part to render (if render_mode is 'single')

        # Define custom positions for each part
        self.part_positions = {
            'N00_000_00_FaceMouth_00_FACE_(Instance)': (0, 2, 10),
            'N00_000_00_EyeIris_00_EYE_(Instance)': (0, 2, 10),
            'N00_000_00_EyeHighlight_00_EYE_(Instance)': (0, 2, 10.1),
            'N00_000_00_Face_00_SKIN_(Instance)': (0, 2, 10),
            'N00_000_00_EyeWhite_00_EYE_(Instance)': (0, 2, 10),
            'N00_000_00_FaceBrow_00_FACE_(Instance)': (0, 2, 10),
            'N00_000_00_FaceEyeline_00_FACE_(Instance)': (0, 2, 10),
            'N00_000_00_Body_00_SKIN_(Instance)': (0, 2, 10),
            'N00_005_01_Shoes_01_CLOTH_(Instance)': (0, 2, 10),
            'N00_001_02_Bottoms_01_CLOTH_(Instance)': (0, 2, 10),
            'N00_007_03_Tops_01_CLOTH_(Instance)': (0, 2, 10),
            'N00_000_00_HairBack_00_HAIR_(Instance)': (0, 2, 10),
            'N00_010_01_Onepiece_00_CLOTH_(Instance)': (0, 2, 10),
            'N00_000_Hair_00_HAIR_(Instance)': (0, 2, 10),
        }

        # Load all parts from the VBO
        vbo = app.mesh.vao.vbo.vbos[vao_name]
        
      
        
        # Debug: Check if VBO has parts
        #print(f"Cat VBO Parts: {len(vbo.parts)}")
        #print(vbo.parts.keys())
        
        # Iterate over all parts and create a VAO for each
        for part_name, vertex_data in vbo.parts.items():
            if len(vertex_data) > 0:  # Avoid empty VAOs
                # Create a new VBO for the part
                part_vbo = app.ctx.buffer(vertex_data)
                part_vao = app.ctx.vertex_array(self.program, [(part_vbo, vbo.format, *vbo.attribs)])

                # Get the custom position for this part
                part_position = self.part_positions.get(part_name, pos)  # Use default position if not specified

                # Add the body part with its position transformation
                self.parts[part_name] = BodyPart(
                    vao=part_vao,  # Use the new VAO for the part
                    program=self.program,
                    position=part_position,  # Use the custom position for this part
                    rotation=(0, 0, 0),  # Set rotation if needed
                    scale=(1, 1, 1)  # Scale if needed
                )

        print("Cat model initialized")
        print(f"Number of parts: {len(self.parts)}")
        #print(f"Textures: {self.textures}")
        #print(f"Shader program: {self.program}")
        #print(f"self.textures: {self.textures}")
        self.on_init()
        
    def update(self):
        # For each cat part’s texture, bind it again (or just bind the main one if you only have one).
        # If you have multiple textures, you can do something like:
        #   for i, (material_name, tex) in enumerate(self.textures.items()):
        #       tex.use(location=i)
        #       self.program[f"u_texture_{i}"] = i
        
        # But if you only have one, do something like:
        if not isinstance(self.tex_id, str):
            # Single integer texture ID
            print(f'text_id: {self.tex_id}')
            self.textures[self.tex_id].use(location=0)
            self.program["u_texture_0"] = 0
        else:
            # For each material in cat
            for i, (mat_name, tex) in enumerate(self.textures.items()):
                print(f'mat_name: {mat_name}')
                tex.use(location=i)
                uniform_name = f"u_texture_{i}"
                self.program[uniform_name] = i

        # also update camera & transform
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
    
    def render(self):
        if self.render_mode == 'all':
            # Render all body parts
            for part_name, part in self.parts.items():
                #print(f"Rendering body part: {part_name}")
                part.render()
        elif self.render_mode == 'single' and self.part_to_render in self.parts:
            # Render only the specified part
           # print(f"Rendering specific part: {self.part_to_render}")
            self.parts[self.part_to_render].render()
        else:
            print(f"Invalid render mode or part not found: {self.part_to_render}")

    def on_init(self):
        
        print(f"self.textures: {self.textures}")
        
        if isinstance(self.tex_id, int):
            # Ensure self.textures[tex_id] is a Texture object and not a dictionary
            texture_entry = self.textures.get(self.tex_id, None)
            
            if isinstance(texture_entry, dict):
                print(f'is Dict: {texture_entry}')
                
                # If it's a dictionary, try to fetch the first valid texture inside it
                first_key = next(iter(texture_entry), None)
                texture = texture_entry[first_key] if first_key else None
                
                print(f'texture : {texture}')
            else:
                texture = texture_entry  # Directly assign if it's already a Texture object

            if isinstance(texture, mgl.Texture):
                print(f"Texture loaded: {texture}")
            else:
                print(f"Warning: Texture is not valid - {type(texture)}")
    
            if isinstance(texture, mgl.Texture):
                print(f'use texture: {texture.use(location=0)}')
                
                texture.use(location=0)
                self.program['u_texture_0'] = 0
            else:
                print(f"Warning: Expected a texture, but got {type(texture)} - tex_id: {self.tex_id}")

        elif isinstance(self.textures, dict):
            for i, (mat_name, tex) in enumerate(self.textures.items()):
                if isinstance(tex, mgl.Texture):  # Ensure it's a valid texture
                    print(f'textures: {mat_name} : {tex}')
                 
                    print(f"Binding texture {tex} to uniform u_texture_{i}")
                    tex.use(location=i)
                    uniform_name = f"u_texture_{i}"
                    
                    print(f'tex_use: {tex.use(location=i)}')
                    print()
                    print(f'uniform: {uniform_name}')
                    
                    if isinstance(tex, mgl.Texture):
                        print(f"Using_texture: {tex}")
                        tex.use(location=i)
                        self.program[f"u_texture_{i}"] = i
                    else:
                        print(f"Warning: Texture is not of type mgl.Texture - {type(tex)}")
    
                    self.program[uniform_name] = i
                else:
                    print(f"Warning: '{mat_name}' is not a texture, got {type(tex)}")

        # Set up shader matrices
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        # Apply lighting settings
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
