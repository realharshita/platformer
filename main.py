import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

background_image = pygame.image.load('background.png')

character_image = pygame.image.load('character.png')
character_rect = character_image.get_rect()
character_rect.center = (100, SCREEN_HEIGHT - 100)

ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
ground_color = (100, 100, 100)

platforms = [
    pygame.Rect(200, SCREEN_HEIGHT - 150, 150, 10),
    pygame.Rect(400, SCREEN_HEIGHT - 300, 150, 10),
    pygame.Rect(600, SCREEN_HEIGHT - 450, 150, 10)
]
platform_color = (50, 50, 200)

moving_platform = pygame.Rect(300, SCREEN_HEIGHT - 220, 150, 10)
moving_platform_color = (50, 200, 50)
moving_platform_speed = 2

obstacles = [
    pygame.Rect(300, SCREEN_HEIGHT - 60, 20, 20),
    pygame.Rect(500, SCREEN_HEIGHT - 220, 20, 20),
    pygame.Rect(700, SCREEN_HEIGHT - 380, 20, 20)
]
obstacle_color = (200, 50, 50)

moving_obstacles = [
    pygame.Rect(350, SCREEN_HEIGHT - 100, 20, 20),
    pygame.Rect(550, SCREEN_HEIGHT - 260, 20, 20)
]
moving_obstacle_speed = 3

interactive_objects = [
    pygame.Rect(600, SCREEN_HEIGHT - 500, 30, 30)
]
interactive_object_color = (200, 200, 50)
interactive_object_effect = "shrink"

collectibles = [
    pygame.Rect(250, SCREEN_HEIGHT - 180, 20, 20),
    pygame.Rect(450, SCREEN_HEIGHT - 330, 20, 20),
    pygame.Rect(650, SCREEN_HEIGHT - 480, 20, 20),
    pygame.Rect(350, SCREEN_HEIGHT - 260, 20, 20),
    pygame.Rect(550, SCREEN_HEIGHT - 410, 20, 20)
]
collectible_color = (50, 200, 200)

jumping = False
jump_count = 10
gravity = 0.5

character_speed = 5
jump_height = 10
max_jump_height = 15
min_jump_height = 5

score = 0
level = 1
font_size = 30

def draw_grid():
    for x in range(0, SCREEN_WIDTH, 20):
        for y in range(0, SCREEN_HEIGHT, 20):
            rect = pygame.Rect(x, y, 20, 20)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_text(text, x, y, font_size=30):
    font = pygame.font.SysFont('Arial', font_size)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

def constrain_character():
    if character_rect.left < 0:
        character_rect.left = 0
    if character_rect.right > SCREEN_WIDTH:
        character_rect.right = SCREEN_WIDTH
    if character_rect.bottom > SCREEN_HEIGHT - 20:
        character_rect.bottom = SCREEN_HEIGHT - 20

