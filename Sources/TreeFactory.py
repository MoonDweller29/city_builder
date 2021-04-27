import random
from enum import Enum

from ETree import ETree


class TreeType(Enum):
    OAK = 0
    BIRCH = 1
    PINE = 2


class TreeFactory:
    __spriteSheetName = "SP-Overworld"
    __spriteCoords = {
        TreeType.OAK: (1, 10),
        TreeType.BIRCH: (1, 13),
        TreeType.PINE: (1, 16)
    }

    @classmethod
    def create_tree(cls, treeType):
        return ETree(0, 0, cls.__spriteSheetName, cls.__spriteCoords[treeType])

    @classmethod
    def create_random_tree(cls):
        treeTypes = [TreeType.OAK, TreeType.BIRCH, TreeType.PINE]
        weights = [1, 1, 1]
        treeType = random.choices(treeTypes, weights=weights, k=1)[0]

        return TreeFactory.create_tree(treeType)
