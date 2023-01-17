import pygame
from pygame.math import Vector2
import pygame.font
import sys


pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 900
BACKGROUND_COLOR = (34, 34, 34) #(44,42,42)
PIECE_COLORS: tuple[tuple[int, int, int], tuple[int, int, int]] = ((209,178,129), (20,22,22))
FRAMERATE = 60

CLOCK = pygame.time.Clock()

Pieces = []
selectedSquares = []

# Font initialization
scoreboardFont = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 35)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


# Thanks to PoDuck for the object class
# Code can be found here: https://github.com/PoDuck/pygame_outlined_text
class OutlinedText(object):
    def __init__(
            self,
            text,
            position,
            outline_width,
            font_size,
            screen,
            foreground_color=(255, 255, 255),
            background_color=(0, 0, 0)
    ):
        """
        Outline text for pygame.
        :param text: bytes or unicode text
        :param position: tuple of form (x, y) you wish text to be rendered at
        :param outline_width: outline width in pixels
        :param font_size: font size
        :param screen: pygame screen you want text rendered to
        :param foreground_color: foreground color of text defaults to white
        :param background_color: background color of text defaults to black
        """
        self.text = text
        self.position = position
        self.foreground = foreground_color
        self.background = background_color
        self.outline_width = outline_width
        self.screen = screen
        self.font = pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 40)
        self.text_surface = self.font.render(self.text, True, self.foreground)
        self.text_outline_surface = self.font.render(self.text, True, self.background)
        # There is no good way to get an outline with pygame, so we draw
        # the text at 8 points around the main text to simulate an outline.
        self.directions = [
            (self.outline_width, self.outline_width),
            (0, self.outline_width),
            (-self.outline_width, self.outline_width),
            (self.outline_width, 0),
            (-self.outline_width, 0),
            (self.outline_width, -self.outline_width),
            (0, -self.outline_width),
            (-self.outline_width, -self.outline_width)
        ]

    def get_width(self):
        """
        Get width of text including border.
        :return: width of text, including border.
        """
        return self.text_surface.get_width() + self.outline_width * 2

    def change_position(self, position):
        """
        change position text is blitted to.
        :param position: tuple in the form of (x, y)
        :return:
        """
        self.position = position

    def change_text(self, text):
        """
        Changes text to "text"
        :param text: New text
        """
        self.text = text
        self._update_text()

    def change_foreground_color(self, color):
        """
        Changes foreground color
        :param color: New foreground color
        """
        self.foreground = color
        self._update_text()

    def change_outline_color(self, color):
        """
        Changes the outline color
        :param color: New outline color
        """
        self.background = color
        self._update_text()

    def _update_text(self):
        """
        "protected" function to replace the text surface with a new one based on updated values.
        """
        self.text_surface = self.font.render(self.text, True, self.foreground)
        self.text_outline_surface = self.font.render(self.text, True, self.background)

    def draw(self):
        # blit outline images to screen
        for direction in self.directions:
            self.screen.blit(
                self.text_outline_surface,
                (
                    self.position[0] - direction[0],
                    self.position[1] - direction[1]
                )
            )
        # blit foreground image to the screen
        self.screen.blit(self.text_surface, self.position)


class ScoreBoard:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.Player1 = OutlinedText("Player 1", (140, 65), 3, 35, win, foreground_color=PIECE_COLORS[1], background_color=(255, 255, 255))
        self.Player1Pos: Vector2 = pygame.math.Vector2(140, 65)
        self.Player2 = OutlinedText("Player 2", (590, 760), 3, 35, win, foreground_color=PIECE_COLORS[0], background_color=(0, 128, 0))
        self.Player2Pos: Vector2 = pygame.math.Vector2(620, 760)

        self.playertexts: tuple[OutlinedText, OutlinedText] = (self.Player2, self.Player1)
        self.selected: int = 0

    def changeSelected(self, newSelected: int):
        self.selected = newSelected
        for text in self.playertexts:
            text.change_outline_color((255, 255, 255))
        self.playertexts[self.selected].change_outline_color((0, 128, 0))

    def draw(self):
        self.Player1.draw()
        self.Player2.draw()


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

    def generateMoveSquares(self, column: float, row: float, yoffset: int, masterPiece):
        """Generates green squares with a y offset depending on the type of piece, when given the position of the piece"""
        posRight = pygame.math.Vector2(column + 1, row + yoffset)
        posLeft = pygame.math.Vector2(column - 1, row + yoffset)
        right = pygame.Rect(posRight.x * self.boxWidth + self.xoffset, posRight.y * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth)
        left = pygame.Rect(posLeft.x * self.boxWidth + self.xoffset, posLeft.y * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth)
        selectedSquares.append(SelectedSquare(right, posRight, masterPiece))
        selectedSquares.append(SelectedSquare(left, posLeft, masterPiece))


class SelectedSquare:
    def __init__(self, rect: pygame.Rect, pos: Vector2, master):
        self.rect = rect
        self.color = (0, 128, 0)
        self.master = master
        self.pos = pos

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)

    def detectPress(self, mousepos: Vector2):
        global selectedSquares, scoreboard
        if self.rect.collidepoint(mousepos.x, mousepos.y):
            self.master.pos = self.pos
            for piece in Pieces:
                piece.clicked = False
            scoreboard.changeSelected(abs(self.master.type - 1))
            selectedSquares = []


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
    def CheckClick(mousepos: pygame.Vector2):
        for piece in Pieces:
            if piece.rect.collidepoint(mousepos.x, mousepos.y):
                piece.clicked = True


class CheckersPiece:
    def __init__(self, row: int, column: int, stepsize: int, offsets: tuple[int, int], color: tuple[int, int, int], radius: int = 20):
        self.pos = pygame.math.Vector2(column, row)
        self.stepsize = stepsize
        self.offsets = offsets
        self.color = color
        self.type = PIECE_COLORS.index(self.color)
        self.radius = radius
        self.rectoffsets = [15, 15] # Offsets are x and y values
        self.rect = pygame.Rect(self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2), self.pos.y * self.stepsize + self.offsets[1]+ (self.stepsize / 2), self.radius * 2, self.radius * 2)

        self.clicked = False

        Pieces.append(self)

    def handleThings(self):
        if self.clicked:
            if scoreboard.selected == PIECE_COLORS.index(self.color):
                if PIECE_COLORS.index(self.color) == 0:
                    mainBoard.generateMoveSquares(self.pos.x, self.pos.y, -1, self)
                else:
                    mainBoard.generateMoveSquares(self.pos.x, self.pos.y, 1, self)
            else:
                self.clicked = False
                return


    def getMiddle(self) -> tuple[float, float]:
        middlex = self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2)
        middley = (self.pos.y * self.stepsize + self.offsets[1]) + (self.stepsize / 2)

        return (middlex, middley)

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
    scoreboard.draw()
    for square in selectedSquares:
        square.draw()
    pygame.display.update()


scoreboard = ScoreBoard(font=scoreboardFont)
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
            for square in selectedSquares:
                square.detectPress(Vector2(pygame.mouse.get_pos()))
            selectedSquares = []
            GameController.CheckClick(Vector2(pygame.mouse.get_pos()))



    drawObjects(win)
    for piece in Pieces:
        piece.handleThings()


#{'8.08.0': [(7.0, 7.0), (9.0, 7.0)]}