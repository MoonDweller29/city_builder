from .EOnGrid import EOnGrid
from .EntitySystem import ES
from .GraphicsEngine import GE
from .UserInput import UserInput


class EFakeBuilding(EOnGrid):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

        self.drawOrder = 800
        self.cellSize = ES().get_grid().cellSize
        self.tint_color = (255, 255, 255)
        self.radius = 0

    def on_start(self):
        super().on_start()
        self.set_solid(False)

    def update(self):
        super().update()

        grid = ES().get_grid()
        userInput = UserInput()
        coord = grid.world_to_cell(userInput.get_mouse_position())

        if (userInput.is_ui()):
            self.tint_color = (100, 100, 100)
        elif (grid.is_cell_free(self.get_pos())):
            self.tint_color = (0, 255, 0)
        else:
            self.tint_color = (255, 0, 0)

        if (grid.is_inside(coord) and not userInput.is_ui()):  # and len(grid.contents[coord[0]][coord[1]]) <= 0):
            self.set_pos(coord)
        else:
            self.x = userInput.get_mouse_position()[0] - 32
            self.y = userInput.get_mouse_position()[1] - 32

    def draw(self):
        grid = ES().get_grid()
        coord = grid.world_to_cell(UserInput().get_mouse_position())

        if self.radius > 0 and grid.is_inside(coord) and not UserInput().is_ui():
            lt = (self.x - self.cellSize * self.radius, self.y - self.cellSize * self.radius)
            rectSize = (self.cellSize * (2 * self.radius + 1), self.cellSize * (2 * self.radius + 1))
            GE().draw_rectangle(self.tint_color, lt, rectSize, 100)
        super().draw()
