import operator

# Vector operations on tuples

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))

def mul(a, b):
    return tuple(map(operator.mul, a, b))

def truediv(a, b):
    return tuple(map(operator.truediv, a, b))

import pygame

# @TODO подумаь о жизни, что с ней не так.
# Скорее всего можно сделать более презентабельными
# Remove dependency on screen
def DrawImage(screen, image, position, size):
    tmp = pygame.transform.scale(image, size)

    rect = tmp.get_rect()
    rect = rect.move(position)

    screen.blit(tmp, rect)

# @TODO проверить на лик texture surface возвращаемого из метода ренедер
def DrawText(screen, position, font, color, text):
    screen.blit(font.render(text, False, color), position)
