#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

# NOTE: Copy this file to 'Astar.py' before modifying.
#
# NOTE: It is recommended to only modify the block of the code
# indicated by "### Insert your code here ###"
#
# NOTE: Do not change the name of the class or the methods, as
# the automated grader relies on the names.


#
# Functions in classes representing state space search problems:
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns [(a1,s1,c1),...,(aN,sN,cN)] where each si is
#               the successor state when action called ai is taken,
#               and ci is the associated cost.
#               Here the name ai of an action is a string.

import time
import queue
import itertools


# ASTAR has to return a pair (plan,cost)
# where
#   plan is the sequence of states on an optimal path to goals,
#   cost is the sum of the costs of actions on that path.
# You can assume the h-function to be monotone.


def ASTAR(initialstate, goaltest, h):
    starttime = time.process_time()

    if goaltest(initialstate):
        return [initialstate], 0

    predecessor = dict()
    predecessor[initialstate] = None

    openSet = set([initialstate])
    closedSet = set()

    g = dict()
    g[initialstate] = 0

    isGoalFound = False
    goalState = None

    while len(openSet) != 0:
        currentState = getLowest(openSet, g, h)

        if (isGoalFound):
            if (g[currentState] + h(currentState) >= g[goalState]):
                break

        openSet.remove(currentState)
        closedSet.add(currentState)

        for aname, nextState, cost in currentState.successors():
            nextCost = g[currentState] + cost

            if not isGoalFound and goaltest(nextState):
                goalState = nextState
                isGoalFound = True

            if nextState not in g or nextCost < g[nextState]:
                predecessor[nextState] = currentState
                g[nextState] = nextCost

                if nextState not in closedSet:
                    openSet.add(nextState)

    if (isGoalFound):
        plan = []
        state = goalState

        while predecessor[state] is not None:
            plan.append(state)
            state = predecessor[state]

        plan.append(initialstate)
        plan.reverse()

        endtime = time.process_time()
        print("Elapsed time: ", str(endtime - starttime))

        return plan, g[goalState]

    return [], 0


def getLowest(openSet, g, h):
    lowestScore = float("inf")
    lowestState = None

    for state in openSet:
        f = g[state] + h(state)

        if f < lowestScore:
            lowestScore = f
            lowestState = state

    return lowestState
