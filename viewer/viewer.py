import pygame
from snapshot import Snapshot

width = 640
height = 480

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

surface = pygame.Surface(screen.get_size())
surface.fill((0, 0, 0))
surface = surface.convert()
screen.blit(surface, (0, 0))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snapshot = Snapshot()

    dx = width / snapshot.width
    dy = height / snapshot.height

    for i in range(snapshot.width):
        for j in range(snapshot.height):
            if snapshot.content[j][i] == '.':
                pygame.draw.rect(surface, (0, 0, 255), (i*dx, j*dy, dx, dy))
            elif snapshot.content[j][i] == 'x':
                pygame.draw.rect(surface, (0, 255, 0), (i*dx, j*dy, dx, dy))
            elif snapshot.content[j][i] == '#':
                pygame.draw.rect(surface, (255, 0, 0), (i*dx, j*dy, dx, dy))

    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(240)
