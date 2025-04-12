import pygame
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound system

# Set up display
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid (16 cards)
CARD_SIZE = WIDTH // GRID_SIZE  # Each card's size

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Purble Pairs - Memory Game")

# Colors
LIGHT_PINK = (255, 182, 193)  # Background color
CARD_BACK_COLOR = (181, 148, 182)  # #B594B6 card back color
WHITE = (255, 255, 255)  # Grid and card border color
BLACK = (0, 0, 0)  # For text

# Load sounds (check if files exist)
flip_sound = pygame.mixer.Sound("flip.wav") if os.path.exists("flip.wav") else None
match_sound = pygame.mixer.Sound("match.wav") if os.path.exists("match.wav") else None
win_sound = pygame.mixer.Sound("win.wav") if os.path.exists("win.wav") else None

# Load card images (8 unique images, duplicated for pairs)
CARD_IMAGES = [
    pygame.transform.scale(pygame.image.load(f"card{i}.png"), (CARD_SIZE, CARD_SIZE))
    for i in range(1, 9)
] * 2  # Duplicate each for pairs

random.shuffle(CARD_IMAGES)  # Shuffle card positions

# Create card data structure
cards = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        card = {
            "image": CARD_IMAGES.pop(),
            "rect": pygame.Rect(col * CARD_SIZE, row * CARD_SIZE, CARD_SIZE, CARD_SIZE),
            "flipped": False,  
            "matched": False  
        }
        cards.append(card)

# Game variables
first_card = None
second_card = None
flipping = False
flip_time = 0
game_won = False

# Font for "You Win!" message
font = pygame.font.Font(None, 60)

def reset_game():
    """Reset the game when all pairs are found."""
    global first_card, second_card, flipping, game_won

    game_won = True  # Set win flag
    if win_sound:
        pygame.mixer.Sound.play(win_sound)  # Play win sound

    # Display "You Win!" for 3 seconds
    screen.fill(LIGHT_PINK)
    text_surface = font.render("You Win!", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Pause for 3 seconds

    # Reset game state
    game_won = False
    for card in cards:
        card["flipped"] = False
        card["matched"] = False
    random.shuffle(cards)  # Shuffle cards again
    first_card, second_card = None, None
    flipping = False

# Main game loop
running = True
while running:
    screen.fill(LIGHT_PINK)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not flipping:
            mouse_pos = pygame.mouse.get_pos()
            for card in cards:
                if card["rect"].collidepoint(mouse_pos) and not card["flipped"] and not card["matched"]:
                    if flip_sound:
                        pygame.mixer.Sound.play(flip_sound)  # Play flip sound
                    card["flipped"] = True
                    if first_card is None:
                        first_card = card
                    elif second_card is None:
                        second_card = card
                        flipping = True
                        flip_time = pygame.time.get_ticks()

    # Check for a match after a delay
    if flipping and pygame.time.get_ticks() - flip_time > 1000:
        if first_card and second_card:
            if first_card["image"] == second_card["image"]:
                if match_sound:
                    pygame.mixer.Sound.play(match_sound)  # Play match sound
                first_card["matched"] = True
                second_card["matched"] = True
            else:
                first_card["flipped"] = False
                second_card["flipped"] = False

        first_card, second_card = None, None
        flipping = False

        # Check if all cards are matched
        if all(card["matched"] for card in cards):
            reset_game()

    # Draw cards and grid lines
    for card in cards:
        if card["flipped"] or card["matched"]:
            screen.blit(card["image"], card["rect"])
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, card["rect"])  # Card back
            pygame.draw.rect(screen, WHITE, card["rect"], 3)  # White grid line

    pygame.display.update()

pygame.quit()
