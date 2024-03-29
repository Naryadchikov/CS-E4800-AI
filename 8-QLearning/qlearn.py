
import random

from qlearnexamples import *

# The Q-Learning Algorithm

# EXERCISE ASSIGNMENT:
# Implement the Q-learning algorithm for MDPs.
# The Q-values are represented as a Python dictionary Q[s, a],
# which is a mapping from the state indices s=0..stateMax to
# and actions a to the Q-values.
#
# Choice of actions can be completely random, or, if you are interested,
# you could implement some scheme that prefers better actions, e.g.
# based on Multi-arm Bandit problems (find more about these in the literature:
# this is an optional addition to the programming assignment.)

# OPTIONAL FUNCTIONS:
# You can implement and use the auxiliary functions bestActionFor and execute
# if you want, as auxiliary functions for Qlearning and makePolicy and makeValues.


# bestActionFor chooses the best action for 'state', given Q values
# Tip: You may return -1 if no action is applicable.
def bestActionFor(mdp, state, Q):
    """
    Find the best available action in `Q` given `state`.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    state : int
       In range [0, mdp.stateMax] (inclusive)
    Q : dict {(state,action) : float}
       Q dictionary mapping from state,action pair to score.

    Returns
    -------
    int
       Applicable action for `state` yielding the maximum score.
    """
    actions = mdp.applicableActions(state)
    maxValue = 0
    bestAction = -1

    for action in actions:
        value = Q[(state, action)]

        if (value > maxValue):
            maxValue = value
            bestAction = action

    return bestAction


# valueOfBestAction gives the value of best action for 'state'
# Tip: You may, if needed, return a dummy value of 0 or -1 if there are no Q values for the state/best action.
def valueOfBestAction(mdp, state, Q):
    """
    Return value of best available action in `Q` given `state`.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    state : int
       In range [0, mdp.stateMax] (inclusive)
    Q : dict {(state, action) : float}
       Q dictionary mapping from state, action pair to score.

    Returns
    -------
    float
       Maximum Q-value for any applicable action in `state`.
    """
    maxValue = -1.0
    bestAction = bestActionFor(mdp, state, Q)

    if bestAction != -1:
        maxValue = Q[(state, bestAction)]

    return maxValue


# 'execute' randomly chooses a successor state for state s w.r.t. action a.
# The probability with which is given successor is chosen must respect
# to the probability given by mdp.successors(s, a).
# execute should return a tuple (s2, r), where s2 is the successor state and r is
# the reward that was obtained.
def execute(mdp, s, a):
    """
    Randomly choose a successor state of state `s` given action `a`.

    The probability of the successor state respects the probability of the
    Markov Decision Process.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
    s : int
       Start/current state as integer in range [0, mdp.stateMax] (inclusive)
    a : int
       Action as int in GridMDP.ACTIONS (`[1, 2, 3, 4]` in effect)

    Returns
    -------
    pair of (int,float)
       First element of pair is the successor state as int in [0, mdp.stateMax] (inclusive).
       Second element is the associated reward.
    """
    successors = mdp.successors(s, a)
    probabilityList = [p for s, p, r in successors]

    chosenSuccessor = random.choices(successors, probabilityList)[0]

    return (chosenSuccessor[0], chosenSuccessor[2])


# OBLIGATORY FUNCTION:
# Qlearning returns the Q-value function after performing the given
# number of iterations i.e. Q-value updates.
def Qlearning(mdp, gamma, lambd, iterations):
    """
    Perform the Q-learning algorithm on Markov Decision Process."

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    gamma : float in [0, 1]
       Discount factor.
    lambd : float in [0, 1]
       Learning rate.
    iterations : int > 0
       Number of iterations to perform.

    Returns
    -------
    dict {(state,action) : float}
       Q-values mapping from state (int in [0, mdp.stateMax] inclusive), action
       (int in mdp.ACTIONS [s.t. the action is applicable in state)) pair to a the q-value.
    """

    # The Q-values are a real-valued dictionary Q[s,a] where s is a state and a is an action.
    Q = dict()

    for state in range(mdp.stateMax + 1):
        actions = mdp.applicableActions(state)

        for action in actions:
            Q[(state, action)] = 0

    s = 0

    for i in range(iterations):
        a = random.choice(mdp.applicableActions(s))
        stateRewardTuple = execute(mdp, s, a)
        s2 = stateRewardTuple[0]
        r = stateRewardTuple[1]

        Q[(s, a)] = (1.0 - lambd) * Q[(s, a)] + lambd * \
            (r + gamma * valueOfBestAction(mdp, s2, Q))

        s = s2

    return Q


# OBLIGATORY FUNCTION:
# makePolicy constructs a policy, i.e. a mapping from state to actions,
# given a Q-value function as produced by Qlearning.
def makePolicy(mdp, Q):
    """
    Get policy for states in `mdp` given Q-values `Q`.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    Q : dict {(state,action) : float}
       As returned by function `Qlearning`.

    Returns
    -------
    dict {state : action}
       Policy as a dict, mapping from every state of `mdp` 
       (int in [0, mdp.stateMax] inclusive) to the best choice of action 
       (int in mdp.ACTIONS) in that state.
    """
    # A policy is an action-valued dictionary P[s] where s is a state
    P = dict()

    for i in range(mdp.stateMax + 1):
        P[i] = bestActionFor(mdp, i, Q)

    return P


# OBLIGATORY FUNCTION:
# makeValues constructs the value function, i.e. a mapping from states to values,
# given a Q-value function as produced by Qlearning.
# Note: It is expected that this function returns a dictionary with with keys
# for every state in mdp. However, it may be that your Q lacks values for some
# state/action combination. For these, you can use a dummy value of -1.
def makeValues(mdp, Q):
    """
    Get best values for states in `mdp` given Q-values `Q`.

    Parameters
    ----------
    mdp : GridMDP object (see `qlearnexamples.py`)
       Markov Decision Process
    Q : dict {(state,action) : float}
       As returned by function `Qlearning`.

    Returns
    -------
    dict {state : float}
       Values of best action in state for every state of `mdp` 
       (int in [0, mdp.stateMax] inclusive) to the Q-value of the
       best action in that state.
    """
    # A value function is a real-valued dictionary V[s] where s is a state
    V = dict()

    for i in range(mdp.stateMax + 1):
        V[i] = valueOfBestAction(mdp, i, Q)

    return V
