import pygame
from ResourceManager import ResourceManager

class GraphicsEngine:
    ##############################################################################
    # public interface
    ##############################################################################

    def init_window(self, resolution, title):
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(resolution)
        self.__screenRect = self.screen.get_rect()

    def clear_screen(self, color):
        self.screen.fill(color)

    def display_flip(self):
        self.drawCalls = 0
        self.culledDrawCalls = 0

        pygame.display.flip()

    # draw methods

    def draw_image(self, name, position, size):
        self.drawCalls += 1

        tmp = pygame.transform.scale(ResourceManager().get_image(name), size)

        rect = tmp.get_rect()
        rect = rect.move(position)

        self.screen.blit(tmp, rect)

    def draw_sprite(self, name, tileCoord, position, size):
        self.spriteDrawCallsCount += 1

        rect = pygame.Rect(position[0], position[1], size[0], size[1])
        if (rect.colliderect(self.__screenRect)):
            tmp = pygame.transform.scale(
                ResourceManager().get_sprite_sheet(name, tileCoord[0], tileCoord[1]), size
            )
            self.screen.blit(tmp, rect)
        else:
            self.culledSprites += 1
        # rect = rect.move(position)


    # @TODO проверить memory leak texture surface возвращаемого из метода ренедер
    def draw_text(self, position, fontName, color, text):
        self.drawCalls += 1
        self.screen.blit(ResourceManager().get_font(fontName).render(text, False, color), position)

    def draw_circle(self, color, pos, radius):
        self.drawCalls += 1
        pygame.draw.circle(self.screen, color, pos, radius)


    def draw_rectangle(self, color, lt, rb):
        self.drawCalls += 1
        pygame.draw.rect(self.screen, color, pygame.Rect(lt[0], lt[1], rb[0], rb[1]))

    ##############################################################################
    # private interface
    ##############################################################################
    __instance = None
    __inited = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GraphicsEngine, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if GraphicsEngine.__inited:
            return
        GraphicsEngine.__inited = True
        self.spriteDrawCallsCount = 0
        self.culledSprites = 0

        self.drawCalls = 0
        self.culledDrawCalls = 0

        if not pygame.get_init():
            pygame.init()
            pygame.font.init()