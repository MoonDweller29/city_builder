import pygame

from EOnGrid import EOnGrid
from Utils import lerp, ease_out_elastic


class EBuilding(EOnGrid):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

        self.startTime = pygame.time.get_ticks()
        self.animationLength = 500
        self.animationAmlitude = 20

    def update(self):
        super().update()

    def draw(self):
        self.size = (self.size[0], int(
            lerp(1 - ease_out_elastic((pygame.time.get_ticks() - self.startTime) / self.animationLength),
                 self.startSize[1], self.startSize[1] + self.animationAmlitude)))

        super().draw()

    def on_start(self):
        self.startSize = self.size

        super().on_start()
