import random
import os
import matplotlib.pyplot as plt
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
        print("Running generation " + str(self.gen))
        for pop_name in self.populations.keys():
            self.run_single_generation_for_population(pop_name)

    def run_single_generation_for_population(self, pop_name):
        new_population = [Agent(self.a_comp, self.b_comp, self.alphabet, "Gen:" + str(self.gen) + "_Pop:" + pop_name + "_Agent:" + str(i)) for i in
                          range(self.pop_size)]
        for learner in new_population:
            learner.learn(self.populations[pop_name], self.exposure)
        old_population = self.populations[pop_name]
        self.populations[pop_name] = new_population

        self.log.write(pop_name + ":\n\n")
        for agent in self.populations[pop_name]:
            self.log.write(str(agent) + "\n\n")
        self.log.write("Compositionality - " + str(self.population_compositionality(pop_name)) + "\n")
        self.log.write("Conformity -  " + str(self.population_conformity(pop_name)) + "\n")
        self.log.write("Size - " + str(self.population_grammar_size(pop_name)) + "\n")
        self.log.write("Regularity - " + str(self.multi_language_conformity(self.population_e_language(old_population), self.population_e_language(new_population))) + "\n\n")

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

    def population_e_language(self, population):
        e_language = {meaning: "" for meaning in self.meanings}

        for meaning in self.meanings:
            frequency_table = {}
            most_common_utterance = None
            highest_frequency = 0

            for agent in population:
                utterance = ""
                for char in agent.produce_utterance(meaning):
                    utterance += char

                if utterance in frequency_table.keys():
                    frequency_table[utterance] += 1
                else:
                    frequency_table[utterance] = 1

            for utterance in frequency_table.keys():
                if frequency_table[utterance] > highest_frequency:
                    highest_frequency = frequency_table[utterance]
                    most_common_utterance = utterance

            e_language[meaning] = most_common_utterance

        return e_language

    def multi_language_conformity(self, a_e_language, b_e_language):
        similarity = 0

        for meaning in self.meanings:
            if a_e_language[meaning] == b_e_language[meaning]:
                similarity += 1

        return similarity / len(self.meanings)

    def population_grammar_size(self, pop_name):
        total_size = 0
        for agent in self.populations[pop_name]:
            total_size += agent.grammar.get_size()
        return total_size / len(self.populations[pop_name])


ilm = Ilm(1, 50, A_COMP, B_COMP, ALPHABET)
# ilm.split_population("BASE")

sizes = []
regularities = []
generations = []
for i in range(100):
    old_e_language = ilm.population_e_language(ilm.populations["BASE"])
    ilm.run_single_generation()
    new_e_language = ilm.population_e_language(ilm.populations["BASE"])
    generations.append(ilm.gen)
    regularities.append(ilm.multi_language_conformity(old_e_language, new_e_language))
    sizes.append(ilm.population_grammar_size("BASE"))

# plotting the points
plt.plot(generations, regularities)

# naming the x axis
plt.xlabel('Generation')
# naming the y axis
plt.ylabel('Regularity')

# giving a title to my graph
plt.title('Language regularity over generations')
plt.show()

# ilm.run_generations(30)
# a_e_language = ilm.population_e_language(ilm.populations["BASE-A"])
# b_e_language = ilm.population_e_language(ilm.populations["BASE-B"])
# ilm.merge_populations(["BASE-A", "BASE-B"], "BASE")
# ilm.run_generations(30)
# final_e_language = ilm.population_e_language(ilm.populations["BASE"])
# print("Similarity to language A - " + str(ilm.multi_language_conformity(a_e_language, final_e_language)))
# print("Similarity to language B - " + str(ilm.multi_language_conformity(b_e_language, final_e_language)))
