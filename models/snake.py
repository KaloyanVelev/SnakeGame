import pygame

from models.enums import Enum

#Manages the snake's body, movement, and collision logic.
class Snake:

    def __init__(self):
        # Start in the middle of the screen
        start_x = (Enum.WINDOW_WIDTH // 2) // Enum.GRID_SIZE * Enum.GRID_SIZE
        start_y = (Enum.WINDOW_HEIGHT // 2) // Enum.GRID_SIZE * Enum.GRID_SIZE
        self.body = [[start_x, start_y]]

        # Initial movement direction (moving right)
        self.dx = Enum.GRID_SIZE
        self.dy = 0

        # Queue for responsive input handling (prevents dropped inputs during fast turns)
        self.input_queue = []

        # Flag to track if the snake should grow on the next move
        self.grow_pending = False
    #Key Handler
    def handle_keys(self, event):
        # Determine the current intended direction
        if self.input_queue:
            current_dx, current_dy = self.input_queue[-1]
        else:
            current_dx, current_dy = self.dx, self.dy

        new_dx, new_dy = current_dx, current_dy

        if event.key == pygame.K_UP and current_dy == 0:
            new_dx, new_dy = 0, -Enum.GRID_SIZE
        elif event.key == pygame.K_DOWN and current_dy == 0:
            new_dx, new_dy = 0, Enum.GRID_SIZE
        elif event.key == pygame.K_LEFT and current_dx == 0:
            new_dx, new_dy = -Enum.GRID_SIZE, 0
        elif event.key == pygame.K_RIGHT and current_dx == 0:
            new_dx, new_dy = Enum.GRID_SIZE, 0

        # Add to queue if direction changed
        if (new_dx != current_dx or new_dy != current_dy) and len(self.input_queue) < 2:
            self.input_queue.append((new_dx, new_dy))

    #Move calculation
    def move(self):
        # Process the next queued input, if any
        if self.input_queue:
            self.dx, self.dy = self.input_queue.pop(0)

        head_x, head_y = self.body[0]
        new_head = [head_x + self.dx, head_y + self.dy]

        # Insert new head at the front
        self.body.insert(0, new_head)

        # If we didn't eat an apple, remove the tail.

        if not self.grow_pending:
            self.body.pop()
        # If we did eat an apple, we keep the tail (meaning the snake grew)
        else:
            self.grow_pending = False
    #Checks for collision
    def check_collision(self):
        head = self.body[0]

        # 1. Wall Collision
        if (head[0] < 0 or head[0] >= Enum.WINDOW_WIDTH or
                head[1] < 0 or head[1] >= Enum.WINDOW_HEIGHT):
            return True

        # 2. Self Collision
        if head in self.body[1:]:
            return True

        return False
    #Draws the snake onto the screen
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, Enum.GREEN, (segment[0], segment[1], Enum.GRID_SIZE, Enum.GRID_SIZE))