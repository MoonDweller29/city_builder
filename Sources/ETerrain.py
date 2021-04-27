import random

import numpy as np
import pygame
from skimage import img_as_ubyte
from skimage.io import imread

from EntitySystem import Entity
from EntitySystem import EntitySystem
from GraphicsEngine import GraphicsEngine
from TreeFactory import TreeFactory


def to_color_hash(r, g, b):
    return (r * 256 + g) * 256 + b


class Dirs:
    def __init__(self,
                 left_up=0, up=0, right_up=0,
                 left=0, center=0, right=0,
                 left_down=0, down=0, right_down=0):
        self.__dirs = [
            [left_up, up, right_up],
            [left, center, right],
            [left_down, down, right_down]
        ]

    def setON(self, i, j):  # i,j in range(-1, 2)
        i += 1
        j += 1
        self.__dirs[i][j] = 1

    def setOFF(self, i, j):  # i,j in range(-1, 2)
        i += 1
        j += 1
        self.__dirs[i][j] = 0

    def to_int(self):
        res = 0
        dirs = [self.__dirs[0][0], self.__dirs[0][1], self.__dirs[0][2],
                self.__dirs[1][0], self.__dirs[1][2],
                self.__dirs[2][0], self.__dirs[2][1], self.__dirs[2][2]]
        for i in range(len(dirs)):
            # print(((dirs[i] << (i+1)) - 1))
            res = res | ((dirs[i] << (i)))

        return res


def get_coast_tiles_dict():
    coastSprites = {

        Dirs(left_up=1).to_int(): [(7, 2)],
        Dirs(right_up=1).to_int(): [(5, 2)],
        Dirs(left_down=1).to_int(): [(7, 0)],
        Dirs(right_down=1).to_int(): [(5, 0)],

        Dirs(up=1).to_int(): [(6, 2)],
        Dirs(left=1).to_int(): [(7, 1)],
        Dirs(right=1).to_int(): [(5, 1)],
        Dirs(down=1).to_int(): [(6, 0)],
        # the left/right/up/down in case of 3 water tiles
        Dirs(left_up=1, up=1, right_up=1).to_int(): [(6, 2)],
        Dirs(left_down=1, left=1, left_up=1).to_int(): [(7, 1)],
        Dirs(right_up=1, right=1, right_down=1).to_int(): [(5, 1)],
        Dirs(right_down=1, down=1, left_down=1).to_int(): [(6, 0)],
        # the left/right/up/down in case of 2 water tiles
        Dirs(left_up=1, up=1).to_int(): [(6, 2)],
        Dirs(up=1, right_up=1).to_int(): [(6, 2)],
        Dirs(left=1, left_up=1).to_int(): [(7, 1)],
        Dirs(left_down=1, left=1).to_int(): [(7, 1)],
        Dirs(right=1, right_down=1).to_int(): [(5, 1)],
        Dirs(right_up=1, right=1).to_int(): [(5, 1)],
        Dirs(down=1, left_down=1).to_int(): [(6, 0)],
        Dirs(right_down=1, down=1).to_int(): [(6, 0)],

        Dirs(left=1, left_up=1, up=1).to_int(): [(1, 2)],
        Dirs(up=1, right_up=1, right=1).to_int(): [(2, 2)],
        Dirs(right=1, right_down=1, down=1).to_int(): [(2, 3)],
        Dirs(down=1, left_down=1, left=1).to_int(): [(1, 3)],
        # the same for 4 water tiles
        Dirs(left_down=1, left=1, left_up=1, up=1).to_int(): [(1, 2)],
        Dirs(left=1, left_up=1, up=1, right_up=1).to_int(): [(1, 2)],
        Dirs(left_up=1, up=1, right_up=1, right=1).to_int(): [(2, 2)],
        Dirs(up=1, right_up=1, right=1, right_down=1).to_int(): [(2, 2)],
        Dirs(right_up=1, right=1, right_down=1, down=1).to_int(): [(2, 3)],
        Dirs(right=1, right_down=1, down=1, left_down=1).to_int(): [(2, 3)],
        Dirs(right_down=1, down=1, left_down=1, left=1).to_int(): [(1, 3)],
        Dirs(down=1, left_down=1, left=1, left_up=1).to_int(): [(1, 3)],
        # the same for 5 water tiles
        Dirs(left_down=1, left=1, left_up=1, up=1, right_up=1).to_int(): [(1, 2)],
        Dirs(left_up=1, up=1, right_up=1, right=1, right_down=1).to_int(): [(2, 2)],
        Dirs(right_up=1, right=1, right_down=1, down=1, left_down=1).to_int(): [(2, 3)],
        Dirs(right_down=1, down=1, left_down=1, left=1, left_up=1).to_int(): [(1, 3)],
    }

    return coastSprites


