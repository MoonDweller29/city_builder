import pygame

from utils import *

from entity import Entity
from terrain import Terrain

pygame.init()

pygame.display.set_caption('City Builder')

# @TODO Вот это дело надо собрать в общий скорее всего синглтон, чтобы не передавать в DrawText и DrawImage

screen = pygame.display.set_mode([1280, 720])

draw_position = (0, 0)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.

# @TODO нужно будет сделать систему подгрузки ресурсов
# 1) Шрифты, картинки, может звуки (потом)
# 2) Доступно из разных модулей программы (Давайте синглтон)
# 3) Понять че за дичь с pygame, там ресурсы создают сразу с локальными свойствами (Например, в грифт зашит размер)
# 4) Подумать о том, что потенциально мы можем грузить данные из zip потом. Просто код под эту замену подготовить.

fontArial = pygame.font.SysFont('Arial', 20)

myimage = pygame.image.load("Resources/Buildings/Mines/CrystalMine/CrystalMine.png")

entities = []

entities.append(Terrain(screen, myimage, (10,10)))

# Run until the user asks to quit
running = True

last_frame = pygame.time.get_ticks()
left_sim_time = 0
lag = 0.0

# @TODO Это желательно вынести в отдельный класс/файл
# Так чтобы из main только дергались функции FPS каунтера
# FPS counting stuff
TARGET_FPS = 60.0
TICK_MS = 1000.0 / TARGET_FPS

update_fps = 0
fps = 0
last_fps_count_time = pygame.time.get_ticks()
FPS_COUNT_CD = 300
update_frames = 0
frames = 0


while running:
    # Input
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_position = pygame.mouse.get_pos()

    left_sim_time += pygame.time.get_ticks() - last_frame
    last_frame = pygame.time.get_ticks()

    while left_sim_time > 0:
        # Update

        for e in entities:
            e.Update()

        update_frames += 1

        left_sim_time -= TICK_MS

    #Render

    # Fill the background with white
    screen.fill((0, 64, 0))

    for e in entities:
        e.Draw()

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), draw_position, 5)
    
    DrawImage(screen, myimage, (10, 10), (64, 64))

    frames += 1

    if pygame.time.get_ticks() - last_fps_count_time > FPS_COUNT_CD:
        delta_time = pygame.time.get_ticks() - last_fps_count_time

        fps = frames / delta_time * 1000.0
        update_fps = update_frames / delta_time * 1000.0

        last_fps_count_time = pygame.time.get_ticks()
        frames = 0
        update_frames = 0

    DrawText(screen, (1100, 10), fontArial, (0, 255, 0), "FPS:  " + str(int(fps)))
    DrawText(screen, (1100, 30), fontArial, (0, 255, 0), "UFPS: " + str(int(update_fps)))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()