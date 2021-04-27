from EntitySystem import EntitySystem, Entity
from GraphicsEngine import GraphicsEngine
from Utils import lerp


class EResourceParticle(Entity):
    def __init__(self, x, y, resourceName, value):
        super().__init__()

        self.x = x
        self.y = y

        self.resourceName = resourceName

        self.lifetime_max = 35
        self.lifetime = self.lifetime_max
        self.alpha = 255
        self.value = value

    def on_start(self):
        super().on_start()

        self.__resourcePanel = EntitySystem().find_entity("ResourcePanel")

    def update(self):
        super().update()

        self.lifetime -= 1

        if self.lifetime < 0:
            EntitySystem().destroy_entity(self.id)

        self.y -= 0.5
        self.alpha = lerp(self.lifetime / self.lifetime_max, 0, 255)

    def draw(self):
        super().draw()

        # GraphicsEngine().draw_rectangle((100, 100, 100), add(self._position, (-48, 32)), (80,20), alpha=100)

        GraphicsEngine().draw_image(
            EntitySystem().get_entity(self.__resourcePanel).get_resource_icon(self.resourceName), (self.x, self.y),
            (24, 24))

        textColor = (255, 255, 255)
        text = "+" + str(self.value)

        if self.value < 0:
            textColor = (255, 45, 17)
            text = "+" + str(self.value)

        GraphicsEngine().draw_text((self.x + 25, self.y), "ShopButtonFont", textColor, text)
