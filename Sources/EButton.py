import pygame
from EUIElement import EUIElement
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput

from Utils import *

class EButton(EUIElement):
    def __init__(self, name, position, size):
        super().__init__()
        self.__textureName = name
        # @TODO: replace position and size by pygame.Rect
        self.__position = position
        self.__size = size
        self.__selected = False
        self.__greyed = False
        # @TODO: change drawOrder
        self.drawOrder = 500

        self.pressed_frames = 0

    # def set_greyed(self, v):
    #     if (self.__greyed != v):
    #         if (self.__greyed):
    #             se
    #         else:

    def update(self):
        super().update()
        input = UserInput()

        mousePosition = input.get_mouse_position()

        self.pressed_frames -= 1

        # @TODO: check collision by pygame rectangle
        if 0 < mousePosition[0] - self.__position[0] + self.__size[0] / 2.0 < self.__size[0] and \
            0 < mousePosition[1] - self.__position[1] + self.__size[1] / 2.0 < self.__size[1]:
            if (not self.__selected):
                self.__selected = True
                self.on_selected()
        else:
            if (self.__selected):
                self.__selected = False
                self.on_deselected()

        if input.is_mouse_down() and self.__selected:
            self.on_pressed()

    def on_selected(self):
        self.__size = toInt(mul(self.__size, (1.2, 1.2)))

    def on_deselected(self):
        self.__size = toInt(mul(self.__size, (1/1.2, 1/1.2)))

    def on_pressed(self):
        self.pressed_frames = 5

    def draw(self):
        super().draw()
        render = GraphicsEngine()

        # @TODO map tint colors and stuff?
        if self.pressed_frames < 0:
            if self.__selected:
                render.draw_image_centered(self.__textureName, self.__position, self.__size, tint_color=(40, 40, 40), tint_flag=pygame.BLEND_RGB_ADD)
            else:
                render.draw_image_centered(self.__textureName, self.__position, self.__size)
        else:
            render.draw_image_centered(self.__textureName, self.__position, self.__size, tint_color=(220, 220, 220))
