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
start_bg = pygame.image.load("Assets/Backgrounds/start_background.png")
start_effect = pygame.image.load("Assets/Backgrounds/start_effect.png")
original_width, original_height = start_bg.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
start_bg = pygame.transform.scale(start_bg, (new_width, SCREEN_HEIGHT))
start_effect = pygame.transform.scale(start_effect, (new_width, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)




# ------------------------ Starting screen -------------------------------- 

def draw_starting_screen(mouse_pos):
    WIN.blit(start_bg, (0, 0))  # Draw the background image

    # Draw the game title
    title_font = pygame.font.Font("Fonts/COMICBD.TTF", 45)
    title_text = title_font.render("Sushi Quest: A Ninja's Journey", True, WHITE)
    WIN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    # Add creators names
    creators_font = pygame.font.Font("Fonts/COMIC.TTF", 15)
    creators_text = creators_font.render("Created by: Neda, Luke, Shirley and Kyloc", True, WHITE)
    WIN.blit(creators_text, (SCREEN_WIDTH // 2 - creators_text.get_width() // 2, 170))

    # Draw the start button
    button_font = pygame.font.Font("Fonts/COMIC.TTF", 40)
    button_text = button_font.render("Start", True, BLACK)
    button_rect = button_text.get_rect()
    button_rect.center = (SCREEN_WIDTH // 2, 425)

    # Check if the mouse is hovering over the button
    if button_rect.collidepoint(mouse_pos):
        WIN.blit(start_effect, (0, 0))  # Draw the background image
        # pygame.draw.rect(WIN, BLACK, button_rect)  # Fill the button with black
        button_text = button_font.render("Start", True, (251, 47, 0))  # Set text color to red
    else:
        # pygame.draw.rect(WIN, WHITE, button_rect)  # Fill the button with white
        button_text = button_font.render("Start", True, BLACK)  # Set text color to black


    WIN.blit(button_text, button_rect)
    # pygame.draw.rect(WIN, WHITE, button_rect, 2)

    pygame.display.update()
    return button_rect



# ----------------------- Character customization screen ------------------------- 

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


def draw_characterCustomization(selected_color, input_text, name):

    WIN.blit(start_bg, (0, 0))  # Draw the background image

    # Draw the text
    font = pygame.font.Font("Fonts/COMICBD.TTF", 16)
    color_text = font.render(f"Toggle between the left and right arrow keys to selected colors: {selected_color.capitalize()}", True, WHITE)
    WIN.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 570))
    
    # Draw the ninja sprite
    WIN.blit(ninja_sprites[selected_color], (SCREEN_WIDTH // 2 - ninja_sprites[selected_color].get_width() // 2, 295))

    # Draw the input box
    font = pygame.font.Font("Fonts/COMIC.TTF", 30)
    label = font.render("Change the character's name:", True, WHITE)
    namePrinted = font.render(f"{name}", True, BLACK)
    WIN.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 50))
    WIN.blit(namePrinted, (SCREEN_WIDTH // 2 - namePrinted.get_width() // 2, 300))
    input_rect = input_box(input_text, SCREEN_WIDTH // 2 - 130 // 2, 130)
    font1 = pygame.font.Font("Fonts/COMIC.TTF", 17)
    label1 = font1.render("Press enter to save the name", True, WHITE)
    WIN.blit(label1, (SCREEN_WIDTH // 2 - label1.get_width() // 2, 90))

    pygame.display.update()
    return input_rect
    



# -------------------------------- Main Loop -------------------------------------

def main():

    run = True # Main loop

    # Starting screen loop
    starting_screen = True
    while starting_screen and run:
        mouse_pos = pygame.mouse.get_pos()
        start_button = draw_starting_screen(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting_screen = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    starting_screen = False

    # Character customization variables
    global selected_color
    customization_screen = True
    input_text = "Ninja"
    name = "Ninja"
    active = True

    # Character customization loop
    while customization_screen and run:
        input_rect = draw_characterCustomization(selected_color, input_text, name)
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
                        name = input_text # save the name of the character
                        ninjaColor = selected_color # save the color of the character
                    else:
                        input_text += event.unicode

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if input_rect.collidepoint(event.pos):
            #         active = not active
            #     else:
            #         active = False
             
    pygame.quit()

if __name__ == "__main__":
    main()
