import pygame
import random
import sys

# Khởi tạo pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

# Kích thước màn hình
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏎️ Đua Xe Siêu Tốc")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Font chữ
font = pygame.font.SysFont(None, 36)

# Thông số xe
car_width = 50
car_height = 90
car_speed = 8  # Tăng tốc độ xe người chơi


def draw_car(x, y):
    pygame.draw.rect(screen, RED, (x, y, car_width, car_height))


def draw_obstacle(ob):
    pygame.draw.rect(screen, BLACK, (ob['x'], ob['y'], car_width, car_height))


def show_text(text, y):
    msg = font.render(text, True, RED)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, y))


def show_score(score):
    txt = font.render(f"Score: {score}", True, BLACK)
    screen.blit(txt, (10, 10))


def game_loop():
    car_x = WIDTH // 2 - car_width // 2
    car_y = HEIGHT - car_height - 10

    num_obstacles = 3
    obstacles = []
    for _ in range(num_obstacles):
        ox = random.randint(0, WIDTH - car_width)
        oy = random.randint(-600, -100)
        speed = random.uniform(7, 10)
        obstacles.append({'x': ox, 'y': oy, 'speed': speed})

    score = 0
    game_over = False

    while True:
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Điều khiển
            if keys[pygame.K_LEFT] and car_x > 0:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
                car_x += car_speed

            draw_car(car_x, car_y)

            for ob in obstacles:
                ob['y'] += ob['speed']
                draw_obstacle(ob)

                if ob['y'] > HEIGHT:
                    ob['y'] = random.randint(-600, -100)
                    ob['x'] = random.randint(0, WIDTH - car_width)
                    ob['speed'] += 0.5
                    score += 1

                # Kiểm tra va chạm
                if (
                    car_y < ob['y'] + car_height and
                    car_y + car_height > ob['y'] and
                    car_x < ob['x'] + car_width and
                    car_x + car_width > ob['x']
                ):
                    game_over = True

            show_score(score)

        else:
            show_text("💥 Game Over!", HEIGHT // 2 - 40)
            show_text("Nhấn Space để chơi lại", HEIGHT // 2)
            show_text("Nhấn Esc để thoát", HEIGHT // 2 + 40)

            if keys[pygame.K_SPACE]:
                return  # Restart
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


# Game bắt đầu lặp vô hạn
while True:
    game_loop()
