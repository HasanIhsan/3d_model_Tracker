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

        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n,n,s):
                add(Cube(app, pos=(x, -s, z)))

        add(Cat(app, pos=(0,2,10), scale=(0.5,0.5,0.5)))

    def render(self):
        for obj in self.objects:
            obj.render()