from typing import override
import pygame
from models.enums import Enum
from objects.apple import Apple


class PoisonApple(Apple):
    #Initialises values
    def __init__(self):
        super().__init__()

    #Draws the apple
    @override
    def draw(self, surface):
        """Draws the poisonous apple in purple."""
        pygame.draw.rect(surface, Enum.PURPLE, (self.x, self.y, Enum.GRID_SIZE, Enum.GRID_SIZE))