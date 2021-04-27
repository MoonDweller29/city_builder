from .EntitySystem import Entity
from .GraphicsEngine import GraphicsEngine


class EActor(Entity):
    def __init__(self, x, y, size, sprite, spritePos=None):
        super().__init__()

        self.x = x
        self.y = y

        self.size = size

        self.sprite = sprite
        self.spritePos = spritePos  # coord in spriteSheet
        self.tint_color = None

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        if self.spritePos is None:
            GraphicsEngine().draw_image(self.sprite, (self.x, self.y), self.size, tint_color=self.tint_color)
        else:
            GraphicsEngine().draw_sprite(
                self.sprite, self.spritePos, (self.x, self.y), self.size, tint_color=self.tint_color
            )
