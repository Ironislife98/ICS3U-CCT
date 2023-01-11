import pygame
from pygame.math import Vector2
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 900
BACKGROUND_COLOR = (34, 34, 34)#(44,42,42)
PIECE_COLORS: tuple[tuple[int, int, int], tuple[int, int, int]] = ((209,178,129), (20,22,22))


Pieces = []


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


class Board:
    def __init__(self):
        self.vector = pygame.math.Vector2(0, 0)
        self.width = 9  # Width is number of squares
        self.boxWidth = 70    # Box width is how wide the squares are
        self.xoffset, self.yoffset = 135, 120
        self.ranCalc = False
        self.squares = {}

    def draw(self):
        if not self.ranCalc:
            row, column = 0, 0
            colors = [(212, 190, 167), (107, 70, 61)]
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


class GameController:
    def __init__(self):
        pass

    @staticmethod
    def GeneratePieces(board: Board):
        posy = 0
        for space in range(board.width):
            Pieces.append(CheckersPiece(posy, space, board.boxWidth, (board.xoffset, board.yoffset), PIECE_COLORS[1]))
            posy = abs(posy - 1)

        posy = 0
        for space in range(board.width):
            Pieces.append(CheckersPiece(board.width - posy -1, space, board.boxWidth, (board.xoffset, board.yoffset), PIECE_COLORS[0]))
            posy = abs(posy - 1)


class CheckersPiece:
    def __init__(self, row: int, column: int, stepsize: int, offsets: tuple[int, int], color: tuple[int, int, int], radius: int = 20):
        self.pos = pygame.math.Vector2(column, row)
        self.stepsize = stepsize
        self.offsets = offsets
        self.color = color
        self.radius = radius

        Pieces.append(self)

    def getMiddle(self) -> tuple[float, float]:
        middlex = self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2)
        middley = (self.pos.y * self.stepsize + self.offsets[1]) + (self.stepsize / 2)

        return (middlex, middley)

    def draw(self):
        middles = self.getMiddle()
        pygame.draw.circle(win, self.color, (middles[0], middles[1]), self.radius, )


def drawObjects(win):
    win.fill(BACKGROUND_COLOR)
    mainBoard.draw()
    for piece in Pieces:
        piece.draw()

    pygame.display.update()


mainBoard = Board()

GameController.GeneratePieces(mainBoard)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()
    drawObjects(win)
