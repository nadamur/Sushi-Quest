import pygame
import os

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Character Customization")

# Load background image
background = pygame.image.load("Assets/Backgrounds/characterCustomization_background.jpg")
original_width, original_height = background.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
background = pygame.transform.scale(background, (new_width, SCREEN_HEIGHT))

# Load and resize ninja images
NINJA_COLORS = {
    "blue": "Assets/Ninja/ninja_hero_sprite_blue.png",
    "green": "Assets/Ninja/ninja_hero_sprite_green.png",
    "orange": "Assets/Ninja/ninja_hero_sprite_orange.png",
    "pink": "Assets/Ninja/ninja_hero_sprite_pink.png",
    "purple": "Assets/Ninja/ninja_hero_sprite_purple.png",
    "yellow": "Assets/Ninja/ninja_hero_sprite_yellow.png",
}
SCALE_FACTOR = 0.3  # Change this value to adjust the size of the ninja sprite
ninja_sprites = {
    color: pygame.transform.scale(
        pygame.image.load(path),
        (int(pygame.image.load(path).get_width() * SCALE_FACTOR),
         int(pygame.image.load(path).get_height() * SCALE_FACTOR))
    )
    for color, path in NINJA_COLORS.items()
}

# Set the default ninja color
selected_color = "blue"
ninja = ninja_sprites[selected_color]

# Colors
WHITE = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

def draw_window(selected_color):
    WIN.blit(background, (0, 0))  # Draw the background image
    color_text = font.render(f"Selected color: {selected_color.capitalize()}", True, (0, 0, 0))
    WIN.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 50))
    WIN.blit(ninja_sprites[selected_color], (SCREEN_WIDTH // 2 - ninja_sprites[selected_color].get_width() // 2, SCREEN_HEIGHT // 2 - ninja_sprites[selected_color].get_height() // 2))
    pygame.display.update()

def main():
    global selected_color
    run = True
    while run:
        draw_window(selected_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_color = list(ninja_sprites.keys())[list(ninja_sprites.keys()).index(selected_color) - 1]
                if event.key == pygame.K_RIGHT:
                    selected_color = list(ninja_sprites.keys())[(list(ninja_sprites.keys()).index(selected_color) + 1) % len(ninja_sprites)]
    pygame.quit()

if __name__ == "__main__":
    main()
