import pygame

from GraphicsEngine import GraphicsEngine

# @TODO вынести нахер шрифт и скрин отсюда в централизованную точку
class Debug:
    def __init__(self, font):
        self.TARGET_FPS = 60.0
        self.TICK_MS = 1000.0 / self.TARGET_FPS

        self.updateFps = 0
        self.fps = 0
        self.lastFpsCountTime = pygame.time.get_ticks()
        self.FPS_COUNT_CD = 300
        self.updateFrames = 0
        self.frames = 0

        self.font = font

    def update(self):
        self.updateFrames += 1 

        if pygame.time.get_ticks() - self.lastFpsCountTime > self.FPS_COUNT_CD:
            deltaTime = pygame.time.get_ticks() - self.lastFpsCountTime

            self.fps = self.frames / deltaTime * 1000.0
            self.updateFps = self.updateFrames / deltaTime * 1000.0

            self.lastFpsCountTime = pygame.time.get_ticks()
            self.frames = 0
            self.updateFrames = 0

    def draw(self):
        self.frames += 1

        renderer = GraphicsEngine()
        renderer.draw_text((1100, 10), self.font, (0, 255, 0), "FPS:  " + str(int(self.fps)))
        renderer.draw_text((1100, 30), self.font, (0, 255, 0), "UFPS: " + str(int(self.updateFps)))
