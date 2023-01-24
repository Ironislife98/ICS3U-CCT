import pygame
from pygame.math import Vector2
import pygame.font
import sys
from typing import Callable
import threading


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


crownImage = pygame.image.load("data/images/crown.png").convert_alpha()         # Convert to maximize fps
crownImage = pygame.transform.scale_by(crownImage, .07)


quitProgram = False


# Invoke functions like unity
def Invoke(func: Callable, delay: int):
    start = threading.Timer(delay, func)
    start.start()



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
            font=pygame.font.Font("data/fonts/Montserrat-ExtraBold.ttf", 35),
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
        self.font = font
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


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


class Button:
    """Base Class for buttons"""
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple[int, int, int], fill: int=100, round: int=40, delay: float = .3):
        self.rect = pygame.Rect(x, y, width, height)
        self.color: tuple[int, int, int] = color
        self.colorHover: tuple[int, int, int] = self.color
        self.onClick = None
        self.hover = False
        self.fill: int = fill
        self.round: int = round
        self.delay: float = delay

    def setColorOnHover(self, color):
        """
        Sets color when mouse hovers over button
        :param color: rgb(r, g, b)
        :return:
        """
        # Returns self to do some js syntax stuff
        self.colorHover = color
        return self

    def setOnClick(self, func: Callable):
        """
        Defines action when clicked
        :param func:
        :return:
        """
        # Returns self to do some js syntax stuff
        self.onClick = func
        return self

    """ "Private" functions """
    def _getHover(self):
        """
        Checks if mouse is over button and sets hover accordingly
        :return:
        """
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            self.hover =True
        else:
            self.hover = False

    def _getPressed(self):
        """
        Checks if right mouse button is pressed and checks mouse pos
        :return:
        """
        mousepos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(3)[0]:
            if self.rect.collidepoint(mousepos):
                Invoke(self.onClick, self.delay)

    def draw(self):
        self._getHover()
        self._getPressed()
        if self.hover:
            pygame.draw.rect(win, self.colorHover, self.rect, self.fill, self.round)
        else:
            pygame.draw.rect(win, self.color, self.rect, self.fill, self.round)


class TitleScreen:
    def __init__(self) -> None:
        self.font = pygame.font.Font("data/fonts/BebasNeue-Regular.ttf", 70)
        self.smallfont = pygame.font.Font("data/fonts/BebasNeue-Regular.ttf", 45)
        self.title = OutlinedText("Checkers The Game!", (240, 300), 4, 70, win, font=self.font, foreground_color=(180, 28, 28),background_color=(0, 0, 0))
        self.playText = OutlinedText("2 Players", (380, 425), 4, 30, win, font=self.smallfont, background_color=(0, 0, 0))
        self.playButton = Button(350, 400, 200, 100, (60, 60, 60), round=10)
        self.playButton\
            .setOnClick(self.doExit)\
            .setColorOnHover((80, 80, 80))       # Love the javascript syntax

        self.exitText = OutlinedText("Quit", (420, 550), 4, 30, win, font=self.smallfont,
                                     background_color=(0, 0, 0))
        self.exitButton = Button(350, 525, 200, 100, (60, 60, 60), round=10, delay=0)
        self.exitButton.setOnClick(self.quit).setColorOnHover((80, 80, 80))
        self.exit = False

    def quit(self):
        global quitProgram
        quitProgram = True

    def doExit(self) -> None:
        self.exit = True

    def draw(self) -> None:
        win.fill(BACKGROUND_COLOR)

        self.title.draw()
        self.playButton.draw()
        self.playText.draw()
        self.exitButton.draw()
        self.exitText.draw()

        pygame.display.update()


titleScreen = TitleScreen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if titleScreen.exit:
        running = False
        break
    if quitProgram:
        pygame.quit()
        sys.exit()

    titleScreen.draw()



class ScoreBoard:
    def __init__(self, font: pygame.font.Font):
        """Initalize the Scoreboard"""
        self.font = font
        self.Player1 = OutlinedText("Player 1", (140, 65), 3, 35, win, foreground_color=PIECE_COLORS[1], background_color=(255, 255, 255))
        self.Player1Pos: Vector2 = pygame.math.Vector2(140, 65)
        self.Player2 = OutlinedText("Player 2", (590, 760), 3, 35, win, foreground_color=PIECE_COLORS[0], background_color=(0, 128, 0))
        self.Player2Pos: Vector2 = pygame.math.Vector2(620, 760)

        self.playertexts: tuple[OutlinedText, OutlinedText] = (self.Player2, self.Player1)
        self.selected: int = 0

    def changeSelected(self, newSelected: int):
        """
        Changes the selected color
        :param newSelected: Index of the color from PIECE_COLOURS
        :return:
        """
        self.selected = newSelected
        for text in self.playertexts:
            text.change_outline_color((255, 255, 255))
        self.playertexts[self.selected].change_outline_color((0, 128, 0))

    def draw(self):
        """
        Draws the text using the OulinedText classes draw method
        :return:
        """
        self.Player1.draw()
        self.Player2.draw()


