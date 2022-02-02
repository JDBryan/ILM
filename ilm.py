ALPHABET = "abcdefghijklmnopqrstuvwxyz"
A_COMP = ["a1", "a2", "a3", "a4", "a5"]
B_COMP = ["b1", "b2", "b3", "b4", "b5"]
MEANINGS = [(x, y) for x in A_COMP for y in B_COMP]


class Grammar:
    def __init__(self):
        self.a_count = 1
        self.rules = []

    def __repr__(self):
        output = ""
        for rule in self.rules:
            output += rule.__repr__()
            output += "\n"
        return output

    # Get all rules under a given label
    def get_rules_by_label(self, label):
        labeled_rules = []
        for rule in self.rules:
            if label == rule.label:
                labeled_rules.append(rule)
        return labeled_rules

    def induction(self, meaning, string):
        self.incorporate(Rule("S", meaning, string))
        self.generalise()

    def find_closest_meaning(self, meaning):
        for i in A_COMP:
            if self.parse((i, meaning[1])) != "-":
                closest_meaning = (i, meaning[1])
                return closest_meaning

        for i in B_COMP:
            if self.parse((meaning[0], i)) != "-":
                closest_meaning = (meaning[0], i)
                return closest_meaning

        for i in A_COMP:
            for j in B_COMP:
                if self.parse((i, j)) != "-":
                    closest_meaning = (i, j)
                    return closest_meaning

    def invent(self, meaning):
        closest_meaning = self.find_closest_meaning(meaning)

    def remove_duplicates(self):
        self.rules = list(dict.fromkeys(self.rules))

    def generalise(self):
        for i in range(len(self.rules)):
            rule_a = self.rules[i]
            for j in range(len(self.rules)):
                rule_b = self.rules[j]
                if i == j:
                    continue
                elif self.generalise_pair(rule_a, rule_b):
                    self.generalise()

    # Uses the generalisation rules on a specific pair of rules
    def generalise_pair(self, rule_a, rule_b):
        substring_marker = rule_a.is_substring(rule_b)
        changed = False
        if rule_a.meaning == rule_b.meaning and rule_a.string == rule_b.string:
            rule_b.label = rule_a.label
            changed = True
        elif rule_a.label == "S" and rule_b.label == "S" and not changed:
            new_rule_a_meaning = ""
            new_rule_b_meaning = ""
            new_rule_s_meaning = ""
            meaning_var = ""
            if rule_a.meaning[0] == rule_b.meaning[0] and rule_a.meaning[0] in A_COMP:
                new_rule_a_meaning = rule_a.meaning[1]
                new_rule_b_meaning = rule_b.meaning[1]
                new_rule_s_meaning = (rule_a.meaning[0], "y")
                meaning_var = "y"
            if rule_a.meaning[1] == rule_b.meaning[1] and rule_a.meaning[1] in B_COMP:
                new_rule_a_meaning = rule_a.meaning[0]
                new_rule_b_meaning = rule_b.meaning[0]
                new_rule_s_meaning = ("x", rule_a.meaning[1])
                meaning_var = "x"
            if new_rule_a_meaning != "":
                new_string_a, new_string_b, remaining = chunk(rule_a.string, rule_b.string)
                splits = split_list(remaining, "-")
                new_label = "A" + str(self.a_count)
                new_string_s = splits[0] + [new_label + ":" + meaning_var] + splits[1]
                self.rules.append(Rule(new_label, new_rule_a_meaning, new_string_a))
                self.rules.append(Rule(new_label, new_rule_b_meaning, new_string_b))
                self.a_count += 1
                self.rules.append(Rule("S", new_rule_s_meaning, new_string_s))
            self.rules.remove(rule_a)
            self.rules.remove(rule_b)
            changed = True
        elif substring_marker != -1 and rule_b.label == "S" and not changed:
            if rule_a.meaning == rule_b.meaning[0]:
                new_string = rule_b.string[:substring_marker] + [rule_a.label + ":x"] + rule_b.string[substring_marker + len(rule_a.string):]
                self.rules.append(Rule("S", ("x", rule_b.meaning[1]), new_string))
                self.rules.remove(rule_b)
            if rule_a.meaning == rule_b.meaning[1]:
                new_string = rule_b.string[:substring_marker] + [rule_a.label + ":y"] + rule_b.string[substring_marker + len(rule_a.string):]
                self.rules.append(Rule("S", (rule_b.meaning[0], "y"), new_string))
                self.rules.remove(rule_b)
            rule_a.is_substring(rule_b)
        self.remove_duplicates()

    # Incorporates the given rule into the grammar
    def incorporate(self, rule):
        if self.parse(rule.meaning) == "-":
            self.rules.append(rule)

    # Use grammar to find string for a given meaning
    # returns "-" if no string can be generated
    def parse(self, meaning):
        for rule in self.get_rules_by_label("S"):
            if rule.meaning_match(meaning):
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

    def __repr__(self):
        string_str = ""
        for item in self.string:
            string_str += item

        if self.label == "S":
            meaning_str = "(" + self.meaning[0] + "," + self.meaning[1] + ")"
        else:
            meaning_str = self.meaning
        return self.label + ": " + meaning_str + " -> " + string_str

    def meaning_match(self, meaning):
        if self.label == "S":
            if meaning[0] == self.meaning[0] or self.meaning[0] not in A_COMP:
                if meaning[1] == self.meaning[1] or self.meaning[1] not in B_COMP:
                    return True
        return False

    def is_substring(self, rule):
        for i in range(len(rule.string)):
            found_substring = True
            for j in range(len(self.string)):
                if i+j > len(rule_b.string)-1 or rule.string[i + j] != self.string[j]:
                    found_substring = False
            if found_substring:
                return i
        return -1


def split_list(list_l, split_marker):
    marker = -1
    new_list = []
    for i in range(len(list_l)):
        if list_l[i] == split_marker:
            new_list.append(list_l[marker+1:i])
            marker = i

    new_list.append(list_l[marker+1:])
    return new_list


def chunk(string_a, string_b):
    i = 0
    j = 0

    while string_a[i] == string_b[i]:
        i += 1
        if i >= min(len(string_a), len(string_b)):
            break

    while string_a[len(string_a) - (1+j)] == string_b[len(string_b) - (1+j)]:
        j += 1
        if i >= min(len(string_a), len(string_b)):
            break

    if i == 0 and j == 0:
        return "-", "-", "-"

    chunk_a = string_a[i:len(string_a) - j]
    chunk_b = string_b[i:len(string_b) - j]
    remaining = string_a[:i] + ["-"] + string_a[len(string_a)-j:]

    for letter in chunk_a:
        if len(letter) > 1:
            return "-", "-", "-"

    for letter in chunk_b:
        if len(letter) > 1:
            return "-", "-", "-"

    if len(chunk_a) == 0 or len(chunk_b) == 0:
        return "-", "-", "-"

    return chunk_a, chunk_b, remaining


my_grammar = Grammar()
rule_a = Rule("S", ("a1", "b1"), ["l", "a", "d", "a", "b", "l", "a"])
rule_b = Rule("A", "a1", ["d", "a", "b"])
my_grammar.rules.append(rule_a)
my_grammar.rules.append(rule_b)
my_grammar.generalise_pair(rule_a, rule_b)
print(my_grammar)

# a, b, s = my_grammar.chunk("helloabcgoodbye", "hellodefgoodbye")
