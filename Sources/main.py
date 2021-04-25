import pygame
from GraphicsEngine import GraphicsEngine

from Utils import *

from EntitySystem import EntitySystem, Entity
from ETerrain import ETerrain

from EGrid import EGrid

from Debug import Debug
from ResourceManager import ResourceManager

GraphicsEngine().init_window([1280, 720], 'City Builder')

drawPosition = (0, 0)

fontArial = ResourceManager().get_font("Arial_20")
testImage = ResourceManager().get_image("CrystalMine")
testImage = ResourceManager().get_sprite_sheet("SP-Overworld", 2, 3)

terrain = ETerrain("Resources/Maps/test_map.png", (32,32))
EntitySystem().add_entity(terrain)

# Run until the user asks to quit
running = True

lastFrameStartTime = pygame.time.get_ticks()
leftSimTime = 0

# @TODO Это желательно вынести в отдельный класс/файл
# Так чтобы из main только дергались функции FPS каунтера
# FPS counting stuff

debugPanel = Debug("Arial_20")

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawPosition = pygame.mouse.get_pos()

    deltaTime = pygame.time.get_ticks() - lastFrameStartTime
    leftSimTime += deltaTime

    lastFrameStartTime = pygame.time.get_ticks()

    while leftSimTime > debugPanel.TICK_MS:
        # Update

        EntitySystem().update()

        debugPanel.update()

        leftSimTime -= debugPanel.TICK_MS

    #Render

    GraphicsEngine().clear_screen((0, 30, 0))
    GraphicsEngine().clearStats()
    EntitySystem().draw()

    debugPanel.draw()

    # Draw a solid blue circle
    GraphicsEngine().draw_circle((0, 0, 255), drawPosition, 5)

    # Flip the display
    GraphicsEngine().display_flip()
    # print(f"{GraphicsEngine().culledSprites} / {GraphicsEngine().spriteDrawCallsCount}")

# Done! Time to quit.
pygame.quit()