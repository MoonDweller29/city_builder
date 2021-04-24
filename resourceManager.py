# Resource Manager - all resources in game load from it

import pygame
 
# @TODO нужно будет сделать систему подгрузки ресурсов
# 1) Шрифты, картинки, может звуки (потом)
# 2) Доступно из разных модулей программы (Давайте синглтон)
# 3) Понять че за дичь с pygame, там ресурсы создают сразу с локальными свойствами (Например, в грифт зашит размер)
# 4) Подумать о том, что потенциально мы можем грузить данные из zip потом. Просто код под эту замену подготовить.

class ResourceManager:
    _instance = None
    _imageDict = {}
    _fontDict = {}

    def __new__(cls):
        if not ResourceManager._instance:
            if not pygame.get_init():
                pygame.init()
            ResourceManager._instance = super(ResourceManager, cls).__new__(cls)
        return ResourceManager._instance

    def __init__(self):
        pass

    def __load_img(self, path):
        return pygame.image.load(path).convert_alpha()

    def __load_font(self, path, size):
        return pygame.font.Font(path, size)

    def create_img(self, name, path):
        if name in self._imageDict:
            raise ValueError(f"Resource img {name} exist!")
        self._imageDict[name] = self.__load_img(path)
        return self._imageDict[name]

    def create_font(self, name, path, size):
        if name in self._fontDict:
            raise ValueError(f"Resource font {name} exist!")
        
        # Проверка на системный шрифт
        if pygame.font.match_font(path):
            path = pygame.font.match_font(path)

        self._fontDict[name] = self.__load_font(path, size)
        return self._fontDict[name]

    def get_image(self, name):
        if name in self._imageDict:
            return self._imageDict[name]
        else:
            raise ValueError(f"Image resource {name} not exist!")

    def get_font(self, name):
        if name in self._fontDict:
            return self._fontDict[name]
        else:
            raise ValueError(f"Font resource {name} not exist!")