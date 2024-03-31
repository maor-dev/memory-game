import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH = 600
HEIGHT = 600
ROWS = 4
COLS = 4
TILE_SIZE = 150
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
tiles = []
revealed_tiles = []
current_selection = []
matched_pairs = 0
game_over = False

# Load images
# Determine the desired size of the images based on the game screen size
IMAGE_SIZE = (150, 150)  # Example size, adjust as needed

# Load and resize images
images = [
    pygame.transform.scale(pygame.image.load("images/image1.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image2.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image3.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image4.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image5.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image6.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image7.png"), IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load("images/image8.png"), IMAGE_SIZE),
]

# Duplicate images to create pairs
images *= 2

# Shuffle images
random.shuffle(images)

# Create tiles
for row in range(ROWS):
    for col in range(COLS):
        tile = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tiles.append(tile)

# Main game loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, tile in enumerate(tiles):
                if tile.collidepoint(mouse_x, mouse_y) and i not in revealed_tiles:
                    if len(current_selection) < 2:
                        current_selection.append((i, images[i]))
                        revealed_tiles.append(i)

    # Draw tiles
    for i, tile in enumerate(tiles):
        if i in revealed_tiles or game_over:
            image_index = images[i]
            screen.blit(image_index, tile)
        else:
            pygame.draw.rect(screen, BLACK, tile)

    # Check if two tiles are selected
    if len(current_selection) == 2:
        if current_selection[0][1] == current_selection[1][1]:
            matched_pairs += 1
            if matched_pairs == len(images) // 2:
                game_over = True
        else:
            pygame.time.delay(500)
            revealed_tiles.remove(current_selection[0][0])
            revealed_tiles.remove(current_selection[1][0])
        current_selection = []

    # Display game over message
    if game_over:
        font = pygame.font.Font(None, 64)
        text = font.render("Congratulations! You won!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
