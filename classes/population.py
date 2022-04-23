from classes.agent import Agent
import random

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
        self.regularities = []
        self.sizes = []
        self.is_stable = False

    def initialise_agents(self):
        new_agents = []
        for i in range(self.pop_size):
            name = "Gen:" + str(self.gen) + "_Pop:" + self.name + "_Agent:" + str(i)
            new_agents.append(Agent(self.l_parameters, name))
        self.agents = new_agents

    def has_converged(self):
        # if len(self.sizes) < 5:
        #     return False
        #
        # else:
        #     s = self.sizes[len(self.sizes)-1]
        #     for size in self.sizes[len(self.sizes)-5:]:
        #         if size != s:
        #             return False

        if len(self.regularities) < 5:
            return False

        else:
            for reg in self.regularities[len(self.regularities) - 5:]:
                if reg < 0.95:
                    return False
        return True

    def set_agents(self, agents):
        if len(agents) != self.pop_size:
            raise Exception("Incorrect population size, expected " + str(self.pop_size) + " agents, got " + str(len(agents)))
        else:
            self.agents = agents

    def coherence(self):
        conformities = []
        for meaning in self.l_parameters.meanings:
            utterance_dict = {}
            total = 0
            for agent in self.agents:
                char_list = agent.grammar.get_utterance(meaning)

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
                conformities.append(0)
            else:
                conformities.append(max(utterance_dict.values()) / total)
        return sum(conformities) / len(conformities)

    def regularity(self):
        previous_language = self.previous_e_language()
        current_language = self.current_e_language()
        successful_communications = 0

        for meaning in previous_language.keys():
            for i in range(10):
                utterances = previous_language[meaning]
                if utterances != []:
                    utterance = utterances[random.randint(0, len(utterances)-1)]
                    if utterance in current_language[meaning]:
                        successful_communications += 1

        for meaning in current_language.keys():
            for i in range(10):
                utterances = current_language[meaning]
                if utterances != []:
                    utterance = utterances[random.randint(0, len(utterances)-1)]
                    if utterance in previous_language[meaning]:
                        successful_communications += 1

        return successful_communications/500

    def current_e_language(self):
        e_language = {tuple(meaning): [] for meaning in self.l_parameters.meanings}

        for agent in self.agents:
            for meaning in agent.grammar.map.keys():
                e_language[meaning] += agent.grammar.map[meaning]

        return e_language

    def previous_e_language(self):
        e_language = {tuple(meaning): [] for meaning in self.l_parameters.meanings}

        for agent in self.previous_agents:
            for meaning in agent.grammar.map.keys():
                e_language[meaning] += agent.grammar.map[meaning]

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

        self.log.write(self.name + ":\n\n")
        for agent in self.agents:
            self.log.write(str(agent) + "\n\n")
        # self.log.write("Conformity -  " + str(self.conformity()) + "\n")
        self.log.write("Size - " + str(self.average_grammar_size()) + "\n")
        self.log.write("Regularity - " + str(self.regularity()) + "\n\n")
        self.sizes.append(self.average_grammar_size())
        self.regularities.append(self.regularity())
