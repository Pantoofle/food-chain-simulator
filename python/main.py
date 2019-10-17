from math import sqrt
from random import randint, uniform
from time import sleep
import numpy as np
import pygame, sys

from display import *
from Animal import Animal, Rabbit, Fox, Plant

def check_collisions(objects):
    foxes = []
    rabbits = []
    plants = []

    # Sort the objects following their class
    for o in objects:
        if isinstance(o, Fox):
            foxes.append(o)
        elif isinstance(o, Rabbit):
            rabbits.append(o)
        elif isinstance(o, Plant):
            plants.append(o)

    # Resolve the foxes
    for f in foxes:
        for r in rabbits:
            if f.dist(r) < f.size:
                f.eat(r)
                rabbits.remove(r)
                objects.remove(r)
                print("MIAM")
                break

    for i, r in enumerate(rabbits):
        for b in rabbits[i+1:]:
            if r.dist(b) < r.size:
                r.mate_with(b, objects)
                print("We mate !")
                break
        for p in plants:
            if r.dist(p) < r.size:
                r.eat(p)
                plants.remove(p)
                objects.remove(p)
                print("MIAM la plante")
                break


if __name__ == "__main__":
    # Prepare the screen
    pygame.init()
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)

    animals = [Rabbit(randint(0, width),randint(0, height)) for r in range(50)]
    animals += [Fox(randint(0, width),randint(0, height)) for r in range(5)]
    animals += [Plant(randint(0, width),randint(0, height)) for r in range(30)]
    screen.fill(Color.GREEN.value)
    draw(screen, animals)

    while True:
        for a in animals:
            target = a.find_direction(animals)
            pygame.draw.line(screen, Color.BLACK.value, (a.x, a.y), (a.x+target[0], a.y+target[1]), 1)
            a.move(target)

        check_collisions(animals)
        animals += [Plant(randint(0, width),randint(0, height)) for r in range(5)]

        for a in animals:
            a.get_old(animals)

        pygame.display.update()
        sleep(0.3)
        screen.fill(Color.GREEN.value)
        draw(screen, animals)
