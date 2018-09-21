# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
############################################################ MODIFICATION BELOW ############################################################ 
    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    "Add more of your code here if you want to"
    return legalMoves[random.choice([index for index in range(len(scores)) if scores[index] == max(scores)])]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    st = min(newScaredTimes)

    "*** YOUR CODE HERE ***"

    #First get the current state
    curPos = currentGameState.getPacmanPosition()
    ghostPos = successorGameState.getGhostPositions()
    curFoodList = currentGameState.getFood().asList()
    curCap = currentGameState.getCapsules()

    #Then get the new state
    newFoodList = newFood.asList()
    newCap = successorGameState.getCapsules()

    closestFoodDist = 1000000000
    farthestFoodDist = -1000000000
    closestCapDist = 1000000000
    foundClosestFood = False
    foundFarthestFood = False
    foundClosetCap = False

    for food in newFoodList:
      dist = manhattanDistance(newPos,food)
      if dist < closestFoodDist and dist != 0:
        closestFoodDist = dist
        closestFoodPos = food
        foundClosestFood = True

    if foundClosestFood:
      for food in newFoodList:
        dist = manhattanDistance(food,closestFoodPos)
        if dist >farthestFoodDist and dist != 0:
          farthestFoodDist = dist
          foundFarthestFood = True

    for capsule in newCap:
      dist = manhattanDistance(capsule, newPos)
      if dist < closestCapDist and dist != 0:
        closestCapDist = dist
        foundClosetCap = True

    #Mind the Ghosts
    closestGhost = 100000000000
    for g in ghostPos:
      closestGhost = min(manhattanDistance(g, newPos),closestGhost)
    
    #Evluation: Get food and capsule, and stay away from the ghost

    getFood = 0
    
    if len(newFoodList)<len(curFoodList):
      getFood = 10000.0

    getCapsles = 0.0

    if (len(newCap)<len(curCap)):
      getCapsles = 10000.0

    if getCapsles == 10000 and st < 2:
      getCapsles = 15000.0

    getCaught = 10000.0

    if st > closestGhost:
      getCaught = 20000.0

    if closestGhost<2:
      if st < 2:
        getCaught = -100000.0

    evaluation = getFood + getCapsles + getCaught + closestGhost
    if foundClosestFood:
      evaluation += 1000.0/closestFoodDist
    if foundFarthestFood:
      evaluation += 1000.0/farthestFoodDist
    if foundClosetCap:
      evaluation += 1000.0/closestCapDist

    return evaluation

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):

    legalMoves=gameState.getLegalActions(0)
    futureStates=[gameState.generateSuccessor(0,move) for move in legalMoves]
    
    scores = [self.minimizer(0,state,1) for state in futureStates]
    return legalMoves[random.choice([i for i in range(len(scores)) if scores[i] == max(scores)])]

  def maximizer(self,currentDepth,gameState):
    searchEnded = self.depth==currentDepth or gameState.isLose() or gameState.isWin()
    if not searchEnded:
      return max([self.minimizer(currentDepth,state,1) for state in [gameState.generateSuccessor(0,move) for move in gameState.getLegalActions(0)]])
    else:
      return self.evaluationFunction(gameState)
      
  def minimizer(self,currentDepth,gameState,ghostIndex):
    searchEnded = self.depth==currentDepth or gameState.isLose() or gameState.isWin()
    if searchEnded:
      return self.evaluationFunction(gameState)
      
    if (ghostIndex < gameState.getNumAgents()-1):
      return min([self.minimizer(currentDepth,state,ghostIndex+1) for state in [gameState.generateSuccessor(ghostIndex, move) for move in gameState.getLegalActions(ghostIndex)]])
    else:
      return min([self.maximizer(currentDepth+1,state) for state in [gameState.generateSuccessor(ghostIndex, move) for move in gameState.getLegalActions(ghostIndex)]])



############################################################ MODIFICATION BELOW ############################################################ 

class AlphaBetaAgent(MultiAgentSearchAgent):

  def getAction(self, gameState):
    val = -1000000.0
    alpha = -1000000.0
    beta = 1000000.0
    actionSeq = []
    moves = gameState.getLegalActions(0)
    successors = [(move, gameState.generateSuccessor(0, move)) for move in moves]
    for successor in successors:
      t = minimaxPrune(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction, alpha, beta)
      if t > val:
        val = t
        actionSeq = successor[0]
      if val > beta:
        return actionSeq
      alpha = max(alpha, val)   
    return actionSeq

def minimaxPrune(agent, agents, state, depth, evalFunc, alpha, beta):
    searchEnded = depth <= 0 or state.isWin() == True or state.isLose() == True
    if searchEnded:
      return evalFunc(state)
    if agent == 0:
      val = -10000000.0
    else:
      val = 10000000.0
    legalMoves = state.getLegalActions(agent)

    for move in legalMoves:
      successor = state.generateSuccessor(agent, move)
      if agent == 0:
        val = max(val, minimaxPrune(agents[agent+1], agents, successor, depth, evalFunc, alpha, beta))
        alpha = max(alpha, val)
        if val > beta:
          return val
      elif agent == agents[-1]:
        val = min(val, minimaxPrune(agents[0], agents, successor, depth - 1, evalFunc, alpha, beta))
        beta = min(beta, val)
        if val < alpha:
          return val
      else:
        val = min(val, minimaxPrune(agents[agent+1], agents, successor, depth, evalFunc, alpha, beta))
        beta = min(beta, val)
        if val < alpha:
          return val
    return val


class ExpectimaxAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    legalMoves = gameState.getLegalActions(0)
    scores=[self.expecti(0,state,1) for state in [gameState.generateSuccessor(0,move) for move in legalMoves]]
    return legalMoves[random.choice([index for index in range(len(scores)) if scores[index] == max(scores)])]
  def expecti (self,currentDepth,gameState,ghostIndex):
    searchEnded = self.depth == currentDepth or gameState.isLose() or gameState.isWin()
    if searchEnded:
      return self.evaluationFunction(gameState)
    if(ghostIndex == gameState.getNumAgents()-1):
      scores = [self.maximizer(currentDepth+1,state) for state in [gameState.generateSuccessor(ghostIndex,move) for move in gameState.getLegalActions(ghostIndex)]]
    elif(ghostIndex < gameState.getNumAgents()-1):
      scores = [self.expecti(currentDepth,state,ghostIndex+1) for state in [gameState.generateSuccessor(ghostIndex,move) for move in gameState.getLegalActions(ghostIndex)]]
    return sum(scores)/len(scores)
  def maximizer(self,currentDepth,gameState):
    searchEnded = self.depth == currentDepth or gameState.isLose() or gameState.isWin()
    if searchEnded:
      return self.evaluationFunction(gameState)
    return max([self.expecti(currentDepth,state,1) for state in [gameState.generateSuccessor(0,move) for move in gameState.getLegalActions(0)]])

# def betterEvaluationFunction(currentGameState):
#   pos= currentGameState.getPacmanPosition()
#   foodList = currentGameState.getFood().asList()
#   ghostStates = currentGameState.getGhostStates()
#   walls = currentGameState.getWalls()
#   closestFoodDist = -1
#   ghostEvaluation = 0
#   capsuleEvaluation = 0
#   #Loop throught foodList
#   for food in foodList:
#     if(closestFoodDist < 0 or mazeDistance(pos,food,walls) < closestFoodDist):
#         closestFoodDist = mazeDistance(pos,food,walls)
#   if(closestFoodDist < 0):
#     foodEvaluation = 0
#   else:
#     foodEvaluation = -0.25 * closestFoodDist
#   #Now mind the capsule and the ghosts
#   for ghostState in ghostStates:
#     ghostPos = ghostState.getPosition()
#     if(ghostState.scaredTimer <= 0):
#       if(mazeDistance(pos, ghostPos,walls) <= 3):
#         ghostEvaluation -= (3 - mazeDistance(pos,ghostPos,walls)) ** 4
#     else:
#       capsuleEvaluation += 15
#   return  foodEvaluation + ghostEvaluation + capsuleEvaluation + scoreEvaluationFunction(currentGameState) 
def betterEvaluationFunction(currentGameState):
  pos= currentGameState.getPacmanPosition()
  foodList = currentGameState.getFood().asList()
  ghostStates = currentGameState.getGhostStates()
  walls = currentGameState.getWalls()
  closestFoodDist = -1
  ghostEvaluation = 0
  capsuleEvaluation = 0
  #Loop throught foodList
  for food in foodList:
    if(closestFoodDist < 0 or manhattanDistance(pos,food) < closestFoodDist):
        closestFoodDist = manhattanDistance(pos,food)
  if(closestFoodDist < 0):
    foodEvaluation = 0
  else:
    foodEvaluation = -0.25 * closestFoodDist
  #Now mind the capsule and the ghosts
  for ghostState in ghostStates:
    ghostPos = ghostState.getPosition()
    if(ghostState.scaredTimer <= 0):
      if(manhattanDistance(pos,ghostPos) <= 3):
        ghostEvaluation -= (3 - manhattanDistance(pos,ghostPos)) ** 4
    else:
      capsuleEvaluation += 15
  return  foodEvaluation + ghostEvaluation + capsuleEvaluation + scoreEvaluationFunction(currentGameState) 

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def mazeDistance(p1, p2, walls):
  from util import Queue
  q = Queue()
  visited = set()
  q.push((p1, 0))
  while not q.isEmpty():
    curNode = q.pop()
    if(curNode[0] == p2):
      return curNode[1]
    successors = getRealSuccessors(curNode[0], walls)
    for successor in successors:
      if successor not in visited:
        #push next node
        q.push((successor, curNode[1] + 1))
        visited.add(successor)
  #closing up
  return None

def getRealSuccessors(pos, walls):
  successors = []
  x = pos[0]
  y = pos[1]

  if x >= 1:
    if not walls[x-1][y]:
      successors.append((x-1,y-1))
  if y >= 1:
    if not walls[x-1][y-1]:
      successors.append((x-1,y-1))

  if x < walls.width-1:
    if not walls[x+1][y]:
      successors.append((x+1,y))
    if y >= 1:
      if not walls[x+1][y-1]:
        successors.append((x+1,y-1))
      if not walls[x][y-1]:
        successors.append((x,y-1))
  if y < walls.height-1:
    if not walls[x-1][y+1]:
      successors.append((x-1,y-1))
    if x < walls.width-1:
      if not walls[x+1][y+1]:
        successors.append((x+1,y+1))
      if not walls[x][y+1]:
        successors.append((x,y+1))

  return successors
def manhattanDistance(p1,p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
