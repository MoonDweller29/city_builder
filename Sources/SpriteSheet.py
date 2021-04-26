import pygame

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
        if x >= self.__tile_count_width or y >= self.__tile_count_height:
            raise ValueError("Index out of range")
        return self.__spriteArr[x + y * self.__tile_count_width]