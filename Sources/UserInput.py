import pygame

class UserInput:
    __instance = None
    __initialized = None
    __keyDown = set()
    __eventType = set()

    def __new__(cls):
        if not UserInput.__instance:
            if not pygame.get_init():
                pygame.init()
            UserInput.__instance = super(UserInput, cls).__new__(cls)
        return UserInput.__instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True

    def update(self):
        self.__keyDown.clear()
        self.__eventType.clear()
        
        for event in pygame.event.get():
            self.__eventType.add(event.type)
            if event.type == pygame.KEYDOWN:
                self.__keyDown.add(event.key)

    def is_exit(self):
        return (pygame.QUIT in self.__eventType) or self.is_key_down(pygame.K_ESCAPE)

    def is_key_down(self, key):
        return key in self.__keyDown
    
    def is_mouse_down(self):
        return self.check_event(pygame.MOUSEBUTTONDOWN)

    def check_event(self, eventType):
        return eventType in self.__eventType

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

