from models.enums import Enum
from objects.apple import Apple
from models.snake import Snake
from objects.poison_apple import PoisonApple
from models.enemy import Enemy
import pygame
import sys

#The main game engine that ties all the objects together.
class Game:


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Enum.WINDOW_WIDTH, Enum.WINDOW_HEIGHT))
        pygame.display.set_caption("OOP Snake with Loading Screen")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Game State Variables
        self.state = "LOADING"  # Can be "LOADING", "START_MENU", "PLAYING", or "GAME_OVER"
        self.loading_progress = 0
        self.running = True
        self.score = 0

        # Instantiate our game objects
        self.snake = Snake()
        self.apple = Apple()
        self.poison_apple = PoisonApple()
        self.enemies = [Enemy() for _ in range(2)]  # Add 3 enemies
        self.lasers = []

        self.apple.spawn(self.snake.body)
        self.poison_apple.spawn(self.snake.body, [self.apple.x, self.apple.y])

    #Resets the game state to play again.
    def reset_game(self):

        self.snake = Snake()
        self.apple = Apple()
        self.poison_apple = PoisonApple()
        self.enemies = [Enemy() for _ in range(3)]
        self.lasers = []
        self.score = 0
        self.state = "PLAYING"

        self.apple.spawn(self.snake.body)
        self.poison_apple.spawn(self.snake.body, [self.apple.x, self.apple.y])

    #Processes all user inputs.
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Only let the snake handle keys if we are actively playing
                if self.state == "PLAYING":
                    self.snake.handle_keys(event)
                # Start game from menu
                elif self.state == "START_MENU":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = "PLAYING"
                # Play again hotkey
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()

    #Updates game logic based on the current state.
    def update(self):

        if self.state == "LOADING":
            # Simulate a loading process by increasing progress every frame
            self.loading_progress += 3
            if self.loading_progress >= 100:
                self.state = "START_MENU"  # Switch to start menu when loaded!

        elif self.state == "PLAYING":
            self.snake.move()

            # Check for collisions leading to Game Over
            if self.snake.check_collision():
                self.state = "GAME_OVER"

            # Update Enemies and Lasers
            for enemy in self.enemies:
                enemy.update(self.lasers)

            for laser in self.lasers[:]:  # Iterate over a copy to safely remove items
                laser.move()
                # If laser hits the snake body, GAME OVER
                if [laser.x, laser.y] in self.snake.body:
                    self.state = "GAME_OVER"

                # Clean up lasers that go off screen
                if (laser.x < 0 or laser.x >= Enum.WINDOW_WIDTH or
                        laser.y < 0 or laser.y >= Enum.WINDOW_HEIGHT):
                    if laser in self.lasers:
                        self.lasers.remove(laser)

            # Check if snake eats the regular apple
            if self.snake.body[0] == [self.apple.x, self.apple.y]:
                self.snake.grow_pending = True
                self.score += 1
                self.apple.spawn(self.snake.body, [self.poison_apple.x, self.poison_apple.y])

            # Check if snake eats the poison apple
            elif self.snake.body[0] == [self.poison_apple.x, self.poison_apple.y]:
                if len(self.snake.body) > 1:
                    # Shrink the snake and optionally reduce score
                    self.snake.body.pop()
                    self.score = max(0, self.score - 1)
                    self.poison_apple.spawn(self.snake.body, [self.apple.x, self.apple.y])
                else:
                    # If length is 1, just respawn the poison apple without dying!
                    self.poison_apple.spawn(self.snake.body, [self.apple.x, self.apple.y])

    #Renders graphics to the screen based on the current state.
    def draw(self):

        self.screen.fill(Enum.BLACK)

        if self.state == "LOADING":
            # Draw "Loading..." Text
            text = self.font.render("Loading Assets...", True, Enum.WHITE)
            text_rect = text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(text, text_rect)

            # Draw Loading Bar Outline
            pygame.draw.rect(self.screen, Enum.WHITE, (Enum.WINDOW_WIDTH // 2 - 150, Enum.WINDOW_HEIGHT // 2, 300, 20), 2)
            # Draw Loading Bar Fill based on progress
            fill_width = int((296 * self.loading_progress) / 100)
            if fill_width > 296: fill_width = 296
            pygame.draw.rect(self.screen, Enum.BLUE, (Enum.WINDOW_WIDTH // 2 - 148, Enum.WINDOW_HEIGHT // 2 + 2, fill_width, 16))

        elif self.state == "START_MENU":
            # Draw Title
            title_text = self.font.render("OOP SNAKE", True, Enum.GREEN)
            title_rect = title_text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(title_text, title_rect)

            # Draw Start Instruction
            start_text = self.font.render("Press SPACE to Start", True, Enum.WHITE)
            start_rect = start_text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(start_text, start_rect)

        elif self.state == "PLAYING":
            # Draw entities
            for enemy in self.enemies:
                enemy.draw(self.screen)
            for laser in self.lasers:
                laser.draw(self.screen)

            self.apple.draw(self.screen)
            self.poison_apple.draw(self.screen)
            self.snake.draw(self.screen)

            score_text = self.font.render(f"Score: {self.score}", True, Enum.WHITE)
            self.screen.blit(score_text, (10, 10))

        elif self.state == "GAME_OVER":
            go_text = self.font.render("GAME OVER", True, Enum.RED)
            go_rect = go_text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(go_text, go_rect)

            sc_text = self.font.render(f"Final Score: {self.score}", True, Enum.WHITE)
            sc_rect = sc_text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2))
            self.screen.blit(sc_text, sc_rect)

            # Play again instruction
            pa_text = self.font.render("Press SPACE to Play Again", True, Enum.BLUE)
            pa_rect = pa_text.get_rect(center=(Enum.WINDOW_WIDTH // 2, Enum.WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(pa_text, pa_rect)

        pygame.display.flip()

    #The main Game loop.
    def run(self):

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(Enum.FPS)

        pygame.quit()
        sys.exit()