def check_collisions():
    global score
    global level
    if character_rect.colliderect(ground_rect):
        character_rect.bottom = ground_rect.top
    for platform_rect in platforms:
        if character_rect.colliderect(platform_rect):
            character_rect.bottom = platform_rect.top
            score += 1
    if character_rect.colliderect(moving_platform):
        character_rect.bottom = moving_platform.top
        score += 2
    for obstacle_rect in obstacles:
        if character_rect.colliderect(obstacle_rect):
            draw_text("Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
    for moving_obstacle in moving_obstacles:
        if character_rect.colliderect(moving_obstacle):
            draw_text("Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
    for interactive_object in interactive_objects:
        if character_rect.colliderect(interactive_object):
            if interactive_object_effect == "shrink":
                character_rect.inflate_ip(-10, -10)
            interactive_objects.remove(interactive_object)
    for collectible_rect in collectibles:
        if character_rect.colliderect(collectible_rect):
            score += 5
            collectibles.remove(collectible_rect)
    if not collectibles:
        level += 1
        setup_level(level)

def increase_score():
    global score
    draw_text(f"Score: {score}", 10, 40, font_size)

def draw_obstacles():
    for obstacle_rect in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle_rect)

def draw_moving_obstacles():
    for moving_obstacle in moving_obstacles:
        pygame.draw.rect(screen, obstacle_color, moving_obstacle)

def draw_interactive_objects():
    for interactive_object in interactive_objects:
        pygame.draw.rect(screen, interactive_object_color, interactive_object)

def draw_collectibles():
    for collectible_rect in collectibles:
        pygame.draw.rect(screen, collectible_color, collectible_rect)

def move_platform():
    moving_platform.x += moving_platform_speed
    if moving_platform.left <= 0 or moving_platform.right >= SCREEN_WIDTH:
        moving_platform_speed *= -1

def move_moving_obstacles():
    for moving_obstacle in moving_obstacles:
        moving_obstacle.y += moving_obstacle_speed
        if moving_obstacle.top <= 0 or moving_obstacle.bottom >= SCREEN_HEIGHT:
            moving_obstacle_speed *= -1

def setup_level(level):
    global platforms, obstacles, moving_obstacles, interactive_objects, collectibles
    if level == 1:
        platforms = [
            pygame.Rect(200, SCREEN_HEIGHT - 150, 150, 10),
            pygame.Rect(400, SCREEN_HEIGHT - 300, 150, 10),
            pygame.Rect(600, SCREEN_HEIGHT - 450, 150, 10)
        ]
        obstacles = [
            pygame.Rect(300, SCREEN_HEIGHT - 60, 20, 20),
            pygame.Rect(500, SCREEN_HEIGHT - 220, 20, 20),
            pygame.Rect(700, SCREEN_HEIGHT - 380, 20, 20)
        ]
        moving_obstacles = [
            pygame.Rect(350, SCREEN_HEIGHT - 100, 20, 20),
            pygame.Rect(550, SCREEN_HEIGHT - 260, 20, 20)
        ]
        interactive_objects = [
            pygame.Rect(600, SCREEN_HEIGHT - 500, 30, 30)
        ]
        collectibles = [
            pygame.Rect(250, SCREEN_HEIGHT - 180, 20, 20),
            pygame.Rect(450, SCREEN_HEIGHT - 330, 20, 20),
            pygame.Rect(650, SCREEN_HEIGHT - 480, 20, 20)
        ]
    elif level == 2:
        platforms = [
            pygame.Rect(250, SCREEN_HEIGHT - 200, 150, 10),
            pygame.Rect(450, SCREEN_HEIGHT - 350, 150, 10),
            pygame.Rect(650, SCREEN_HEIGHT - 500, 150, 10)
        ]
        obstacles = [
            pygame.Rect(350, SCREEN_HEIGHT - 80, 20, 20),
            pygame.Rect(550, SCREEN_HEIGHT - 240, 20, 20),
            pygame.Rect(750, SCREEN_HEIGHT - 400, 20, 20)
        ]
        moving_obstacles = [
            pygame.Rect(400, SCREEN_HEIGHT - 100, 20, 20),
            pygame.Rect(600, SCREEN_HEIGHT - 260, 20, 20)
        ]
        interactive_objects = [
            pygame.Rect(700, SCREEN_HEIGHT - 500, 30, 30)
        ]
        collectibles = [
            pygame.Rect(300, SCREEN_HEIGHT - 230, 20, 20),
            pygame.Rect(500, SCREEN_HEIGHT - 380, 20, 20),
            pygame.Rect(700, SCREEN_HEIGHT - 530, 20, 20)
        ]
    # Additional levels can be added similarly

setup_level(level)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True
                jump_height = max_jump_height
            elif event.key == pygame.K_DOWN and jumping:
                jump_height = min_jump_height

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_rect.x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_rect.x += character_speed

    if jumping:
        character_rect.y -= jump_height
        jump_height -= gravity
        if jump_height < -max_jump_height:
            jumping = False
            jump_height = max_jump_height

    move_platform()
    move_moving_obstacles()

    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    
    pygame.draw.rect(screen, ground_color, ground_rect)
    for platform_rect in platforms:
        pygame.draw.rect(screen, platform_color, platform_rect)
    pygame.draw.rect(screen, moving_platform_color, moving_platform)
    draw_obstacles()
    draw_moving_obstacles()
    draw_interactive_objects()
    draw_collectibles()
    
    screen.blit(character_image, character_rect)

    constrain_character()

    draw_grid()
    draw_text("Platformer Game", 10, 10)

    check_collisions()

    increase_score()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
