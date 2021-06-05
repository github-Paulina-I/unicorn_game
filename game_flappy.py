import os
import pygame
import sys
from pygame.locals import *
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


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
            return False
    if unicorn_rectangle.top <= 0 or unicorn_rectangle.bottom >= 510:
        return False
    return True


#ef update_score:

def display_scores(game_state):
    #scores = game_font.render(str(int(score)), True, (51,102,204))
    #scores_rect = scores.get_rect(center = (100, 50))
    #screen.blit(scores, scores_rect)
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (51,102,204))
        score_rect = score_surface.get_rect(center=(100, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (51,102,204))
        score_rect = score_surface.get_rect(center=(350, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (51,102,204))
        high_score_rect = high_score_surface.get_rect(center=(350, 180))
        screen.blit(high_score_surface, high_score_rect)


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Unicorn Journey")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arialblack",50)

gravity = 0.3
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
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height = [270, 380, 450]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on:
                unicorn_move = 0
                unicorn_move -= 7
            if event.key == pygame.K_SPACE and game_on == False:
                game_on = True
                pipe_list.clear()
                unicorn_rectangle.center = (200, 300)
                unicorn_move = 0

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
        display_scores("game_over")

    move_ground()
    if ground_x <= -700:
        ground_x = 0
    screen.blit(ground_image, (ground_x, 510))

    pygame.display.update()
    clock.tick(60)