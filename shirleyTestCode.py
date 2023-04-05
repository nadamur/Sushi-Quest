

import pygame

# Initialize pygame
pygame.init()

# Set up the display
WIN_WIDTH = 800
WIN_HEIGHT = 600
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Win Screen Test")



def display_win_screen(screen, WIN_WIDTH, WIN_HEIGHT):
    win_font = pygame.font.Font(None, 72)
    win_text = win_font.render("You Win!", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    screen.blit(win_text, win_text_rect)
    pygame.display.update()
    pygame.time.delay(3000)



# Main loop
run = True
while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                display_win_screen(screen, WIN_WIDTH, WIN_HEIGHT)

    pygame.display.update()

# Quit pygame
pygame.quit()
