import pygame

class GraphicsEngine:
    __instance = None
    __inited = False
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GraphicsEngine, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if GraphicsEngine.__inited:
            return
        GraphicsEngine.__inited = True

        if not pygame.get_init():
            pygame.init()
            pygame.font.init()

    def init_window(self, resolution, title):
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(resolution)

    def get_screen(self):
        return self.screen

    # @TODO: Remove dependency on screen
    def draw_image(self, image, position, size):
        tmp = pygame.transform.scale(image, size)

        rect = tmp.get_rect()
        rect = rect.move(position)

        self.screen.blit(tmp, rect)

    # @TODO проверить memory leak texture surface возвращаемого из метода ренедер
    def draw_text(self, position, font, color, text):
        self.screen.blit(font.render(text, False, color), position)
