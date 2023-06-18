# TODO: Game Over: Cats Game vs Victory
# Ask if players want to play again
# Track scores
# Custom player names √
# Make bot smarter, selecting to block opponent victory, from most likely to win √
# Change positions and positionWeight to dicts
# Dicts enable randomization of positions to pick based on weights
import random

class Board:
	def resetGame(self):
		self.positions = [0] * 9
		self.resetWeight()

	def __init__(self):
		self.threeInARowPositions = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
		self.promptString = "{0}, select where you want to go next: "
		self.congrats = "Congrats {0}!"
		self.namePrompt = "Enter name of player {0}: "
		self.keepGoingPrompt = "Would you like to keep playing? (y/n):"
		self.currentPlayer = 0
		self.playerNames = ["Player 1","Player 2"]
		self.scoreReport = "{0} has {1} wins to {2}'s {3}"
		self.twoPlayer = False
		self.botDifficulty = 0
		self.resetGame()
		self.botOrPlayer()
		self.setNames()
		self.scores = [0,0]
		self.keepGoing = True

	def ynInput(self, ynPrompt):
		inStr = ""
		while inStr == "":
			try:
				inStr = input(ynPrompt).strip().lower()
				if inStr != 'y' and inStr != 'n':
					raise TypeError() 
			except TypeError:
				print("Please input 'y' or 'n'")
				inStr = ""
		if inStr == 'y':
			return True

	def botOrPlayer(self):
		self.twoPlayer = self.ynInput("Do you want to play with a second player? (y/n): ")

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
		if 0 not in t:
			return True
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
		# Ignore Cats Game and restart
		# Congratulate winner (current player)
		print(self.congrats.format(self.playerNames[self.currentPlayer-1]))
		# Increase score
		self.scores[self.currentPlayer-1] += 1
		# Show final board
		self.display()

	def getScores(self):
		print(self.scoreReport.format(self.playerNames[0], self.scores[0], self.playerNames[1], self.scores[1]))

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
		self.resetGame()

	def keepGoingIn(self):
		self.keepGoing = self.ynInput("Do you want to continue playing? (y/n): ")

	def run(self):
		while self.keepGoing:
			self.play()
			self.getScores()
			self.keepGoingIn()

	def find(self, lst, a):
		return [i for i, x in enumerate(lst) if x==a]

	def bot(self):
		self.updatePositions(self.spotFinder(),2)

	def resetWeight(self):
		self.positionWeight = [0] * 9

	def spotFinder(self):
		# Current set up will select position to go based on threeInARowPositions order. Check all possible winning combos and then pick bot winning first and blocking player second √
		# take botDifficulty value and use it to modify random selection of bot positioning
		# if bot has two in a row and third in row open, go for it √
		# if player has two in a row and third in row open, go for it √
		# determine what spots are most likely to win for player and go √
		# determine what spots are most likely for bot to win and go for it √
		self.resetWeight()
		plaPos = set(self.find(self.positions,1))
		botPos = set(self.find(self.positions,2))
		for option in self.threeInARowPositions:
			option = set(option)
			plaPosInOpt = plaPos.intersection(option)
			botPosInOpt = botPos.intersection(option)
			plaCount = len(plaPosInOpt)
			botCount = len(botPosInOpt)
			# print("botPosInOpt",botPosInOpt)
			# print("botCount",botCount)
			# print("plaPosInOpt",plaPosInOpt)
			# print("plaCount",plaCount)
			if botCount == 2 and plaCount == 0:
				# print("option",option)
				# print("botPosInOpt",botPosInOpt)
				# print("bot winning pos:",list(option.difference(botPosInOpt))[0])
				self.positionWeight[list(option.difference(botPosInOpt))[0]] += 5
				# print("bot winning weight:",self.positionWeight[list(option.difference(botPosInOpt))[0]])
			elif botCount == 0 and plaCount == 2:
				# print("option",option)
				# print("plaPosInOpt",plaPosInOpt)
				# print("pla winning pos:",list(option.difference(plaPosInOpt))[0])
				self.positionWeight[list(option.difference(plaPosInOpt))[0]] += 1
				# print("pla winning weight:",self.positionWeight[list(option.difference(plaPosInOpt))[0]])
		i = 0
		goHere = 0
		while i < len(self.positionWeight):
			if(self.positions[i] == 0):
				# print(self.positionWeight)
				# print(self.positionWeight[goHere]," <= ",self.positionWeight[i],"?")
				if self.positionWeight[goHere] <= self.positionWeight[i]:
					# print("yes")
					goHere = i
			# 	else:
			# 		print("no")
			# print("i:",i,"\n[i]:",self.positionWeight[i])
			i += 1
		return goHere

		if self.botDifficulty == 0:
			return random.choice(self.find(self.positions,0))


b = Board()

b.run()

