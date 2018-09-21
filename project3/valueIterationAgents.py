# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):

  def __init__(self, mdp, discount = 0.9, iterations = 100):
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0

    for i in range(0,iterations):
      storage = self.values.copy()
      for state in self.mdp.getStates():
        Vmax = None
        for action in self.mdp.getPossibleActions(state):
          totalR = 0
          for (next_state,prob) in self.mdp.getTransitionStatesAndProbs(state,action):
            totalR += prob * (self.mdp.getReward(state,action,next_state)+self.discount*storage[next_state])
          Vmax=max(totalR,Vmax)
        if self.mdp.isTerminal(state):
          self.values[state] = 0
        else:
          self.values[state] = Vmax

    
  def getValue(self, state):
    return self.values[state]


  def getQValue(self, state, action):
    Q = 0
    for transition in self.mdp.getTransitionStatesAndProbs(state,action):
      Q += transition[1]*(self.mdp.getReward(state,action,transition[0])+self.discount*self.values[transition[0]])
    return Q


  def getPolicy(self, state):
    if len(self.mdp.getPossibleActions(state))>0:
      return max([(self.getQValue(state,action),action) for action in self.mdp.getPossibleActions(state)])[1]
    else:
      return None

  def getAction(self, state):
    return self.getPolicy(state)
  
