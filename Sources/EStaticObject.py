from EOnGrid import EOnGrid


class EStaticObject(EOnGrid):
    def __init__(self, x, y, sprite, spritePos=None):
        super().__init__(x, y, sprite, spritePos)

    def update(self):
        super().update()

    def draw(self):
        super().draw()
