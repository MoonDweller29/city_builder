from .BuildingDatabase import BuildingDatabase
from .EFakeBuilding import EFakeBuilding
from .EntitySystem import ES, Entity
from .UserInput import UserInput, MouseButton


class EBuilder(Entity):
    def __init__(self):
        super().__init__()

    def on_start(self):
        super().on_start()

        self.buildingName = ""

        self.__resourcePanelId = ES().find_entity("ResourcePanel")
        self.fakeBuilding = ES().add_entity(EFakeBuilding(0, 0, "CrystalMine"))

        ES().get_entity(self.fakeBuilding).disable()

    def start_building(self, buildingName):
        self.buildingName = buildingName

        ES().get_entity(self.fakeBuilding).enable()
        ES().get_entity(self.fakeBuilding).sprite = buildingName
        radius = BuildingDatabase().get_affect_radius(buildingName)
        ES().get_entity(self.fakeBuilding).radius = radius

    def update(self):
        super().update()

        if self.buildingName == "":
            return

        if UserInput().is_mouse_down(MouseButton.RIGHT) or \
                UserInput().is_ui_mouse_down(MouseButton.RIGHT):
            self.__stop_building()
            return

        if UserInput().is_mouse_down(MouseButton.LEFT):
            grid = ES().get_grid()
            coord = grid.world_to_cell(UserInput().get_mouse_position())

            if (grid.is_inside(coord) and grid.is_cell_free(coord)):
                costs = BuildingDatabase().GetBuildingCosts(self.buildingName)
                ES().get_entity(self.__resourcePanelId).spend(costs)

                buildingId = ES().add_entity(BuildingDatabase().GetBuilding(self.buildingName))
                ES().get_entity(buildingId).set_pos(coord)

                self.__stop_building()

    def draw(self):
        super().draw()

    def __stop_building(self):
        self.buildingName = ""
        ES().get_entity(self.fakeBuilding).disable()
