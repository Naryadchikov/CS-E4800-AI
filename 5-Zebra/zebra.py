#!/usr/bin/python3

import itertools
from logic2 import ATOM, AND, OR, NOT, FALSE, TRUE

############################################
# Predicates

# This is a class for the most important form
# of atomic formulas P(t1,...,tn). We allow
# numeric terms here, but everything numeric
# gets evaluated and the resulting numbers get
# in the end treated as strings.


class Pred:
    def __init__(self, P, terms):
        self.P = P
        self.terms = terms

    def __repr__(self):
        return self.P + "_" + ('_'.join([str(t) for t in self.terms]))

    def subst(self, v, expr):  # substitution while in schematic form
        def ssubst(s, v, expr):
            if isinstance(s, str):
                if s == v:
                    return str(expr)
                else:
                    return s
            else:
                return s.subst(v, expr)
        return Pred(self.P, [ssubst(s, v, expr) for s in self.terms])

    def toAtom(self):  # generate the string representation of the atomic formula
        def evalterm(t):
            if isinstance(t, str):  # Term is a string
                return t
            else:  # Term is an integer expression
                return t.evalZ()
        terms = [evalterm(t) for t in self.terms]
        return ATOM(self.P + "_" + ('_'.join([str(evalterm(t)) for t in self.terms])))

###################################################
# Integer terms / expressions

# The 'subst' method is used for replacing variable
# values by integer-valued expressions.
# The 'evalZ' method is used for calculating the
# value of an integer-valued term _after_ all
# quantification has been eliminated, so that no
# variables remain in the terms. Terms get evaluated
# in the 'toAtom' method for the atomic formulas ZEq,
# which always get replaced by TRUE or FALSE
# depending on the values on the two sides of
# the equality (as obtained by 'evalZ'.)

# Integer constants


class ZConst:
    def __init__(self, c):
        self.value = c

    def __repr__(self):
        return str(self.value)

    def subst(self, v, expr):
        return self  # ZConst(self.value)

    def evalZ(self):
        return self.value


# Integer variables


class ZVar:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def subst(self, v, expr):
        if v == self.name:
            return expr
        else:
            return self  # ZVar(self.name)

    def evalZ(self):
        raise Exception("Cannot evaluate the value of a variable")


# Integer Plus


class ZPlus:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return str(self.e1) + "+" + str(self.e2)

    def subst(self, v, expr):
        return ZPlus(self.e1.subst(v, expr),
                     self.e2.subst(v, expr))

    def evalZ(self):
        return self.e1.evalZ() + self.e2.evalZ()


#############################################
# Integer inequalities


class ZEq:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        return str(self.e1) + " = " + str(self.e2)

    def toAtom(self):
        if self.e1.evalZ() == self.e2.evalZ():
            return TRUE()
        else:
            return FALSE()

    def subst(self, v, expr):
        return ZEq(self.e1.subst(v, expr),
                   self.e2.subst(v, expr))

####################################################################
# Reduction of forall, forsome, exactlyone to propositional logic
####################################################################

######### Cardinality constraints #########


def atLeast1(fmas):
    return OR(fmas)


def allpairs(lst):
    return [(lst[i], lst[j]) for i in range(0, len(lst)) for j in range(i+1, len(lst))]


def atMost1(fmas):
    return AND([NOT(AND([f1, f2])) for (f1, f2) in allpairs(fmas)])


def exactly1(fmas):
    return AND([atMost1(fmas), atLeast1(fmas)])

# substitute returns every occurrences of variable 'v' in atoms in 'fma'
# by 'val'.


def substitute(v, val, fma):
    def subs(e):
        return ATOM(e.subst(v, val))
    return fma.map(subs)


def forall(v, D, fma):
    return AND([substitute(v, val, fma) for val in D])


def forsome(v, D, fma):
    return OR([substitute(v, val, fma) for val in D])


def exactlyone(v, D, fma):
    fmas = [substitute(v, val, fma) for val in D]
    return AND([atLeast1(fmas), atMost1(fmas)])

# Notice that above the correct handling of scoping is based on expressing
# the quantifers as regular Python function so that Python's evaluation order
# takes care of the scoping rules: innermost quantifiers get eliminated first

########################################################################
###################### THE ZEBRA PUZZLE ################################
########################################################################

# / The Gentlemen


M = {"Eng", "Spa", "Ukr", "Nor", "Jap"}

# The 5 cigarette brands

C = {"OldGold", "Kools", "Chesterfields", "LuckyStrike", "Parliaments"}

# The 5 colors of houses

P = {"Red", "Green", "Ivory", "Yellow", "Blue"}

# The 5 pets

A = {"Dog", "Snails", "Fox", "Horse", "Zebra"}

# The 5 drinks

D = {"Coffee", "Tea", "Milk", "OrangeJuice", "Water"}

# Houses numbered from 1 to 5 so that we can talk about neighboring houses

H = {ZConst(1), ZConst(2), ZConst(3), ZConst(4), ZConst(5)}
H4 = {ZConst(1), ZConst(2), ZConst(3), ZConst(4)}

# variables

i = "i"
j = "j"
k = "k"
l = "l"
x = "x"
m = "m"
c = "c"
z = "z"
h = "h"
p = "p"
d = "d"

# predicates


def Smokes(t1, t2):
    return ATOM(Pred("Smokes", [t1, t2]))


def Pet(t1, t2):
    return ATOM(Pred("Pet", [t1, t2]))


def Color(t1, t2):
    return ATOM(Pred("Color", [t1, t2]))


