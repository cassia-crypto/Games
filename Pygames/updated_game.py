import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid (16 cards)
CARD_SIZE = WIDTH // GRID_SIZE  # Each card's size
TOP_BAR_HEIGHT = 50  # Space for timer & score

screen = pygame.display.set_mode((WIDTH, HEIGHT + TOP_BAR_HEIGHT))
pygame.display.set_caption("Purble Pairs - Memory Game")

# Colors
LIGHT_PINK = (255, 182, 193)
CARD_BACK_COLOR = (181, 148, 182)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load sounds safely
flip_sound = pygame.mixer.Sound("flip.wav") if os.path.exists("flip.wav") else None
match_sound = pygame.mixer.Sound("match.wav") if os.path.exists("match.wav") else None
win_sound = pygame.mixer.Sound("win.wav") if os.path.exists("win.wav") else None

# Load card images
CARD_IMAGES = [
    pygame.transform.scale(pygame.image.load(f"card{i}.png"), (CARD_SIZE, CARD_SIZE))
    for i in range(1, 9)
] * 2  # Duplicate each for pairs

random.shuffle(CARD_IMAGES)

# Create card structure
cards = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        card = {
            "image": CARD_IMAGES.pop(),
            "rect": pygame.Rect(col * CARD_SIZE, row * CARD_SIZE + TOP_BAR_HEIGHT, CARD_SIZE, CARD_SIZE),
            "flipped": True,  # Initially flipped to show all cards
            "matched": False,
            "animating": False,
            "scale": CARD_SIZE,
            "shrinking": True
        }
        cards.append(card)

# Show all cards for 1.5 seconds
screen.fill(LIGHT_PINK)
for card in cards:
    screen.blit(card["image"], card["rect"])
    pygame.draw.rect(screen, WHITE, card["rect"], 3)  # Draw white border
pygame.display.update()
pygame.time.delay(1500)  # Wait for 1.5 seconds

# Flip all cards back
for card in cards:
    card["flipped"] = False

# Game variables
first_card = None
second_card = None
flipping = False
flip_time = 0
game_won = False
start_time = pygame.time.get_ticks()
moves = 0

# Font
font = pygame.font.Font(None, 36)

def flip_animation(card):
    """Animate card flip."""
    if card["shrinking"]:
        card["scale"] -= 10  # Shrink
        if card["scale"] <= 0:
            card["shrinking"] = False
            card["flipped"] = not card["flipped"]  # Swap image
    else:
        card["scale"] += 10  # Expand
        if card["scale"] >= CARD_SIZE:
            card["scale"] = CARD_SIZE
            card["animating"] = False  # Stop animation

def reset_game():
    """Reset the game when all pairs are found."""
    global first_card, second_card, flipping, game_won, start_time, moves

    game_won = True
    if win_sound:
        pygame.mixer.Sound.play(win_sound)

    screen.fill(LIGHT_PINK)
    text_surface = font.render(f"You Win! Moves: {moves}", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)

    game_won = False
    for card in cards:
        card["flipped"] = False
        card["matched"] = False
    random.shuffle(cards)
    first_card, second_card = None, None
    flipping = False
    start_time = pygame.time.get_ticks()
    moves = 0

# Main game loop
running = True
while running:
    screen.fill(LIGHT_PINK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not flipping:
            mouse_pos = pygame.mouse.get_pos()
            for card in cards:
                if card["rect"].collidepoint(mouse_pos) and not card["flipped"] and not card["matched"] and not card["animating"]:
                    if flip_sound:
                        pygame.mixer.Sound.play(flip_sound)
                    card["animating"] = True
                    card["shrinking"] = True
                    moves += 1
                    if first_card is None:
                        first_card = card
                    elif second_card is None:
                        second_card = card
                        flipping = True
                        flip_time = pygame.time.get_ticks()

    # Flip animation
    for card in cards:
        if card["animating"]:
            flip_animation(card)

    # Check for a match after a delay
    if flipping and pygame.time.get_ticks() - flip_time > 1000:
        if first_card and second_card:
            if first_card["image"] == second_card["image"]:
                if match_sound:
                    pygame.mixer.Sound.play(match_sound)
                first_card["matched"] = True
                second_card["matched"] = True
            else:
                first_card["animating"] = True
                second_card["animating"] = True
                first_card["shrinking"] = True
                second_card["shrinking"] = True

        first_card, second_card = None, None
        flipping = False

        if all(card["matched"] for card in cards):
            reset_game()

    # Draw UI
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, TOP_BAR_HEIGHT))
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
    moves_text = font.render(f"Moves: {moves}", True, BLACK)
    screen.blit(timer_text, (20, 10))
    screen.blit(moves_text, (WIDTH - 150, 10))

    # Draw cards
    for card in cards:
        x, y, w, h = card["rect"]
        scaled_rect = pygame.Rect(x + (CARD_SIZE - card["scale"]) // 2, y, card["scale"], h)

        if card["flipped"] or card["matched"]:
            screen.blit(pygame.transform.scale(card["image"], (card["scale"], CARD_SIZE)), scaled_rect)
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, scaled_rect)
            pygame.draw.rect(screen, WHITE, scaled_rect, 3)  # White border for hidden cards

    if game_won:
        text_surface = font.render(f"You Win! Moves: {moves}", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.update()

pygame.quit()
