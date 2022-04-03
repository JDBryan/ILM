from classes.agent import Agent


class Population:
    def __init__(self, name, size, exposure, l_parameters, gen, log):
        self.name = name
        self.pop_size = size
        self.previous_agents = []
        self.l_parameters = l_parameters
        self.gen = gen
        self.log = log
        self.exposure = exposure
        self.initialise_agents()

    def initialise_agents(self):
        new_agents = []
        for i in range(self.pop_size):
            name = "Gen:" + str(self.gen) + "_Pop:" + self.name + "_Agent:" + str(i)
            new_agents.append(Agent(self.l_parameters, name))
        self.agents = new_agents

    def set_agents(self, agents):
        if len(agents) != self.pop_size:
            raise Exception("Incorrect population size, expected " + str(self.pop_size) + " agents, got " + str(len(agents)))
        else:
            self.agents = agents

    def compositionality(self):
        comps = 0
        for agent in self.agents:
            comps += agent.grammar.get_compositionality()
        return comps / self.pop_size

    def conformity(self):
        conformities = []
        for meaning in self.l_parameters.meanings:
            utterance_dict = {}
            total = 0
            for agent in self.agents:
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
                    conformities.append(max(utterance_dict.values()) / total)
        return sum(conformities) / len(conformities)

    def regularity(self):
        similarity = 0

        previous_language = self.previous_e_language()
        current_language = self.current_e_language()
        for meaning in self.l_parameters.meanings:
            if previous_language[meaning] == current_language[meaning]:
                similarity += 1

        return similarity / len(self.l_parameters.meanings)

    def current_e_language(self):
        e_language = {meaning: "" for meaning in self.l_parameters.meanings}

        for meaning in self.l_parameters.meanings:
            frequency_table = {}
            most_common_utterance = None
            highest_frequency = 0

            for agent in self.agents:
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

    def previous_e_language(self):
        e_language = {meaning: "" for meaning in self.l_parameters.meanings}

        for meaning in self.l_parameters.meanings:
            frequency_table = {}
            most_common_utterance = None
            highest_frequency = 0

            for agent in self.previous_agents:
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

    def average_grammar_size(self):
        total_size = 0
        for agent in self.agents:
            total_size += agent.grammar.get_size()
        return total_size / self.pop_size

    def run_single_generation(self):
        self.gen += 1
        self.previous_agents = self.agents

        self.initialise_agents()

        for learner in self.agents:
            learner.learn(self.previous_agents, self.exposure)

        # for learner in self.agents:
        #     learner.learn(self.agents, self.exposure)

        self.log.write(self.name + ":\n\n")
        for agent in self.agents:
            self.log.write(str(agent) + "\n\n")
        self.log.write("Compositionality - " + str(self.compositionality()) + "\n")
        self.log.write("Conformity -  " + str(self.conformity()) + "\n")
        self.log.write("Size - " + str(self.average_grammar_size()) + "\n")
        self.log.write("Regularity - " + str(self.regularity()) + "\n\n")