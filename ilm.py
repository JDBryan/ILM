import random
from grammar import Grammar

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a1", "a2", "a3", "a4", "a5"]
B_COMP = ["b1", "b2", "b3", "b4", "b5"]
MEANINGS = [(x, y) for x in A_COMP for y in B_COMP]


def run_sim(number_of_generations):
    grammar = Grammar(A_COMP, B_COMP, ALPHABET)
    for i in range(number_of_generations):
        print("-- GEN: " + str(i) + " --")
        print(grammar)
        grammar.print_word_table()
        grammar = generation(grammar)


def generation(old_grammar):
    new_grammar = Grammar(A_COMP, B_COMP, ALPHABET)
    for i in range(50):
        meaning = MEANINGS[random.randint(0, 24)]
        string = old_grammar.parse(meaning)
        if string is None:
            string = old_grammar.invent(meaning)
        new_grammar.incorporate(meaning, string)
    return new_grammar


run_sim(30)

