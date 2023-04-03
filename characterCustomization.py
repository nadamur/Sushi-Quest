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
background = pygame.image.load("Assets/Backgrounds/characterCustomization_background.png")
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


# Load input box for name
def input_box(input_text, x, y):
    input_box_font = pygame.font.Font("Fonts/COMIC.TTF", 36)
    input_box_surface = input_box_font.render(input_text, True, WHITE)
    input_box_rect = input_box_surface.get_rect()
    input_box_rect.topleft = (x, y)
    WIN.blit(input_box_surface, input_box_rect)
    pygame.draw.rect(WIN, WHITE, input_box_rect, 2)
    return input_box_rect

# Set the default ninja color
selected_color = "blue"
ninja = ninja_sprites[selected_color]

# Colors
WHITE = (255, 255, 255)



def draw_window(selected_color, input_text):

    WIN.blit(background, (0, 0))  # Draw the background image

    # Draw the ninja sprite
    WIN.blit(ninja_sprites[selected_color], (SCREEN_WIDTH // 2 - ninja_sprites[selected_color].get_width() // 2, 295))

    # Draw the text
    font = pygame.font.Font("Fonts/COMICBD.TTF", 16)
    color_text = font.render(f"Toggle between the left and right arrow keys to selected colors: {selected_color.capitalize()}", True, WHITE)
    WIN.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 570))
    
    # Draw the input box
    font = pygame.font.Font("Fonts/COMIC.TTF", 30)
    label = font.render("Change the character's name:", True, WHITE)
    WIN.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 70))
    input_rect = input_box(input_text, SCREEN_WIDTH // 2 - 130 // 2, 130)
    pygame.display.update()
    return input_rect
    

def main():
    global selected_color
    run = True
    input_text = "Ninja"
    active = True
    while run:
        input_rect = draw_window(selected_color, input_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_color = list(ninja_sprites.keys())[list(ninja_sprites.keys()).index(selected_color) - 1]
                if event.key == pygame.K_RIGHT:
                    selected_color = list(ninja_sprites.keys())[(list(ninja_sprites.keys()).index(selected_color) + 1) % len(ninja_sprites)]
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("Character name:", input_text)
                    else:
                        input_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
    pygame.quit()

if __name__ == "__main__":
    main()
