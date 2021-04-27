import pygame
from GraphicsEngine import GraphicsEngine

from Utils import *

from EntitySystem import EntitySystem, Entity

from ETerrain import ETerrain
from EGrid import EGrid
from EActor import EActor
from EOnGrid import EOnGrid
from EBuilder import EBuilder
from EShop import EShop
from EResourcePanel import EResourcePanel

from Debug import Debug
from ResourceManager import ResourceManager
from UserInput import UserInput
from EButton import EButton

GraphicsEngine().init_window([1280, 720], 'City Builder')

fontArial = ResourceManager().get_font("Arial_20")

terrainOrigin = (64, 64)
terrainTileSize = 40
terrain = ETerrain("Resources/Maps/test_map.png", origin=terrainOrigin, tileSize=terrainTileSize)

EntitySystem().add_entity(terrain)
EntitySystem().gridId = EntitySystem().add_entity(EGrid(terrainOrigin, terrain.get_size(), terrainTileSize))

grid = EntitySystem().get_entity(EntitySystem().gridId)

terrain.fill_grid(grid)

EntitySystem().add_entity(EResourcePanel())
EntitySystem().add_entity(EShop())

TARGET_FPS = 60.0
TICK_MS = 1000.0 / TARGET_FPS

EntitySystem().add_entity(Debug("Arial_20", TICK_MS))

print(grid.world_to_cell(grid.cell_to_world((3, 3))))

# Run until the user asks to quit
running = True

lastFrameStartTime = pygame.time.get_ticks()
leftSimTime = 0

while running:
    deltaTime = pygame.time.get_ticks() - lastFrameStartTime
    leftSimTime += deltaTime

    lastFrameStartTime = pygame.time.get_ticks()

    # Update
    while leftSimTime > 0:
        # Input
        UserInput().update()

        if UserInput().is_exit():
            running = False

        EntitySystem().update()

        leftSimTime -= TICK_MS

    #Render
    GraphicsEngine().clear_screen((0, 30, 0))

    EntitySystem().draw()

    # Flip the display
    GraphicsEngine().display_flip()

# Done! Time to quit.
pygame.quit()
