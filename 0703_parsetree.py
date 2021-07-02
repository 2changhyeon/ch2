# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 00:58:41 2021

@author: PC
"""
import nltk
from nltk.parse import RecursiveDescentParser
from nltk import Nonterminal, nonterminals, Production, CFG
nt1 = Nonterminal('NP')
nt2 = Nonterminal('VP')
S, NP, VP, PP = nonterminals('S, NP, VP, PP')
N, V, P, DT = nonterminals('N, V, P, DT')

prod1 = Production(S, [NP, VP])
prod2 = Production(NP, [DT, NP])

prod1.rhs()
prod1.lhs()

grammar = CFG.fromstring("""
                         S -> NP VP
                         PP -> P NP
                         NP -> 'the' N | N PP | 'the' N PP
                         VP -> V NP | V PP | V NP PP
                         N -> 'cat'
                         N -> 'dog'
                         N -> 'rug'
                         V -> 'chased'
                         V -> 'sat'
                         P -> 'in'
                         P -> 'on'
                         """)

rd = RecursiveDescentParser(grammar)

sentence1 = 'the cat chased the dog'.split()
sentence2 = 'the cat chased the dog on the rug'.split()

for t in rd.parse(sentence1):
    t.pretty_print()
    

for t in rd.parse(sentence2):
    t.pretty_print()
        