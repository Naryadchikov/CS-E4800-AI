# POMDP
states = [0, 1]
actions = {"a1", "a2"}
observations = {"o1", "o2"}


# Dictionary for transition probabilities
P = {
    (0, "a1", 0): 0.2,
    (0, "a1", 1): 0.8,
    (0, "a2", 0): 0.0,
    (0, "a2", 1): 1.0,
    (1, "a1", 0): 0.7,
    (1, "a1", 1): 0.3,
    (1, "a2", 0): 0.6,
    (1, "a2", 1): 0.4
}


# Dictionary for rewards
R = {
    (0, "a1", 0): 1.0,
    (0, "a1", 1): 1.0,
    (0, "a2", 0): 2.0,
    (0, "a2", 1): 2.0,
    (1, "a1", 0): 2.0,
    (1, "a1", 1): 2.0,
    (1, "a2", 0): -1.0,
    (1, "a2", 1): -1.0
}


# Dictionary for observation probabilities
O = {
    ("a1", 0, "o1"): 0.0,
    ("a1", 0, "o2"): 1.0,
    ("a1", 1, "o1"): 0.9,
    ("a1", 1, "o2"): 0.1,
    ("a2", 0, "o1"): 0.0,
    ("a2", 0, "o2"): 1.0,
    ("a2", 1, "o1"): 0.9,
    ("a2", 1, "o2"): 0.1
}

B0 = (0.8, 0.2)
gamma = 0.9
V0 = [(1.0, 2.5), (1.0, 0.5)]


# Value of a belief state w.r.t. a value vector
def Bvalue(B, v):
    """
    Compute scalar product of B and v.

    Parameters
    ----------
    B : tuple or list of float (length 2)
    v : tuple or list of float (length 2)

    Note, above assumes that the global `states` are 0,1.

    Returns
    -------
    float
       scalar product.
    """
    sum = 0.0
    for s in states:  # Note: states global.
        sum = sum + B[s] * v[s]
    return sum


# Create value vector based on alpha, a and o
def value(alpha, a, o):
    """
    Compute the value of all state (in global `states`).
    Corresponds to the function $values_{a,o}^{\alpha}(s)$ 
    on MyCourses 8.3 (section 'Point-based POMDP algorithms')
    applied to all states.

    Parameters
    ----------
    alpha : list of float (length 2)
       Backup values for every state.
    a : str
       Action.
    o : str
       Observation

    Returns
    -------
    list of float
       value for every state
    """

    # Helper function, computes value for a specific state.
    def stateValue(s):
        sum = 0.0
        for s1 in states:
            sum = sum + P[(s, a, s1)] * (R[(s, a, s1)] + gamma * alpha[s1])
        return O[(a, s, o)] * sum
    return [stateValue(s) for s in states]


# Value vector for best policy tree with action a in root
# and immediate subtrees those with value vectors in V
def backupA(a, B, V):
    """
    Perform backup operation for all states given some action.

    Corresponds to the function $backup_{a}(B,V)$ 
    on MyCourses 8.3 (section 'Point-based POMDP algorithms')
    applied to all states.
    (Middle equation.)

    Parameters
    ----------
    a : str
       Action.
    B : tuple or list of float (length 2)
       Belief state (One value for each state in `states`).
    V : list of tuples (of float)
       Collection of value vectors.

    Returns
    -------
    list of float
       One value per state in `states`, and the value is computed using the
       sum over observations as described by the equation on MyCourses 8.3
       ('Point-based POMDP algorithms').
    """
    vsum = [0.0 for s in states]

    for o in observations:
        maxProduct = 0.0

        for alpha in V:
            alpha_0 = value(alpha, a, o)
            result = Bvalue(B, alpha_0)

            if result > maxProduct:
                maxProduct = result
                argmax_alpha_0 = alpha_0

        for i in range(len(states)):
            vsum[i] = vsum[i] + argmax_alpha_0[i]

    return vsum


# Value vector for best policy tree that has
# immediate subtrees those with value vectors in V
def backup(B, V):
    """
    Perform backup operation for all states.

    Corresponds to the function $backup(B,V)$ 
    on MyCourses 8.3 (section 'Point-based POMDP algorithms')
    applied to all states.

    Parameters
    ----------
    B : tuple of float (length 2)
       Belief state (One value for each state in `states`).
    V : list of tuples (of float)
       Collection of value vectors.

    Returns
    -------
    list of float
       One value per state in `states`, and the value is the
       argument maximizing the dot product of belief and backup
       vector over all possible actions.
    """
    hasBest = False
    for a in actions:
        alpha = backupA(a, B, V)
        if not hasBest or Bvalue(B, alpha) > bestValue:
            bestValue = Bvalue(B, alpha)
            best = alpha
            hasBest = True
    if not hasBest:
        print("Error")
    return best


# Test case
print("This is a TEST RESULT, which should be [3.98,0.3374]: ")
print(backup(B0, [(0.8, 2.2), (1.5, 1.5)]))

# Answer to the exercise
print("EXERCISE ANSWER:")
print(backup([0.3, 0.7], V0))
