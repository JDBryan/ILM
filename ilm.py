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

    # Uses the generalisation rules on a specific pair of rules
    def generalise_pair(self, rule_a, rule_b):
        if rule_a.meaning == rule_b.meaning and rule_a.string == rule_b.string:
            rule_b.label = rule_a.label
        elif rule_a.label[0] == "S" and rule_b.label[0] == "S":
            if rule_a.meaning[0] == rule_b.meaning[0] and rule_a.meaning in A_COMP:
                return True


    # Get all rules under a given label
    def get_rules_by_label(self, label):
        labeled_rules = []
        for rule in self.rules:
            if label == rule.label:
                labeled_rules.append(rule)
        return labeled_rules

    # Incorporates the given rule into the grammar
    def incorporate(self, rule):
        if self.parse(rule.meaning) == "-":
            self.rules.append(rule)
            self.s_count += 1

    def meaning_match(self, rule, meaning):
        if rule.label[0] == "S":
            if meaning[0] == rule.meaning[0] or rule.meaning[0] not in A_COMP:
                if meaning[1] == rule.meaning[1] or rule.meaning[1] not in B_COMP:
                    return True
        return False


    # Use grammar to find string for a given meaning
    # returns "-" if no string can be generated
    def parse(self, meaning):
        for rule in self.rules:
            if self.meaning_match(rule, meaning):
                output = self.parse_rule(meaning, rule)
                if output != "-":
                    return output
        return "-"

    def parse_rule(self, meaning, rule):
        output = ""

        for item in rule.string:
            if len(item) == 1:
                output += item
            else:
                rule_found = False
                label = item.split(":")[0]
                labeled_rules = self.get_rules_by_label(label)
                meaning_var = item.split(":")[1]
                if meaning_var == rule.meaning[0]:
                    concrete_meaning = meaning[0]
                else:
                    concrete_meaning = meaning[1]
                for i_rule in labeled_rules:
                    if i_rule.meaning == concrete_meaning:
                        rule_found = True
                        for i in i_rule.string:
                            output += i
                if not rule_found:
                    return "-"
        return output

class Rule:
    def __init__(self, label, meaning, string):
        self.label = label
        self.meaning = meaning
        self.string = string


my_grammar = Grammar()
my_grammar.rules.append(Rule("S1", ("a1", "x"), ["d", "a", "b", "A1:x"]))
my_grammar.rules.append(Rule("A1", "b1", ["l", "a"]))
print(my_grammar.parse(("a1", "b1")))
