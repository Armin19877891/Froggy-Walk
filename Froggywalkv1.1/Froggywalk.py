import pygame
import sys
import math

pygame.init()

# Window

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Froggy walk")

# colors of froggy
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)

# load background

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# draw froggy
# ---------------------------------------
# De kikker wordt voorgesteld als een groene cirkel.
# - frog_radius: bepaalt hoe groot de kikker is.
# - frog_pos: startpositie van de kikker (aan de linkerkant van het scherm).
frog_radius = 15
frog_pos = pygame.Vector2(100, HEIGHT // 2)

# Turn point and destination
# ---------------------------------------
# De kikker loopt eerst naar een 'turn point' (een soort tussenstop),
# en pas daarna naar zijn eindbestemming aan de rechterkant van het scherm.
turn_point = pygame.Vector2(WIDTH // 2, 100)
destination = pygame.Vector2(WIDTH - 100, HEIGHT // 2)

# Snelheid van de kikker
speed = 3
current_target = turn_point

clock = pygame.time.Clock()

def move_towards(pos, target, speed):
    # Deze functie laat een object (de kikker) richting een doel bewegen.
    # De richting wordt berekend met vectoren en genormaliseerd zodat
    # de kikker steeds even snel beweegt, ongeacht de afstand.
    direction = target - pos
    if direction.length() < speed:
        return target
    return pos + direction.normalize() * speed

def reached(pos, target, threshold=5):
    # Controleert of de kikker dicht genoeg bij het doel is gekomen.
    # threshold = hoeveel pixels afstand geldt als "bereikt".
    return pos.distance_to(target) < threshold

running = True
reached_destination = False

while running:
    clock.tick(60)  # Beperkt de game tot 60 FPS zodat alles vloeiend beweegt.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

    screen.blit(background, (0, 0))  # Tekent de achtergrond opnieuw bij elk frame.

    # Move the frog
    # ---------------------------------------
    # Als de kikker nog niet op zijn eindbestemming is, wordt hij verplaatst.
    # Eerst gaat hij naar het tussenpunt (turn_point). Zodra hij dat bereikt,
    # verandert het doel en loopt hij naar de eindbestemming (destination).
    if not reached_destination:

        if current_target == turn_point:
            frog_pos = move_towards(frog_pos, turn_point, speed)
            if reached(frog_pos, turn_point):
                current_target = destination

        elif current_target == destination:
            frog_pos = move_towards(frog_pos, destination, speed)
            if reached(frog_pos, destination):
                reached_destination = True

        pygame.draw.circle(screen, GREEN, frog_pos, frog_radius)

    else:
        # Als hij is aangekomen: teken een donkerdere kikker op de eindpositie.
        pygame.draw.circle(screen, DARK_GREEN, destination, frog_radius)

    pygame.display.flip()  # Update het scherm met alle nieuwe tekeningen.

pygame.quit()  
sys.exit()