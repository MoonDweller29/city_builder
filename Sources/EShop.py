from EButton import EButton
from GraphicsEngine import GraphicsEngine

from EntitySystem import Entity, EntitySystem

from Utils import *

class EShop(Entity):
    def __init__(self):
        super().__init__()

    def on_start(self):
        for x in range(3):
            for y in range(5): 
                EntitySystem().add_entity(EButton("CrystalMine", add((960, 180), (110 * x, 110 * y)), (100, 100)))

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GraphicsEngine().draw_rectangle((100, 100, 0), (900, 10), (360, 700))
        GraphicsEngine().draw_text((1060, 20), "Arial_20", (255, 255, 255), "Shop")