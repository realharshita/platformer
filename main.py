import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

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

collectibles = [
    pygame.Rect(250, SCREEN_HEIGHT - 180, 20, 20),
    pygame.Rect(450, SCREEN_HEIGHT - 330, 20, 20),
    pygame.Rect(650, SCREEN_HEIGHT - 480, 20, 20)
]
collectible_color = (50, 200, 200)

jumping = False
jump_count = 10
gravity = 0.5

character_speed = 5
jump_height = 10

score = 0
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
    for collectible_rect in collectibles:
        if character_rect.colliderect(collectible_rect):
            score += 5
            collectibles.remove(collectible_rect)

def increase_score():
    global score
    draw_text(f"Score: {score}", 10, 40, font_size)

def draw_obstacles():
    for obstacle_rect in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle_rect)

def draw_collectibles():
    for collectible_rect in collectibles:
        pygame.draw.rect(screen, collectible_color, collectible_rect)

def move_platform():
    moving_platform.x += moving_platform_speed
    if moving_platform.left <= 0 or moving_platform.right >= SCREEN_WIDTH:
        moving_platform_speed *= -1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_rect.x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_rect.x += character_speed

    if jumping:
        character_rect.y -= jump_height
        jump_height -= gravity
        if jump_height < -10:
            jumping = False
            jump_height = 10

    move_platform()

    screen.fill(WHITE)
    
    pygame.draw.rect(screen, ground_color, ground_rect)
    for platform_rect in platforms:
        pygame.draw.rect(screen, platform_color, platform_rect)
    pygame.draw.rect(screen, moving_platform_color, moving_platform)
    draw_obstacles()
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
