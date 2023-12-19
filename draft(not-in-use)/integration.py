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
intro_bg = pygame.image.load("Assets/Backgrounds/intro_background.png")
original_width, original_height = start_bg.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
start_bg = pygame.transform.scale(start_bg, (new_width, SCREEN_HEIGHT))
start_effect = pygame.transform.scale(start_effect, (new_width, SCREEN_HEIGHT))
intro_bg = pygame.transform.scale(intro_bg, (new_width, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# -------------------------------- Starting screen -------------------------------------- 

def create_button(text, font, color, bg_color, pos, padding=10, border_width=1, border_color=BLACK):
    """
    Creates a button with the given text, font, color, and background color at the given position.
    """
    text_surface = font.render(text, True, color)
    button_rect = text_surface.get_rect()
    button_rect.center = pos

    # Check if the mouse is hovering over the button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(WIN, bg_color, button_rect)  # Fill the button with background color
        text_surface = font.render(text, True, color)  # Set text color to foreground color
    else:
        pygame.draw.rect(WIN, color, button_rect)  # Fill the button with foreground color
        text_surface = font.render(text, True, bg_color)  # Set text color to background color

    # Add padding and border to the button
    button_rect.inflate_ip(padding, padding)
    pygame.draw.rect(WIN, border_color, button_rect, border_width)

    # Draw the button and update the display
    WIN.blit(text_surface, text_surface.get_rect(center=pos))
    pygame.display.update(button_rect)

    return button_rect



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


# ----------------------- Create Button Function -------------------
def create_button(text, pos, text_color=WHITE, border_color=BLACK, padding=10, border_width=0, font_path="Fonts/COMIC.TTF", font_size=30):
    button_font = pygame.font.Font(font_path, font_size)
    button_text = button_font.render(text, True, text_color)
    button_rect = button_text.get_rect()
    button_rect.inflate_ip(padding * 2, 0)
    button_rect.center = pos

    pygame.draw.rect(WIN, border_color, button_rect, border_width)
    WIN.blit(button_text, (button_rect.x + padding, button_rect.y))

    return button_rect


# ----------------------- Background screen ------------------------- 


def draw_background_page(mouse_pos):
    WIN.blit(intro_bg, (0, 0))  # Draw the background image

    # Draw the game title
    title_font = pygame.font.Font("Fonts/COMICBD.TTF", 45)
    title_text = title_font.render("Background", True, WHITE)
    WIN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))


    # Draw the game introduction text
    intro_font = pygame.font.Font("Fonts/COMIC.TTF", 18)
    intro_text = (
        "You are a skilled ninja on a mission to create the ultimate sushi, a revered work of art in this enchanted world. "
        "Armed with your lightning-fast reflexes, you must collect the sushi ingredients through combating various challenges. "
        "Along the way, wise NPCs will offer hints and humor to aid you. Will you rise to the challenge and craft the ultimate sushi? "
        "The journey begins now."
    )
    intro_lines = intro_text.split(" ")
    rendered_lines = []
    current_line = ""

    for word in intro_lines:
        temp_line = current_line + word + " "
        if intro_font.size(temp_line)[0] > SCREEN_WIDTH - 60:
            rendered_lines.append(current_line)
            current_line = word + " "
        else:
            current_line = temp_line

    rendered_lines.append(current_line)

    y_pos = 220
    for line in rendered_lines:
        rendered_text = intro_font.render(line, True, WHITE)
        WIN.blit(rendered_text, (30, y_pos))
        y_pos += rendered_text.get_height() + 5


    # Draw the continue button using the create_button function
    button_rect = create_button("Continue", (400, 500))

    # Update the button colors based on mouse hover
    if button_rect.collidepoint(mouse_pos):
        button_rect = create_button("Continue", (400, 500), border_color=(251, 47, 0))
    else:
        button_rect = create_button("Continue", (400, 500), text_color=BLACK, border_color=WHITE)

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
    "red": "Assets/Ninja/ninja_hero_sprite_red.png",
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

    # Background page loop
    background_page = True
    while background_page and run:
        mouse_pos = pygame.mouse.get_pos()
        continue_button = draw_background_page(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                background_page = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    background_page = False

    # Character customization loop
    global selected_color
    customization_screen = True
    input_text = "Ninja"
    name = "Ninja"
    active = True
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

    while level2 and run:
        #event loop
        clock.tick(FPS)
        draw_bg()
        world.draw()
        sc = round(score)
        s = str(sc)
        screen.blit(fontScore.render("Score: " + s,True,(255,0,0)),(50,50))
        if ninja.alive:
            score += score_increment
    
        # commenting out the enemy for now
        healthbar.draw(ninja.health,screen)
        ninja.update()
        ninja.draw(screen)

        #draw enemies on screen
        for enemy in enemy_ninja_group:
            enemy.draw(screen)
            enemy.ai(ninja)
            enemy.update()
            enemy.move_towards_ninja(ninja)
            if pygame.sprite.spritecollide(enemy,hero_group,False):
                if enemy.alive:
                    enemy.hit()

        for p in punch_group:
            p.move(moving_left,moving_right)
            p.draw()
            p.update()
        for h in hit_group:
            h.update()
            h.draw()


        if ninja.alive:
            screen_scroll = ninja.move(moving_left,moving_right)
            bg_scroll -= screen_scroll
            if punch:
                ninja.punch()
                punch = False
                
        #game logic
        screen.blit(fontText.render(getReadyText,True,(0,0,0)),(100,100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #keyboard press
            if event.type == pygame.USEREVENT:
                counter -= 1
                if phaseNum ==0:
                    if counter > 2:
                        text = str(counter-2)
                    elif counter > 0:
                        text = 'Start'
                    elif counter == 0:
                        text = 'Start!'
                        phaseNum += 1
                if phaseNum == 2:
                    counter = reset_count(counter,reset_counter_2)
                    reset_counter_2 = False
                    if counter == 7:
                        getReadyText = '   Phase 1 Complete!'
                    elif counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 2!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level1_done = True
                if phaseNum == 3:
                    counter = reset_count(counter,reset_counter_3)
                    reset_counter_3 = False
                    if counter == 7:
                        getReadyText = '   Phase 2 Complete!'
                    if counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 3!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level2_done = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right= True
                if event.key == pygame.K_UP and ninja.alive:
                    ninja.jump = True
                    for p in punch_group:
                        p.jump = True
                if event.key == pygame.K_SPACE:
                    punch = True
            #keyboard release
            if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right= False
        screen.blit(fontNum.render(text,True,(0,0,0)),(350,200))
        if text == 'Start!':
            text = ''
            getReadyText = ''
        start = pygame.time.get_ticks()

        if level_done:
            phaseNum += 1
            level_done = False
        
        if phaseNum == 1 and x == 0:
            print(phaseNum)
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(3,createEnemy)
            timer.start()
            x = 1
            level1_intro_done = True

        if phaseNum == 2 and level1_done == True:
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level1_done = False

        if phaseNum ==3 and level2_done == True:
            level1_done = False
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level2_done = False
        if phaseNum == 4:
            getReadyText = '     YOU DID IT!'
            
        level_done = check_level_done()
        if level_done == True:
            reset_enemies()

        pygame.display.update()
        #render
        #event loop
        clock.tick(FPS)
        draw_bg()
        world.draw()
        sc = round(score)
        s = str(sc)
        screen.blit(fontScore.render("Score: " + s,True,(255,0,0)),(50,50))
        if ninja.alive:
            score += score_increment
    
        # commenting out the enemy for now
        healthbar.draw(ninja.health,screen)
        ninja.update()
        ninja.draw(screen)

        #draw enemies on screen
        for enemy in enemy_ninja_group:
            enemy.draw(screen)
            enemy.ai(ninja)
            enemy.update()
            enemy.move_towards_ninja(ninja)
            if pygame.sprite.spritecollide(enemy,hero_group,False):
                if enemy.alive:
                    enemy.hit()

        for p in punch_group:
            p.move(moving_left,moving_right)
            p.draw()
            p.update()
        for h in hit_group:
            h.update()
            h.draw()


        if ninja.alive:
            screen_scroll = ninja.move(moving_left,moving_right)
            bg_scroll -= screen_scroll
            if punch:
                ninja.punch()
                punch = False
                
        #game logic
        screen.blit(fontText.render(getReadyText,True,(0,0,0)),(100,100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #keyboard press
            if event.type == pygame.USEREVENT:
                counter -= 1
                if phaseNum ==0:
                    if counter > 2:
                        text = str(counter-2)
                    elif counter > 0:
                        text = 'Start'
                    elif counter == 0:
                        text = 'Start!'
                        phaseNum += 1
                if phaseNum == 2:
                    counter = reset_count(counter,reset_counter_2)
                    reset_counter_2 = False
                    if counter == 7:
                        getReadyText = '   Phase 1 Complete!'
                    elif counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 2!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level1_done = True
                if phaseNum == 3:
                    counter = reset_count(counter,reset_counter_3)
                    reset_counter_3 = False
                    if counter == 7:
                        getReadyText = '   Phase 2 Complete!'
                    if counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 3!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level2_done = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right= True
                if event.key == pygame.K_UP and ninja.alive:
                    ninja.jump = True
                    for p in punch_group:
                        p.jump = True
                if event.key == pygame.K_SPACE:
                    punch = True
            #keyboard release
            if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right= False
        screen.blit(fontNum.render(text,True,(0,0,0)),(350,200))
        if text == 'Start!':
            text = ''
            getReadyText = ''
        start = pygame.time.get_ticks()

        if level_done:
            phaseNum += 1
            level_done = False
        
        if phaseNum == 1 and x == 0:
            print(phaseNum)
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(3,createEnemy)
            timer.start()
            x = 1
            level1_intro_done = True

        if phaseNum == 2 and level1_done == True:
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level1_done = False

        if phaseNum ==3 and level2_done == True:
            level1_done = False
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level2_done = False
        if phaseNum == 4:
            getReadyText = '     YOU DID IT!'
            
        level_done = check_level_done()
        if level_done == True:
            reset_enemies()

        pygame.display.update()
        #render










    pygame.quit()

if __name__ == "__main__":
    main()
