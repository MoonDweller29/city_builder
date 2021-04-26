import pygame

from EButton import EButton
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput

from EntitySystem import EntitySystem

class EShopButton(EButton):
    def __init__(self, name, position, size, buildingName, shopPanel):
        super().__init__(name, position, size)

        self.buildingName = buildingName
        self.shopPanel = shopPanel
    
    def update(self):
        super().update()
        if EntitySystem().get_entity(self.shopPanel).can_buy(self.buildingName):
            self.set_greyed(False)
        else:
            self.set_greyed(True)

    def on_pressed(self):
        super().on_pressed()

        EntitySystem().get_entity(self.shopPanel).try_buying(self.buildingName) 