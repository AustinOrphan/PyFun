# TODO: Game Over: Cats Game vs Victory
# Ask if players want to play again
# Track scores
# Custom player names √
# Make bot smarter, selecting to block opponent victory, from most likely to win
import random

class Board:
	def reset(self):
		self.positions = [0] * 9

	def __init__(self):
		self.threeInARowPositions = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
		self.promptString = "{0}, select where you want to go next: "
		self.congrats = "Congrats {0}!"
		self.namePrompt = "Enter name of player {0}: "
		self.currentPlayer = 0
		self.playerNames = ["Player 1","Player 2"]
		self.twoPlayer = False
		self.reset()
		self.botOrPlayer()
		self.setNames()

	def botOrPlayer(self):
		inStr = ""
		while inStr == "":
			try:
				inStr = input("Do you want to play with a second player? (y/n): ").strip().lower()
				if inStr != 'y' and inStr != 'n':
					raise TypeError() 
			except TypeError:
				print("Please input 'y' or 'n'")
				inStr = ""
		if inStr == 'y':
			self.twoPlayer = True

	def setNames(self):
		self.inputName(1)
		if self.twoPlayer:
			self.inputName(2)

	def inputName(self,playerNumber):
		nameInput = input(self.namePrompt.format(playerNumber)).strip()
		if nameInput != "":
			self.playerNames[playerNumber-1] = nameInput

	def getSymbol(self, c):
		if c == 1:
			return "X"
		elif c == 2:
			return "O"
		else:
			return " "

	def toText(self, positions):
		j = 0
		board = ""
		row = ""
		for i in range(9):
			row += " " + self.getSymbol(positions[i])
			if (i+1) % 3 == 0:
				if i+1 < 7:
					row = "\033[4m" + row + " \033[0m"
				board += row + "\n"
				row = ""
			else:
				row += " |"
		return board

	def display(self, positions = None):
		if positions == None:
			positions = self.positions
		print(self.toText(positions))

	def switchPlayer(self):
		if self.currentPlayer == 1:
			self.currentPlayer = 2
		else:
			self.currentPlayer = 1
		print(f"\n{self.playerNames[self.currentPlayer-1]} is up")

	def updatePositions(self, location = -1, newValue = 0):
		if location > -1 and location < 9 and self.positions[location] == 0:
			self.positions[location] = newValue
			return True
		else:
			return False

	def guide(self):
		board = ""
		row = ""
		for i in range(10):
			if i == 0:
				continue
			else:
				row += " " + str(i)
			if i % 3 == 0:
				if i < 7:
					row = "\033[4m" + row + " \033[0m"
				board += row + "\n"
				row = ""
			else:
				row += " |"
		print(board)

	def isGameOver(self):
		t = self.positions
		for pSet in self.threeInARowPositions:
			if t[pSet[0]] == 0:
				continue
			elif t[pSet[0]] == t[pSet[1]] and t[pSet[1]] == t[pSet[2]]:
				return True
		return False

	def prompt(self):
		self.display()
		self.guide()
		while not self.updatePositions(int(input(self.promptString.format(self.playerNames[self.currentPlayer-1])))-1,self.currentPlayer):
			continue

	def declareWinner(self):
		print(self.congrats.format(self.playerNames[self.currentPlayer-1]))
		self.display()

	def play(self):
		while not self.isGameOver():
			self.switchPlayer()
			if self.twoPlayer:
				self.prompt()
			else:
				if self.currentPlayer == 1:
					self.prompt()
				else:
					self.bot()
		self.declareWinner()

	def find(self, lst, a):
		return [i for i, x in enumerate(lst) if x==a]

	def bot(self):
		self.updatePositions(random.choice(self.find(self.positions,0)),2)

b = Board()

b.play()

