from EButton import EButton
from GraphicsEngine import GraphicsEngine

from EntitySystem import Entity, EntitySystem

from Utils import *

class EResourcePanel(Entity):
    def __init__(self):
        super().__init__()

        self.drawOrder = 1001

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((0, 0, 0), (0, 0), (1280, 40))
        GraphicsEngine().draw_text((10, 10), "Arial_20", (255, 255, 255), "Gold: 100")