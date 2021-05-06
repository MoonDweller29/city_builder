from .EActor import EActor
from .EntitySystem import ES


class EOnGrid(EActor):
    def __init__(self, x, y, sprite, spritePos=None):
        cellSize = ES().get_grid().cellSize

        super().__init__(x * cellSize, y * cellSize, (cellSize, cellSize), sprite, spritePos)

        self.__cell_x = x
        self.__cell_y = y

        self.is_solid = True

    def set_solid(self, v):
        if v != self.is_solid:
            self.is_solid = v
            if v:
                ES().get_grid().on_add_to_cell(self.id)
            else:
                ES().get_grid().on_remove_from_cell(self.id)

    # @TODO Рефакторить!
    def on_start(self):
        self.set_pos((self.__cell_x, self.__cell_y))

    def set_pos(self, coord):
        if (self.is_solid):
            ES().get_grid().on_remove_from_cell(self.id)

        self.__cell_x = coord[0]
        self.__cell_y = coord[1]

        cellSize = ES().get_grid().cellSize
        origin = ES().get_grid().origin

        self.x = self.__cell_x * cellSize + origin[0]
        self.y = self.__cell_y * cellSize + origin[1]

        if (self.is_solid):
            ES().get_grid().on_add_to_cell(self.id)

    def get_pos(self):
        return (self.__cell_x, self.__cell_y)

    def on_destroy(self):
        ES().get_grid().on_remove_from_cell(self.id)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
