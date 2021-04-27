import pygame

from EButton import EButton
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput

from EntitySystem import EntitySystem

from BuildingDatabase import BuildingDatabase
from EResourcePanel import EResourcePanel

from Utils import *

class EShopButton(EButton):
    def __init__(self, name, position, size, buildingName, shopPanel):
        super().__init__(name, position, size)

        self.buildingName = buildingName
        self.shopPanel = shopPanel
    
        self.__resourcePanel = EntitySystem().find_entity("ResourcePanel")

    def on_start(self):
        super().on_start()

        self.costs = BuildingDatabase().GetBuildingCosts(self.buildingName)

    def update(self):
        super().update()
        if EntitySystem().get_entity(self.shopPanel).can_buy(self.buildingName):
            self.set_greyed(False)
        else:
            self.set_greyed(True)

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((100, 100, 100), add(self._position, (-48, 32)), (80,20), alpha=100)

        resourceStatus = EntitySystem().get_entity(self.__resourcePanel).check_needed_resources(self.costs)

        for i in range(len(self.costs)):
            GraphicsEngine().draw_image(EntitySystem().get_entity(self.__resourcePanel).get_resource_icon(self.costs[i][0]), add(add(self._position, (-32, 25)), (38 * i, 0)), (24, 24))
            
            textColor = (255, 255, 255)

            if not resourceStatus[i]:
                textColor = (255, 45, 17)

            GraphicsEngine().draw_text(add(add(self._position, (-32 + 25, 25)), (38 * i, 0)), "ShopButtonFont", textColor, str(self.costs[i][1]))

    def on_pressed(self):
        super().on_pressed()

        EntitySystem().get_entity(self.shopPanel).try_buying(self.buildingName) 