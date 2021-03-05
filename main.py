# importing libraries
import pygame
import sys
import random


# creating the obstacles
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # randomly choosing obstacle height
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos + 20))  # bottom obstacles
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 250))  # top obstacles
    return bottom_pipe, top_pipe


# moving the obstacles
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


# drawing the obstacles
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 640:
            screen.blit(pipe_surface, pipe)
        else:
            # If bottom obstacle is less than 640px, flip the obstacle
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# checking the bird colliding with obstacle
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 640:
        can_score = True
        return False

    return True


# rotating the bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# bird animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# displaying the score
def score_display(game_state):
    # when game is running
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 20))
        screen.blit(score_surface, score_rect)
    # when game is over
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 20))
        screen.blit(score_surface, score_rect)
        # high score surface
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(240, 610))
        screen.blit(high_score_surface, high_score_rect)


# scoring is getting updated
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# checking the score
def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


# pygame initialization
pygame.init()
screen = pygame.display.set_mode((480, 640))  # setting the screen size
pygame.display.set_caption('Flappy Bird\'s Visit to IUBAT')  # setting the display caption
clock = pygame.time.Clock()  # tracking the time
game_font = pygame.font.Font('assets/04B_19.ttf', 40)  # getting the game font

# game variables
gravity = 0.50
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
bg_surface = pygame.image.load('assets/background.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (480, 640))

# bird variables
bird_downflap = bird_midflap = bird_upflap = pygame.transform.scale(
    pygame.image.load('assets/bird.png').convert_alpha(), (50, 40))  # getting the bird
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 320))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# pipe variables
pipe_surface = pygame.image.load('assets/pipe.png')  # getting the pipe
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 300, 350, 400]

# game over variables
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(240, 320))

# game sounds
flap_sound = pygame.mixer.Sound('assets/sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('assets/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('assets/sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 9
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 320)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    pygame.display.update()
    clock.tick(90)
