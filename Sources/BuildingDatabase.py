from EBuilding import EBuilding

class BuildingDatabase:
    def get_all_building_names(self):
        return list(self.buildings.keys())

    def get_building_cost(self, name):
        return self.buildings[name][2]

    def get_building(self, name):
        return self.buildings[name][0](0, 0, self.buildings[name][1], spriteScale=self.buildings[name][4])

    def get_building_mask(self, name):
        return self.buildings[name][3]

    def get_building_sprite(self, name):
        return self.buildings[name][1]

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BuildingDatabase, cls).__new__(cls)
            cls.__instance.__init__singleton()
        return cls.__instance

    def __init__singleton(self):
        self.buildings = {
            "CrystalMine": (EBuilding, "CrystalMine", [("Wood", 10)], [[1]], 1),
            "Sawmill"    : (EBuilding, "Sawmill", [("Wood", 10), ("CrystalMine", 2)], [[1]], 1),
            "WindMill"   : (EBuilding, "WindMill", [("CrystalMine", 1)], [[1]], 1),
            "BlackMarket"   : (EBuilding, "BlackMarket", [("Wood", 1)], [[1, 1], [1, 1]], 2),
        }
