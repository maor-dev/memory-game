import pygame
import random
import sys
import time

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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

# Start time
start_time = time.time()
end_time = None
# Load positive sound
positive_sound = pygame.mixer.Sound("sound/success.MP3")

# Define reset button
reset_button = pygame.Rect(10, 10, 100, 50)  # x, y, width, height

# Main game loop
while True:
    # Calculate elapsed time if the game is not over
    if not game_over:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"

    screen.fill(WHITE)

    # Draw grid lines
    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if reset_button.collidepoint(mouse_x, mouse_y):
                # Reset game variables
                tiles = []
                revealed_tiles = []
                current_selection = []
                matched_pairs = 0
                game_over = False
                start_time = time.time()
                end_time = None
                # Shuffle images
                random.shuffle(images)

                # Create tiles
                for row in range(ROWS):
                    for col in range(COLS):
                        tile = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        tiles.append(tile)
            else:
                # Check if a tile is clicked
                for i, tile in enumerate(tiles):
                    if tile.collidepoint(mouse_x, mouse_y) and i not in revealed_tiles:
                        if len(current_selection) < 2:
                            current_selection.append((i, images[i]))
                            revealed_tiles.append(i)
                            
    # Draw reset button
    pygame.draw.rect(screen, GREEN, reset_button)
    font = pygame.font.Font(None, 36)
    reset_text = font.render("Reset", True, WHITE)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)

    # Draw tiles
    for i, tile in enumerate(tiles):
        if i in revealed_tiles or game_over:
            image_index = images[i]
            screen.blit(image_index, tile)

    # Draw timer if the game is not over
    if not game_over:
        font = pygame.font.Font(None, 36)
        timer_surface = font.render(timer_text, True, RED)
        timer_rect = timer_surface.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(timer_surface, timer_rect)

    # Check if two tiles are selected
    if len(current_selection) == 2:
        if current_selection[0][1] == current_selection[1][1]:
            positive_sound.play()
            matched_pairs += 1
            if matched_pairs == len(images) // 2:
                # Record end time when game is won
                end_time = time.time()
                # Stop the timer
                game_over = True
        else:
            pygame.time.delay(500)
            revealed_tiles.remove(current_selection[0][0])
            revealed_tiles.remove(current_selection[1][0])
        current_selection = []

    # Display game over message
    if game_over:
        # Calculate total elapsed time
        total_elapsed_time = int(end_time - start_time)
        total_minutes = total_elapsed_time // 60
        total_seconds = total_elapsed_time % 60
       

        total_timer_text = f"Total Time: {total_minutes:02d}:{total_seconds:02d}"

        font = pygame.font.Font(None, 64)
        text = font.render("Congratulations! You won!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        # Display total elapsed time
        timer_surface = font.render(total_timer_text, True, GREEN)
        timer_rect = timer_surface.get_rect(midtop=(WIDTH // 2, text_rect.bottom + 20))
        screen.blit(timer_surface, timer_rect)

    pygame.display.flip()
