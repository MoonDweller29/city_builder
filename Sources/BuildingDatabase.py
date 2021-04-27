from EBuilding import EBuilding
from ESource import ESource, ESourceType

from EResourceProvider import EResourceProvider

class BuildingDatabase:
    def GetAllBuildingNames(self):
        return list(self.buildings.keys())

    def GetBuildingCosts(self, name):
        return self.buildings[name][2]

    def GetBuilding(self, name):
        if (name == "House"):
            return EResourceProvider(0, 0, *(self.buildings[name][1]), [("People", 4)])

        return self.buildings[name][0](0, 0, *(self.buildings[name][1]))

    def get_affect_radius(self, name):
        buildingClass = self.buildings[name][0]
        if (buildingClass is EBuilding):
            return 0
        elif (buildingClass is ESource):
            buildingType = ESource.nameToTypeDict[name]
            typeInfo = ESource.typeInfoDict[buildingType]
            return typeInfo.effectRadius

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BuildingDatabase, cls).__new__(cls)
            cls.__instance.__init__singleton()
        return cls.__instance

    def __init__singleton(self):
        self.buildings = {
            "Sawmill": (ESource, [ESourceType.SAW_MILL], [("Wood", 10), ("People", 1)]),
            "CrystalMine": (EBuilding, ["CrystalMine"], [("Wood", 10), ("People", 2)]),
            "WindMill": (ESource, [ESourceType.WIND_MILL], [("People", 1)]),
            "House": (EBuilding, ["House"], [("Wood", 30), ("Food", 10)])
        }
