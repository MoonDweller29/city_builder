import pygame

from .Debug import Debug
from .ECursor import ECursor
from .EGrid import EGrid
from .EResourcePanel import EResourcePanel
from .EShop import EShop
from .ETerrain import ETerrain
from .EntitySystem import ES
from .GraphicsEngine import GE
from .RootPath import RootPath
from .UserInput import UserInput


def app():
    GE().init_window([1280, 720], 'City Builder')

    terrainOrigin = (0, 0)
    terrainTileSize = 40
    terrain = ETerrain(RootPath().create_path("Resources/Maps/test_map.png"),
                       origin=terrainOrigin,
                       tileSize=terrainTileSize)

    ES().add_entity(terrain)
    ES().gridId = ES().add_entity(EGrid(terrainOrigin, terrain.get_size(), terrainTileSize))

    grid = ES().get_entity(ES().gridId)

    terrain.fill_grid(grid)

    ES().add_entity(EResourcePanel())
    ES().add_entity(EShop())

    ES().add_entity(ECursor())

    TARGET_FPS = 60.0
    TICK_MS = 1000.0 / TARGET_FPS

    ES().add_entity(Debug("Arial_20", TICK_MS))

    print(grid.world_to_cell(grid.cell_to_world((3, 3))))

    # Run until the user asks to quit
    running = True

    lastFrameStartTime = pygame.time.get_ticks()
    leftSimTime = 0

    pygame.mouse.set_visible(False)

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

            ES().update()

            leftSimTime -= TICK_MS

        # Render
        GE().clear_screen((36, 159, 222))

        ES().draw()

        # Flip the display
        GE().display_flip()

    # Done! Time to quit.
    pygame.quit()
