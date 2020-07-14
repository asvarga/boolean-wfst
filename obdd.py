
import pynini
import os
import itertools as it
from functools import *
from random import random

####

dir_path = os.path.dirname(os.path.realpath(__file__))

ST = pynini.SymbolTable.read_text(f"{dir_path}/syms.txt")

def draw(x, opt=True):
    if opt: x.optimize()
    x.draw(f"{dir_path}/obdd.dot", ST, ST, 
        portrait=True, 
        acceptor=True)

####

# constants
T = pynini.acceptor("T", token_type=ST)
F = pynini.acceptor("F", token_type=ST)
ANY = T|F
TAUT = (T|F).closure()  # sigma-star
ABSURD = T-T

# boolean operators
def AND(*args): return reduce(pynini.intersect, map(v, args), TAUT)
def OR(*args): return reduce(pynini.union, map(v, args), ABSURD)
def NOT(x): return TAUT-v(x)
def IMP(x, y): return OR(NOT(x), y)

# boolean variables
V = [TAUT, T+TAUT]
def v(i): 
    if not isinstance(i, int): return i
    if i < 0: return NOT(v(-i))
    if i >= len(V): V.append(ANY+v(i-1))
    return V[i]

####

# draw(AND(-1, IMP(2, 3), IMP(3, 4), IMP(4, 5)))

# generate a random DNF on n vars
def randDNF(n):
    ret = ABSURD
    for tup in it.product([-1, 1], repeat=n):
        if random() < 0.5:  # select random subset of conjunctions
            conj = AND(*[v((i+1)*b) for i,b in enumerate(tup)])
            ret = OR(ret, conj).optimize()  # optimize as we go
    return ret

draw(randDNF(5))

