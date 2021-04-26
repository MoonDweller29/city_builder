from EntitySystem import EntitySystem
from EActor import EActor

from GraphicsEngine import GraphicsEngine

class EOnGrid(EActor):
    def __init__(self, x, y, sprite):
        cellSize = EntitySystem().get_grid().cellSize

        super().__init__(x * cellSize, y * cellSize, (cellSize, cellSize) , sprite)

        self.__cell_x = x
        self.__cell_y = y

    # @TODO ГОВНО ГОВНА
    def on_start(self):
        self.set_pos((self.__cell_x, self.__cell_y))

    def set_pos(self, coord):
        EntitySystem().get_grid().on_remove_from_cell(self.id)

        self.__cell_x = coord[0]
        self.__cell_y = coord[1]

        cellSize = EntitySystem().get_grid().cellSize
        origin   = EntitySystem().get_grid().origin

        self.x = self.__cell_x * cellSize + origin[0]
        self.y = self.__cell_y * cellSize + origin[1]

        EntitySystem().get_grid().on_add_to_cell(self.id)

    def get_pos(self):
        return (self.__cell_x, self.__cell_y)

    def on_destroy(self):
        EntitySystem().get_grid().on_remove_from_cell(self.id)

    def update(self):
        super().update()

    def draw(self):
        super().draw()