def Drinks(t1, t2):
    return ATOM(Pred("Drinks", [t1, t2]))


def LivesIn(t1, t2):
    return ATOM(Pred("LivesIn", [t1, t2]))


def EQ(t1, t2):
    return ATOM(ZEq(t1, t2))

########################################################################
# All formulas representing the Zebra Puzzle

# What is in 'formulas' is what would be produced by the front-end of
# a system that takes in a high-level specification language based on
# the predicate logic, after parsing, typing and disambiguation.

# Background assumptions about uniqueness:
# Everybody smokes exactly one cigarette.
# Every cigarette is smoked by exactly one person.
# Same with pets, drinks, homes, and colors of houses.


formulas = {

    forall(m, M, exactlyone(c, C, Smokes(m, c))),
    forall(c, C, exactlyone(m, M, Smokes(m, c))),

    forall(m, M, exactlyone(x, A, Pet(m, x))),
    forall(z, A, exactlyone(m, M, Pet(m, z))),

    forall(h, H, exactlyone(p, P, Color(h, p))),
    forall(p, P, exactlyone(h, H, Color(h, p))),

    forall(m, M, exactlyone(d, D, Drinks(m, d))),
    forall(d, D, exactlyone(m, M, Drinks(m, d))),

    forall(m, M, exactlyone(h, H, LivesIn(m, h))),
    forall(h, H, exactlyone(m, M, LivesIn(m, h))),

    # The remaining formulas are the explicitly stated parts of the puzzle.

    # The Englishman lives in the red house.

    forsome(i, H, AND([LivesIn("Eng", i), Color(i, "Red")])),

    # The Spaniard owns the dog.

    Pet("Spa", "Dog"),

    # Coffee is drunk in the green house.

    forsome(i, M, forsome(
        j, H, AND([LivesIn(i, j), Drinks(i, "Coffee"), Color(j, "Green")]))),

    # The Ukrainian drinks tea.

    Drinks("Ukr", "Tea"),

    # The green house is immediately to the right of the ivory house.

    forsome(i, H4, AND([Color(i, "Ivory"), Color(
        ZPlus(ZVar(i), ZConst(1)), "Green")])),

    # The Old Gold smoker owns snails.

    forsome(i, M, AND([Smokes(i, "OldGold"), Pet(i, "Snails")])),

    # Kools are smoked in the yellow house.

    forsome(i, M, forsome(
        j, H, AND([LivesIn(i, j), Color(j, "Yellow"), Smokes(i, "Kools")]))),

    # Milk is drunk in the middle house.

    forsome(i, M, AND([LivesIn(i, ZConst(3)), Drinks(i, "Milk")])),

    # The Norwegian lives in the first house.

    LivesIn("Nor", ZConst(1)),

    # The man who smokes Chesterfields lives in the house next to the man with the fox.

    forsome(i, M,
            forsome(j, M,
                    forsome(k, H,
                            forsome(l, H, AND([Smokes(i, "Chesterfields"),
                                               Pet(j, "Fox"),
                                               LivesIn(i, k),
                                               LivesIn(j, l),
                                               OR([EQ(ZVar(k), ZPlus(ZVar(l), ZConst(1))),
                                                   EQ(ZVar(l), ZPlus(ZVar(k), ZConst(1)))])]))))),

    # Kools are smoked in the house next to the house where the horse is kept.

    forsome(i, M,
            forsome(j, M,
                    forsome(k, H,
                            forsome(l, H, AND([Smokes(i, "Kools"),
                                               Pet(j, "Horse"),
                                               LivesIn(i, k),
                                               LivesIn(j, l),
                                               OR([EQ(ZVar(k), ZPlus(ZVar(l), ZConst(1))),
                                                   EQ(ZVar(l), ZPlus(ZVar(k), ZConst(1)))])]))))),

    # The Lucky Strike smoker drinks orange juice.

    forsome(i, M, AND([Smokes(i, "LuckyStrike"), Drinks(i, "OrangeJuice")])),

    # The Japanese smokes Parliaments.

    Smokes("Jap", "Parliaments"),

    # The Norwegian lives next to the blue house.

    forsome(i, H, forsome(j, H, AND([LivesIn("Nor", i),
                                     Color(j, "Blue"),
                                     OR([EQ(ZVar(i), ZPlus(ZVar(j), ZConst(1))),
                                         EQ(ZVar(j), ZPlus(ZVar(i), ZConst(1)))])])))
}

#############################################################
# Transform all atomic formulas to strings
#
# In 'formulas' above, the atomic formulas are either P(a,b,c) or
# integer inequalities. The integer inequalities have to be
# evaluated and replaced by True or False, and P(a,b,c)
# have to be turned into string atoms. This is done by 'eval'.


def formAtoms(f):
    def evalAtom(a):
        return a.toAtom()
    return f.map(evalAtom)

# For cosmetic reasons we want to split ANDs to separate formulas


def concatlists(ll):
    return list(itertools.chain.from_iterable(ll))


def splitAnds(f):
    if isinstance(f, AND):
        return concatlists([splitAnds(g) for g in f.subformulas])
    else:
        return [f]

##############################################################
# Generate output in the SMTLIB format for MathSAT, Z3 etc.


pformulas0 = [formAtoms(f) for f in formulas]
pformula = AND(pformulas0)
allvars = pformula.vars()
pformulas = concatlists([splitAnds(f) for f in pformulas0])
for v in allvars:
    print("(declare-fun " + v + " () Bool)")
for f in pformulas:
    print("(assert " + str(f) + ")")
print("(check-sat)")
print("(exit)")
