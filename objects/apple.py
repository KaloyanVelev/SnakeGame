import pygame
import random
from models.enums import Enum

#Apple
class Apple:

    def __init__(self):
        self.x = 0
        self.y = 0
    #Spawns the Apple
    def spawn(self, snake_body, avoid_pos=None):
        while True:
            self.x = random.randrange(0, Enum.WINDOW_WIDTH, Enum.GRID_SIZE)
            self.y = random.randrange(0, Enum.WINDOW_HEIGHT, Enum.GRID_SIZE)
            if [self.x, self.y] not in snake_body:
                #Makes sure not to stack the apples one another
                if avoid_pos is None or [self.x, self.y] != avoid_pos:
                    break
    #Draws the apple
    def draw(self, surface):
        pygame.draw.rect(surface, Enum.RED, (self.x, self.y, Enum.GRID_SIZE, Enum.GRID_SIZE))


