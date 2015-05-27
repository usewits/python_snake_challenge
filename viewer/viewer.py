import pygame
import pickle
from snapshot import Snapshot
from window import Window

pygame.init()

window = Window(640, 480)

running = True

snapshot = Snapshot()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                window.toggleFullscreen()
            if event.key == pygame.K_i:
                window.toggleInfo()

    
    snapshot = snapshot.load("../snake/logs/state.dat")
    #pickle.load("../snake/logs/state.dat")

    window.drawSnapshot(snapshot)
    window.flip()
    window.pause(30)
