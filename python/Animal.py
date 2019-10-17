from display import Color
from math import sqrt
from random import randint
import pygame

class Animal():
    def __init__(self, x, y):
        self.color = Color.WHITE

        self.x = x
        self.y = y
        self.size = 10

        self.vision = 1
        self.speed = 10

        self.hunger = 0
        self.start_hunting = 30
        self.mate = 0
        self.start_mating = 30

        self.age = 0
        self.maturity = 10
        self.mature = False

        self.predator = None
        self.food = None

    def dist(self, b):
        return sqrt((self.x - b.x)**2 + (self.y - b.y)**2)

    def go_direction(self, b):
        return (b.x-self.x, b.y-self.y)

    def run_away_from(self, b):
        return (self.x-b.x, self.y-b.y)

    def run_away_from_group(self, g):
        cumul = [0, 0]
        for o in g:
            d = self.dist(o)
            if d == 0:
                d = 1
            cumul[0] += (self.x - o.x)*self.speed / d
            cumul[1] += (self.y - o.y)*self.speed / d
        return cumul

    def draw(self, screen):
        pygame.draw.circle(screen, self.color.value, (self.x, self.y), self.size)

    def look_around(self, objects):
        dists = [(self.dist(o), o) for o in objects]
        seen = sorted([(d, o) for (d, o) in dists if d <= self.vision], key=lambda x:x[0])
        return seen

    def move(self, direction):
        direction = list(direction)
        v = sqrt(direction[0]**2 + direction[1]**2)
        if v > self.speed:
            direction[0] /= v
            direction[0] *= self.speed
            direction[1] /= v
            direction[1] *= self.speed

        direction[0] = int(direction[0])
        direction[1] = int(direction[1])
        self.x += direction[0]
        self.y += direction[1]
        self.hunger += self.speed

    def random_direction(self):
        return [randint(-self.speed, self.speed), randint(-self.speed, self.speed)]

    def find_direction(self, objects):
        seen = self.look_around(objects)
        if self.predator:
            pred = [o for (d, o) in seen if isinstance(o, self.predator)]
            if pred:
                return self.run_away_from_group(pred)

        if self.hunger >= self.mate and self.hunger > self.start_hunting:
            food = [(d, o) for (d, o) in seen if isinstance(o, self.food)]
            food.sort(key=lambda x: x[0])
            if food:
                return self.go_direction(food[0][1])

        if self.mate >= self.hunger and self.mate > self.start_mating:
            mates = [(d, o) for (d, o) in seen if isinstance(o, self.__class__) and o != self and o.mature]
            mates.sort(key=lambda x: x[0])
            if mates:
                return self.go_direction(mates[0][1])

        return self.random_direction()

    def step(self, objects):
        self.move(self.find_direction(objects))

    def eat(self, target):
        self.hunger = 0

    def get_old(self, objects):
        self.age += 1
        if self.age > self.maturity:
            self.mature = True
            self.mate += 5
        if self.hunger > 1000:
            objects.remove(self)

    def mate_with(self, b, objects):
        if not self.mature or not b.mature:
            return
        self.mate = 0
        self.mature = False
        self.age = 0
        objects.append(self.__class__(self.x, self.y))


####################################
# DEFINE SOME ANIMALS AND VEGETALS #

class Rabbit(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.color = Color.WHITE

        self.vision = 80
        self.speed = 10
        self.weight = 10

        self.food = Plant
        self.predator = Fox

class Fox(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.color = Color.ORANGE

        self.vision = 150
        self.speed = 30
        self.weight = 10
        self.size = 20

        self.food = Rabbit

class Plant(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.color = Color.PLANT
        self.speed = 0
        self.weight = 10
        self.size = 5

    def find_direction(self, objects):
        return (0, 0)
