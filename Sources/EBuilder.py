from EntitySystem import EntitySystem, Entity

from GraphicsEngine import GraphicsEngine 
from UserInput import UserInput 

from BuildingDatabase import BuildingDatabase

from EFakeBuilding import EFakeBuilding

class EBuilder(Entity):
    def __init__(self):
        super().__init__()
        
    def on_start(self):
        super().on_start()

        self.buildingName = ""

        self.fakeBuilding = EntitySystem().add_entity(EFakeBuilding(0, 0, "CrystalMine")) 

        EntitySystem().get_entity(self.fakeBuilding).disable()

    def start_building(self, buildingName):
        self.buildingName = buildingName
        
        EntitySystem().get_entity(self.fakeBuilding).enable()
        EntitySystem().get_entity(self.fakeBuilding).sprite = buildingName

    def update(self):
        super().update()

        grid = EntitySystem().get_grid()

        if UserInput().is_mouse_down() and self.buildingName != "":
            coord = grid.world_to_cell(UserInput().get_mouse_position())
            
            if (grid.is_inside(coord) and grid.is_cell_free(coord)):
                buildingId = EntitySystem().add_entity(BuildingDatabase().GetBuilding(self.buildingName))
                EntitySystem().get_entity(buildingId).set_pos(coord)

                EntitySystem().get_entity(self.fakeBuilding).disable()

    def draw(self):
        super().draw()