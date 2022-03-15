import random
import os
import shutil
from grammar import Grammar

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a1", "a2", "a3", "a4", "a5"]
B_COMP = ["b1", "b2", "b3", "b4", "b5"]
MEANINGS = [(x, y) for x in A_COMP for y in B_COMP]


class Ilm:
    def __init__(self, pop_size, exposure, a_comp, b_comp, alphabet):
        for filename in os.listdir("logs"):
            os.remove("logs/" + filename)
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.meanings = [(x, y) for x in a_comp for y in b_comp]
        self.pop_size = pop_size
        self.alphabet = alphabet
        self.exposure = exposure
        self.gen = 0
        self.population = [Grammar(a_comp, b_comp, alphabet, "G" + str(self.gen) + "A" + str(i)) for i in range(pop_size)]
        self.log = open("logs/ilm.txt", "w+")
        self.log.write(str(self))

    def __repr__(self):
        output = "GENERATION " + str(self.gen) + ":\n"
        for agent in self.population:
            output += "AGENT " + str(agent.name) + ":\n\n"
            output += "I-LANGUAGE:\n"
            output += str(agent) + "\n"
            output += "E-LANGUAGE:\n"
            output += agent.get_word_table() + "\n"
        return output

    def run_single_generation(self):
        self.gen += 1
        new_population = [Grammar(self.a_comp, self.b_comp, self.alphabet, "G" + str(self.gen) + "A" + str(i)) for i in range(self.pop_size)]
        for learner in new_population:
            for i in range(self.exposure):
                teacher = self.population[random.randint(0, self.pop_size - 1)]
                learner.learn(teacher)
        self.population = new_population
        self.log.write(str(self))

    def run_generations(self, generations):
        for i in range(generations):
            self.run_single_generation()


ilm = Ilm(2, 50, A_COMP, B_COMP, ALPHABET)
ilm.run_generations(30)

