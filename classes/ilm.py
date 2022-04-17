
import os
from classes.population import Population

DIRNAME = os.path.dirname(__file__)

class Ilm:
    def __init__(self, l_parameters, pop_size, exposure):
        for filename in os.listdir(os.path.join(DIRNAME, "../logs")):
            os.remove(os.path.join(DIRNAME, "../logs/" + filename))
        log_filename = os.path.join(DIRNAME, "../logs/ilm.txt")
        self.log = open(log_filename, "w+")
        self.pop_size = pop_size
        self.l_parameters = l_parameters
        self.exposure = exposure
        self.gen = 0
        base_population = Population("BASE", pop_size, exposure, l_parameters, self.gen, self.log)
        self.populations = {
            "BASE": base_population}
        self.log.write(str(self))

    def __repr__(self):
        output = "GENERATION " + str(self.gen) + ":\n"
        for pop_name in self.populations.keys():
            output += "POPULATION " + pop_name + ":\n"
            output += ""
        return output

    def add_population(self, name, agents):
        new_population = Population(name, self.pop_size, self.exposure, self.l_parameters, self.gen, self.log)
        new_population.set_agents(agents)
        self.populations[name] = new_population

    def run_single_generation(self):
        self.gen += 1
        self.log.write("GENERATION " + str(self.gen) + ":\n")
        print("Running generation " + str(self.gen))
        for population in self.populations.values():
            population.run_single_generation()

    def run_generations(self, generations):
        for i in range(generations):
            self.run_single_generation()

    def split_population(self, pop_name):
        self.log.write("Splitting population " + pop_name + "\n")
        if pop_name in self.populations:
            pop = self.populations.pop(pop_name)
            a_agents = pop.agents[:int(pop.pop_size/2)] + pop.agents[:int(pop.pop_size/2)]
            b_agents = pop.agents[int(pop.pop_size/2):] + pop.agents[int(pop.pop_size/2):]
            self.add_population(pop_name + "-A", a_agents)
            self.add_population(pop_name + "-B", b_agents)

    def merge_populations(self, pop_a_name, pop_b_name, new_name, a_amount):
        print("Merging populations " + pop_a_name + " and " + pop_b_name + " into population " + new_name)
        self.populations[new_name] = []
        b_amount = self.pop_size - a_amount
        # pop_a_amount = int(self.pop_size * a_ratio)
        # pop_b_amount = int(self.pop_size * (1-a_ratio))
        print(a_amount)
        print(b_amount)
        pop_a = self.populations.pop(pop_a_name)
        pop_b = self.populations.pop(pop_b_name)
        self.add_population(new_name, pop_a.agents[:a_amount] + pop_b.agents[:b_amount])

    def multi_language_conformity(self, a_e_language, b_e_language):
        similarity = 0

        for meaning in self.l_parameters.meanings:
            if a_e_language[tuple(meaning)] == b_e_language[tuple(meaning)]:
                similarity += 1

        return similarity / len(self.l_parameters.meanings)






