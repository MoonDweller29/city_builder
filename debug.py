import pygame

from GraphicsEngine import GraphicsEngine

# @TODO вынести нахер шрифт и скрин отсюда в централизованную точку
class Debug:
    def __init__(self, font):
        self.TARGET_FPS = 60.0
        self.TICK_MS = 1000.0 / self.TARGET_FPS

        self.update_fps = 0
        self.fps = 0
        self.last_fps_count_time = pygame.time.get_ticks()
        self.FPS_COUNT_CD = 300
        self.update_frames = 0
        self.frames = 0

        self.font = font

    def Update(self):
        self.update_frames += 1 

        if pygame.time.get_ticks() - self.last_fps_count_time > self.FPS_COUNT_CD:
            delta_time = pygame.time.get_ticks() - self.last_fps_count_time

            self.fps = self.frames / delta_time * 1000.0
            self.update_fps = self.update_frames / delta_time * 1000.0

            self.last_fps_count_time = pygame.time.get_ticks()
            self.frames = 0
            self.update_frames = 0

    def Draw(self):
        self.frames += 1

        renderer = GraphicsEngine()
        renderer.draw_text((1100, 10), self.font, (0, 255, 0), "FPS:  " + str(int(self.fps)))
        renderer.draw_text((1100, 30), self.font, (0, 255, 0), "UFPS: " + str(int(self.update_fps)))
