
# ICS3U CCT

This game is made for my course culminating task of the ICS3U course. It was made to demonstrate a through understanding of data structures and algorithms and their practical applications. As well as to demonstrate a through understanding of the Python language and more advanced object oriented programming (OOP) concepts


### Roadmap


- [x] Drawing board/pieces
- [x] Piece movement
- [x] King movement and capturing
- [x] Menu UI
- [x] Endless gameplay

## Rules
### Movement
A pawn checker can only move one diagonal space forward, towards your opponents checkers.
Once the player makes a move, the other player is allowed their move, and so on.

### Jumping Checkers
If your checker is in the diagonal space nearest to an opponents checker, you can jump and
capture that checkers. To capture a checker, you move two diagonal spaces in the direction
of the opponents checker you are attacking.
#### Rules for jumping
- The space on the other side your opponents checker must be empty

### King Pieces
A checker becomes a king when it has reached the end of the board on the opponents side.
A king can move forward and backward, diagonally and jump diagonally with the same rules as
a pawn checker. There is no limit to how many king checkers you can have.

#### More rules [here](https://www.wikihow.com/Play-Checkers)


## Software Development Cycle

### Problem Definition
Problem: Make checkers in Python

### Analysis
#### What needs to be done?
- Movement
- Endless gameplay
- King Movement
- Capturing pieces

#### Generic functions needed
- Algorithm to make board pieces
- Win-state algorithm
- Piece generator
- Interactions  between user and gameplay

### Design
#### Layout
Should be layed out so board is in the middle, with UI indicators of turns. 

#### Other
No real formulas needed

### Writing code
See commits [here](https://github.com/Ironislife98/ICS3U-CCT/commits/main)

### Testing
#### Bugs encountered
- Squares moving off board
- Squares overlapping other pieces

#### Solutions
```
if self.pos.x < 0 or self.pos.x >= mainBoard.width or self.pos.y < 0 or self.pos.y >= mainBoard.width:

    self.rect.x = 100000
    return 
```
Essentially checking if movement square is off the board, if so, the movement square is moved out of the way.

```
if piece.color == self.master.color:
    self.rect.x += 100000
```
Checks if the color of the piece being collided with is the same as the master of the movement square. Where the master if the piece generating the movement square. If so, then the movement square is moved off screen.

### Implementation
Releases can be found [here](https://github.com/Ironislife98/ICS3U-CCT/releases)
## Acknowledgements
See [Here](https://docs.google.com/document/d/1RqiBmbadei_6bYUjA1werJNm_PFnq0WH54d84ZVi_D8/edit?usp=sharing) for citations




## Authors

- [@Ironislife98](https://www.github.com/Ironislife98)

