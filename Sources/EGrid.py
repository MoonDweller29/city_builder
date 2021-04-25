from Utils import *

from EntitySystem import Entity
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput

class EGrid(Entity):
    def __init__(self, origin, size, cellSize):
        super().__init__()

        self.origin = origin
        self.size = size
        self.cellSize = cellSize

        self.contents = []

        for x in range(size[0]):
            self.contents.append([])

            for y in range(size[1]):
                self.contents[x].append(0)

    def is_inside(self, coord):
        return coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size[0] and coord[1] < self.size[1]

    def world_to_cell(self, worldCoord):
        return toInt(div(sub(worldCoord, self.origin), (self.cellSize, self.cellSize)))

    def cell_to_world(self, coord):
        return add(mul(coord, (self.cellSize, self.cellSize)), self.origin)

    def cell_to_world_center(self, coord):
        return add(mul(coord, (self.cellSize, self.cellSize)), add(self.origin, (self.cellSize * 0.5, self.cellSize * 0.5)))

    def get_cell_world(self, worldCoord):
        return self.get_cell(self.world_to_cell(worldCoord))

    def get_cell(self, coord):
        if (not self.is_inside(coord)):
            return None
        else:
            return self.contents[coord[0]][coord[1]]


    def update(self):
        super().update()

        if UserInput().is_mouse_down():
            coord = self.world_to_cell(UserInput().get_mouse_position())
            
            if (self.is_inside(coord)):
                self.contents[coord[0]][coord[1]] = 255

    def draw(self):
        super().draw()

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                GraphicsEngine().draw_circle((0, self.get_cell((x, y)), 0), toInt(self.cell_to_world_center((x, y))), (self.cellSize >> 1) - 10)