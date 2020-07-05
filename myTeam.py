# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.treeDepth = 3

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        # foodLeft = len(self.getFood(gameState).asList())

        # if foodLeft <= 2:
        #     bestDist = 9999
        #     for action in actions:
        #         successor = self.getSuccessor(gameState, action)
        #         pos2 = successor.getAgentPosition(self.index)
        #         dist = self.getMazeDistance(self.start, pos2)
        #         if dist < bestDist:
        #             bestAction = action
        #             bestDist = dist
        #     return bestAction

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        return {'successorScore': 1.0}


class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    # def getAction(self, gameState):
    #     opponents = {}
    #     for enemy in self.getOpponents(gameState):
    #         opponents[enemy] = gameState.getAgentState(enemy).getPosition()
    #     directions = {'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0)}
    #     ghost_weights = {'distance': 5, 'scared': 5}
    #
    #     def get_ghost_actions(current_pos):
    #         walls = gameState.getWalls().asList()
    #
    #         max_x = max([wall[0] for wall in walls])
    #         max_y = max([wall[1] for wall in walls])
    #
    #         actions = []
    #         for direction in directions:
    #             action = directions[direction]
    #             new_pos = (int(current_pos[0] + action[0]), int(current_pos[1] + action[1]))
    #             if new_pos not in walls:
    #                 if (1 <= new_pos[0] < max_x) and (1 <= new_pos[1] < max_y):
    #                     actions.append(direction.title())
    #
    #         return actions
    #
    #     def get_new_position(current_pos, action):
    #         act = directions[action.lower()]
    #         return current_pos[0] + act[0], current_pos[1] + act[1]
    #
    #     def expectation(gamestate, position, legalActions):
    #         ghost_dict = {}
    #         for action in legalActions:
    #             newPos = get_new_position(position, action)
    #             ghost_dict[action] = self.getMazeDistance(position, newPos) * ghost_weights['distance']
    #         min_action = min(ghost_dict)
    #         for action in ghost_dict:
    #             if ghost_dict[action] == min_action:
    #                 ghost_dict[action] = .8
    #             else:
    #                 ghost_dict[action] = .2 / len(legalActions)
    #         return ghost_dict
    #
    #     def ghost_eval(gamestate, opponents, opponent):
    #         newPos = opponents[opponent]
    #         enemy = gamestate.getAgentState(opponent)
    #         myPos = gamestate.getAgentState(self.index).getPosition()
    #
    #         if enemy.scaredTimer != 0:
    #             distance = -self.getMazeDistance(myPos, newPos) * ghost_weights['distance']
    #         else:
    #             distance = self.getMazeDistance(myPos, newPos) * ghost_weights['distance']
    #
    #         return distance
    #
    #     def minimax(gamestate, depth, agent, opponents, alpha=-float('inf'), beta=float('inf')):
    #         """
    #         """
    #         # Get legal moves per agent
    #         legalActions = [action for action in gamestate.getLegalActions(self.index) if action != Directions.STOP]
    #
    #         # Generate optimal action recursively
    #         actions = {}
    #         if agent == self.index:
    #             max_value = -float('inf')
    #             for action in legalActions:
    #                 eval = self.evaluate(gamestate, action)
    #                 if depth == self.treeDepth:
    #                     value = eval
    #                 else:
    #                     value = eval + minimax(self.getSuccessor(gamestate, action), depth, agent + 1, opponents, alpha,
    #                                            beta)
    #                 max_value = max(max_value, value)
    #                 if beta < max_value:
    #                     return max_value
    #                 else:
    #                     alpha = max(alpha, max_value)
    #                 if depth == 1:
    #                     actions[value] = action
    #             if depth == 1:
    #                 return actions[max_value]
    #             return max_value
    #         else:
    #             min_value = float('inf')
    #             for opponent in opponents:
    #                 if gamestate.getAgentState(opponent).getPosition() is not None:
    #                     legalActions = get_ghost_actions(opponents[opponent])
    #                     expectations = expectation(gamestate, opponents[opponent], legalActions)
    #                     for action in legalActions:
    #                         new_opponents = opponents.copy()
    #                         new_opponents[opponent] = get_new_position(opponents[opponent], action)
    #                         ghost_val = ghost_eval(gamestate, new_opponents, opponent) * expectations[action]
    #                         value = ghost_val + minimax(gamestate, depth + 1, self.index, new_opponents, alpha, beta)
    #                         min_value = min(min_value, value)
    #                         if min_value < alpha:
    #                             return min_value
    #                         else:
    #                             beta = min(beta, min_value)
    #             if min_value == float('inf'):
    #                 return 0
    #             return min_value
    #
    #     return minimax(gameState, 1, self.index, opponents)

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        foodList = self.getFood(successor).asList()
        features['successorScore'] = self.getScore(successor)

        myPos = successor.getAgentState(self.index).getPosition()
        myState = successor.getAgentState(self.index)

        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]

        if len(ghosts) > 0:
            regular_ghosts = [ghost for ghost in ghosts if ghost.scaredTimer == 0]
            scared_ghosts = [ghost for ghost in ghosts if ghost.scaredTimer > 0]
            regular_value = 0
            if len(regular_ghosts) > 0:
                regular_value = min([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in regular_ghosts])
                if regular_value <= 1:
                    regular_value = -float('inf')
            if len(scared_ghosts) > 0:
                scared_value = min([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in scared_ghosts])
                if scared_value == 0:
                    scared_value = -10
                features['ghostScared'] = scared_value
            features['distanceToGhost'] = regular_value
            if regular_value < 6 and 12 <= myPos[0] <= 15:
                features['otherWay'] = myPos[0]

        if gameState.getAgentState(self.index).numCarrying == myState.numCarrying > 0:
            start_distance = self.getMazeDistance((1, 1) if self.red else (30, 15), myPos) - 20
            features['goStart'] = start_distance * myState.numCarrying

        if action == Directions.STOP:
            features['stop'] = 1

        if len(foodList) > 0:  # This should always be True,  but better safe than sorry
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            features['numCarrying'] = myState.numCarrying

        # Compute distance to the capsules
        capsules = self.getCapsules(gameState)
        if len(capsules) > 0:
            min_distance = min([self.getMazeDistance(myPos, capsule) for capsule in capsules])
            features['distanceToCapsules'] = -100 if min_distance == 0 else min_distance
        x = features * self.getWeights(gameState, action)
        return features

    def getWeights(self, gameState, action):
        return {'successorScore': 100, 'distanceToFood': -1, 'goStart': -2, 'distanceToGhost': 1, 'ghostScared': -1.5, 'otherWay': -1, 'numCarrying': 10, 'foodRemaining': -1, 'stop': -100, 'distanceToCapsules': -0.5}


class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see and their distance to the food we are defending
        if not myState.isPacman and myState.scaredTimer > 0:
            # Compute distance to the nearest food
            foodList = self.getFood(successor).asList()
            if len(foodList) > 0:  # This should always be True,  but better safe than sorry
                minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
                features['distanceToFood'] = minDistance + 1
            features['defenseFoodDistance'] = 0.

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dist = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
            if dist == 0:
                dist = -100
            features['invaderDistance'] = dist

        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'numInvaders': -1000, 'onDefense': 100, 'distanceToFood': -1, 'defenseFoodDistance': -8, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
