import math
import random

import pygame

from .EStaticObject import EStaticObject
from .Utils import add, sub, mul


class ETree(EStaticObject):
    def __init__(self, x, y, sprite, spritePos):
        super().__init__(x, y, sprite, spritePos)

        self.seed = random.random() * 12331
        self.__startSize = self.size
        self.__origin = (0.5, 0.875)

    def on_start(self):
        super().on_start()

        self.__startPos = (self.x, self.y)

    def update(self):
        super().update()

    def draw(self):
        self.size = (
            self.size[0],
            int(math.sin(self.seed + pygame.time.get_ticks() / 1200.0) * 2 - 3 + self.__startSize[1])
        )

        originPos = add(self.__startPos, mul(self.__startSize, self.__origin))
        self.x, self.y = sub(originPos, mul(self.size, self.__origin))

        super().draw()
