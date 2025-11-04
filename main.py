
import pygame
import sys
import os

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Jumper")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Load assets
def load_image(name):
    path = os.path.join("assets", name)
    return pygame.image.load(path).convert_alpha()

player_img = load_image("player.png")  # Your custom sprite!
platform_img = pygame.Surface((120, 20))
platform_img.fill((139, 69, 19))  # Brown platform
coin_img = pygame.Surface((20, 20))
pygame.draw.circle(coin_img, (255, 215, 0), (10, 10), 10)  # Gold coin

# Game objects
player = pygame.Rect(100, 500, 50, 50)
player_vel = [0, 0]
gravity = 0.5
jump_strength = -12
on_ground = False

platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(200, 450, 120, 20),
    pygame.Rect(400, 350, 120, 20),
    pygame.Rect(600, 250, 120, 20)
]

coins = [pygame.Rect(p.x + 40, p.y - 30, 20, 20) for p in platforms[1:]]
score = 0

# Game loop
def game_loop():
    global player_vel, on_ground, score
    while True:
        screen.fill((135, 206, 235))  # Sky blue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_vel[0] = -5
        elif keys[pygame.K_RIGHT]:
            player_vel[0] = 5
        else:
            player_vel[0] = 0

        if keys[pygame.K_SPACE] and on_ground:
            player_vel[1] = jump_strength

        # Apply gravity
        player_vel[1] += gravity
        player.x += player_vel[0]
        player.y += player_vel[1]

        # Collision
        on_ground = False
        for plat in platforms:
            if player.colliderect(plat) and player_vel[1] > 0:
                player.bottom = plat.top
                player_vel[1] = 0
                on_ground = True

        # Draw platforms
        for plat in platforms:
            screen.blit(platform_img, plat)

        # Draw coins
        for coin in coins[:]:
            screen.blit(coin_img, coin)
            if player.colliderect(coin):
                coins.remove(coin)
                score += 1

        # Draw player
        screen.blit(player_img, player)

        # Score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

game_loop()
