from EntitySystem import Entity
from Utils import *
from GraphicsEngine import GraphicsEngine
from skimage.io import imread
import numpy as np
from skimage import img_as_ubyte
from enum import Enum

def to_color_hash(r, g, b):
    return (r*256 + g)*256 + b

class ETerrain(Entity):

    __tileColorHash = {
        "WATER"  : to_color_hash(40,  92,  196),
        "GROUND" : to_color_hash(89,  193, 53 ),
        "TREE"   : to_color_hash(113, 65,  59 )
    }
    __tileTypeToCode = { key : i for i, key in enumerate(__tileColorHash) }
    __tileCodeToType = { i : key for i, key in enumerate(__tileColorHash) }
    __spriteTypes = {
        "WATER"  : (6, 1), # x, y
        "GROUND" : (0, 1),
        "TREE"   : (1, 10)
    }


    def __init__(self, mapPath, tileSize):
        super().__init__()

        self.__tileSize = tileSize
        self.__name = "CrystalMine"
        self.__spriteSheetName = "SP-Overworld"
        self.__load_map(mapPath)

    def __load_map(self, path):
        img_map = img_as_ubyte(imread(path))[:,:,:3].astype(np.uint32)
        img_map = to_color_hash(img_map[:,:,0], img_map[:,:,1], img_map[:,:,2])

        for key in self.__tileColorHash.keys():
            img_map = np.where(img_map == self.__tileColorHash[key], self.__tileTypeToCode[key], img_map)

        self.__logicMap = img_map.astype(np.uint8)
        print("SHAPE", self.__logicMap.shape)
        print(self.__logicMap)
        print(self.__tileColorHash)
        print(self.__tileTypeToCode)
        print(self.__tileCodeToType)
        self.__spriteIds = []
        for y in range(self.__logicMap.shape[0]):
            self.__spriteIds.append([])

            for x in range(self.__logicMap.shape[1]):
                tileType = self.__tileCodeToType[self.__logicMap[y,x]]
                self.__spriteIds[y].append(self.__spriteTypes[tileType])

    def update(self):
        super().update()
        
        pass

    def draw(self):
        super().draw()

        renderer = GraphicsEngine()

        for y in range(self.__logicMap.shape[0]):
            for x in range(self.__logicMap.shape[1]):
                # tileType = self.__tileCodeToType[self.__logicMap[y,x]]
                # spriteInfo = self.__spriteTypes[tileType]
                # renderer.draw_sprite(self.__spriteSheetName,
                #                      spriteInfo,
                #                     add((64, 64), (self.__tileSize[0] * x, self.__tileSize[1] * y)),
                #                     self.__tileSize)
                renderer.draw_sprite(self.__spriteSheetName,
                                     self.__spriteIds[y][x],
                                     add((64, 64), (self.__tileSize[0] * x, self.__tileSize[1] * y)),
                                     self.__tileSize)
                # renderer.draw_image(self.__name,
                #                      add((64, 64), (self.__tileSize[0] * x, self.__tileSize[1] * y)),
                #                      self.__tileSize)
