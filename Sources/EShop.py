from EShopButton import EShopButton
from GraphicsEngine import GraphicsEngine

from EBuilder import EBuilder

from BuildingDatabase import BuildingDatabase

from EntitySystem import Entity, EntitySystem

from Utils import *

class EShop(Entity):
    def __init__(self):
        super().__init__()

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
                EntitySystem().add_entity(EShopButton(names[id], add((960, 180), (110 * x, 110 * y)), (100, 100), names[id], self.id))
                id += 1

    def try_buying(self, buildingName):
        costs = BuildingDatabase().GetBuildingCosts(buildingName)

        if (EntitySystem().get_entity(self.resourcePanel).can_buy(costs)):
            EntitySystem().get_entity(self.resourcePanel).spend(costs)
            EntitySystem().get_entity(self.builder).start_building(buildingName)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((100, 100, 0), (900, 10), (360, 700))
        GraphicsEngine().draw_text((1060, 20), "Arial_20", (255, 255, 255), "Shop")