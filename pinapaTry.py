import pygame
import random

pygame.init()

W = 400
screen = pygame.display.set_mode((W, W))
clock = pygame.time.Clock()

snake = [(200, 200)]
direction = (20, 0)

food = (
    random.randrange(0, W, 20),
    random.randrange(0, W, 20)
)

running = True

while running:

    clock.tick(10)

    # Check events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                direction = (0, -20)

            if event.key == pygame.K_DOWN:
                direction = (0, 20)

            if event.key == pygame.K_LEFT:
                direction = (-20, 0)

            if event.key == pygame.K_RIGHT:
                direction = (20, 0)

    # Move snake
    head = (
        snake[0][0] + direction[0],
        snake[0][1] + direction[1]
    )

    snake.insert(0, head)

    # Eat food
    if head == food:
        food = (
            random.randrange(0, W, 20),
            random.randrange(0, W, 20)
        )
    else:
        snake.pop()

    # Collision
    if (
        head[0] < 0
        or head[0] >= W
        or head[1] < 0
        or head[1] >= W
        or head in snake[1:]
    ):
        running = False

    # Draw background
    screen.fill((20, 20, 20))

    # Draw snake
    for s in snake:
        pygame.draw.rect(
            screen,
            (0, 255, 100),
            (s[0], s[1], 20, 20)
        )

    # Draw food
    pygame.draw.rect(
        screen,
        (255, 50, 50),
        (food[0], food[1], 20, 20)
    )

    pygame.display.flip()

pygame.quit()