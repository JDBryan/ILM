from classes.grammar import Grammar
import random
import os
DIRNAME = os.path.dirname(__file__)


class Agent:
    def __init__(self, l_parameters, name):
        self.name = name
        self.l_parameters = l_parameters
        self.log = open(os.path.join(DIRNAME, "../logs/" + name + ".txt"), "w+")
        self.grammar = Grammar(l_parameters, self.log)
        self.log.write("AGENT " + name + ":\n")

    def __repr__(self):
        output = ""
        output += "AGENT " + str(self.name) + ":\n\n"
        output += "I-LANGUAGE:\n"
        output += self.get_i_language() + "\n"
        output += "E-LANGUAGE:\n"
        output += self.get_e_language() + "\n"
        return output

    def set_parameters(self, new_params):
        self.l_parameters = new_params
        self.grammar.set_parameters(new_params)

    def get_i_language(self):
        return str(self.grammar)

    def get_e_language(self):
        output = " xx "
        for a in self.l_parameters.a_comp:
            output += "| " + a + " "
        output += "\n"
        for b in self.l_parameters.b_comp:
            output += " " + b + " "
            for a in self.l_parameters.a_comp:
                meaning = [a, b]
                result = self.grammar.get_shortest_utterance(meaning)
                if result is None:
                    new_result = "-"
                else:
                    new_result = ""
                    for item in result:
                        new_result += item
                output += "| " + new_result + " "
            output += "\n"
        return output

    def learn(self, teachers, exposure):
        training_data = []

        for i in range(exposure):
            teacher = teachers[random.randint(0, len(teachers) - 1)]
            meaning = self.grammar.get_random_meaning()
            utterance = teacher.produce_utterance(meaning)
            training_data.append((meaning, utterance))

        for pair in training_data:
            utterance = pair[1]
            meaning = pair[0]
            utterance_string = ""
            for char in utterance:
                utterance_string += char
            self.log.write("Learning utterance " + utterance_string + " for meaning " + str(
                meaning) + "\n")
            self.grammar.incorporate(meaning, utterance)

    def learn_single_utterance(self, teacher):
        meaning = self.grammar.get_random_meaning()
        utterance = teacher.produce_utterance(meaning)
        utterance_string = ""
        for char in utterance:
            utterance_string += char
        self.log.write("Learning utterance " + utterance_string + " for meaning " + str(meaning) + " from teacher " + teacher.name + "\n")
        self.grammar.incorporate(meaning, utterance)

    def produce_utterance(self, meaning):
        attempt = self.grammar.get_shortest_utterance(meaning)
        if attempt is None:
            return self.grammar.invent(meaning)
        else:
            return attempt
