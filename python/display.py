import pygame
from enum import Enum

class Color(Enum):
    GREEN = (0, 200, 50)
    ORANGE = (200, 80, 0)
    WHITE = (255, 255, 255)
    PLANT = (0, 100, 0)
    BLACK = (0, 0, 0)
    YELLOW = (100, 100, 0)
    RED = (255, 0, 0)

def draw(screen, animals):
    for a in animals:
        a.draw(screen)
    pygame.display.update()
