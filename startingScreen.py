import pygame
import os

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sushi Quest: a Ninja’s Journey")

# Load background image
background = pygame.image.load("Assets/Backgrounds/characterCustomization_background.png")
original_width, original_height = background.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
background = pygame.transform.scale(background, (new_width, SCREEN_HEIGHT))

# ... [rest of your code]

def draw_starting_screen():
    WIN.blit(background, (0, 0))  # Draw the background image

    # Draw the game title
    title_font = pygame.font.Font("Fonts/COMICBD.TTF", 48)
    title_text = title_font.render("Sushi Quest: a Ninja's Journey", True, WHITE)
    WIN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    # Draw the start button
    button_font = pygame.font.Font("Fonts/COMIC.TTF", 36)
    button_text = button_font.render("Start", True, WHITE)
    button_rect = button_text.get_rect()
    button_rect.center = (SCREEN_WIDTH // 2, 300)
    WIN.blit(button_text, button_rect)
    pygame.draw.rect(WIN, WHITE, button_rect, 2)

    pygame.display.update()
    return button_rect

def main():
    # ... [your main function]

    starting_screen = True
    while starting_screen:
        start_button = draw_starting_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting_screen = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    starting_screen = False

    # ... [rest of your main function]

if __name__ == "__main__":
    main()
