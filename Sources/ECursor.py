from Utils import ease_out_elastic, lerp
from UserInput import UserInput, MouseButton
from EActor import EActor
import pygame


class ECursor(EActor):
    def __init__(self):
        super().__init__(0, 0, (32, 32), "Cursor")

        self.startTime = -10000
        self.animationTime = 520

        self.drawOrder = 100000

    def update(self):
        super().update()

        if (UserInput().is_mouse_down(MouseButton.LEFT) or UserInput().is_ui_mouse_down(MouseButton.LEFT)):
            self.startTime = pygame.time.get_ticks()

    def draw(self):
        super().draw()

        (self.x, self.y) = UserInput().get_mouse_position()

        size = int(lerp(ease_out_elastic((pygame.time.get_ticks() - self.startTime) / self.animationTime), 16, 32))

        self.size = (size, size)
