from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        
    def app_objects(self, obj):
        self.objects.append(obj)
        
    def load(self):
        app = self.app
        add = self.app_objects
        
        
        add(Cube(app))
        add(Cube(app, tex_id=1, pos=(-2.5,0,0), rot=(45,0,0)))
        add(Cube(app, tex_id=1, pos=(2.5, 0,0), rot=(0,0,45)))
        
    def render(self):
        for obj in self.objects:
            obj.render()