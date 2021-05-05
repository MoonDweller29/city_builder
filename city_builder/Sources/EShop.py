from .BuildingDatabase import BuildingDatabase
from .EBuilder import EBuilder
from .EShopButton import EShopButton
from .EUIElement import EUIElement
from .Utils import Vec
from .EntitySystem import ES
from .GraphicsEngine import GE
from .RootPath import RootPath
import gettext
import locale


language = gettext.translation('EShop',
                               localedir=RootPath().create_path("Resources/locales"),
                               languages=[locale.getdefaultlocale()[0], 'en-us'])

language.install()
_ = language.gettext


class EShop(EUIElement):
    def __init__(self):
        super().__init__((900, 100), (360, 280))

    def on_start(self):
        self.builder = ES().add_entity(EBuilder())

        names = BuildingDatabase().GetAllBuildingNames()
        self.resourcePanel = ES().find_entity("ResourcePanel")

        id = 0

        for y in range(5):
            if id >= len(names):
                break

            for x in range(3):
                if id >= len(names):
                    break
                ES().add_entity(
                    EShopButton(names[id], ((965, 180) + (110 * x, 110 * y)), (100, 100), names[id], self.id))
                id += 1

    def can_buy(self, buildingName):
        costs = BuildingDatabase().GetBuildingCosts(buildingName)
        return ES().get_entity(self.resourcePanel).can_buy(costs)

    def try_buying(self, buildingName):
        if self.can_buy(buildingName):
            ES().get_entity(self.builder).start_building(buildingName)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

        GE().draw_rectangle(self._position, self._size, (99, 68, 57), alpha=245)
        GE().draw_text("ShopTitleFont", self._position + Vec((10 - 3, 5 + 3)), (0, 0, 0), _("Shop"))
        GE().draw_text("ShopTitleFont", self._position + Vec((10, 5)), (255, 255, 255), _("Shop"))
