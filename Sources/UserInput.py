import pygame

class UserInput:
    __instance = None
    __initialized = None
    __pushKey = set()
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
        self.__pushKey.clear()
        self.__eventType.clear()
        for event in pygame.event.get():
            self.__eventType.add(event.type)
            if event.type == pygame.KEYDOWN:
                self.__pushKey.add(event.key)

    def is_exit(self):
        return (pygame.QUIT in self.__eventType) or (pygame.K_ESCAPE in self.__pushKey)

    def get(self, key):
        return event in self.__pushKey

    def get_type(self, eventType):
        return eventType in self.__eventType

    def get_mouse_position(self):
        return pygame.mouse.get_pos()

