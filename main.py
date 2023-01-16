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
        self.Player1 =OutlinedText("Player 1", (400, 60), 3, 35, win, foreground_color=(255, 255, 255), background_color=(255, 0, 0))
        self.Player1Pos = pygame.math.Vector2(130, 60)
        self.Player2 = self.font.render("Player 2", False, PIECE_COLORS[0])
        self.Player2Pos = pygame.math.Vector2(620, 760)

        self.pos = (pygame.math.Vector2(), pygame.math.Vector2())
        #self.selectedMessage = self.font.render("Your Turn")
        self.selected = 0

    def toggleSelected(self):
        self.selected = abs(self.selected - 1)

    def draw(self):
        #win.blit(self.Player1, self.Player1Pos)
        #win.blit(self.Player2, self.Player2Pos)
        self.Player1.draw()


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
                piece.genPositions()
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
        self.availableSpots = []

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

    def genPositions(self):
        upleft = pygame.Vector2(self.startpos.x - 1, self.startpos.y - 1)
        upright = pygame.Vector2(self.startpos.x + 1, self.startpos.y - 1)
        self.availableSpots = [upleft.xy, upright.xy]
        print(self.availableSpots)

    def checkPosition(self):
        if self.pos.x in (self.startpos.x - 1, self.startpos.x + 1):
            if self.pos.y in (self.startpos.y - 1):
                print("Valid move")
        else:
            self.pos.xy = self.startpos.xy

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
            for piece in Pieces:
                piece.dragging = False
                piece.startpos = piece.pos
                GameController.CheckDrag(pygame.Vector2(pygame.mouse.get_pos()))
        if event.type == pygame.MOUSEBUTTONUP:
            for piece in Pieces:
                piece.checkPosition()
                piece.dragging = False

    for piece in Pieces:
        piece.handleDrag()

    drawObjects(win)

#{'8.08.0': [(7.0, 7.0), (9.0, 7.0)]}