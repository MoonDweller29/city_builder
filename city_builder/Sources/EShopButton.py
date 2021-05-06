from .BuildingDatabase import BuildingDatabase
from .EButton import EButton
from .EntitySystem import ES
from .GraphicsEngine import GE
from .Utils import Vec
from .RootPath import RootPath
import gettext
import locale


language = gettext.translation('EShopButton',
                               localedir=RootPath().create_path('Resources/locales'),
                               languages=[locale.getdefaultlocale()[0], 'en-us'])
language.install()
_ = language.gettext


class EShopButton(EButton):
    def __init__(self, name, position, size, buildingName, shopPanel):
        super().__init__(name, position, size)

        self.buildingName = buildingName
        self.shopPanel = shopPanel

        # @TODO Remove this
        self.outputNames = {
            "CrystalMine": _(u"Mine"),
            "Sawmill": _(u"Sawmill"),
            "WindMill": _(u"Windmill"),
            "House": _(u"House"),
        }

        self.__resourcePanel = ES().find_entity("ResourcePanel")

    def on_start(self):
        super().on_start()

        self.costs = BuildingDatabase().GetBuildingCosts(self.buildingName)

    def update(self):
        super().update()
        if ES().get_entity(self.shopPanel).can_buy(self.buildingName):
            self.set_greyed(False)
        else:
            self.set_greyed(True)

    def draw(self):
        super().draw()

        # GE().draw_rectangle(add(self._position, (-48, 32 - 3)), (80, 20), (0, 0, 0), alpha=100)
        # GE().draw_rectangle(add(self._position, (-48, 32)), (80, 20), (230, 230, 230), alpha=200)

        GE().draw_text("ShopButtonFont", self._position + (-48 - 3, 20 + 3),
                       (0, 0, 0), self.outputNames[self.buildingName])

        GE().draw_text("ShopButtonFont", self._position + (-48, 20),
                       (255, 255, 255), self.outputNames[self.buildingName])

        resourceStatus = ES().get_entity(self.__resourcePanel).check_needed_resources(self.costs)

        for i in range(len(self.costs)):
            GE().draw_sprite(
                ES().get_entity(self.__resourcePanel).get_resource_icon(self.costs[i][0]),
                self._position + (-48, 20 + 25) + (64 * i, 0), (24, 24))

            textColor = (255, 255, 255)

            if not resourceStatus[i]:
                textColor = (255, 45, 17)

            GE().draw_text("ShopButtonFont",
                           self._position + Vec((-48 + 25 - 3, 20 + 25 + 3)) + (64 * i, 0),
                           (0, 0, 0), str(self.costs[i][1]))

            GE().draw_text("ShopButtonFont",
                           self._position + (-48 + 25, 20 + 25) + (64 * i, 0),
                           textColor, str(self.costs[i][1]))

    def on_pressed(self):
        super().on_pressed()

        ES().get_entity(self.shopPanel).try_buying(self.buildingName)
