from entity_system import Entity
from utils import *

class Terrain(Entity):
    def __init__(self, screen, image, size):
        super().__init__()

        self.size = size
        self.image = image
        self.screen = screen

    def Update(self):
        super().Update()
        
        pass

    def Draw(self):
        super().Draw()

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                DrawImage(self.screen, self.image, add((100, 100), (64 * x, 64 * y)), (64, 64))
