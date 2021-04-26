from EntitySystem import EntitySystem, Entity

from GraphicsEngine import GraphicsEngine 
from UserInput import UserInput 

from BuildingFactory import GetBuilding

from EFakeBuilding import EFakeBuilding

class EBuilder(Entity):
    def __init__(self):
        super().__init__()
        
    def on_start(self):
        super().on_start()
        
        self.fakeBuilding = EntitySystem().add_entity(EFakeBuilding(0, 0, "CrystalMine")) 

    def update(self):
        super().update()

        grid = EntitySystem().get_grid()

        if UserInput().is_mouse_down():
            coord = grid.world_to_cell(UserInput().get_mouse_position())
            
            if (grid.is_inside(coord) and len(grid.contents[coord[0]][coord[1]]) <= 0):
                buildingId = EntitySystem().add_entity(GetBuilding("CrystalMine"))
                EntitySystem().get_entity(buildingId).set_pos(coord)

                #self.contents[coord[0]][coord[1]] = 255

    def draw(self):
        super().draw()