ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a1", "a2", "a3", "a4", "a5"]
B_COMP = ["b1", "b2", "b3", "b4", "b5"]
MEANINGS = [(x, y) for x in A_COMP for y in B_COMP]


class Grammar:
    def __init__(self):
        self.s_count = 1
        self.a_count = 1
        self.rules = []

    def induction(self, meaning, string):
        label = "S" + str(self.s_count)
        self.incorporate(Rule(label, meaning, string))

    def generalise_pair(self, label_a, label_b):
        rule_a = self.rules[label_a]
        rule_b = self.rules[label_b]
        if rule_a.meaning == rule_b.meaning and rule_a.string == rule_b.string:
            del self.rules[rule_b]

    def get_rules_by_label(self, label):
        labeled_rules = []
        for rule in self.rules:
            if label == rule.label:
                labeled_rules.append(rule)
        return labeled_rules

    def incorporate(self, rule):
        if self.parse(rule.meaning) == "-":
            self.rules.append(rule)
            self.s_count += 1

    def parse(self, meaning):
        for rule in self.rules:
            if rule.label[0] == "S":
                output = self.parse_rule(meaning, rule)
                if output != "-":
                    return output
            return "-"

    def find_subrule(self, meaning_variable, concrete_meaning, rule):
        for item in rule.string:
            if len(item) > 1 and item.split(":")[1] == meaning_variable:
                rule_label = item.split(":")[0]
                for rule in self.get_rules_by_label(rule_label):
                    if rule.meaning == concrete_meaning:
                        return rule
        return "-"

    def parse_rule(self, meaning, rule):
        output = ""
        a_rule = ""
        b_rule = ""

        #Find subrule for first meaning variable
        if rule.meaning[0] not in A_COMP:
            a_rule = self.find_subrule(rule.meaning[0], meaning[0], rule)

        #Find subrule for second meaning variable
        if rule.meaning[1] not in B_COMP:
            b_rule = self.find_subrule(rule.meaning[1], meaning[1], rule)

        #Check that rule meaning matches given meaning
        if (a_rule != "" or meaning[0] == rule.meaning[0]) and (b_rule != "" or meaning[1] == rule.meaning[1]):
            for item in rule.string:
                if len(item) == 1:
                    output += item
                else:
                    items = item.split(":")
                    if items[1] == rule.meaning[0]:
                        for i in a_rule.string:
                            output += i
                    if items[1] == rule.meaning[1]:
                        for i in b_rule.string:
                            output += i
            return output
        return "-"


class Rule:
    def __init__(self, label, meaning, string):
        self.label = label
        self.meaning = meaning
        self.string = string


my_grammar = Grammar()
my_grammar.rules.append(Rule("S1", ("a1", "x"), ["d", "a", "b", "A1:x"]))
my_grammar.rules.append(Rule("A1", "b1", ["l", "a"]))
print(my_grammar.parse(("a1", "b1")))
