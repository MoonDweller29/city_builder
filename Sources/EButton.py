import pygame
from EUIElement import EUIElement
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput, MouseButton

from Utils import *

import copy

class EButton(EUIElement):
    def __init__(self, name, position, size):
        super().__init__(position, size)
        self.__textureName = name
        self.__selected = False
        self.__greyed = False
        self.__originSize = copy.deepcopy(size)
        # @TODO: change drawOrder
        self.drawOrder = 500

        self.pressed_frames = 0

    def set_greyed(self, v):
        self.__greyed = v
        if v == True:
            self._size = self.__originSize

    def update(self):
        super().update()
        if self.__greyed:
            return
        input = UserInput()

        mousePosition = input.get_mouse_position()

        self.pressed_frames -= 1
        # @TODO: check collision by pygame rectangle
        if 0 < mousePosition[0] - self._position[0] + self._size[0] / 2.0 < self._size[0] and \
            0 < mousePosition[1] - self._position[1] + self._size[1] / 2.0 < self._size[1]:
            if (not self.__selected):
                self.__selected = True
                self.on_selected()
        else:
            if (self.__selected):
                self.__selected = False
                self.on_deselected()

        if input.is_ui_mouse_down(MouseButton.LEFT) and self.__selected:
            self.on_pressed()

    def on_selected(self):
        self._size = toInt(mul(self.__originSize, (1.2, 1.2)))

    def on_deselected(self):
        self._size = self.__originSize

    def on_pressed(self):
        self.pressed_frames = 5

    def draw(self):
        super().draw()
        render = GraphicsEngine()

        # @TODO map tint colors and stuff?
        if self.__greyed:
            render.draw_image_centered(self.__textureName, self._position, self._size, tint_color=(50, 50, 50))
        elif self.pressed_frames < 0:
            if self.__selected:
                render.draw_image_centered(self.__textureName, self._position, self._size, tint_color=(40, 40, 40), tint_flag=pygame.BLEND_RGB_ADD)
            else:
                render.draw_image_centered(self.__textureName, self._position, self._size)
        else:
            render.draw_image_centered(self.__textureName, self._position, self._size, tint_color=(220, 220, 220))
