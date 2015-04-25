import os
import pygame

class Window:

    background = (255, 255, 204)
    walls = (192, 192, 192)

    snakeColors = [(0, 160, 176), (106, 74, 60), (204, 51, 63),
                    (235, 104, 65), (237, 201, 81)]

    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.mainSurface = pygame.Surface(self.screen.get_size())
        self.mainSurface.fill((0, 0, 0))

    def flip(self):
        pygame.display.flip()

    def pause(self, maxFPS = None):
        self.clock.tick(maxFPS)

    def drawSnapshot(self, snapshot):
        # First, compute coordinate distances
        x, y = self.screen.get_size()
        dx, dy = x / snapshot.width, y / snapshot.height

        # Second, draw background and walls
        for i in range(snapshot.width):
            for j in range(snapshot.height):
                if snapshot.content[j][i] == '.':
                    pygame.draw.rect(self.mainSurface, Window.background,
                            (i*dx, j*dy, dx, dy))
                elif snapshot.content[j][i] == '#':
                    pygame.draw.rect(self.mainSurface, Window.walls,
                            (i*dx, j*dy, dx, dy))
        self.screen.blit(self.mainSurface, (0, 0))

        # Third, draw snakes
        snakeW, snakeH = int(.95 * dx), int(.95 * dy)
        snakeX, snakeY = int(.025 * dx), int(.025 * dy)
        snakeSurface = pygame.Surface(self.mainSurface.get_size(),
                pygame.SRCALPHA, 32)
        colorIndex = 0
        for snake in snapshot.snakes:
            for coordinateX, coordinateY in snake:
                pygame.draw.rect(snakeSurface, Window.snakeColors[colorIndex],
                        (coordinateX*dx + snakeX, coordinateY*dy + snakeY,
                         snakeW, snakeH))
            colorIndex += 1
            if colorIndex >= len(Window.snakeColors):
                colorIndex = 0
        self.screen.blit(snakeSurface, (0, 0))

        # Fourth, draw food
        apple = pygame.image.load(os.path.join('img', 'apple.png'))
        appleW, appleH = int(dx / 2), int(dy / 2)
        appleX, appleY = int(appleW / 2), int(appleH / 2)
        apple = pygame.transform.scale(apple, (appleW, appleH))
        for foodx, foody in snapshot.food:
            self.screen.blit(apple, (foodx*dx + appleX, foody*dy + appleY))
