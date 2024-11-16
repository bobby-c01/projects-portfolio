import pygame
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge!")
clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, radius=20, color=BLUE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_a]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collides_with(self, obstacle):
        dist = ((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) ** 0.5
        return dist < self.radius + obstacle.radius


class Obstacle:
    def __init__(self, screen_width, screen_height, radius=30, color=RED):
        self.radius = radius
        self.color = color

        self.spawn_side = random.randint(1, 4)

        if self.spawn_side == 1:  # Top
            self.x = random.randint(self.radius, screen_width - self.radius)
            self.y = -self.radius
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(0.5, 1)
        elif self.spawn_side == 2:  # Right
            self.x = screen_width + self.radius
            self.y = random.randint(self.radius, screen_height - self.radius)
            self.dx = random.uniform(-1, -0.5)
            self.dy = random.uniform(-1, 1)
        elif self.spawn_side == 3:  # Bottom
            self.x = random.randint(self.radius, screen_width - self.radius)
            self.y = screen_height + self.radius
            self.dx = random.uniform(-1, 1)
            self.dy = random.uniform(-1, -0.5)
        elif self.spawn_side == 4:  # Left
            self.x = -self.radius
            self.y = random.randint(self.radius, screen_height - self.radius)
            self.dx = random.uniform(0.5, 1)
            self.dy = random.uniform(-1, 1)

        self.speed = random.randint(3, 7)

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        if self.x < -self.radius or self.x > WIDTH + self.radius or self.y < -self.radius or self.y > HEIGHT + self.radius:
            self.__init__(WIDTH, HEIGHT)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Coin:
    def __init__(self, screen_width, screen_height, radius=15, color=YELLOW):
        self.radius = radius
        self.color = color
        self.x = random.randint(radius, screen_width - radius)
        self.y = random.randint(radius, screen_height - radius)

    def update(self, player):
        if player.collides_with(self):
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


player = Player(WIDTH // 2, HEIGHT // 2)
obstacles = [Obstacle(WIDTH, HEIGHT) for _ in range(5)]
coins = [Coin(WIDTH, HEIGHT) for _ in range(3)]
score = 0

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    for obstacle in obstacles:
        obstacle.update()
    for coin in coins:
        if coin.update(player):
            score += 1
            coins.remove(coin)
            coins.append(Coin(WIDTH, HEIGHT))

    for obstacle in obstacles:
        if player.collides_with(obstacle):
            running = False

    screen.fill(BLACK)

    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for coin in coins:
        coin.draw(screen)

    font = pygame.font.SysFont("Comic Sans MS", 35)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 3))

    pygame.display.flip()

pygame.quit()