class ETerrain(Entity):
    __tileColorHash = {
        "WATER": to_color_hash(40, 92, 196),
        "GROUND": to_color_hash(89, 193, 53),
        "TREE": to_color_hash(113, 65, 59)
    }
    __tileCodeToName = ["WATER", "GROUND", "TREE", "COAST"]
    __tileNameToCode = {key: i for i, key in enumerate(__tileCodeToName)}
    # coords: x, y
    __spriteTypes = {
        "WATER": [
            (6, 1),  # empty
            (7, 3)  # waves
        ],
        "GROUND": [
            (1, 0), (2, 0),  # flowers
            (3, 0), (4, 0),  # grass
            (0, 1),  # empty ground
            (1, 1), (2, 1),  # wood
            (3, 1), (4, 1)  # stones
        ],
        "TREE": [
            (3, 0), (4, 0),  # grass
            (0, 1),  # empty ground
        ],
        "COAST": get_coast_tiles_dict()
    }
    __waterSpriteWeights = [4, 1]
    __groundSpriteWeights = [0.9, 0.8, 2, 2, 10, 0.4, 0.4, 0.4, 0.4]

    def __init__(self, mapPath, origin, tileSize):
        super().__init__()

        self.__origin = origin
        self.__tileSize = (tileSize, tileSize)
        self.__spriteSheetName = "SP-Overworld"
        self.__load_map(mapPath)
        self.__draw_to_surface()

    def __load_map(self, path):
        imgMap = img_as_ubyte(imread(path))[:, :, :3].astype(np.uint32)
        imgMap = to_color_hash(imgMap[:, :, 0], imgMap[:, :, 1], imgMap[:, :, 2])

        for key in self.__tileColorHash.keys():
            imgMap = np.where(imgMap == self.__tileColorHash[key], self.__tileNameToCode[key], imgMap)

        self.__logicMap = imgMap.astype(int)
        self.__finalize_logic_map()

        self.__spriteIds = []
        for y in range(self.__logicMap.shape[0]):
            self.__spriteIds.append([])
            for x in range(self.__logicMap.shape[1]):
                self.__spriteIds[y].append(self.__get_sprite_coord(x, y))

        # @TODO: Tree object generation is supposed to be there

    def __finalize_logic_map(self):
        shape = self.__logicMap.shape
        for y in range(shape[0]):
            for x in range(shape[1]):
                tileName = self.__tileCodeToName[self.__logicMap[y, x]]
                if tileName == "GROUND":
                    self.__check_coast(x, y)

    def __check_coast(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 == j:
                    continue
                iInd = np.clip(i + y, 0, self.__logicMap.shape[0] - 1)
                jInd = np.clip(j + x, 0, self.__logicMap.shape[1] - 1)
                neighbourName = self.__tileCodeToName[self.__logicMap[iInd, jInd]]
                if neighbourName == "WATER":
                    self.__logicMap[y, x] = self.__tileNameToCode["COAST"]
                    return

    def __get_sprite_coord(self, x, y):
        tileName = self.__tileCodeToName[self.__logicMap[y, x]]
        if tileName == "WATER":
            spriteCoords = self.__spriteTypes[tileName]
            return random.choices(spriteCoords, weights=self.__waterSpriteWeights, k=1)[0]

        elif tileName == "TREE":
            spriteCoords = self.__spriteTypes[tileName]
            randInd = random.randint(0, len(spriteCoords) - 1)
            return spriteCoords[randInd]

        elif tileName == "GROUND":
            spriteCoords = self.__spriteTypes[tileName]
            return random.choices(spriteCoords, weights=self.__groundSpriteWeights, k=1)[0]

        elif tileName == "COAST":
            spriteTypes = self.__spriteTypes[tileName]
            dirs = Dirs()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 == j:
                        continue
                    shape = self.__logicMap.shape
                    iInd = np.clip(i + y, 0, shape[0] - 1)
                    jInd = np.clip(j + x, 0, shape[1] - 1)
                    neighbourName = self.__tileCodeToName[self.__logicMap[iInd, jInd]]
                    if neighbourName == "WATER":
                        dirs.setON(i, j)
            key = dirs.to_int()
            spriteCoords = spriteTypes[key]

            randInd = random.randint(0, len(spriteCoords) - 1)
            return spriteCoords[randInd]

        return (0, 0)

    def __draw_to_surface(self):
        shape = self.__logicMap.shape
        surfSize = (self.__tileSize[0] * shape[1], self.__tileSize[1] * shape[1])
        self.__terrainTex = pygame.Surface(surfSize)

        renderer = GraphicsEngine()
        renderer.set_render_target(self.__terrainTex)

        for y in range(self.__logicMap.shape[0]):
            for x in range(self.__logicMap.shape[1]):
                renderer.draw_sprite(self.__spriteSheetName,
                                     self.__spriteIds[y][x],
                                     (self.__tileSize[0] * x, self.__tileSize[1] * y),
                                     self.__tileSize)

        renderer.set_render_target()
        # pygame.image.save(self.__terrainTex, "current_map.png")

    def get_size(self):
        return (self.__logicMap.shape[1], self.__logicMap.shape[0])

    def fill_grid(self, grid):
        shape = self.__logicMap.shape
        for y in range(shape[0]):
            for x in range(shape[1]):
                tileName = self.__tileCodeToName[self.__logicMap[y, x]]
                if tileName == "COAST" or tileName == "WATER":
                    grid.on_add_to_cell_xy(self.id, x, y)
                elif tileName == "TREE":
                    tree = TreeFactory.create_random_tree()
                    EntitySystem().add_entity(tree)
                    tree.set_pos((x, y))

    def update(self):
        super().update()

        pass

    def draw(self):
        super().draw()

        renderer = GraphicsEngine()
        renderer.draw_surface(self.__terrainTex, self.__origin)

        # non optimal approach
        # for y in range(self.__logicMap.shape[0]):
        #     for x in range(self.__logicMap.shape[1]):
        #         renderer.draw_sprite(self.__spriteSheetName,
        #                              self.__spriteIds[y][x],
        #                              add(self.__origin, (self.__tileSize[0] * x, self.__tileSize[1] * y)),
        #                              self.__tileSize)
