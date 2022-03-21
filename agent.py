from grammar import Grammar
import random


class Agent:
    def __init__(self, a_comp, b_comp, alphabet, name):
        self.name = name
        self.log = open("logs/" + name + ".txt", "w+")
        self.grammar = Grammar(a_comp, b_comp, alphabet, self.log)
        self.log.write("AGENT " + name + ":\n")

    def __repr__(self):
        output = ""
        output += "AGENT " + str(self.name) + ":\n\n"
        output += "I-LANGUAGE:\n"
        output += self.get_i_language() + "\n"
        output += "E-LANGUAGE:\n"
        output += self.get_e_language() + "\n"
        return output

    def get_i_language(self):
        return str(self.grammar)

    def get_e_language(self):
        output = " xx "
        for a in self.grammar.a_comp:
            output += "| " + a + " "
        output += "\n"
        for b in self.grammar.b_comp:
            output += " " + b + " "
            for a in self.grammar.a_comp:
                meaning = (a, b)
                result = self.grammar.parse(meaning)
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
        for i in range(exposure):
            teacher = teachers[random.randint(0, len(teachers)-1)]
            self.learn_single_utterance(teacher)

    def learn_single_utterance(self, teacher):
        meaning = self.grammar.get_random_meaning()
        utterance = teacher.produce_utterance(meaning)
        utterance_string = ""
        for char in utterance:
            utterance_string += char
        self.log.write("Learning utterance " + utterance_string + " for meaning " + str(meaning) + " from teacher " + teacher.name + "\n")
        self.grammar.incorporate(meaning, utterance)

    def produce_utterance(self, meaning):
        attempt = self.grammar.parse(meaning)
        if attempt is None:
            return self.grammar.invent(meaning)
        else:
            return attempt
