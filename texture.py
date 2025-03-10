import pygame as pg
import moderngl as mgl
import os


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img1.png')
        self.textures[1] = self.get_texture(path='textures/test.png')
        self.textures[2] = self.get_texture(path='textures/notex.png')
        #self.textures['cat1'] = self.get_texture(path= 'objects/loli/model.jpg')
        self.textures['cat'] = self.load_texture_mtl('objects/vtuber/ImageToStl.com_fak3rR_.vrm.obj', tex_id='cat')
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'), dtype='f1')
        
        #mipimaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        
        #AF
        texture.anisotropy = 32.0
        
        return texture
    
    def load_texture_mtl(self, obj_path, tex_id):
        """Loads textures from the .mtl file and stores them under tex_id."""
        mtl_path = obj_path.replace('.obj', '.mtl')  # Get corresponding .mtl file
        if not os.path.exists(mtl_path):
            print(f"MTL file not found: {mtl_path}")
            return None

        material_textures = {}
        material_name = None

        with open(mtl_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue

                if parts[0] == 'newmtl':
                    # Start of a new material
                    material_name = parts[1]

                elif parts[0] == 'map_Kd' and material_name:
                    # Diffuse texture found
                    texture_path = os.path.join(os.path.dirname(mtl_path), parts[1])  # Absolute path

                    if os.path.exists(texture_path):
                        material_textures[material_name] = self.get_texture(texture_path)
                    else:
                        print(f"Warning: Texture file not found: {texture_path}")

        if material_textures:
            self.textures[tex_id] = material_textures  # Store multiple textures under tex_id
            print(f"Loaded {len(material_textures)} textures for {tex_id} from {mtl_path}")
            return material_textures

        return None
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]