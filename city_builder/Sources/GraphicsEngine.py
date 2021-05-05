import pygame

from .ResourceManager import ResourceManager
from enum import Enum


class VAlign(Enum):
    CENTER = 1
    C = 1

    BOTTOM = 2
    BOT = 2
    B = 2

    TOP = 3
    T = 3


class HAlign(Enum):
    CENTER = 1
    CTR = 1
    C = 1

    LEFT = 2
    L = 2

    RIGHT = 3
    R = 3


def GE():
    return GraphicsEngine()


class GraphicsEngine:
    ##############################################################################
    # public interface
    ##############################################################################

    def init_window(self, resolution, title):
        pygame.display.set_caption(title)
        self.__screen = pygame.display.set_mode(resolution)
        self.__renderTarget = self.__screen
        self.__renderTargetRect = self.__screen.get_rect()

        self.vfunc = {
            VAlign.TOP   : self.__vtop_position,
            VAlign.CENTER: self.__vcenter_position,
            VAlign.BOTTOM: self.__vbot_position
        }

        self.hfunc = {
            HAlign.LEFT  : self.__hleft_position,
            HAlign.CENTER: self.__hcenter_position,
            HAlign.RIGHT : self.__hright_position
        }

    def clear_screen(self, color):
        self.__renderTarget.fill(color)

    def display_flip(self):
        self.drawCalls = 0
        self.culledDrawCalls = 0

        pygame.display.flip()

    def set_render_target(self, surface=None):
        if surface is None:
            surface = self.__screen

        self.__renderTarget = surface
        self.__renderTargetRect = surface.get_rect()

    # draw methods

    def draw_sprite(self, name, position, size, alpha=255, tileCoord=None, tint_color=None,
                    tint_flag=pygame.BLEND_RGBA_MULT, valign=VAlign.TOP, halign=HAlign.LEFT):
        if (tileCoord):
            self.__draw_tile(name, tileCoord, position, size, alpha=alpha, tint_color=tint_color,
                             tint_flag=tint_flag, valign=valign, halign=halign)
            return

        self.drawCalls += 1

        tmp = pygame.transform.scale(ResourceManager().get_image(name), size)

        position = self.__apply_alignment(position, size, halign, valign)

        rect = tmp.get_rect()
        rect = rect.move(position)

        # , special_flags=pygame.BLEND_RGBA_ADD
        #
        if (alpha == 255):
            tmp.set_alpha(alpha)
        else:
            tmp.set_alpha(None)

        if tint_color is not None:
            tint_image = pygame.Surface(size)
            tint_image.fill(tint_color)
            tmp.blit(tint_image, (0, 0), special_flags=tint_flag)

        self.__renderTarget.blit(tmp, rect)

    # @TODO проверить memory leak texture surface возвращаемого из метода ренедер
    def draw_text(self, fontName, position, color, text, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        font = ResourceManager().get_font(fontName)

        size = font.size(text)

        position = self.__apply_alignment(position, size, halign, valign)

        self.__renderTarget.blit(font.render(text, False, color), position)

    def draw_circle(self, position, radius, color, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        position = self.__apply_alignment(position, (radius, radius), halign, valign)

        pygame.draw.circle(self.__renderTarget, color, position, radius)

    def draw_rectangle(self, position, size, color, alpha=None, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1
        # pygame.draw.rect(self.__renderTarget, color, pygame.Rect(position[0], position[1], size[0], size[1]))

        position = self.__apply_alignment(position, size, halign, valign)

        s = pygame.Surface(size)
        if not (alpha is None):
            s.set_alpha(alpha)
        s.fill(color)
        self.__renderTarget.blit(s, position)

    def draw_surface(self, surface, position):
        self.drawCalls += 1
        self.__renderTarget.blit(surface, position)

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

    def __apply_alignment(self, position, size, halign, valign):
        return (self.hfunc[halign](position[0], size[0]), self.vfunc[valign](position[1], size[1]))

    def __hcenter_position(self, position, size):
        return position - size / 2

    def __hleft_position(self, position, size):
        return position

    def __hright_position(self, position, size):
        return position - size

    def __vcenter_position(self, position, size):
        return position - size / 2

    def __vbot_position(self, position, size):
        return position - size

    def __vtop_position(self, position, size):
        return position

    def __draw_tile(self, name, tileCoord, position, size, alpha=255, tint_color=None,
                    tint_flag=pygame.BLEND_RGBA_MULT, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        position = self.__apply_alignment(position, size, halign, valign)

        rect = pygame.Rect(position[0], position[1], size[0], size[1])

        if (rect.colliderect(self.__renderTargetRect)):
            tmp = pygame.transform.scale(
                ResourceManager().get_sprite_sheet(name, tileCoord[0], tileCoord[1]), size
            )
            if (alpha == 255):
                tmp.set_alpha(alpha)
            else:
                tmp.set_alpha(None)

            if tint_color is not None:
                tint_image = pygame.Surface(size)
                tint_image.fill(tint_color)
                tmp.blit(tint_image, (0, 0), special_flags=tint_flag)

            self.__renderTarget.blit(tmp, rect)
        else:
            self.culledDrawCalls += 1
