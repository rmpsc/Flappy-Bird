import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 200))
    return bottom_pipe, top_pipe  # returns 2 rectangles for pipes


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # flip y but not x
            screen.blit(flip_pipe, pipe)


def delete_pipes(pipes):
    for pipe in pipes:
        if pipe.right <= 0:
            pipes.remove(pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    else:
        return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]  # new surface
    # centery is pos of last bird, so it transitions smoothly
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))  # new rect
    return new_bird, new_bird_rect


# displays when game is over
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))  # boolean for anti-aliasing
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))  # boolean for anti-aliasing
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

        # displays game over
        screen.blit(game_over_surface, game_over_rect)


# updates high score
def update_score(s, hs):
    if s > hs:
        hs = s
    return hs


def pipe_score_check():
    global score, can_score

    can_score = True
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False


# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
width, height = 576, 1024
screen = pygame.display.set_mode((width, height))  # can only be display screen
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Game Variables
gravity = 0.40
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-day.png').convert()  # convert helps game run smoother
bg_surface = pygame.transform.scale2x(bg_surface)  # doubles the size of the surface

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1  # every timed event after the first must have an int added (+ 1, + 2, etc)
pygame.time.set_timer(BIRDFLAP, 200)
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()  # alpha so black box is not drawn
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT  # outside of while loop bc its a timed event
pygame.time.set_timer(SPAWNPIPE, 1200)  # event triggers every 1.2 seconds
pipe_height = [400, 600, 800, 450, 500, 550, 650, 700, 750]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
flap_sound.set_volume(.10)
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
death_sound.set_volume(.10)
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound.set_volume(.10)


while True:
    for event in pygame.event.get():  # looks for all inputs
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                # print("flap")
                bird_movement = 0
                bird_movement -= 9
                flap_sound.play()
            # resets game
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                bird_rect.center = (100, 256)
                bird_movement = 0
                pipe_list.clear()
                score = 0

        if event.type == SPAWNPIPE:
            # pipe_list.append(create_pipe())
            pipe_list.extend(create_pipe())  # use extend when returning a tuple

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            # takes item form bird frames and puts new rectangle around it
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))  # displays background surface

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement  # left, right, top , bottom, centerx, centery
        screen.blit(rotated_bird, bird_rect)  # combines bird image and invisible rect
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        delete_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')

    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:  # resets floor pos for loop
        floor_x_pos = 0

    pygame.display.update()  # draws on the display surface
    clock.tick(80)
