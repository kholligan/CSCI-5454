import math
import random
import numpy as np 

choices = []
opp_choice = []
# Weighted choice implementation from 
# http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
def weighted_choice(choices):
	total = sum(w for c, w in choices)
	r = random.uniform(0, total)
	upto = 0
	for c, w in choices:
		if upto + w >= r:
			return c
		upto += w
	assert False, "Shouldn't get here"

def hedge(epsilon, opp_choice, matrix):
	choice = weighted_choice(choices)

	# Calculate what the loss would have been for each choice in the matrix
	for jt in range(len(matrix[0])):
		loss = -matrix[opp_choice][jt]
		# Update the weights with exponentially proportional loss
		choices[jt] = (jt, math.pow((1 - epsilon),loss)*choices[jt][1])

	# Normalize the weights so they are expressed as a strict probability
	total = sum(w for c, w in choices)
	for i in range(len(choices)):
		normalized = choices[i][1]/total
		choices[i] = (i, normalized)
	
	return choice

def gameManager(rounds, width, height):
	# generate the initial choice matrix
	initial_probability = 1/float(width)
	for i in range(width):
		choices.append((i,initial_probability))

	# Generate matrix of supplied dimensions
	matrix = [[0 for x in range(width)] for y in range(height)]

	rewards = [-1, 0, 1]
	# Populate matrix with random rewards of -1, 0, or 1
	for i in range(height):
		for j in range(width):
			matrix[i][j] = random.choice(rewards)
	
	print "Game matrix: ", matrix
	T = rounds
	actions = 2*T
	# Set epsilon based on the number of actions and rounds
	epsilon = math.sqrt(math.log(actions)/T)
	payout = [0,0]

	for t in range(1,rounds+1):
		user_input = int(raw_input("Round " +str(t)+" choice: "))-1
		ai_choice = hedge(epsilon, user_input, matrix)
		payout[0] += matrix[user_input][ai_choice]
		payout[1] += matrix[user_input][ai_choice]
		print("User choice: {0}, AI choice: {1}, User gains (min): {2}, AI gains (max): {3}").format(user_input+1, ai_choice+1, matrix[user_input][ai_choice], -matrix[user_input][ai_choice]) 
		# print("New choices: {}").format(choices)

	print("Total user gains (min): {0}, total AI gains (max): {1}").format(payout[0], payout[1])

if __name__ == "__main__":
   rounds = int(raw_input("Enter number of rounds to be played: "))
   width = int(raw_input("Enter matrix width: "))
   height = int(raw_input("Enter matrix height: "))

   gameManager(rounds, width, height)
