from EOnGrid import EOnGrid

class EBuilding(EOnGrid):
    def __init__(self, x, y, sprite, spriteScale=1):
        super().__init__(x, y, sprite, spriteScale)

    def update(self):
        super().update()

    def draw(self):
        super().draw()