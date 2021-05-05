import pygame

from .EntitySystem import ES, Entity
from .GraphicsEngine import GE
from .UserInput import UserInput


class Debug(Entity):
    def __init__(self, fontName, TICK_MS):
        super().__init__()

        self.TICK_MS = TICK_MS

        self.updateFps = 0
        self.fps = 0
        self.lastFpsCountTime = pygame.time.get_ticks()
        self.FPS_COUNT_CD = 300
        self.updateFrames = 0
        self.frames = 0

        self.drawOrder = 10000

        self.fontName = fontName

        self.active = False

    def update(self):
        super().update()

        self.updateFrames += 1

        if UserInput().is_key_down(pygame.K_F1):
            self.active = not self.active

        if pygame.time.get_ticks() - self.lastFpsCountTime > self.FPS_COUNT_CD:
            deltaTime = pygame.time.get_ticks() - self.lastFpsCountTime

            self.fps = self.frames / deltaTime * 1000.0
            self.updateFps = self.updateFrames / deltaTime * 1000.0

            self.lastFpsCountTime = pygame.time.get_ticks()
            self.frames = 0
            self.updateFrames = 0

    def draw(self):
        super().draw()

        self.frames += 1

        if (not self.active):
            return

        renderer = GE()

        GE().draw_rectangle((1090, 5), (1260, 100), (0, 0, 0))

        renderer.draw_text(self.fontName, (1100, 10), (0, 255, 0), "FPS:  " + str(int(self.fps)))
        renderer.draw_text(self.fontName, (1100, 30), (0, 255, 0), "UFPS: " + str(int(self.updateFps)))
        renderer.draw_text(self.fontName, (1100, 50), (0, 255, 0),
                           "Entities: " + str(int(len(ES().entities))))
        drawCallCount = GE().drawCalls
        renderer.draw_text(self.fontName, (1100, 70), (0, 255, 0),
                           f"DCalls: {drawCallCount - GE().culledDrawCalls}/{drawCallCount}")
