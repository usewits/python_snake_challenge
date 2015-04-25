import pygame
from snapshot import Snapshot
from window import Window

pygame.init()

window = Window(640, 480)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snapshot = Snapshot()

    window.drawSnapshot(snapshot)
    window.flip()
    window.pause(30)
