from EntitySystem import Entity
from Utils import *
from GraphicsEngine import GraphicsEngine
from skimage.io import imread
import numpy as np
from skimage import img_as_ubyte
from enum import Enum
import random

def to_color_hash(r, g, b):
    return (r*256 + g)*256 + b

class Dirs:
    def __init__(self,
                 left_up=0, up=0, right_up=0,
                 left=0, center=0, right=0,
                 left_down=0, down=0, right_down=0):
        self.__dirs = [
            [left_up,   up,     right_up  ],
            [left,      center, right     ],
            [left_down, down,   right_down]
        ]

    def setON(self, i, j): # i,j in range(-1, 2)
        i += 1
        j += 1
        self.__dirs[i][j] = 1

    def setOFF(self, i, j): # i,j in range(-1, 2)
        i += 1
        j += 1
        self.__dirs[i][j] = 0

    def toInt(self):
        res = 0
        dirs = [self.__dirs[0][0], self.__dirs[0][1], self.__dirs[0][2],
                self.__dirs[1][0],                    self.__dirs[1][2],
                self.__dirs[2][0], self.__dirs[2][1], self.__dirs[2][2]]
        for i in range(len(dirs)):
            # print(((dirs[i] << (i+1)) - 1))
            res = res | ((dirs[i] << (i)))

        return res

def getFullGroundSpriteWeights():
    return [0.9, 0.8, 2, 2, 10, 0.4, 0.4, 0.4, 0.4]

def getGroundTilesDict():
    groundTiles = {
        Dirs().toInt() : [
            (1,0),(2,0), #flowers
            (3,0),(4,0), #grass
            (0,1),       #empty
            (1,1),(2,1), #wood
            (3,1),(4,1)  #stones
    ],

        Dirs(left_up=1).toInt()   : [(7,2)],
        Dirs(up=1).toInt()        : [(6,2)],
        Dirs(right_up=1).toInt()  : [(5,2)],
        Dirs(left=1).toInt()      : [(7,1)],
        Dirs(right=1).toInt()     : [(5,1)],
        Dirs(left_down=1).toInt() : [(7,0)],
        Dirs(down=1).toInt()      : [(6,0)],
        Dirs(right_down=1).toInt(): [(5,0)],
        # the left/right/up/down in case of 3 water tiles
        Dirs(left_up=1, up=1, right_up=1).toInt(): [(6, 2)],
        Dirs(left_down=1, left=1, left_up=1).toInt(): [(7, 1)],
        Dirs(right_up=1, right=1, right_down=1).toInt(): [(5, 1)],
        Dirs(right_down=1, down=1, left_down=1).toInt(): [(6, 0)],
        # the left/right/up/down in case of 2 water tiles
        Dirs(left_up=1, up=1).toInt(): [(6, 2)],
        Dirs(up=1, right_up=1).toInt(): [(6, 2)],
        Dirs(left=1, left_up=1).toInt(): [(7, 1)],
        Dirs(left_down=1, left=1).toInt(): [(7, 1)],
        Dirs(right=1, right_down=1).toInt(): [(5, 1)],
        Dirs(right_up=1, right=1).toInt(): [(5, 1)],
        Dirs(down=1, left_down=1).toInt(): [(6, 0)],
        Dirs(right_down=1, down=1).toInt(): [(6, 0)],

        Dirs(left=1, left_up=1, up=1).toInt()       : [(1,2)],
        Dirs(up=1, right_up=1, right=1).toInt()     : [(2,2)],
        Dirs(right=1, right_down=1, down=1).toInt() : [(2,3)],
        Dirs(down=1, left_down=1, left=1).toInt()   : [(1,3)],
        # the same for 4 water tiles
        Dirs(left_down=1, left=1, left_up=1, up=1).toInt(): [(1, 2)],
        Dirs(left=1, left_up=1, up=1, right_up=1).toInt() : [(1, 2)],
        Dirs(left_up=1, up=1, right_up=1, right=1).toInt()   : [(2, 2)],
        Dirs(up=1, right_up=1, right=1, right_down=1).toInt(): [(2, 2)],
        Dirs(right_up=1, right=1, right_down=1, down=1).toInt() : [(2, 3)],
        Dirs(right=1, right_down=1, down=1, left_down=1).toInt(): [(2, 3)],
        Dirs(right_down=1, down=1, left_down=1, left=1).toInt(): [(1, 3)],
        Dirs(down=1, left_down=1, left=1, left_up=1).toInt()   : [(1, 3)],
        # the same for 5 water tiles
        Dirs(left_down=1, left=1, left_up=1, up=1, right_up=1).toInt(): [(1, 2)],
        Dirs(left_up=1, up=1, right_up=1, right=1, right_down=1).toInt(): [(2, 2)],
        Dirs(right_up=1, right=1, right_down=1, down=1, left_down=1).toInt(): [(2, 3)],
        Dirs(right_down=1, down=1, left_down=1, left=1, left_up=1).toInt(): [(1, 3)],
    }

    return groundTiles



