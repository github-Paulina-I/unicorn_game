import os
import pygame
import sys
from pygame.locals import *
import random
import pygame_menu

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Unicorn Journey")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("SANS_BOLD",70, bold=True)

def start_the_game(difficulty):
    if difficulty == 1: #łatwy
        unicornSpeed = 4
        pipeSpeed = 1300
    elif difficulty == 2: #średni
        unicornSpeed = 7
        pipeSpeed = 1300
    else: #trudny
        unicornSpeed = 5
        pipeSpeed = 1000

    def move_ground():
        screen.blit(ground_image, (ground_x, 510))
        screen.blit(ground_image, (ground_x + 700, 510))


    def create_pipe():
        random_hight = random.choice(pipe_height)
        bottom_pipe = rainbow_image.get_rect(midtop=(700, random_hight))
        top_pipe = rainbow_image.get_rect(midtop=(700, random_hight - 600))
        return bottom_pipe, top_pipe


    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes


    def draw_pipes(pipes):
        for pipe in pipes:
            screen.blit(rainbow_image, pipe)


    def check_collisions(pipes):
        for pipe in pipes:
            if unicorn_rectangle.colliderect(pipe):
                horse_sound.play()
                return False
        if unicorn_rectangle.top <= 0 or unicorn_rectangle.bottom >= 510:
            horse_sound.play()
            return False
        return True


    def update_score(score, high_score):
        if score > high_score:
            high_score = score
        return  high_score

    def display_scores(game_state):
        if game_state == 'main_game':
            score_surface = game_font.render(str(int(score)), True, (51,102,204))
            score_rect = score_surface.get_rect(center=(60, 50))
            screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = game_font.render(f'Score: {int(score)}', True, (51,102,204))
            score_rect = score_surface.get_rect(center=(350, 160))
            screen.blit(score_surface, score_rect)

            high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (51,102,204))
            high_score_rect = high_score_surface.get_rect(center=(350, 220))
            screen.blit(high_score_surface, high_score_rect)

    def display_over():
        display_over = game_font.render("Game over!", True, (230,28,102))
        over_rect = display_over.get_rect(center=(350, 70))
        screen.blit(display_over, over_rect)

        start_font = pygame.font.SysFont("SANS_BOLD", 40, bold=True)
        display_start = start_font.render("Tap SPACE to play again", True, (230, 28, 102))
        start_rect = display_start.get_rect(center=(350, 350))
        screen.blit(display_start, start_rect)



    gravity = 0.3 #3
    unicorn_move = 0
    game_on = True
    score = 0
    high_score = 0

    background_image = pygame.image.load("images/minibackground.png").convert()

    ground_image = pygame.image.load("images/miniground.png").convert()
    ground_x = 0

    unicorn_image = pygame.image.load("images/miniunicorn.png").convert()
    # unicorn_image = pygame.transform.scale((unicorn_image),(120,120))
    unicorn_rectangle = unicorn_image.get_rect(center=(200, 300))
    colorkey = unicorn_image.get_at((0, 0))  # odczytaj kolor w punkcie (0,0)
    unicorn_image.set_colorkey(colorkey, RLEACCEL)  # ustaw kolor jako przezroczysty

    rainbow_image = pygame.image.load("images/minirainbow.png")
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, pipeSpeed) #2
    pipe_height = [270, 380, 450]

    tap_sound = pygame.mixer.Sound("sounds/jump_sound2.wav")
    horse_sound = pygame.mixer.Sound("sounds/horse.wav")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_on:
                    unicorn_move = 0
                    unicorn_move -= unicornSpeed
                    tap_sound.play()
                if event.key == pygame.K_SPACE and game_on == False:
                    game_on = True
                    pipe_list.clear()
                    unicorn_rectangle.center = (200, 300)
                    unicorn_move = 0
                    score = 0
                    mainMenu()

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

        screen.blit(background_image, (0, 0))
        ground_x -= 1
        # move_ground()

        # if ground_x <= -700:
        # ground_x = 0
        if game_on:
            unicorn_move += gravity
            unicorn_rectangle.centery += unicorn_move
            game_on = check_collisions(pipe_list)

            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            score +=0.01
            display_scores("main_game")

            screen.blit(unicorn_image, unicorn_rectangle)

        else:
            high_score = update_score(high_score, score)
            display_over()
            display_scores("game_over")

        move_ground()
        if ground_x <= -700:
            ground_x = 0
        screen.blit(ground_image, (ground_x, 510))

        pygame.display.update()
        clock.tick(60)

#-----------------------------------------------------------------------
# MENU
#-----------------------------------------------------------------------

font = pygame_menu.font.FONT_OPEN_SANS_BOLD

myimage = pygame_menu.baseimage.BaseImage(
    image_path=("images/minibackground.png"),
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)

mytheme = pygame_menu.themes.THEME_BLUE.copy()
mytheme.widget_font = font
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mytheme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
mytheme.background_color = myimage
mytheme.widget_font_color = (0,0,0)
mytheme.widget_font_shadow_color = (0,0,0)



def mainMenu():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Welcome',
                            theme=mytheme)
    menu.add.button('Play', setDifficulty)
    menu.add.text_input('Name ', default='Player 1')
    menu.add.button('How to play', howToPlay)
    menu.add.button('High scores', highScores)
    menu.add.button('Autors', about)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)

def setDifficulty():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'How to play',
                            theme=mytheme)
    description = 'Choose difficulty'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Easy', start_the_game,1)
    menu.add.button('Medium', start_the_game,2)
    menu.add.button('Hard', start_the_game,3)
    menu.add.button('Back', mainMenu)
    menu.mainloop(screen)

def howToPlay():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'How to play',
                            theme=mytheme)
    description= 'Press SPACE to jump and avoid rainbow'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(screen)

def highScores():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'High Scores',
                            theme=mytheme)
    description= 'Test'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(screen)

def about():
    menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Autors',
                            theme=mytheme)
    description= 'Paulina Iwach \n Matematyka stosowana I rok\n Programowanie'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(screen)

mainMenu()