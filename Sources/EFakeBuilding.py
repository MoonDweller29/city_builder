from EOnGrid import EOnGrid
from EntitySystem import EntitySystem
from UserInput import UserInput

class EFakeBuilding(EOnGrid):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

        self.drawOrder = 800

    def on_start(self):
        super().on_start()
        self.set_solid(False)

    def update(self):
        super().update()

        grid = EntitySystem().get_grid()
        userInput = UserInput()
        coord = grid.world_to_cell(userInput.get_mouse_position())

        if (userInput.is_ui()):
            self.tint_color = (100, 100, 100)
        elif (grid.is_cell_free(self.get_pos())):
            self.tint_color = (0, 255, 0)
        else:
            self.tint_color = (255, 0, 0)

        if (grid.is_inside(coord)):# and len(grid.contents[coord[0]][coord[1]]) <= 0):
            self.set_pos(coord)


    def draw(self):
        super().draw()