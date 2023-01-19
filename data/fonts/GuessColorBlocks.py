import random


def new_game():
  global comp_block1, comp_block2, comp_block3
  comp_block1 = random.randint(1, 4)
  while comp_block2 == comp_block1 or comp_block2 == 0:
    comp_block2 = random.randint(1, 4)
  while comp_block3 == comp_block1 or comp_block3 == comp_block2 or comp_block3 == 0:
    comp_block3 = random.randint(1, 4)


def check_positions_correct(user_block1_in, user_block2_in, user_block3_in):
  global comp_block1, comp_block2, comp_block3
  positions_correct = 0
  if user_block1_in == comp_block1:
    positions_correct += 1
  if user_block2_in == comp_block2:
    positions_correct += 1
  if user_block3_in == comp_block3:
    positions_correct += 1
  return positions_correct


comp_block1, comp_block2, comp_block3 = 0, 0, 0

print("In this game, there are four different coloured blocks (red, green, blue, and yellow). The computer will randomly generate coloured blocks. You have to guess what the computer has generated.")

try_again = 1
new_game()

while try_again:
  user_colour1 = input("Guess the first colour: ").upper()
  user_colour2 = input("Guess the second colour: ").upper()
  user_colour3 = input("Guess the third colour: ").upper()
  print()
  print(f"You chose {user_colour1[0]}, {user_colour2[0]}, {user_colour3[0]}")
  converter = ["R", "G", "B", "Y"]
  num_correct = check_positions_correct(converter.index(user_colour1[0]), converter.index(user_colour2[0]), converter.index(user_colour3[0]))
  print()
  print(f"Positions correct: {num_correct}")
  print()
  if num_correct == 3:
    print("CONGRATULATIONS YOU WON")
    try_again = 0
  else:
    print("Try again: 1\nExit: 0")
    try_again = int(input("Enter choice: "))
    print()
    