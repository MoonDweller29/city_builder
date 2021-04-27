import pygame
from ResourceManager import ResourceManager

from Utils import *

class GraphicsEngine:
    ##############################################################################
    # public interface
    ##############################################################################

    def init_window(self, resolution, title):
        pygame.display.set_caption(title)
        self.__screen = pygame.display.set_mode(resolution)
        self.__renderTarget = self.__screen
        self.__renderTargetRect = self.__screen.get_rect()

    def clear_screen(self, color):
        self.__renderTarget.fill(color)

    def display_flip(self):
        self.drawCalls = 0
        self.culledDrawCalls = 0

        pygame.display.flip()

    def set_render_target(self, surface = None):
        if surface is None:
            surface = self.__screen

        self.__renderTarget = surface
        self.__renderTargetRect = surface.get_rect()

    # draw methods

    def draw_image_bot(self, name, position, size, tint_color=None, tint_flag=pygame.BLEND_RGBA_MULT):
        self.draw_image(name, sub(position, size), size, tint_color=tint_color, tint_flag= tint_flag)

    def draw_image_centered(self, name, position, size, tint_color=None, tint_flag=pygame.BLEND_RGBA_MULT):
        self.draw_image(name, sub(position, div(size, (2, 2))), size, tint_color=tint_color, tint_flag= tint_flag)

    def draw_image(self, name, position, size, alpha=255, tint_color=None, tint_flag=pygame.BLEND_RGBA_MULT):
        self.drawCalls += 1

        tmp = pygame.transform.scale(ResourceManager().get_image(name), size)

        rect = tmp.get_rect()
        rect = rect.move(position)

        # , special_flags=pygame.BLEND_RGBA_ADD
        #
        if (alpha == 255):
            tmp.set_alpha(alpha)
        else: 
            tmp.set_alpha(None)

        if (not tint_color is None):
            tint_image = pygame.Surface(size)
            tint_image.fill(tint_color)
            tmp.blit(tint_image, (0, 0), special_flags=tint_flag)
        
        # @TODO alpha не работает у AlexHonor провить эту дичь
        #tmp.set_alpha(128)

        self.__renderTarget.blit(tmp, rect)

    def draw_sprite(self, name, tileCoord, position, size, alpha=255, tint_color=None, tint_flag=pygame.BLEND_RGBA_MULT):
        self.drawCalls += 1

        rect = pygame.Rect(position[0], position[1], size[0], size[1])
        if (rect.colliderect(self.__renderTargetRect)):
            tmp = pygame.transform.scale(
                ResourceManager().get_sprite_sheet(name, tileCoord[0], tileCoord[1]), size
            )
            if (alpha == 255):
                tmp.set_alpha(alpha)
            else:
                tmp.set_alpha(None)

            if (not tint_color is None):
                tint_image = pygame.Surface(size)
                tint_image.fill(tint_color)
                tmp.blit(tint_image, (0, 0), special_flags=tint_flag)

            self.__renderTarget.blit(tmp, rect)
        else:
            self.culledDrawCalls += 1

    # @TODO проверить memory leak texture surface возвращаемого из метода ренедер
    def draw_text(self, position, fontName, color, text):
        self.drawCalls += 1
        self.__renderTarget.blit(ResourceManager().get_font(fontName).render(text, False, color), position)

    def draw_circle(self, color, pos, radius):
        self.drawCalls += 1
        pygame.draw.circle(self.__renderTarget, color, pos, radius)


    def draw_rectangle(self, color, lt, rectSize, alpha=None):
        self.drawCalls += 1
        # pygame.draw.rect(self.__renderTarget, color, pygame.Rect(lt[0], lt[1], rectSize[0], rectSize[1]))

        s = pygame.Surface(rectSize)
        if not (alpha is None):
            s.set_alpha(alpha)
        s.fill(color)
        self.__renderTarget.blit(s, lt)

    def draw_surface(self, surface, lt):
        self.drawCalls += 1
        self.__renderTarget.blit(surface, lt)


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

        self.drawCalls = 0
        self.culledDrawCalls = 0

        if not pygame.get_init():
            pygame.init()
            pygame.font.init()