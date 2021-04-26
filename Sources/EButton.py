import pygame
from EUIElement import EUIElement
from GraphicsEngine import GraphicsEngine
from UserInput import UserInput

class EButton(EUIElement):
    def __init__(self, name, position, size):
        super().__init__()
        self.__textureName = name
        # @TODO: replace position and size by pygame.Rect
        self.__position = position
        self.__size = size
        self.__enable = False
        # @TODO: change drawOrder
        self.drawOrder = 100

    def update(self):
        super().update()
        input = UserInput()
        if input.is_mouse_down():
            mousePosition = input.get_mouse_position()
            # @TODO: check collision by pygame rectangle
            if 0 < mousePosition[0] - self.__position[0] < self.__size[0] and \
               0 < mousePosition[1] - self.__position[1] < self.__size[1]:
                self.__enable = True

    def draw(self):
        super().draw()
        render = GraphicsEngine()
        render.draw_image(self.__textureName, self.__position, self.__size)