from .EntitySystem import Entity


class EUIElement(Entity):
    def __init__(self, position, size):
        super().__init__()
        # @TODO: replace position and size by pygame.Rect
        self._position = position
        self._size = size

    def is_inside(self, coord):
        return 0 <= coord[0] - self._position[0] <= self._size[0] and \
            0 <= coord[1] - self._position[1] <= self._size[1]

    def update(self):
        super().update()

    def draw(self):
        super().draw()
