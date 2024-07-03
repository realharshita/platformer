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

platform_rect = pygame.Rect(200, SCREEN_HEIGHT - 150, 150, 10)
platform_color = (50, 50, 200)

obstacle_rect = pygame.Rect(400, SCREEN_HEIGHT - 40, 20, 20)
obstacle_color = (200, 50, 50)

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
    if character_rect.colliderect(platform_rect):
        character_rect.bottom = platform_rect.top
    if character_rect.colliderect(obstacle_rect):
        draw_text("Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

def increase_score():
    global score
    if character_rect.colliderect(platform_rect):
        score += 1
    draw_text(f"Score: {score}", 10, 40, font_size)

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

    screen.fill(WHITE)
    
    pygame.draw.rect(screen, ground_color, ground_rect)
    pygame.draw.rect(screen, platform_color, platform_rect)
    pygame.draw.rect(screen, obstacle_color, obstacle_rect)
    
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
