from entity_system import Entity

class Grid(Entity):
    def __init__(self, origin, size, cellSize):
        super().__init__()

        self.origin = origin
        self.size = size
        self.cellSize = cellSize

        self.contents = []

        for x in range(size[0]):
            for y in range(size[1]):
                self.contents[x][y] = []

    def world_to_cell(self, worldCoord):
        return (worldCoord - self.origin) / (self.cellSize, self.cellSize)

    def Update(self):
        super().Update()

    def Draw(self):
        super().Draw()