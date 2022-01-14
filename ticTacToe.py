# TODO: Game Over: Cats Game vs Victory
# Ask if players want to continue playing
# Track scores
# Custom player names
		
class Board:
	def reset(self):
		self.positions = [0] * 9
		self.threeInARowPositions = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
		self.promptString = "Player {0}, select where you want to go next: "
		self.congrats = "Congrats player {0}"
		self.currentPlayer = 0

	def __init__(self):
		self.reset()

	def getSymbol(self,c):
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
		print("Player {0} is up".format(self.currentPlayer))

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
		while not self.updatePositions(int(input(self.promptString.format(self.currentPlayer)))-1,self.currentPlayer):
			continue

	def declareWinner(self):
		print(self.congrats.format(self.currentPlayer))
		self.display()

	def play(self):
		self.reset()
		while not self.isGameOver():
			self.switchPlayer()
			self.prompt()
		self.declareWinner()

b = Board()

b.play()

