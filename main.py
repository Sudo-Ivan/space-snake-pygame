import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Snake")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

SNAKE_SIZE = 20
ASTEROID_SIZE = 30
FONT = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.speed = 150  # pixels per second

    def move(self, dt):
        self.direction = self.next_direction
        move_distance = self.speed * dt
        new_x = self.body[0][0] + self.direction[0] * move_distance
        new_y = self.body[0][1] + self.direction[1] * move_distance
        head = (new_x, new_y)
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_direction):
        if new_direction[0] * -1 != self.direction[0] or new_direction[1] * -1 != self.direction[1]:
            self.next_direction = new_direction

    def check_collision(self):
        head = self.body[0]
        return (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            any(abs(head[0] - segment[0]) < SNAKE_SIZE and abs(head[1] - segment[1]) < SNAKE_SIZE for segment in self.body[1:])
        )

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(WINDOW, GREEN, (int(segment[0]), int(segment[1]), SNAKE_SIZE, SNAKE_SIZE))

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(50, 100)  # pixels per second

    def move(self, dt):
        self.y += self.speed * dt
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.rect(WINDOW, GRAY, (int(self.x), int(self.y), ASTEROID_SIZE, ASTEROID_SIZE))

def draw_text(text, x, y):
    surface = FONT.render(text, True, WHITE)
    WINDOW.blit(surface, (x, y))

def draw_menu(paused):
    pygame.draw.rect(WINDOW, (50, 50, 50), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
    if paused:
        draw_text("PAUSED", WIDTH // 2 - 50, HEIGHT // 2 - 50)
    else:
        draw_text("GAME OVER", WIDTH // 2 - 70, HEIGHT // 2 - 50)
    draw_text("Press R to Resume", WIDTH // 2 - 100, HEIGHT // 2)
    draw_text("Press Q to Quit", WIDTH // 2 - 80, HEIGHT // 2 + 50)

def game_loop():
    snake = Snake()
    asteroids = [Asteroid() for _ in range(5)]
    clock = pygame.time.Clock()
    score = 0
    lives = 3
    running = True
    paused = False
    game_over = False
    last_time = time.time()

    while running:
        dt = time.time() - last_time
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_q and (paused or game_over):
                    running = False
                elif event.key == pygame.K_r and (paused or game_over):
                    snake = Snake()
                    score = 0
                    lives = 3
                    paused = False
                    game_over = False
                elif not paused and not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))

        if not paused and not game_over:
            snake.move(dt)
            for asteroid in asteroids:
                asteroid.move(dt)

            if snake.check_collision():
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    snake = Snake()

            score += int(60 * dt)  # Increase score based on time

        WINDOW.fill(BLACK)
        snake.draw()
        for asteroid in asteroids:
            asteroid.draw()

        draw_text(f"Lives: {lives}", WIDTH - 120, 10)
        draw_text(f"Score: {score}", WIDTH - 120, 50)

        if paused or game_over:
            draw_menu(paused)

        pygame.display.flip()
        clock.tick(120)  # Increase frame rate for smoother animations

    pygame.quit()

if __name__ == "__main__":
    game_loop()