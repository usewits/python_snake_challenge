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
        dx = x / snapshot.width
        dy = y / snapshot.height

        for i in range(snapshot.width):
            for j in range(snapshot.height):
                if snapshot.content[j][i] == '.':
                    pygame.draw.rect(self.surface, (0, 0, 255), (i*dx, j*dy, dx, dy))
                elif snapshot.content[j][i] == 'x':
                    pygame.draw.rect(self.surface, (0, 255, 0), (i*dx, j*dy, dx, dy))
                elif snapshot.content[j][i] == '#':
                    pygame.draw.rect(self.surface, (255, 0, 0), (i*dx, j*dy, dx, dy))

        self.screen.blit(self.surface, (0, 0))
