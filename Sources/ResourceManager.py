# Resource Manager - all resources in game load from it

import pygame
 
# @TODO нужно будет сделать систему подгрузки ресурсов
# 1) Шрифты, картинки, может звуки (потом)
# 2) Доступно из разных модулей программы (Давайте синглтон)
# 3) Понять че за дичь с pygame, там ресурсы создают сразу с локальными свойствами (Например, в грифт зашит размер)
# 4) Подумать о том, что потенциально мы можем грузить данные из zip потом. Просто код под эту замену подготовить.

class ResourceManager:
    __instance = None
    __imageDict = {}
    __fontDict = {}

    def __new__(cls):
        if not ResourceManager.__instance:
            if not pygame.get_init():
                pygame.init()
            ResourceManager.__instance = super(ResourceManager, cls).__new__(cls)
        return ResourceManager.__instance

    def __init__(self):
        pass

    def __load_img(self, path):
        return pygame.image.load(path).convert_alpha()

    def __load_font(self, path, size):
        return pygame.font.Font(path, size)

    def create_img(self, name, path):
        if name in self.__imageDict:
            raise ValueError(f"Resource img {name} exist!")
        self.__imageDict[name] = self.__load_img(path)
        return self.__imageDict[name]

    def create_font(self, name, path, size):
        if name in self.__fontDict:
            raise ValueError(f"Resource font {name} exist!")
        
        # Проверка на системный шрифт
        if pygame.font.match_font(path):
            path = pygame.font.match_font(path)

        self.__fontDict[name] = self.__load_font(path, size)
        return self.__fontDict[name]

    def get_image(self, name):
        if name in self.__imageDict:
            return self.__imageDict[name]
        else:
            raise ValueError(f"Image resource {name} not exist!")

    def get_font(self, name):
        if name in self.__fontDict:
            return self.__fontDict[name]
        else:
            raise ValueError(f"Font resource {name} not exist!")