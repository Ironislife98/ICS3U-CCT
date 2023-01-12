import pygame
from pygame.math import Vector2
import sys
import math
import threading

pygame.init()

WIDTH, HEIGHT = 900, 900
BACKGROUND_COLOR = (34, 34, 34)#(44,42,42)
PIECE_COLORS: tuple[tuple[int, int, int], tuple[int, int, int]] = ((209,178,129), (20,22,22))
FRAMERATE = 60

CLOCK = pygame.time.Clock()

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
    @staticmethod
    def GeneratePieces(board: Board):
        posy = 0
        for space in range(board.width):
            Pieces.append(CheckersPiece(posy, space, board.boxWidth, (board.xoffset, board.yoffset), PIECE_COLORS[1]))
            posy = abs(posy - 1)

        posy = 0
        for space in range(board.width):
            Pieces.append(CheckersPiece(board.width - posy - 1, space, board.boxWidth, (board.xoffset, board.yoffset), PIECE_COLORS[0]))
            posy = abs(posy - 1)

    @staticmethod
    def CheckDrag(mousepos: pygame.Vector2):
        for piece in Pieces:
            if piece.rect.collidepoint(mousepos.x, mousepos.y):
                piece.dragging = True


class CheckersPiece:
    def __init__(self, row: int, column: int, stepsize: int, offsets: tuple[int, int], color: tuple[int, int, int], radius: int = 20):
        self.pos = pygame.math.Vector2(column, row)
        self.stepsize = stepsize
        self.offsets = offsets
        self.color = color
        self.radius = radius
        self.rectoffsets = [15, 15] # Offsets are x and y values
        self.rect = pygame.Rect(self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2), self.pos.y * self.stepsize + self.offsets[1]+ (self.stepsize / 2), self.radius * 2, self.radius * 2)

        self.dragoffsets = [2, 2]     # Offsets are in rows and columns
        self.dragging = False
        self.startpos = pygame.math.Vector2()
        self.availableSpots = {}

        Pieces.append(self)

    def handleDrag(self):
        if self.dragging:
            mousepos = pygame.mouse.get_pos()
            self.pos.x = mousepos[0] // self.stepsize - self.dragoffsets[0]
            self.pos.y = mousepos[1] // self.stepsize - self.dragoffsets[1]

    def getMiddle(self) -> tuple[float, float]:
        middlex = self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2)
        middley = (self.pos.y * self.stepsize + self.offsets[1]) + (self.stepsize / 2)

        return (middlex, middley)

    def calculateAvailableSpots(self):
        if self.color == PIECE_COLORS[0] and not self.dragging:
            self.availableSpots[f"{self.pos.x}{self.pos.y}"] = [(self.pos.x - 1, self.pos.y - 1), (self.pos.x + 1, self.pos.y  - 1)]

    def gracefulExit(self):
        try:
            if (self.pos.x, self.pos.y) in self.availableSpots[f"{self.pos.x}{self.pos.y}"]:
                pass
            print(self.availableSpots[f"{self.pos.x}{self.pos.y}"])
        except KeyError:
            self.pos = self.startpos

    def draw(self):
        middles = self.getMiddle()
        self.rect = pygame.Rect(self.pos.x * self.stepsize + self.offsets[0] + self.rectoffsets[0], self.pos.y * self.stepsize + self.offsets[1] + self.rectoffsets[1], self.radius * 2, self.radius * 2)
        #pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.circle(win, self.color, (middles[0], middles[1]), self.radius)


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
    CLOCK.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in Pieces:
                piece.dragging = False
                piece.startpos = piece.pos
                GameController.CheckDrag(pygame.Vector2(pygame.mouse.get_pos()))
        if event.type == pygame.MOUSEBUTTONUP:
            for piece in Pieces:
                piece.dragging = False
                piece.gracefulExit()

    for piece in Pieces:
        piece.handleDrag()
        piece.calculateAvailableSpots()

    drawObjects(win)

#{'8.08.0': [(7.0, 7.0), (9.0, 7.0)]}