# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  
  def __init__(self, **args):
    ReinforcementAgent.__init__(self, **args)
    self.values=util.Counter()

  def getQValue(self, state, action):
    return self.values[(state,action)]

  def getValue(self, state):
    actions = self.getLegalActions(state)
    if len(actions)>0:
      return max([self.getQValue(state,action) for action in actions])
    else:
      return 0.0

  def bestQAction(self,state):
    actions = self.getLegalActions(state)
    if len(actions) == 0:
      return None
    else:
      bestQ = max([(self.getQValue(state,action),action) for action in actions])[0]
    return random.choice([a for (q,a) in [(self.getQValue(state,action),action) for action in actions] if q == bestQ])

  def getPolicy(self, state):
    return self.bestQAction(state)
    
  def getAction(self, state):
    actions = self.getLegalActions(state)
    if len(actions) == 0:
      return None
    else:
      if util.flipCoin(self.epsilon):
        return random.choice(actions)
      else:
        return self.getPolicy(state)


  def update(self, state, action, nextState, reward):
    self.values[(state,action)]=(1-self.alpha)*self.values[(state,action)]+self.alpha*(reward+ self.getValue(nextState)*self.discount)


class PacmanQAgent(QLearningAgent):

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):

    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    self.weights = util.Counter()

  def getQValue(self, state, action):
    features=self.featExtractor.getFeatures(state,action)
    ans = 0
    for f in features:
      ans += features[f]*self.weights[f]
    return ans

  def update(self, state, action, nextState, reward):
    features=self.featExtractor.getFeatures(state,action)
    for f in features:
      self.weights[f] += self.alpha * features[f] * (reward+self.discount*self.getValue(nextState))-self.getQValue(state,action)



  def final(self, state):
    PacmanQAgent.final(self, state)
    if self.episodesSoFar == self.numTraining:
      pass
