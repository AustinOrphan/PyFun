# TODO: Game Over: Cats Game vs Victory √
# Ask if players want to play again √
# Track scores √
# Custom player names √
# Make bot smarter, selecting to block opponent victory, from most likely to win √
# Change positions and positionWeight to dicts
# Dicts enable randomization of positions to pick based on weights
import random

class Board:
# Initilization and Setup

	def __init__(self):
		# Define winning positions (three in a row)
		self.threeInARowPositions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 4, 8], [2, 4, 6], [0, 3, 6],
            [1, 4, 7], [2, 5, 8]
		]
		# Prompt strings for user interaction
		self.promptString = "{0}, select where you want to go next: "
		self.congrats = "Congrats {0}!"
		self.namePrompt = "Enter name of player {0}: "
		self.keepGoingPrompt = "Would you like to keep playing? (y/n):"
		self.playerNames = ["Player 1","Player 2"]
		self.scoreReport = "{0} has {1} wins to {2}'s {3}"
		# Initialize game state variables
		self.currentPlayer = 0
		self.twoPlayer = False
		self.botDifficulty = 0
		self.scores = [0,0]
		self.keepGoing = True
		# Initialize board and game settings
		self.resetBoard()
		self.botOrPlayer()
		self.setNames()

	# Reset the board positions to empty
	def resetBoard(self):
		self.positions = [" "] * 9
		self.resetWeight()

	# Reset position weights for the bot's decision-making
	def resetWeight(self):
		self.positionWeight = [0] * 9

	# Game Flow

	# Main game loop
	def run(self):
		while self.keepGoing:
			self.play()
			self.getScores()
			self.promptKeepGoing()

	# Single game loop
	def play(self):
		while True:
			game_status = self.getGameStatus()
			if game_status != "ongoing":
				break
			self.switchPlayer()
			self.display()
			if self.twoPlayer or self.currentPlayer == 1:
				self.guide()
				self.getPlayerMove()
			else:
				self.botMove()
		if game_status == "win":
			self.declareWinner()
		elif game_status == "draw":
			print("It's a draw!")
		self.resetBoard()

	# Check the current status of the game (ongoing, win, draw)
	def getGameStatus(self):
		t = self.positions
		for pSet in self.threeInARowPositions:
			if t[pSet[0]] == " ":
				continue
			elif t[pSet[0]] == t[pSet[1]] and t[pSet[1]] == t[pSet[2]]:
				return "win"
		if " " not in t:
			return "draw"
		return "ongoing"

	# Congratulate winner (current player), update score, and display final board
	def declareWinner(self):
		print(self.congrats.format(self.playerNames[self.currentPlayer-1]))
		self.scores[self.currentPlayer-1] += 1
		self.display()

	# Display the current scores
	def getScores(self):
		print(self.scoreReport.format(self.playerNames[0], self.scores[0], self.playerNames[1], self.scores[1]))

	# Switch the current player
	def switchPlayer(self):
		if self.currentPlayer == 1:
			self.currentPlayer = 2
		else:
			self.currentPlayer = 1
		print(f"\n{self.playerNames[self.currentPlayer-1]} is up")

	# Update the board position at the given location if the move is valid
	def updatePositions(self, location = -1, newValue = " "):
		if location > -1 and location < 9 and self.positions[location] == " ":
			self.positions[location] = newValue
			return True
		else:
			return False

# Utility Functions

	# Get the player symbol based on the player number
	def getPlayerSymbol(self, c):
		symbols = {1: "X", 2: "O"}
		return symbols.get(c, " ")

	# Underline the given text
	def underline(self, text):
		return f"\033[4m{text}\033[0m"

	# Convert the board positions to a text representation
	def toText(self, positions):
		board = ""
		row = ""
		for i in range(9):
			row += " " + str(positions[i])
			if (i+1) % 3 == 0:
				if i < 6:
					row = self.underline(row)
				board += row + "\n"
				row = ""
			else:
				row += " |"
		return board

	# Display the current board
	def display(self, positions = None):
		if positions == None:
			positions = self.positions
		print(self.toText(positions))

	# Display a guide for the board positions
	def guide(self):
		guide_positions = list(range(1, 10))
		print(self.toText(guide_positions))

	# Find all positions in the list that match the given value
	def find(self, lst, a):
		return [i for i, x in enumerate(lst) if x == a]

	# Get the positions of the player and bot
	def getPlayerAndBotPositions(self):
		plaPos = {i for i, pos in enumerate(self.positions) if pos == "X"}
		botPos = {i for i, pos in enumerate(self.positions) if pos == "O"}
		return plaPos, botPos

# Bot Logic

	# Make a move for the bot
	def botMove(self):
		self.updatePositions(self.findBestMove(), self.getPlayerSymbol(2))

	# Find the best move for the bot
	def findBestMove(self):
		self.resetWeight()
		plaPos, botPos = self.getPlayerAndBotPositions()
		self.updateWeights(plaPos, botPos)
		return self.selectBestPosition()

	# Update the weights for the bot's decision-making process
	def updateWeights(self, plaPos, botPos):
		for option in self.threeInARowPositions:
			option = set(option)
			plaPosInOpt = plaPos.intersection(option)
			botPosInOpt = botPos.intersection(option)
			plaCount = len(plaPosInOpt)
			botCount = len(botPosInOpt)
			if botCount == 2 and plaCount == 0:
				self.positionWeight[list(option.difference(botPosInOpt))[0]] += 5
			elif botCount == 0 and plaCount == 2:
				self.positionWeight[list(option.difference(plaPosInOpt))[0]] += 1

	# Select the best position for the bot to move
	def selectBestPosition(self):
		goHere = 0
		for i in range(len(self.positionWeight)):
			if self.positions[i] == " " and self.positionWeight[goHere] <= self.positionWeight[i]:
				goHere = i
		if self.botDifficulty == 0:
			return random.choice(self.find(self.positions, " "))
		return goHere
	
# User Input and Prompts

	# Determine if the game is two-player or against the bot
	def botOrPlayer(self):
		self.twoPlayer = self.promptYesNoInput("Do you want to play with a second player? (y/n): ")

	# Set the names of the players
	def setNames(self):
		self.promptPlayerName(1)
		if self.twoPlayer:
			self.promptPlayerName(2)

	# Get the move from the current player
	def getPlayerMove(self):
		while True:
			try:
				move = int(input(self.promptString.format(self.playerNames[self.currentPlayer-1])))-1
				if self.updatePositions(move, self.getPlayerSymbol(self.currentPlayer)):
					break
			except ValueError:
				print("Invalid input. Please enter a number between 1 and 9.")

	# Prompt the user for a yes or no input
	def promptYesNoInput(self, promptText):
		while True:
			userInput = input(promptText).strip().lower()
			if userInput in ['y', 'n']:
				return userInput == 'y'
			print("Please input 'y' or 'n'")

	# Prompt the user to continue playing
	def promptKeepGoing(self):
		self.keepGoing = self.promptYesNoInput("Do you want to continue playing? (y/n): ")

	# Prompt the user to input a name for a player
	def promptPlayerName(self, playerNumber):
		nameInput = input(self.namePrompt.format(playerNumber)).strip()
		if nameInput != "":
			self.playerNames[playerNumber-1] = nameInput

# Initilize and run the game
b = Board()
b.run()

