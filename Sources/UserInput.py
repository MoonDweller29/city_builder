import pygame
from EntitySystem import EntitySystem
from EUIElement import EUIElement

class UserInput:
    __instance = None
    __initialized = None
    __keyDown = set()
    __mouseLeft = False
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
        self.__mouseLeft = False
        self.__isUI = self.__check_ui(self.get_mouse_position())
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.__mouseLeft = True
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

    def is_mouse_down(self):
        return self.__mouseLeft and not self.__isUI

    def is_ui_mouse_down(self):
        return self.__mouseLeft and self.__isUI

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

