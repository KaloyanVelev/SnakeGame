import pygame
import random
from models.enums import Enum
from objects.laserobj import Laser

#An enemy that sits on the edge of the screen and shoots lasers.
class Enemy:


    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.shoot_timer = random.randint(0, 30)  # Offset initial shot timings
        self.randomize_position()

    #Moves the enemy to a random edge of the screen and faces it inward.
    def randomize_position(self):

        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x = random.randrange(0, Enum.WINDOW_WIDTH, Enum.GRID_SIZE)
            self.y = 0
            self.dx, self.dy = 0, Enum.GRID_SIZE
        elif edge == "bottom":
            self.x = random.randrange(0, Enum.WINDOW_WIDTH, Enum.GRID_SIZE)
            self.y = Enum.WINDOW_HEIGHT - Enum.GRID_SIZE
            self.dx, self.dy = 0, - Enum.GRID_SIZE
        elif edge == "left":
            self.x = 0
            self.y = random.randrange(0, Enum.WINDOW_HEIGHT, Enum.GRID_SIZE)
            self.dx, self.dy = Enum.GRID_SIZE, 0
        elif edge == "right":
            self.x = Enum.WINDOW_WIDTH - Enum.GRID_SIZE
            self.y = random.randrange(0, Enum.WINDOW_HEIGHT, Enum.GRID_SIZE)
            self.dx, self.dy = -Enum.GRID_SIZE, 0

    #Updates the shooting cooldown and spawns lasers.
    def update(self, lasers):

        self.shoot_timer += 1
        if self.shoot_timer >= 45:  # Shoot every 3 seconds (assuming 15 FPS)
            self.shoot_timer = 0
            lasers.append(Laser(self.x, self.y, self.dx, self.dy))
            self.randomize_position()  # Move to a new spot after shooting!

    #Draws the enemy on the screen.
    def draw(self, surface):

        pygame.draw.rect(surface, Enum.ORANGE, (self.x, self.y, Enum.GRID_SIZE, Enum.GRID_SIZE))