import math
import random

import pygame

from EStaticObject import EStaticObject


class ETree(EStaticObject):
    def __init__(self, x, y, sprite, spritePos):
        super().__init__(x, y, sprite, spritePos)

        self.seed = random.random() * 12331

    def on_start(self):
        super().on_start()

        self.y_start = self.y

    def update(self):
        super().update()

    def draw(self):
        self.size = (self.size[0], int(math.sin(self.seed + pygame.time.get_ticks() / 1200.0) * 3 + 32))

        self.y = self.y_start - self.size[1] + 32

        super().draw()
