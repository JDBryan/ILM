import random
import os
from agent import Agent

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a" + str(i) for i in range(1, 6)]
B_COMP = ["b" + str(i) for i in range(1, 6)]
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
        self.populations = {
            "BASE": [Agent(a_comp, b_comp, alphabet, "Gen:" + str(self.gen) + "_Pop:BASE" + "_Agent:" + str(i)) for i in range(pop_size)]}
        self.log = open("logs/ilm.txt", "w+")
        self.log.write(str(self))

    def __repr__(self):
        output = "GENERATION " + str(self.gen) + ":\n"
        for pop_name in self.populations.keys():
            output += "POPULATION " + pop_name + ":\n"
            output += ""
        return output

    def run_single_generation(self):
        self.gen += 1
        self.log.write("GENERATION " + str(self.gen) + ":\n")
        for pop_name in self.populations.keys():
            self.run_single_generation_for_population(pop_name)
        for pop_name in self.populations.keys():
            self.log.write(pop_name + ":\n")
            self.log.write("Compositionality - " + str(self.population_compositionality(pop_name)) + "\n")
            self.log.write("Conformity -  " + str(self.population_conformity(pop_name)) + "\n")
            self.log.write("Size - " + str(self.population_grammar_size(pop_name)) + "\n\n")
            for agent in self.populations[pop_name]:
                self.log.write(str(agent))

    def run_single_generation_for_population(self, pop_name):
        new_population = [Agent(self.a_comp, self.b_comp, self.alphabet, "Gen:" + str(self.gen) + "_Pop:" + pop_name + "_Agent:" + str(i)) for i in
                          range(self.pop_size)]
        for learner in new_population:
            learner.learn(self.populations[pop_name], self.exposure)
        self.populations[pop_name] = new_population

    def run_generations(self, generations):
        for i in range(generations):
            self.run_single_generation()

    def split_population(self, pop_name):
        self.log.write("Splitting population " + pop_name + "\n")
        if pop_name in self.populations:
            pop = self.populations.pop(pop_name)
            a_split = pop[:int(len(pop)/2)]
            b_split = pop[int(len(pop)/2):]
            self.populations[pop_name + "-A"] = a_split
            self.populations[pop_name + "-B"] = b_split

    def merge_populations(self, pop_names, new_name):
        print("Merging populations " + str(pop_names) + " into population " + new_name)
        self.populations[new_name] = []
        for pop_name in pop_names:
            self.populations[new_name] += self.populations.pop(pop_name)

    def population_compositionality(self, pop_name):
        comps = 0
        for agent in self.populations[pop_name]:
            comps += agent.grammar.get_compositionality()
        return comps / len(self.populations[pop_name])

    def population_conformity(self, pop_name):
        conformities = []
        for meaning in self.meanings:
            utterance_dict = {}
            total = 0
            for agent in self.populations[pop_name]:
                char_list = agent.grammar.parse(meaning)

                if char_list is not None:
                    utterance = ""
                    for char in char_list:
                        utterance += char
                    total += 1
                    if utterance in utterance_dict.keys():
                        utterance_dict[utterance] += 1
                    else:
                        utterance_dict[utterance] = 1
                if len(utterance_dict) == 0:
                    conformities.append(1)
                else:
                    conformities.append(max(utterance_dict.values())/total)
        return sum(conformities) / len(conformities)

    def population_grammar_size(self, pop_name):
        total_size = 0
        for agent in self.populations[pop_name]:
            total_size += agent.grammar.get_size()
        return total_size / len(self.populations[pop_name])


ilm = Ilm(1, 50, A_COMP, B_COMP, ALPHABET)
ilm.run_generations(50)

