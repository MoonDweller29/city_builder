from EButton import EButton
from GraphicsEngine import GraphicsEngine

from EntitySystem import Entity, EntitySystem

from Utils import *

class EResourcePanel(Entity):
    def __init__(self):
        super().__init__()

        self.__init_resources()

        self.drawOrder = 1001


    def __init_resources(self):
        self.resources = {}
        self.resourcesInfo = {}

        self.resources["Wood"] = 100
        self.resourcesInfo["Wood"] = ("Wood", 0)

        self.resources["CrystalMine"] = 2
        self.resourcesInfo["CrystalMine"] = ("CrystalMine", 0)

    def update(self):
        super().update()

        #self.wood += 1

    def draw_resource(self, id, sprite, text):
        GraphicsEngine().draw_image_centered(sprite, add((20, 20), (id * 100, 0)), (32, 32))
        GraphicsEngine().draw_text(add((40, 10), (id * 100, 0)), "Arial_20", (255, 255, 255), text)

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((0, 0, 0), (0, 0), (1280, 40))

        id = 0
        for k, v in self.resourcesInfo.items():
            self.draw_resource(id, v[0], str(self.resources[k]))
            
            id += 1
