class Board:
	def reset(self):
		self.positions = [0] * 9
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
				board += row + "\n"
				row = ""
			else:
				row += " |"
		return board
	def display(self, positions = None):
		if positions == None:
			positions = self.positions
		print(self.toText(positions))
	def updatePositions(self, location, newValue):
		self.positions[location] = newValue
	def printGuide(self):
		board = ""
		row = ""
		for i in range(10):
			if i == 0:
				continue
			else:
				row += " " + str(i)
			if i % 3 == 0:
				board += row + "\n"
				row = ""
			else:
				row += " |"
		print(board)

b = Board()

b.display()
b.printGuide()
b.updatePositions(0,1)
b.display()
b.updatePositions(1,2)
b.display()
b.updatePositions(2,1)
b.display()
b.updatePositions(3,2)
b.display()
b.updatePositions(4,1)
b.display()
