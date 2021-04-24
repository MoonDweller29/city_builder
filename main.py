import pygame

from utils import *

from entity_system import EntitySystem, Entity
from terrain import Terrain

from debug import Debug

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

EntitySystem().AddEntity(Terrain(screen, myimage, (10,10)))
id = EntitySystem().AddEntity(Terrain(screen, myimage, (10,10)))
id = EntitySystem().AddEntity(Terrain(screen, myimage, (10,10)))
id = EntitySystem().AddEntity(Terrain(screen, myimage, (10,10)))

EntitySystem().GetEntity(id).drawOrder = -100

# Run until the user asks to quit
running = True

last_frame_time = pygame.time.get_ticks()
left_sim_time = 0
lag = 0.0

# @TODO Это желательно вынести в отдельный класс/файл
# Так чтобы из main только дергались функции FPS каунтера
# FPS counting stuff

debugPanel = Debug(screen, fontArial)

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_position = pygame.mouse.get_pos()

    delta_time = pygame.time.get_ticks() - last_frame_time
    left_sim_time += delta_time

    last_frame_time = pygame.time.get_ticks()

    while left_sim_time > debugPanel.TICK_MS:
        # Update

        EntitySystem().Update()

        debugPanel.Update()

        left_sim_time -= debugPanel.TICK_MS

    #Render

    # Fill the background with white
    screen.fill((0, 64, 0))

    EntitySystem().Draw()

    debugPanel.Draw()

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), draw_position, 5)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()