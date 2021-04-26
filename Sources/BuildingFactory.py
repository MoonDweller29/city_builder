from EBuilding import EBuilding

def GetBuilding(name):
    buildings = {
        "CrystalMine": EBuilding(0, 0, "CrystalMine")
    }

    return buildings[name]
