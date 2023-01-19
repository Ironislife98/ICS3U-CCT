import random

print("Rock-Paper-Scissors is a game played between two individuals. The rules of the game are:\n")
print("Rock breaks Scissors,\nScissors cut Paper, and \nPaper covers Rock.\n")
print("In this game, the user will play against the computer.\n")


w, l, t = 0, 0, 0

def determine_outcome(user, comp):
  global w, l, t
  outcomes = {
  "rock": {
    "win": "scissors",
    "lose": "paper",
  },
  "scissors": {
    "win": "paper",
    "lose": "rock",
  },
  "paper": {
    "win": "rock",
    "lose": "scissors",
  }
  }
  if user == outcomes[comp]["win"]:
    w += 1
    return "WIN"
  elif user == comp:
    t += 1
    return "TIE"
  elif user == outcomes[comp]["lose"]:
    l += 1
    return "LOSE"

    
def RockPaperScissors(n=0):
  options = ["rock","paper", "scissors"]
  if n == 0:
    print("Rock: 1\nPaper: 2\nScissors: 3\n")
    playerChoice = int(input("Enter your choice: "))
    compChoice = options[random.randint(0, 2)]
    print()
    print(determine_outcome(options[playerChoice - 1], compChoice))
    print()
  else:
    print("Rock: 1\nPaper: 2\nScissors: 3\n")
    playerChoice = int(input("Enter your choice: "))
    print()
    compChoice = int(input("Enter computers choice: "))
    print()
    print(determine_outcome(options[playerChoice - 1], options[compChoice - 1]))
    print()
    print(f"Wins: {w}, Ties: {t}, Losses: {l}\n")

  RockPaperScissors(n=n)