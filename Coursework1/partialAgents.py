# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


class PartialAgent(Agent):

	#__name__ == '__main__' 
	#According to this function to decide what is the next step for the pacman, 
	#getAction will choose the best action according to the evaluation function.
	#Therefore, evaluationFunction is the heart for this Agent, because it will 
	#access every input score.
	def getAction(self, gameState):
		#Collect the possibility for the next step, might be west,esat,north,stop.....
		legalMoves = gameState.getLegalActions() 
		#according to the evaluation function, get all the scores from next step
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves] 
		#get the maximum score 
		bestScore = max(scores) 
		#collect the best action set according to the maximum score
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore] 
		#choose an action at random from the best action set
		chosenIndex = random.choice(bestIndices)  
		return legalMoves[chosenIndex]
	
	#This function will calculate the distance from food to Agent, Ghost to Agent, Capsule to Agent....
	def evaluationFunction(self, currentGameState, action): 
		#All these information you can extract from a Gamestate in pacman.py
		#Generates the successor state after the specified pacman move
		successorGameState = currentGameState.generatePacmanSuccessor(action) 
		
		#Get the New position after move
		newPos = successorGameState.getPacmanPosition() 
		
	
		#Get the food position in the grid
		newFood = successorGameState.getFood() 
		curFood = currentGameState.getFood() 
		
		#Get the Ghost Position
		newGhostStates = successorGameState.getGhostStates() 
		
		#Collect the time after pacman eat the capsule,
		#Moves ghosts are scared
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] 
		
        	#Calculate all the left food , then print it.
		food_left = sum(int(j) for i in newFood for j in i)
		print food_left		

		currscore = 0 

		if action == "Stop":	
			return -100 
		
		#If current state makes the ghost scared, then join the time into currscore
		for st in newScaredTimes: 
			currscore += st 
		
		default = 1;
		ghost_distances = [] 
		try:
    			min_gho = min(ghost_distances) 
		except ValueError:
    			min_gho = default
		#according to the ghost position, use the manhattanDistance 
		#to calculate the distance between ghost and current pacman,
		#then store the distance into a list.
		for gs in newGhostStates: 
			ghost_distances += [util.manhattanDistance(gs.getPosition(),newPos)] 
		
		#Get all the food position, either current position and new position.
		foodList = newFood.asList() 
		curfoodList = curFood.asList() 
		
		wallList = currentGameState.getWalls().asList()		

		
		#Store the distance to the food into a list.
		food_distences = []
		try:
    			min_val = min(food_distences) 
		except ValueError:
    			min_val = default
		
		#Use manhattanDistance to calculate the distance from all the food to current pacman position
		for foodpos in foodList: 
			food_distences += [manhattanDistance(newPos,foodpos)] 
        	#This inverse_food_distences solution comes from He11o_Liu 
		inverse_food_distences=0;
		if len(food_distences)>0 and min_val > 0: 
			inverse_food_distences = 1.0 / min_val
        #Considering the distance between ghosts to pacman and food to pacman,
        #And the ghost score is higher.
		currscore += min_gho *(inverse_food_distences**4)
        #Collect the current gamestate score
		currscore += successorGameState.getScore()
        #The score would be higher if pacman eat food now
		if newPos in curfoodList: 
			currscore = currscore * 1.1
		return currscore

def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()