class ETerrain(Entity):

    __tileColorHash = {
        "WATER"  : to_color_hash(40,  92,  196),
        "GROUND" : to_color_hash(89,  193, 53 ),
        "TREE"   : to_color_hash(113, 65,  59 )
    }
    __tileNameToCode = { key : i for i, key in enumerate(__tileColorHash) }
    __tileCodeToName = { i : key for i, key in enumerate(__tileColorHash) }
    # coords: x, y
    __spriteTypes = {
        "WATER"  : [
            (6, 1), # empty
            (7, 3)  # waves
        ],
        "GROUND" : getGroundTilesDict(),
        "TREE"   : [
            (1, 10), #regular tree
            (1, 13), #birch tree
            (1, 16)  #pine
        ]
    }
    __waterSpriteWeights = [4, 1]
    __groundSpriteWeights = getFullGroundSpriteWeights()


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
            img_map = np.where(img_map == self.__tileColorHash[key], self.__tileNameToCode[key], img_map)

        self.__logicMap = img_map.astype(np.uint8)
        print("SHAPE", self.__logicMap.shape)
        print(self.__logicMap)
        print(self.__tileColorHash)
        print(self.__tileNameToCode)
        print(self.__tileCodeToName)
        self.__spriteIds = []
        for y in range(self.__logicMap.shape[0]):
            self.__spriteIds.append([])
            for x in range(self.__logicMap.shape[1]):
                self.__spriteIds[y].append(self.__getSpriteCoord(x,y))

    def __getSpriteCoord(self, x, y):
        tileName = self.__tileCodeToName[self.__logicMap[y, x]]
        if tileName == "WATER":
            spriteCoords = self.__spriteTypes[tileName]
            return random.choices(spriteCoords, weights=self.__waterSpriteWeights, k=1)[0]

        elif tileName == "TREE":
            spriteCoords = self.__spriteTypes[tileName]
            randInd = random.randint(0, len(spriteCoords) - 1)
            return spriteCoords[randInd]
        elif tileName == "GROUND":
            spriteTypes = self.__spriteTypes[tileName]
            dirs = Dirs()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i==0==j:
                        continue
                    shape = self.__logicMap.shape
                    iInd = np.clip(i+y, 0, shape[0]-1)
                    jInd = np.clip(j+x, 0, shape[1]-1)
                    neighbourName = self.__tileCodeToName[self.__logicMap[iInd, jInd]]
                    if neighbourName == "WATER":
                        dirs.setON(i,j)
            key = dirs.toInt()
            spriteCoords = spriteTypes[key]
            if (key == 0):
                return random.choices(spriteCoords, weights=self.__groundSpriteWeights, k=1)[0]

            randInd = random.randint(0, len(spriteCoords) - 1)
            return spriteCoords[randInd]



        return (0,0)

    def update(self):
        super().update()
        
        pass

    def draw(self):
        super().draw()

        renderer = GraphicsEngine()

        for y in range(self.__logicMap.shape[0]):
            for x in range(self.__logicMap.shape[1]):
                # tileType = self.__tileCodeToName[self.__logicMap[y,x]]
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

