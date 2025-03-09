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
        
    def render(self):
        for obj in self.objects:
            obj.render()