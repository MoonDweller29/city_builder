from EBuilding import EBuilding
from EntitySystem import EntitySystem
from enum import Enum

class ESourceType(Enum):
    WIND_MILL = 0
    SAW_MILL  = 1

class ResourceModifyingInfo:
    def __init__(self, resourceName, onTickCount, tickPeriod):
        self.resourceName = resourceName
        self.onTickCount  = onTickCount
        self.tickPeriod   = tickPeriod #in update ticks

class ESourceInfo:
    def __init__(self, spriteName, effectRadius, modifyingResourses):
        self.spriteName        = spriteName
        self.effectRadius      = effectRadius
        self.modifyingResources = modifyingResourses

class ESource(EBuilding):
    nameToTypeDict = {
        "WindMill" : ESourceType.WIND_MILL,
        "Sawmill"  : ESourceType.SAW_MILL
    }
    typeInfoDict = {
        ESourceType.WIND_MILL : ESourceInfo("WindMill", 5, []),
        ESourceType.SAW_MILL  : ESourceInfo("Sawmill", 2, [
            ResourceModifyingInfo("Wood", 1, 120)
        ])
    }

    def __init__(self, x, y, sourceType):
        super().__init__(x, y, self.typeInfoDict[sourceType].spriteName)

        self.__sourceType    = sourceType
        self.__typeInfo      = self.typeInfoDict[sourceType]
        self.__effectRadius  = self.__typeInfo.effectRadius
        self.__modifyingResources = self.__typeInfo.modifyingResources
        self.__tickCounters = [ 0 for _ in self.__modifyingResources ]

    def update(self):
        super().update()
        for i, modRes in enumerate(self.__modifyingResources):
            if self.__tickCounters[i] >= modRes.tickPeriod:
                self.__resourcePanel.add_resource(modRes.resourceName, modRes.onTickCount)
                self.__tickCounters[i] = 0

        self.__tickCounters = [i+1 for i in self.__tickCounters]

    def draw(self):
        super().draw()

    def on_start(self):
        super().on_start()
        self.__resourcePanel = EntitySystem().get_entity(EntitySystem().find_entity("ResourcePanel"))


    def set_pos(self, coord):
        super().set_pos(coord)
        self.__tickCounter = 0
