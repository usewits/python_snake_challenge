import os
import pygame

class Window:

    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface.fill((0, 0, 0))

    def flip(self):
        pygame.display.flip()

    def pause(self, maxFPS = None):
        self.clock.tick(maxFPS)

    def drawSnapshot(self, snapshot):
        x, y = self.screen.get_size()
        dx, dy = x / snapshot.width, y / snapshot.height

        for i in range(snapshot.width):
            for j in range(snapshot.height):
                if snapshot.content[j][i] == '.':
                    pygame.draw.rect(self.surface, (0, 0, 255), (i*dx, j*dy, dx, dy))
                elif snapshot.content[j][i] == '#':
                    pygame.draw.rect(self.surface, (255, 0, 0), (i*dx, j*dy, dx, dy))

        self.screen.blit(self.surface, (0, 0))

        apple = pygame.image.load(os.path.join('img', 'apple.png'))
        appleW, appleH = int(dx / 2), int(dy / 2)
        appleX, appleY = int(appleW / 2), int(appleH / 2)
        apple = pygame.transform.scale(apple, (appleW, appleH))

        for foodx, foody in snapshot.food:
            self.screen.blit(apple, (foodx*dx + appleX, foody*dy + appleY))
