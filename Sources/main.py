import pygame
from GraphicsEngine import GraphicsEngine

from Utils import *

from EntitySystem import EntitySystem, Entity
from ETerrain import ETerrain

from EGrid import EGrid

from Debug import Debug
from ResourceManager import ResourceManager
from UserInput import UserInput
from EButton import EButton

GraphicsEngine().init_window([1280, 720], 'City Builder')

drawPosition = (0, 0)

fontArial = ResourceManager().get_font("Arial_20")
testImage = ResourceManager().get_image("CrystalMine")
testImage = ResourceManager().get_sprite_sheet("SP-Land", 2, 3)

EntitySystem().add_entity(ETerrain("CrystalMine", (10,10)))
EntitySystem().add_entity(EButton("Wood", (0, 0), (100, 100)))

# Run until the user asks to quit
running = True

lastFrameStartTime = pygame.time.get_ticks()
leftSimTime = 0

# @TODO Это желательно вынести в отдельный класс/файл
# Так чтобы из main только дергались функции FPS каунтера
# FPS counting stuff

debugPanel = Debug("Arial_20")

while running:
    deltaTime = pygame.time.get_ticks() - lastFrameStartTime
    leftSimTime += deltaTime

    lastFrameStartTime = pygame.time.get_ticks()

    while leftSimTime > debugPanel.TICK_MS:
        # Input
        UserInput().update()
        if UserInput().is_exit():
            running = False

        if UserInput().is_mouse_down():
            drawPosition = UserInput().get_mouse_position()
        
        # Update

        EntitySystem().update()

        debugPanel.update()

        leftSimTime -= debugPanel.TICK_MS

    #Render

    GraphicsEngine().clear_screen((0, 64, 0))

    EntitySystem().draw()

    debugPanel.draw()

    # Draw a solid blue circle
    GraphicsEngine().draw_circle((0, 0, 255), drawPosition, 5)

    # Flip the display
    GraphicsEngine().display_flip()

# Done! Time to quit.
pygame.quit()