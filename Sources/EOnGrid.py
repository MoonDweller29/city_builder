from EntitySystem import EntitySystem
from EActor import EActor

from GraphicsEngine import GraphicsEngine

class EOnGrid(EActor):
    def __init__(self, x, y, sprite, spritePos=None, mask=[[1]], spriteScale=1):
        cellSize = int(EntitySystem().get_grid().cellSize * spriteScale)

        super().__init__(x * cellSize, y * cellSize, (cellSize, cellSize), sprite, spritePos)

        self.__cell_x = x
        self.__cell_y = y

        self.mask = mask

    def set_solid(self, v):
        if v != self.is_solid:
            self.is_solid = v
            if v:
                for x in range(len(self.mask)):
                    for y in range(len(self.mask[0])):
                        EntitySystem().get_grid().on_add_to_cell_xy(self.id, self.__cell_x + x, self.__cell_y + y)
            else:
                for x in range(len(self.mask)):
                    for y in range(len(self.mask[0])):
                        EntitySystem().get_grid().on_remove_from_cell_xy(self.id, self.__cell_x + x, self.__cell_y + y)


    # @TODO Рефакторить!
    def on_start(self):
        self.is_solid = True

        self.set_pos((self.__cell_x, self.__cell_y))

    def set_pos(self, coord):
        if (self.is_solid):
            for x in range(len(self.mask)):
                for y in range(len(self.mask[0])):
                    EntitySystem().get_grid().on_remove_from_cell_xy(self.id, self.__cell_x + x, self.__cell_y + y)

        self.__cell_x = coord[0]
        self.__cell_y = coord[1]

        cellSize = EntitySystem().get_grid().cellSize
        origin   = EntitySystem().get_grid().origin

        self.x = self.__cell_x * cellSize + origin[0]
        self.y = self.__cell_y * cellSize + origin[1]

        if (self.is_solid):
            for x in range(len(self.mask)):
                for y in range(len(self.mask[0])):
                    EntitySystem().get_grid().on_add_to_cell_xy(self.id, self.__cell_x + x, self.__cell_y + y)


    def get_pos(self):
        return (self.__cell_x, self.__cell_y)

    def on_destroy(self):
        for x in range(len(self.mask)):
            for y in range(len(self.mask[0])):
                EntitySystem().get_grid().on_remove_from_cell_xy(self.id, self.__cell_x + x, self.__cell_y + y)

    def update(self):
        super().update()

    def draw(self):
        super().draw()