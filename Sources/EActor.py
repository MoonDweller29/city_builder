from EntitySystem import Entity
from GraphicsEngine import GraphicsEngine

class EActor(Entity):
    def __init__(self, x, y, size, sprite):
        super().__init__()

        self.x = x
        self.y = y

        self.size = size

        self.sprite = sprite

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GraphicsEngine().draw_image(self.sprite, (self.x, self.y), self.size)