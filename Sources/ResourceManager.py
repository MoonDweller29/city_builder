# Resource Manager - all resources in game load from it

import pygame
import json
 
# @TODO нужно будет сделать систему подгрузки ресурсов
# 1) Шрифты, картинки, может звуки (потом)
# 2) Доступно из разных модулей программы (Давайте синглтон)
# 3) Понять че за дичь с pygame, там ресурсы создают сразу с локальными свойствами (Например, в грифт зашит размер)
# 4) Подумать о том, что потенциально мы можем грузить данные из zip потом. Просто код под эту замену подготовить.

class SpriteSheet:
    def __init__(self, image, tile_width, tile_height):
        self.__image = image
        self.__tile_width = tile_width
        self.__tile_height = tile_height
        self.__tile_count_width = image.get_width() // tile_width
        self.__tile_count_height = image.get_height() // tile_height
        self.__spriteArr = []
        for y in range(self.__tile_count_height):
            for x in range(self.__tile_count_width):
                self.__spriteArr.append(
                    image.subsurface(
                        x * tile_width, y * tile_height, 
                        tile_width, tile_height
                    )
                )
    
    def get_sprite(self, x, y):
        if x >= self.__tile_width or y >= self.__tile_height:
            raise ValueError("Index out of range")
        return self.__spriteArr[x + y * self.__tile_count_width]

class ResourceManager:
    __instance = None
    __initialized = None
    __imageDict = {}
    __spriteSheetDict = {}
    __fontDict = {}

    def __new__(cls):
        if not ResourceManager.__instance:
            if not pygame.get_init():
                pygame.init()
            ResourceManager.__instance = super(ResourceManager, cls).__new__(cls)
        return ResourceManager.__instance

    def __init__(self):
        if not self.__initialized:
            with open('Resources.json') as json_file:
                data = json.load(json_file)
                for (name, path) in data["Images"].items():
                    self.create_img(name, path)
                for (name, sprite_args) in data["SpriteSheet"].items():
                    self.create_sprite_sheet(name, sprite_args[0], sprite_args[1], sprite_args[2])
                for (name, font_args) in data["Fonts"].items():
                    self.create_font(name, font_args[0], font_args[1])
            self.__initialized = True

    def __load_img(self, path):
        return pygame.image.load(path).convert_alpha()

    def __load_font(self, path, size):
        return pygame.font.Font(path, size)

    def create_img(self, name, path):
        if name in self.__imageDict:
            raise ValueError(f"Resource img {name} exist!")
        self.__imageDict[name] = self.__load_img(path)
        return self.__imageDict[name]

    def create_sprite_sheet(self, name, path, width, height):
        if name in self.__spriteSheetDict:
            raise ValueError(f"SpriteSheet resource {name} exist!")

        image = self.__load_img(path)
        self.__spriteSheetDict[name] = SpriteSheet(image, width, height)
        return self.__spriteSheetDict[name]

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
    
    def get_sprite_sheet(self, name, x, y):
        if name in self.__spriteSheetDict:
            return self.__spriteSheetDict[name].get_sprite(x, y)
        else:
            raise ValueError(f"SpriteSheet resource {name} not exist!")

    def get_font(self, name):
        if name in self.__fontDict:
            return self.__fontDict[name]
        else:
            raise ValueError(f"Font resource {name} not exist!")