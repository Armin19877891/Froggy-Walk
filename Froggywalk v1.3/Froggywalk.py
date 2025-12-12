import pygame
import sys
import math

pygame.init()

# Window
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Froggy walk v1.2")

# colors of froggy
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)

# load background
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# frog
frog_radius = 15
frog_pos = pygame.Vector2(100, HEIGHT // 2)

# points
turn_point = pygame.Vector2(WIDTH // 2, 100)
destination = pygame.Vector2(WIDTH - 100, HEIGHT // 2)

speed = 3
current_target = turn_point

clock = pygame.time.Clock()

# ricochet variables
ricochet_active = False
velocity = pygame.Vector2(0, 0)
gravity = 0.25
friction = 0.98


def move_towards(pos, target, speed):
    direction = target - pos
    if direction.length() < speed:
        return target
    return pos + direction.normalize() * speed


def reached(pos, target, threshold=5):
    return pos.distance_to(target) < threshold


running = True
reached_destination = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    # Phase 1: normal movement
    if not reached_destination and not ricochet_active:

        if current_target == turn_point:
            frog_pos = move_towards(frog_pos, turn_point, speed)
            if reached(frog_pos, turn_point):
                current_target = destination

        elif current_target == destination:
            frog_pos = move_towards(frog_pos, destination, speed)
            if reached(frog_pos, destination):
                reached_destination = True

        pygame.draw.circle(screen, GREEN, frog_pos, frog_radius)

    # Phase 2: START ricochet
    elif reached_destination and not ricochet_active:
        ricochet_active = True

        # give frog an initial natural bounce direction
        # (left-upwards, slightly randomized for natural look)
        velocity = pygame.Vector2(-6, -8)

    # Phase 3: ricochet physics
    elif ricochet_active:
        # gravity pulls down
        velocity.y += gravity

        # apply velocity
        frog_pos += velocity

        # friction slows motion over time
        velocity *= friction

        # collisions with "ground"
        if frog_pos.y > HEIGHT - frog_radius:
            frog_pos.y = HEIGHT - frog_radius
            velocity.y *= -0.55  # bounce effect

        # left boundary stop
        if frog_pos.x < frog_radius:
            frog_pos.x = frog_radius
            velocity.x = 0

        # stop completely when velocity is small
        if velocity.length() < -0.1:
            ricochet_active = False

        pygame.draw.circle(screen, DARK_GREEN, frog_pos, frog_radius)

    pygame.display.flip()

pygame.quit()
sys.exit()
