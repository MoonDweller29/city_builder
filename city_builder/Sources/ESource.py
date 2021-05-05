from enum import Enum

from .EBuilding import EBuilding
from .EResourceParticle import EResourceParticle
from .ETree import ETree
from .EntitySystem import ES


class ESourceType(Enum):
    WIND_MILL = 0
    SAW_MILL = 1


class ResourceModifyingInfo:
    def __init__(self, resourceName, perTickAmount, tickPeriod):
        self.resourceName = resourceName
        self.perTickAmount = perTickAmount
        self.tickPeriod = tickPeriod  # in update ticks


class ESourceInfo:
    def __init__(self, spriteName, effectRadius, modifyingResourses, neighbourEffects):
        self.spriteName = spriteName
        self.effectRadius = effectRadius
        self.modifyingResources = modifyingResourses
        self.neighbourEffects = neighbourEffects


class ESource(EBuilding):
    nameToTypeDict = {
        "WindMill": ESourceType.WIND_MILL,
        "Sawmill": ESourceType.SAW_MILL
    }
    typeInfoDict = {
        ESourceType.WIND_MILL: ESourceInfo("WindMill", 0, [
            ResourceModifyingInfo("Food", 1, 140)
        ], {}),
        ESourceType.SAW_MILL: ESourceInfo("Sawmill", 1, [
            ResourceModifyingInfo("Wood", 3, 240)
        ], {
            "Tree": 1  # @TODO: refactor this
        })
    }

    def __init__(self, x, y, sourceType):
        super().__init__(x, y, self.typeInfoDict[sourceType].spriteName)

        self.__sourceType = sourceType
        self.__typeInfo = self.typeInfoDict[sourceType]
        self.__effectRadius = self.__typeInfo.effectRadius
        self.__modifyingResources = self.__typeInfo.modifyingResources
        self.__tickCounters = [0 for _ in self.__modifyingResources]
        self.__onTickResourceCounts = [modRes.perTickAmount for modRes in self.__modifyingResources]

    def update(self):
        super().update()
        for i, modRes in enumerate(self.__modifyingResources):
            if self.__tickCounters[i] >= modRes.tickPeriod:
                perTickAmount = self.__onTickResourceCounts[i]
                self.__resourcePanel.add_resource(modRes.resourceName, perTickAmount)
                self.__tickCounters[i] = 0

                ES().add_entity(EResourceParticle(self.x, self.y, modRes.resourceName, perTickAmount))

        self.__tickCounters = [i + 1 for i in self.__tickCounters]

    def draw(self):
        super().draw()

    def on_start(self):
        super().on_start()
        # @TODO Вот так не надо вообще делать. Понятно, что панель пропасть не должна,
        # но id по идее существуют чтобы косвенно адресовать
        self.__resourcePanel = ES().get_entity(ES().find_entity("ResourcePanel"))

    def set_pos(self, coord):
        super().set_pos(coord)
        self.__tickCounters = [i + 1 for i in self.__tickCounters]
        self.__onTickResourceCounts = [modRes.perTickAmount for modRes in self.__modifyingResources]

        grid = ES().get_grid()
        cellPos = grid.world_to_cell((self.x, self.y))  # @TODO: maybe it's ok to use self.__cell_x from EOnGrid

        for y in range(cellPos[1] - self.__effectRadius, cellPos[1] + self.__effectRadius + 1):
            for x in range(cellPos[0] - self.__effectRadius, cellPos[0] + self.__effectRadius + 1):
                if x == cellPos[0] and y == cellPos[1]:
                    continue
                neighbourIds = grid.get_cell((x, y))
                if neighbourIds is None:
                    continue
                for neighbourId in neighbourIds:
                    if neighbourId > 0:
                        neighbour = ES().get_entity(neighbourId)
                        if isinstance(neighbour, ETree):
                            if "Tree" in self.__typeInfo.neighbourEffects:
                                treeEffect = self.__typeInfo.neighbourEffects["Tree"]
                                self.__onTickResourceCounts = [tickCount + treeEffect for tickCount in
                                                               self.__onTickResourceCounts]