class Board:
    def __init__(self):
        """
        Defines board class
        """
        self.vector: Vector2 = pygame.math.Vector2(0, 0)
        self.width: int = 9  # Width is number of squares
        self.boxWidth: int= 70    # Box width is how wide the squares are
        self.xoffset, self.yoffset = 135, 120
        self.ranCalc: bool = False
        self.squares: dict = {}

    def draw(self):
        """
        Runs calculations for drawing squares, in a grid pattern
        :return:
        """
        if not self.ranCalc:
            row, column = 0, 0
            colors = [(212, 190, 167), (107, 70, 61)]           # Colors for board
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
        """
        Generates the squares that the piece can move to
        :param column:
        :param row:
        :param yoffset:
        :param masterPiece:
        :return:
        """
        if not masterPiece.king:
            posRight = pygame.math.Vector2(column + 1, row + yoffset)
            posLeft = pygame.math.Vector2(column - 1, row + yoffset)
            right = pygame.Rect(posRight.x * self.boxWidth + self.xoffset, posRight.y * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth)
            left = pygame.Rect(posLeft.x * self.boxWidth + self.xoffset, posLeft.y * self.boxWidth + self.yoffset, self.boxWidth, self.boxWidth)
            selectedSquares.append(SelectedSquare(right, posRight, masterPiece, "right"))
            selectedSquares.append(SelectedSquare(left, posLeft, masterPiece, "left"))
        else:
            posRightup = pygame.math.Vector2(column + 1, row + yoffset)
            posLeftup = pygame.math.Vector2(column - 1, row + yoffset)
            posRightdown = pygame.math.Vector2(column + 1, row - yoffset)
            posLeftdown = pygame.math.Vector2(column - 1, row - yoffset)
            right = pygame.Rect(posRightup.x * self.boxWidth + self.xoffset, posRightup.y * self.boxWidth + self.yoffset,
                                self.boxWidth, self.boxWidth)
            left = pygame.Rect(posLeftup.x * self.boxWidth + self.xoffset, posLeftup.y * self.boxWidth + self.yoffset,
                               self.boxWidth, self.boxWidth)
            right2 = pygame.Rect(posRightdown.x * self.boxWidth + self.xoffset,
                                posRightdown.y * self.boxWidth + self.yoffset,
                                self.boxWidth, self.boxWidth)
            left2 = pygame.Rect(posLeftdown.x * self.boxWidth + self.xoffset, posLeftdown.y * self.boxWidth + self.yoffset,
                               self.boxWidth, self.boxWidth)
            selectedSquares.append(SelectedSquare(right, posRightup, masterPiece, "right"))
            selectedSquares.append(SelectedSquare(left, posLeftup, masterPiece, "left"))
            selectedSquares.append(SelectedSquare(right2, posRightdown, masterPiece, "right", king=True, yoffset=yoffset))
            selectedSquares.append(SelectedSquare(left2, posLeftdown, masterPiece, "left", king=True, yoffset=yoffset))


class SelectedSquare:
    def __init__(self, rect: pygame.Rect, pos: Vector2, master, type, king=False, yoffset=0):
        """
        Square for the selected positons a place can move to
        :param rect:
        :param pos:
        :param master:
        :param type:
        """
        self.rect = rect
        self.color = (0, 128, 0)
        self.master = master
        self.pos = pos

        self.destroy = None

        self.type = type
        self.king = king
        self.yoffset = yoffset

        self.moved = False

        #if self.king:
        #    self.color = (0, 0, 255)
    def draw(self):
        """
        Checks whether it can destroy the piece it lies on and draws itself
        :return:
        """
        self.checkIfDestroy()
        pygame.draw.rect(win, self.color, self.rect)

    def resetRect(self):
        """
        Resets the .rect attribute to move the square to the proper position
        :return:
        """
        self.rect.x = self.pos.x * mainBoard.boxWidth + mainBoard.xoffset
        self.rect.y = self.pos.y * mainBoard.boxWidth + mainBoard.yoffset

    def checkIfDestroy(self):
        """
        Iterates over every piece in Pieces and if collides with any, that aren't the same
        type, will move self
        :return:
        """

        # Check before to check and not compute for all pieces
        if self.pos.x < 0 or self.pos.x >= mainBoard.width or self.pos.y < 0 or self.pos.y >= mainBoard.width:
            self.rect.x = 100000
            return

        for piece in Pieces:
            if self.rect.colliderect(piece.rect):
                if not self.moved:
                    if piece.color == self.master.color:
                        self.rect.x += 100000       # Move x off the screen
                    elif piece.color != self.master.color:
                        self.destroy = piece.rect
                        if self.type == "right":
                            self.pos.x += 1
                        if self.type == "left":
                            self.pos.x -= 1

                        if not self.king:
                            if PIECE_COLORS.index(self.master.color) == 0:
                                self.pos.y -= 1
                            else:
                                self.pos.y += 1
                        else:
                            self.pos.y -= self.yoffset

                        self.resetRect()
                        self.moved = True

                    # Redo to check after piece has moved
                    if self.pos.x < 0 or self.pos.x >= mainBoard.width or self.pos.y < 0 or self.pos.y >= mainBoard.width:
                        self.rect.x = 100000
                        return
                else:
                    self.rect.x = 10000

    def detectPress(self, mousepos: Vector2):
        """
        Runs code to move piece, and disable all pieces, as well as removes piece after
        :param mousepos: Mouse position in pygame.math.Vector2 form
        :return:
        """
        global selectedSquares
        self.checkIfDestroy()
        if self.rect.collidepoint(mousepos.x, mousepos.y):
            self.master.pos = self.pos
            for piece in Pieces:
                piece.clicked = False
            scoreboard.changeSelected(abs(self.master.type - 1))
            selectedSquares = []
            if self.destroy != None:
                for piece in Pieces:
                    if piece.rect == self.destroy:
                        Pieces.remove(piece)


