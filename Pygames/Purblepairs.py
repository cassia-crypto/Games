import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid
CARD_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Purble Pairs - Memory Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Fill background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()  # Refresh screen

pygame.quit()
