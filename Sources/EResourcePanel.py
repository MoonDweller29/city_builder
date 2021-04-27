from EButton import EButton
from GraphicsEngine import GraphicsEngine

from EntitySystem import Entity, EntitySystem

from Utils import *

class EResourcePanel(Entity):
    def __init__(self):
        super().__init__()

        self.__init_resources()

        self.name = "ResourcePanel"

        self.drawOrder = 1001


    def __init_resources(self):
        self.__resources = {}
        self.__resourcesInfo = {}

        self.__resources["People"] = 4
        self.__resourcesInfo["People"] = ("PeopleResource", 0)

        self.__resources["Food"] = 10
        self.__resourcesInfo["Food"] = ("Food", 0)

        self.__resources["Wood"] = 50
        self.__resourcesInfo["Wood"] = ("Wood", 0)

        self.__resources["Gold"] = 0
        self.__resourcesInfo["Gold"] = ("Gold", 0)

    def check_needed_resources(self, requiredResources):
        result = []

        for name, amount in requiredResources:
            result.append(self.__resources[name] >= amount)

        return result

    def get_resource_icon(self, name):
        return self.__resourcesInfo[name][0]

    def can_buy(self, requiredResources):
        for name, amount in requiredResources:
            if self.__resources[name] < amount:
                return False
        return True

    def spend(self, requiredResources):
        for name, amount in requiredResources:
            self.__resources[name] -= amount

    def add_resource(self, resourceName, count):
        self.__resources[resourceName] += count

    def update(self):
        super().update()

        #self.wood += 1

    def draw_resource(self, id, sprite, text):
        GraphicsEngine().draw_image_centered(sprite, add((20, 20), (id * 100, 0)), (32, 32))
        GraphicsEngine().draw_text(add((40, 10), (id * 100, 0)), "Arial_20", (255, 255, 255), text)

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((0, 0, 0), (0, 0), (1280, 40), alpha=200)

        id = 0
        for k, v in self.__resourcesInfo.items():
            self.draw_resource(id, v[0], str(self.__resources[k]))
            
            id += 1
