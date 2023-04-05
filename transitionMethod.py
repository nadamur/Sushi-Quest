

import pygame

# Initialize pygame
pygame.init()

# Set up the display
WIN_WIDTH = 800
WIN_HEIGHT = 640
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Win Screen Test")




def display_win_screen(screen, award_image, new_skill, WIN_WIDTH=640, WIN_HEIGHT=800):
    # Render the "You Win!" text
    win_font = pygame.font.Font(None, 72)
    win_text = win_font.render("You Win!", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 100))

    # Load the award image and position it
    award = pygame.image.load(award_image)
    award_rect = award.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    # Render the new skill text
    skill_font = pygame.font.Font(None, 48)
    skill_text = skill_font.render(f"New Skill: {new_skill}", True, (255, 255, 255))
    skill_text_rect = skill_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 100))

    # Draw everything on the screen
    screen.blit(win_text, win_text_rect)
    screen.blit(award, award_rect)
    screen.blit(skill_text, skill_text_rect)

    # Update the display and wait
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
                display_win_screen(screen,"Assets/Sushi/salmon+cucumber.png","Level up")

    pygame.display.update()

# Quit pygame
pygame.quit()
