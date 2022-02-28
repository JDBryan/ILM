import random
import pytest
from grammar import Grammar
from rule import Rule


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


# def test_grammar_init():
#     new_grammar = Grammar(A_COMP, B_COMP, ALPHABET)
#     assert new_grammar.a_count == 1
#     assert new_grammar.rules == []
#     assert new_grammar.a_comp == A_COMP
#     assert new_grammar.b_comp == B_COMP
#     assert new_grammar.meanings == [(x, y) for x in new_grammar.a_comp for y in new_grammar.b_comp]
#     assert new_grammar.alphabet == ALPHABET
#
#
# @pytest.mark.parametrize(
#     "input_pair,output_rules",
#     [
#         # Unchunkable string test
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("S", ("a1", "b2"), ["d", "e", "f", "c", "b", "a"])],
#          [Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("S", ("a1", "b2"), ["d", "e", "f", "c", "b", "a"])]),
#
#         # Basic double chunk test
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("S", ("a1", "b2"), ["a", "b", "c", "c", "b", "a"])],
#          [Rule("S", ("a1", "y"), ["a", "b", "c", "A1:y"]), Rule("A1", ("b1"), ["d", "e", "f"]), Rule("A1", ("b2"), ["c", "b", "a"])]),
#
#         # Unchunkable double chunk meaning test
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("S", ("a2", "b2"), ["a", "b", "c", "c", "b", "a"])],
#          [Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("S", ("a2", "b2"), ["a", "b", "c", "c", "b", "a"])]),
#
#         # Complex double chunk test
#         ([Rule("S", ("x", "b1"), ["a", "b", "c", "A2:x"]), Rule("S", ("x", "b2"), ["a", "b", "d", "A2:x"])],
#          [Rule("S", ("x", "y"), ["a", "b", "A1:y", "A2:x"]), Rule("A1", ("b1"), ["c"]), Rule("A1", ("b2"), ["d"])]),
#
#         # Basic single chunk test
#         ([Rule("S", ("a1", "b2"), ["a", "b", "c", "g", "a", "j"]), Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"])],
#          [Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"]), Rule("A2", ("a1"), ["g", "a", "j"])]),
#
#         # Unchunkable single chunk meaning test
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "g", "a", "j"]), Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"])],
#          [Rule("S", ("a1", "b1"), ["a", "b", "c", "g", "a", "j"]), Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"])])
#     ],
# )
# def test_do_chunk(input_pair, output_rules):
#     grammar = Grammar(A_COMP, B_COMP, ALPHABET)
#     for rule in input_pair:
#         grammar.rules.append(rule)
#     chunk_a, chunk_b, remaining = grammar.chunk(input_pair[0].string, input_pair[1].string)
#     grammar.do_chunk(input_pair[0], input_pair[1], chunk_a, chunk_b, remaining)
#     for rule in grammar.rules:
#         assert rule in output_rules
#
#     for rule in output_rules:
#         assert rule in grammar.rules
#
# @pytest.mark.parametrize(
#     "input_pair,output_rules",
#     [
#         # start rule relabel
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("F", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"])],
#          [Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"])]),
#
#         # No relabel
#         ([Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("F", ("a1", "b2"), ["a", "b", "c", "d", "e", "f"])],
#          [Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"]), Rule("F", ("a1", "b2"), ["a", "b", "c", "d", "e", "f"])]),
#
#         # Relabel non-terminal
#         ([Rule("S", ("x", "b1"), ["a", "b", "c", "A1:x"]), Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"]), Rule("A1", "a1", ["a"]), Rule("A2", "a2", ["b"])],
#          [Rule("S", ("x", "b1"), ["a", "b", "c", "A2:x"]), Rule("S", ("x", "b2"), ["a", "b", "c", "A2:x"]), Rule("A2", "a1", ["a"]), Rule("A2", "a2", ["b"])]),
#     ],
# )
# def test_relabel(input_pair, output_rules):
#     grammar = Grammar(A_COMP, B_COMP, ALPHABET)
#     for rule in input_pair:
#         grammar.rules.append(rule)
#
#     grammar.do_relabel(input_pair[0], input_pair[1])
#
#     for rule in grammar.rules:
#         assert rule in output_rules
#
#     for rule in output_rules:
#         assert rule in grammar.rules


run_sim(50)

# grammar = Grammar(A_COMP, B_COMP, ALPHABET)
# rule_a = Rule("S", ("a1", "b1"), ["a", "b", "c", "d", "e", "f"])
# rule_b = Rule("S", ("a1", "b2"), ["a", "b", "c", "g", "a", "y"])
# grammar.rules.append(rule_a)
# grammar.rules.append(rule_b)
# print(grammar)
# grammar.generalise_pair(rule_a, rule_b)
# print(grammar)
