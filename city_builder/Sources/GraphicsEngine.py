import pygame

from .ResourceManager import ResourceManager
from .Utils import sub, div, add, mul
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
            VAlign.TOP   : self.vtop_position,
            VAlign.CENTER: self.vcenter_position,
            VAlign.BOTTOM: self.vbot_position
        }

        self.hfunc = {
            HAlign.LEFT  : self.hleft_position,
            HAlign.CENTER: self.hcenter_position,
            HAlign.RIGHT : self.hright_position
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

    def hcenter_position(self, position, size):
        return position - size / 2

    def hleft_position(self, position, size):
        return position

    def hright_position(self, position, size):
        return position - size

    def vcenter_position(self, position, size):
        return position - size / 2

    def vbot_position(self, position, size):
        return position - size

    def vtop_position(self, position, size):
        return position

    def draw_image(self, name, position, size, alpha=255, tint_color=None, tint_flag=pygame.BLEND_RGBA_MULT, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        tmp = pygame.transform.scale(ResourceManager().get_image(name), size)

        x = self.hfunc[halign](position[0], size[0])
        y = self.vfunc[valign](position[1], size[1])

        rect = tmp.get_rect()
        rect = rect.move((x, y))

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

        # @TODO alpha не работает у AlexHonor провить эту дичь
        # tmp.set_alpha(128)

        self.__renderTarget.blit(tmp, rect)

    def draw_sprite(self, name, tileCoord, position, size, alpha=255, tint_color=None,
                    tint_flag=pygame.BLEND_RGBA_MULT, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        x = self.hfunc[halign](position[0], size[0])
        y = self.vfunc[valign](position[1], size[1])

        rect = pygame.Rect(x, y, size[0], size[1])
        
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

    # @TODO проверить memory leak texture surface возвращаемого из метода ренедер
    def draw_text(self, fontName, position, color, text, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        font = ResourceManager().get_font(fontName)

        size = font.size(text)

        x = self.hfunc[halign](position[0], size[0])
        y = self.vfunc[valign](position[1], size[1])

        self.__renderTarget.blit(font.render(text, False, color), (x, y))

    def draw_circle(self, position, radius, color, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1

        x = self.hfunc[halign](position[0], radius * 2)
        y = self.vfunc[valign](position[1], radius * 2)

        pygame.draw.circle(self.__renderTarget, color, (x, y), radius)

    def draw_rectangle(self, position, size, color, alpha=None, valign=VAlign.TOP, halign=HAlign.LEFT):
        self.drawCalls += 1
        # pygame.draw.rect(self.__renderTarget, color, pygame.Rect(position[0], position[1], size[0], size[1]))

        x = self.hfunc[halign](position[0], size[0])
        y = self.vfunc[valign](position[1], size[1])

        s = pygame.Surface(size)
        if not (alpha is None):
            s.set_alpha(alpha)
        s.fill(color)
        self.__renderTarget.blit(s, (x, y))

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