class GameController:
    """
    Wrapper for static methods that control global game events
    """
    @staticmethod
    def GeneratePieces(board: Board):
        """
        Generates the pieces for both colors
        :param board:
        :return:
        """
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
        """
        Checks if the mouse is clicked on a piece and sets pieces .clicked value to True
        :param mousepos:
        :return:
        """
        for piece in Pieces:
            if piece.rect.collidepoint(mousepos.x, mousepos.y):
                piece.clicked = True

    @staticmethod
    def CheckWinCases() -> bool:
        """
        Game ends when there is only one color on the board.
        If one color is on board, return True
        :return:
        """
        types = []
        for piece in Pieces:
            if piece.color not in types:
                types.append(piece.color)
        if len(types) == 1:
            return True
        return False


class CheckersPiece:
    def __init__(self, row: int, column: int, stepsize: int, offsets: tuple[int, int], color: tuple[int, int, int], radius: int = 20):
        """
        Base class for all checkers pieces
        :param row:
        :param column:
        :param stepsize:
        :param offsets:
        :param color:
        :param radius:
        """
        self.pos = pygame.math.Vector2(column, row)
        self.stepsize = stepsize
        self.offsets = offsets
        self.color = color
        self.type = PIECE_COLORS.index(self.color)
        self.radius = radius
        self.rectoffsets = [15, 15] # Offsets are x and y values
        self.rect = pygame.Rect(self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2), self.pos.y * self.stepsize + self.offsets[1]+ (self.stepsize / 2), self.radius * 2, self.radius * 2)

        self.king = False
        self.crownOffset = (4, 9)

        self.clicked = False

        Pieces.append(self)

    def handleThings(self):
        """
        Generates move squares
        :return:
        """
        if self.clicked:
            if scoreboard.selected == PIECE_COLORS.index(self.color):
                if PIECE_COLORS.index(self.color) == 0:
                    mainBoard.generateMoveSquares(self.pos.x, self.pos.y, -1, self)
                else:
                    mainBoard.generateMoveSquares(self.pos.x, self.pos.y, 1, self)
            else:
                self.clicked = False
                return

    def determineKing(self):
        if not self.king:
            if PIECE_COLORS.index(self.color) == 0:
                if self.pos.y == 0:
                    self.king = True
                    return
            else:
                if self.pos.y == mainBoard.width - 1:
                    self.king = True
                    return

    def getMiddle(self) -> tuple[float, float]:
        """
        Gets the middle of the squares in an xy position, not row, column
        Returns tuple of middle xy
        :return:  position for a given square
        """

        middlex = self.pos.x * self.stepsize + self.offsets[0] + (self.stepsize / 2)
        middley = (self.pos.y * self.stepsize + self.offsets[1]) + (self.stepsize / 2)

        return (middlex, middley)


    def draw(self):
        """
        Draws the Piece at the middle of the square
        :return:
        """
        self.determineKing()
        middles = self.getMiddle()
        self.rect = pygame.Rect(self.pos.x * self.stepsize + self.offsets[0] + self.rectoffsets[0], self.pos.y * self.stepsize + self.offsets[1] + self.rectoffsets[1], self.radius * 2, self.radius * 2)
        #pygame.draw.rect(win, self.color, self.rect)       # Uncomment to show hitboxes of pieces
        pygame.draw.circle(win, self.color, (middles[0], middles[1]), self.radius)
        if self.king:
            win.blit(crownImage, (self.rect.x + self.crownOffset[0], self.rect.y + self.crownOffset[1]))


def drawObjects(win) -> None:
    """
    Draws objects on pygame.surface
    :param win:
    :return:
    """
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
            for piece in Pieces:
                piece.clicked = False
            for square in selectedSquares:
                square.detectPress(Vector2(pygame.mouse.get_pos()))
            selectedSquares = []
            GameController.CheckClick(Vector2(pygame.mouse.get_pos()))

    drawObjects(win)
    for piece in Pieces:
        piece.handleThings()

    if GameController.CheckWinCases():
        pygame.quit()
        run = False
        sys.exit()
