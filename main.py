import pygame
from pygame.math import Vector2
import sys

pygame.init()

WIDTH, HEIGHT = 900, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


class Board:
    def __init__(self):
        self.vector = pygame.math.Vector2(0, 0)
        self.width = 15     # Width is number of squares
        self.boxWidth = 45    # Box width is how wide the squares are
        self.xoffset, self.yoffset = 110, 100
        self.ranCalc = False
        self.squares = {}

    def draw(self):
        if not self.ranCalc:
            row, column = 0, 0
            colors = [(255, 0, 0), (0, 255, 0)]
            colorselection = True
            for i in range(self.width * self.width):
                pygame.draw.rect(win, colors[int(colorselection)],
                                 pygame.Rect(column * self.boxWidth + self.xoffset, row * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth))
                colorselection = not colorselection
                if column == self.width - 1:
                    column = 0
                    row += 1
                else:
                    column += 1

                if row == self.width:
                    return
                self.squares[str(i)] = colors[int(colorselection)], pygame.Rect(column * self.boxWidth + self.xoffset, row * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth)
            print("finished")
            self.ranCalc = True

        else:
            for key in self.squares:
                pygame.draw.rect(win, self.squares[key][0], self.squares[key][1])

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
