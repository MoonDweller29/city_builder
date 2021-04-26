from EOnGrid import EOnGrid
from EntitySystem import EntitySystem
from UserInput import UserInput

from BuildingDatabase import BuildingDatabase

class EFakeBuilding(EOnGrid):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

        self.drawOrder = 800
        self.buildingName = ""

    def on_start(self):
        super().on_start()
        self.set_solid(False)

    def update(self):
        super().update()

        grid = EntitySystem().get_grid()
        userInput = UserInput()
        coord = grid.world_to_cell(userInput.get_mouse_position())

        if (not grid.is_colliding(coord, BuildingDatabase().get_building_mask(self.buildingName))):
            self.tint_color = (0, 255, 0)
        elif (userInput.is_ui()):
            self.tint_color = (100, 100, 100)
        else:
            self.tint_color = (255, 0, 0)

        if (grid.is_inside(coord)):# and len(grid.contents[coord[0]][coord[1]]) <= 0):
            self.set_pos(coord)


    def draw(self):
        super().draw()