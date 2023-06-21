# Rock Paper Scissors
import random
scores = [0,0]
optionStrings = ["rock","paper","scissors"]
optionNums = [0,1,2]

def printOptions():
	for i in range(len(optionNums)):
		print("{0}: {1}".format(optionNums[i], optionStrings[i]))

def botChoice():
	return random.choice(optionNums)

def play(selection1 = -1, selection2 = -1):
	while selection1 == -1:
		try:
			printOptions()
			inStr = input("Input the number of your selection (0, 1, or 2): ").strip().lower()
			inNum = int(inStr)
			if 0 <= int(inNum) <= 2:
				selection1 = inNum
			else:
				raise TypeError()
		except TypeError:
			print("Acceptable options are the numbers 0, 1, and 2")
		except ValueError:
			print("Enter a number, no other characters")
	if selection2 == -1:
		selection2 = botChoice()
	print("You selected {0} and the bot selected {1}".format(optionStrings[selection1],optionStrings[selection2]))

	if selection1 == selection2:
		result = "You tied!"
	else:
		if selection2 == 2:
			selection2 = -1
		if selection1 == selection2 + 1:
			result = "You win!"
			scores[0] += 1
		else:
			result = "You lose!"
			scores[1] += 1

	print(result)
	print("\nStandings:\nPlayer: {0}\nBot:    {1}\n".format(scores[0],scores[1]))
while True:
	play()