import numpy as np
import moderngl as mgl
import pywavefront
import glm

class VBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbos = {}
        self.parts = {}
        self.vbos['cube'] = CuboVBO(ctx)
        self.vbos['cat'] = CatVBO(ctx)
    
    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: List = None
        
    def get_vertx_data(self): ...
    
    def get_vbo(self):
        vertex_data = self.get_vertx_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.vbo.release()
        

class CuboVBO(BaseVBO):
    def __init__ (self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vertx_data(self):
        vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1),
                    (-1,1,-1), (-1,-1,-1), (1,-1,-1), (1,1,-1)]
        
          
        indices = [(0,2,3), (0,1,2),
                   (1,7,2), (1,6,7),
                   (6,5,4), (4,7,6),
                   (3,4,5), (3,5,0),
                   (3,7,4),(3,2,7),
                   (0,6,1), (0,5,6)]
        
        
        vertex_data = self.get_data(vertices, indices)
        
          
        tex_coord = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [(0,2,3),(0,1,2),
                             (0,2,3),(0,1,2),
                             (0,1,2),(2,3,0),
                             (2,3,0),(2,0,1),
                             (0,2,3),(0,1,2),
                             (3,1,2),(3,0,1),]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)
        
        normals = [(0,0,1) * 6,
                   (1,0,0) * 6,
                   (0,0,-1) * 6,
                   (-1,0,0) * 6,
                   (0,1,0) * 6,
                   (0,-1,0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)
        
        
        
        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        
        return vertex_data
    
class CatVBO(BaseVBO):
    def __init__(self, ctx):
        self.parts = {}  # Store parts separately
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
   
    def get_vertx_data(self, part_name=None):
        # Load the .obj file
        objs = pywavefront.Wavefront('objects/vtuber/ImageToStl.com_fak3rR_.vrm.obj', cache=True, parse=True)
        
        self.parts = {}  # Clear any existing parts
        for name, material in objs.materials.items():
            self.parts[name] = np.array(material.vertices, dtype='f4')  # Store each part separately

        # If part_name is provided, only return the data for that part
        if part_name:
            if part_name in self.parts:
                print(f"Loading part: {part_name}")
                return self.parts[part_name]  # Return the data for the specific part
            else:
                print(f"Part {part_name} not found!")
                return np.array([])  # Return empty if part is not found
        
        # Return all parts as fallback if no specific part requested
        print(f"Loaded {len(self.parts)} parts")
        return np.concatenate(list(self.parts.values()), axis=0)  # Concatenate all parts' vertex data

class BodyPart:
    def __init__(self, vao, program, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1)):
        self.vao = vao
        self.program = program
        self.position = glm.vec3(position)
        self.rotation = glm.vec3([glm.radians(a) for a in rotation])
        self.scale = glm.vec3(scale)

    def get_model_matrix(self):
        m = glm.mat4()
        m = glm.translate(m, self.position)
        m = glm.rotate(m, self.rotation.x, glm.vec3(1, 0, 0))
        m = glm.rotate(m, self.rotation.y, glm.vec3(0, 1, 0))
        m = glm.rotate(m, self.rotation.z, glm.vec3(0, 0, 1))
        m = glm.scale(m, self.scale)
        return m

    def update(self):
        self.program['m_model'].write(self.get_model_matrix())

    def render(self): 
        self.update()
        self.vao.render()
