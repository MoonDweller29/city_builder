from EBuilding import EBuilding

class BuildingDatabase:
    def GetAllBuildingNames(self):
        return list(self.buildings.keys())

    def GetBuildingCosts(self, name):
        return self.buildings[name][2]

    def GetBuilding(self, name):
        return self.buildings[name][0](0, 0, self.buildings[name][1])

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BuildingDatabase, cls).__new__(cls)
            cls.__instance.__init__singleton()
        return cls.__instance

    def __init__singleton(self):
        self.buildings = {
            "CrystalMine": (EBuilding, "CrystalMine", [("Wood", 10)]),
            "Sawmill": (EBuilding, "Sawmill", [("Wood", 10), ("CrystalMine", 2)]),
            "WindMill": (EBuilding, "WindMill", [("CrystalMine", 1)])
        }
