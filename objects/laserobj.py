import pygame
from models.enums import Enum
class Laser:

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    #Updates the laser position
    def move(self):
        self.x += self.dx
        self.y += self.dy
    #Draws the laser
    def draw(self, surface):
        pygame.draw.rect(surface, Enum.YELLOW, (self.x + 4, self.y + 4, Enum.GRID_SIZE - 8, Enum.GRID_SIZE - 8))