import pygame
from EntitySystem import EntitySystem
from EUIElement import EUIElement
from enum import Enum

class MouseButton(Enum):
    LEFT       = 0,
    RIGHT      = 1
    MIDDLE     = 3
    WHEEL_DOWN = 4
    WHEEL_UP   = 5
    EXTRA_1    = 6,
    EXTRA_2    = 7

    @classmethod
    def from_pygame(cls, pygameButtonCode):
        __pygameMouseButtonToMouseButton = {
            pygame.BUTTON_LEFT: MouseButton.LEFT,
            pygame.BUTTON_RIGHT: MouseButton.RIGHT,
            pygame.BUTTON_MIDDLE: MouseButton.MIDDLE,
            pygame.BUTTON_WHEELDOWN: MouseButton.WHEEL_DOWN,
            pygame.BUTTON_WHEELUP: MouseButton.WHEEL_UP,
            pygame.BUTTON_X1: MouseButton.EXTRA_1,
            pygame.BUTTON_X2: MouseButton.EXTRA_2
        }
        return __pygameMouseButtonToMouseButton[pygameButtonCode]

class UserInput:
    __instance = None
    __initialized = None
    __keyDown = set()
    __mouseButtonsPressed = { keyCode :False for keyCode in MouseButton }
    __isUI = False
    __quit = False

    def __new__(cls):
        if not UserInput.__instance:
            if not pygame.get_init():
                pygame.init()
            UserInput.__instance = super(UserInput, cls).__new__(cls)
        return UserInput.__instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True

    def __check_ui(self, coord):
        entitySystem = EntitySystem()
        idEntity = entitySystem.find_all_children(EUIElement)
        for id in idEntity:
            if entitySystem.get_entity(id).is_inside(coord):
                return True
        return False

    def update(self):
        self.__keyDown.clear()
        self.__mouseButtonsPressed = { keyCode :False for keyCode in MouseButton }
        self.__isUI = self.__check_ui(self.get_mouse_position())
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseButton = MouseButton.from_pygame(event.button)
                    self.__mouseButtonsPressed[mouseButton] = True
            elif event.type == pygame.QUIT:
                self.__quit = True
            elif event.type == pygame.KEYDOWN:
                self.__keyDown.add(event.key)

    def is_ui(self):
        return self.__isUI

    def is_exit(self):
        return self.__quit or self.is_key_down(pygame.K_ESCAPE)

    def is_key_down(self, key):
        return key in self.__keyDown

    def is_mouse_down(self, buttonCode):
        return self.__mouseButtonsPressed[buttonCode] and not self.__isUI

    def is_ui_mouse_down(self, buttonCode):
        return self.__mouseButtonsPressed[buttonCode] and self.__isUI

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

