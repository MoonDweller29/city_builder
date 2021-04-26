from EntitySystem import Entity
from Utils import *
from GraphicsEngine import GraphicsEngine

class ETerrain(Entity):
    def __init__(self, name, size):
        super().__init__()

        self.size = size
        self.__name = name

    def update(self):
        super().update()
        
        pass

    def draw(self):
        super().draw()

        renderer = GraphicsEngine()
        
        #for x in range(self.size[0]):
        #    for y in range(self.size[1]):
        #        renderer.draw_image(self.__name, add((100, 100), (64 * x, 64 * y)), (64, 64))
