from .EBuilding import EBuilding
from .EResourceParticle import EResourceParticle
from .EntitySystem import EntitySystem


class EResourceProvider(EBuilding):
    def __init__(self, x, y, sprite, resources):
        super().__init__(x, y, sprite)

        self.__resources = resources
        self.__resourcePanel = EntitySystem().find_entity("ResourcePanel")

    def on_start(self):
        super().on_start()

        for name, value in enumerate(self.__resources):
            EntitySystem().get_entity(self.__resourcePanel).add_resource(value[0], value[1])

            EntitySystem().add_entity(EResourceParticle(self.x, self.y, value[0], value[1]))

    def update(self):
        super().update()

    def draw(self):
        super().draw()
