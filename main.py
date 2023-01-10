import pygame
from pygame.math import Vector2
import sys

pygame.init()

WIDTH, HEIGHT = 900, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))


class Board:
    def __init__(self):
        self.vector = pygame.math.Vector2(0, 0)
        self.width = 15     # Width is number of squares
        self.boxWidth = 10     # Box width is how wide the squares are

    def draw(self):
        column = 0
        row = 0
        for square in range(self.width):
            drawPos = pygame.math.Vector2(square * self.width)


def drawObjects(win):
    mainBoard.draw()

    pygame.display.update()

mainBoard = Board()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()
    drawObjects(win)