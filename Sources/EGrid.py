from EntitySystem import Entity

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
                self.contents[x].append([])

    def world_to_cell(self, worldCoord):
        return div(sub(worldCoord, self.origin), (self.cellSize, self.cellSize))

    def cell_to_world(self, worldCoord):
        return int(add(mul(worldCoord, (self.cellSize, self.cellSize)), self.origin))

    def update(self):
        super().update()

    def draw(self):
        super().draw()