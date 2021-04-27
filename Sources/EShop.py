from EShopButton import EShopButton
from GraphicsEngine import GraphicsEngine

from EBuilder import EBuilder

from BuildingDatabase import BuildingDatabase

from EntitySystem import EntitySystem
from EUIElement import EUIElement

from Utils import *

class EShop(EUIElement):
    def __init__(self):
        super().__init__((900, 100), (360, 280))

    def on_start(self):
        self.builder = EntitySystem().add_entity(EBuilder())

        names = BuildingDatabase().GetAllBuildingNames()
        self.resourcePanel = EntitySystem().find_entity("ResourcePanel")

        id = 0

        for y in range(5):
            if id >= len(names):
                break

            for x in range(3): 
                if id >= len(names):
                    break
                EntitySystem().add_entity(EShopButton(names[id], add((965, 180), (110 * x, 110 * y)), (100, 100), names[id], self.id))
                id += 1

    def can_buy(self, buildingName):
        costs = BuildingDatabase().GetBuildingCosts(buildingName)
        return EntitySystem().get_entity(self.resourcePanel).can_buy(costs)

    def try_buying(self, buildingName):
        if self.can_buy(buildingName):
            EntitySystem().get_entity(self.builder).start_building(buildingName)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((99, 68, 57), self._position, self._size, alpha=245)
        #GraphicsEngine().draw_text(add(self._position, (10, 10)), "Arial_20", (255, 255, 255), "Shop")