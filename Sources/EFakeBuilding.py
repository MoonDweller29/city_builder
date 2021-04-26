from EOnGrid import EOnGrid

class EFakeBuilding(EOnGrid):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

    def update(self):
        super().update()

    def draw(self):
        super().draw()