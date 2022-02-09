from rule import Rule
import random


class Grammar:
    def __init__(self, a_comp, b_comp, alphabet):
        self.a_count = 1
        self.rules = []
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.meanings = [(x, y) for x in self.a_comp for y in self.b_comp]
        self.alphabet = alphabet

    def __repr__(self):
        output = ""
        for rule in self.rules:
            output += rule.__repr__()
            output += "\n"
        return output

    def print_word_table(self):
        top_row = " xx "
        for a in self.a_comp:
            top_row += "| " + a + " "
        print(top_row)
        for b in self.b_comp:
            row = " " + b + " "
            for a in self.a_comp:
                meaning = (a, b)
                result = self.parse(meaning)
                if result is None:
                    new_result = "-"
                else:
                    new_result = ""
                    for item in result:
                        new_result += item
                row += "| " + new_result + " "
            print(row)

    # Returns a rule associated with a specific label and meaning
    def get_rule(self, label, meaning, include_x):
        for rule in self.get_rules_by_label(label, include_x):
            if rule.meaning == meaning:
                return rule
        return None

    # Get all rules under a given label
    def get_rules_by_label(self, label, include_x):
        labeled_rules = []
        for rule in self.rules:
            if label == rule.label or (include_x and label == "x"):
                labeled_rules.append(rule)
        return labeled_rules

    # Use grammar to find string for a given meaning
    # returns None if no string can be generated
    def parse(self, meaning):
        parsable, start_rule, sub_rules = self.parsable(meaning)
        if parsable:
            return self.parse_rule(meaning, start_rule, sub_rules)
        else:
            return None

    def generate_random_string(self):
        length = random.randint(2, 7)
        string = []
        for i in range(length):
            string += [self.alphabet[random.randint(0, 25)]]
        return string

    def chunk(self, string_a, string_b):
        i = 0
        j = 0

        while string_a[i] == string_b[i]:
            i += 1
            if i >= min(len(string_a), len(string_b)):
                return None, None, None

        while string_a[len(string_a) - (1 + j)] == string_b[len(string_b) - (1 + j)]:
            j += 1
            if i >= min(len(string_a), len(string_b)):
                return None, None, None

        if i == 0 and j == 0:
            return None, None, None

        chunk_a = string_a[i:len(string_a) - j]
        chunk_b = string_b[i:len(string_b) - j]
        first = string_a[:i]
        second = string_a[len(string_a) - j:]
        remaining = first + ["-"] + second

        if len(chunk_a) == 0 or len(chunk_b) == 0:
            return None, None, None

        return chunk_a, chunk_b, remaining

    def find_closest_meaning(self, meaning):
        for i in self.a_comp:
            if self.parse((i, meaning[1])) != "-":
                closest_meaning = (i, meaning[1])
                return closest_meaning

        for i in self.b_comp:
            if self.parse((meaning[0], i)) != "-":
                closest_meaning = (meaning[0], i)
                return closest_meaning

        for i in self.a_comp:
            for j in self.b_comp:
                if self.parse((i, j)) != "-":
                    closest_meaning = (i, j)
                    return closest_meaning
        return None

    def invent(self, meaning):
        closest_meaning = self.find_closest_meaning(meaning)
        if closest_meaning is None:
            return self.generate_random_string()
        if meaning[0] == closest_meaning[0]:
            intersection = (meaning[0], "d2")
        elif meaning[1] == closest_meaning[1]:
            intersection = ("d1", meaning[0])
        else:
            intersection = ("d1", "d2")

        d1_rule = ""
        if intersection[0] == "d1":
            d1_rule = Rule("X", "d1", self.generate_random_string())
            self.rules.append(d1_rule)

        d2_rule = ""
        if intersection[1] == "d2":
            d2_rule = Rule("X", "d2", self.generate_random_string())
            self.rules.append(d2_rule)

        invention = self.parse(intersection)
        if invention is None:
            invention = self.generate_random_string()

        if d1_rule != "":
            self.rules.remove(d1_rule)

        if d2_rule != "":
            self.rules.remove(d2_rule)

        return invention

    def remove_duplicates(self):
        changed = True
        while changed:
            changed = False
            for i in range(len(self.rules)):
                for j in range(len(self.rules)):
                    if i == j:
                        continue
                    if changed:
                        break
                    rule_i = self.rules[i]
                    rule_j = self.rules[j]
                    if rule_j.label == rule_i.label and rule_i.meaning == rule_j.meaning and rule_i.string == rule_j.string:
                        self.rules.remove(rule_i)
                        changed = True
                        break
                if changed:
                    break

    def split_list(self, list_l, split_marker):
        marker = -1
        new_list = []
        for i in range(len(list_l)):
            if list_l[i] == split_marker:
                new_list.append(list_l[marker + 1:i])
                marker = i

        new_list.append(list_l[marker + 1:])
        return new_list

    #TODO: change the use of continue
    def generalise(self):
        changed = True
        while changed:
            changed = False
            for i in range(len(self.rules)):
                if changed:
                    break
                else:
                    rule_a = self.rules[i]
                for j in range(len(self.rules)):
                    if i == j or changed:
                        break
                    else:
                        rule_b = self.rules[j]
                        changed = self.generalise_pair(rule_a, rule_b)

    def do_double_chunk(self, rule_a, rule_b, chunk_a, chunk_b, remaining):
        double_chunkable = False
        if rule_a.meaning[0] == rule_b.meaning[0] or rule_a.meaning[1] == rule_b.meaning[1]:
            # Case where there are no meaning variables
            if rule_a.meaning[0] in self.a_comp and rule_a.meaning[1] in self.b_comp:
                if rule_b.meaning[0] in self.a_comp and rule_b.meaning[1] in self.b_comp:
                    double_chunkable = True

            # Case where comp A is a meaning variable
            elif rule_a.meaning[0] == rule_b.meaning[0] and rule_a.meaning[0] not in self.a_comp:
                if rule_a.meaning[1] in self.b_comp and rule_b.meaning[1] in self.b_comp and rule_a.meaning[1] != rule_b.meaning[1]:
                    double_chunkable = True

            # Case where comp B is a meaning variable
            elif rule_a.meaning[1] == rule_b.meaning[1] and rule_a.meaning[1] not in self.a_comp:
                if rule_a.meaning[0] in self.b_comp and rule_b.meaning[0] in self.b_comp and rule_a.meaning[0] != rule_b.meaning[0]:
                    double_chunkable = True

        # Checking that neither chunk contains a non terminal
        if chunk_a is None:
            double_chunkable = False
        else:
            for i in chunk_a:
                if len(i) > 1:
                    double_chunkable = False
            for i in chunk_b:
                if len(i) > 1:
                    double_chunkable = False

        if not double_chunkable:
            return False

        if rule_a.meaning[0] == rule_b.meaning[0] and rule_a.meaning[0] not in self.a_comp:
            new_rule_a_meaning = rule_a.meaning[1]
            new_rule_b_meaning = rule_b.meaning[1]
            new_rule_s_meaning = ("x", "y")
            meaning_var = "y"
            new_label = "B"
        elif rule_a.meaning[1] == rule_b.meaning[1] and rule_a.meaning[1] not in self.b_comp:
            new_rule_a_meaning = rule_a.meaning[0]
            new_rule_b_meaning = rule_b.meaning[0]
            new_rule_s_meaning = ("x", "y")
            meaning_var = "x"
            new_label = "A"
        elif rule_a.meaning[0] == rule_b.meaning[0]:
            new_rule_a_meaning = rule_a.meaning[1]
            new_rule_b_meaning = rule_b.meaning[1]
            new_rule_s_meaning = (rule_a.meaning[0], "y")
            meaning_var = "y"
            new_label = "B"
        elif rule_a.meaning[1] == rule_b.meaning[1]:
            new_rule_a_meaning = rule_a.meaning[0]
            new_rule_b_meaning = rule_b.meaning[0]
            new_rule_s_meaning = ("x", rule_a.meaning[1])
            meaning_var = "x"
            new_label = "A"

        splits = self.split_list(remaining, "-")
        non_terminal = new_label + ":" + meaning_var
        new_string_s = splits[0] + [non_terminal] + splits[1]
        new_rule_a = Rule(new_label, new_rule_a_meaning, chunk_a)
        new_rule_b = Rule(new_label, new_rule_b_meaning, chunk_b)
        new_rule_s = Rule("S", new_rule_s_meaning, new_string_s)
        self.rules.append(new_rule_a)
        self.rules.append(new_rule_b)
        self.rules.append(new_rule_s)
        self.rules.remove(rule_a)
        self.rules.remove(rule_b)
        return True

    # Do chunking where only one rule must be changed, assumed that one meaning contains a single meaning var
    def do_single_chunk(self, rule_a, rule_b, chunk_a, chunk_b, remaining):
        single_chunkable = False
        # Case where comp A's are concrete and equal and either rule (but not both) has a meaning variable for comp B
        if rule_a.meaning[0] == rule_b.meaning[0] and rule_a.meaning[1] != rule_b.meaning[1]:
            if (rule_a.meaning[1] not in self.a_comp or rule_b.meaning[1] not in self.b_comp) and rule_a.meaning[0] in self.a_comp:
                single_chunkable = True

        # Case where comp B's are concrete and equal and either rule (but not both) has a meaning variable for comp A
        elif rule_a.meaning[0] != rule_b.meaning[0] and rule_a.meaning[1] == rule_b.meaning[1]:
            if (rule_a.meaning[0] not in self.a_comp or rule_b.meaning[0] not in self.b_comp) and rule_a.meaning[1] in self.b_comp:
                single_chunkable = True

        # Case where rule_a has two meaning vars and rule_b has one
        elif rule_a.meaning[0] not in self.a_comp and rule_a.meaning[1] not in self.b_comp:
            if rule_b.meaning[0] not in self.a_comp and rule_b.meaning[1] in self.b_comp:
                single_chunkable = True
            elif rule_b.meaning[0] in self.a_comp and rule_b.meaning[1] not in self.b_comp:
                single_chunkable = True

        # Case where rule_b has two meaning vars and rule_a has one
        elif rule_b.meaning[0] not in self.a_comp and rule_b.meaning[1] not in self.b_comp:
            if rule_a.meaning[0] not in self.a_comp and rule_a.meaning[1] in self.b_comp:
                single_chunkable = True
            elif rule_a.meaning[0] in self.a_comp and rule_a.meaning[1] not in self.b_comp:
                single_chunkable = True

        if chunk_a is None:
            single_chunkable = False
        elif len(chunk_a) == 1 and len(chunk_a[0]) > 1 and len(chunk_b) == 1 and len(chunk_b[0]) > 1:
            single_chunkable = False
        elif (len(chunk_a) > 1 or len(chunk_a[0]) == 1) and (len(chunk_b) > 1 or len(chunk_b[0]) == 1):
            single_chunkable = False

        if not single_chunkable:
            return False

        if len(chunk_a) == 1 and len(chunk_a[0]) > 1:
            label = chunk_a[0].split(":")[0]
            if rule_a.meaning[0] not in self.a_comp:
                new_rule = Rule(label, rule_b.meaning[0], chunk_b)
                self.rules.append(new_rule)
            elif rule_a.meaning[1] not in self.b_comp:
                new_rule = Rule(label, rule_b.meaning[1], chunk_b)
                self.rules.append(new_rule)
            self.rules.remove(rule_b)
        else:
            label = chunk_b[0].split(":")[0]
            if rule_b.meaning[0] not in self.a_comp:
                new_rule = Rule(label, rule_a.meaning[0], chunk_a)
                self.rules.append(new_rule)
            elif rule_b.meaning[1] not in self.b_comp:
                new_rule = Rule(label, rule_a.meaning[1], chunk_a)
                self.rules.append(new_rule)
            self.rules.remove(rule_a)
        return True

    def do_substring(self, rule_a, rule_b, substring_marker):
        if substring_marker is None:
            return False
        if rule_a.meaning == rule_b.meaning[0]:
            new_string = rule_b.string[:substring_marker] + [rule_a.label + ":x"] + rule_b.string[
                                                                                    substring_marker + len(
                                                                                        rule_a.string):]
            new_rule = Rule("S", ("x", rule_b.meaning[1]), new_string)
            self.rules.append(new_rule)
            self.rules.remove(rule_b)
        if rule_a.meaning == rule_b.meaning[1]:
            new_string = rule_b.string[:substring_marker] + [rule_a.label + ":y"] + rule_b.string[
                                                                                    substring_marker + len(
                                                                                        rule_a.string):]
            new_rule = Rule("S", (rule_b.meaning[0], "y"), new_string)
            self.rules.append(new_rule)
            self.rules.remove(rule_b)
        return True

    def do_relabel(self, rule_a, rule_b):
        relabel = {}
        if rule_a.label == "S" and rule_b.label == "S" and len(rule_a.string) == len(rule_b.string) and rule_a.string != rule_b.string:
            for i in range(len(rule_a.string)):
                if rule_a.string[i] != rule_b.string[i] and (len(rule_a.string[i]) == 1 or len(rule_b.string[i]) == 1):
                    return False
                elif rule_a.string[i] != rule_b.string[i]:
                    a_meaning = rule_a.string[i].split(":")[1]
                    b_meaning = rule_b.string[i].split(":")[1]
                    a_label = rule_a.string[i].split(":")[0]
                    b_label = rule_b.string[i].split(":")[0]
                    if a_meaning == b_meaning:
                        relabel[a_label] = b_label
                    else:
                        return False
        else:
            return False

        for rule in self.rules:
            if rule.label in relabel.keys():
                rule.label = relabel[rule.label]
            for i in range(len(rule.string)):
                if len(rule.string[i]) > 1:
                    if rule.string[i].split(":")[0] in relabel.keys():
                        rule.string[i] = relabel[rule.string[i].split(":")[0]] + ":" + rule.string[i].split(":")[1]

        return True

    # Uses the generalisation rules on a specific pair of rules
    def generalise_pair(self, rule_a, rule_b):
        changed = False
        substring_marker = None

        if rule_b.label == "S" and rule_a.label != "S":
            if rule_a.meaning == rule_b.meaning[0] or rule_a.meaning == rule_b.meaning[0]:
                substring_marker = rule_a.is_substring(rule_b)

        if rule_a.label == "S" and rule_b.label == "S":
            chunk_a, chunk_b, remaining = self.chunk(rule_a.string, rule_b.string)
        else:
            chunk_a = None
            chunk_b = None
            remaining = None

        # Attempt relabel
        if not changed:
            changed = self.do_relabel(rule_a, rule_b)

        # Attempt single chunk
        if not changed:
            changed = self.do_single_chunk(rule_a, rule_b, chunk_a, chunk_b, remaining)

        # Attempt double chunk
        if not changed:
            changed = self.do_double_chunk(rule_a, rule_b, chunk_a, chunk_b, remaining)

        # Attempt substring
        if not changed:
            changed = self.do_substring(rule_a, rule_b, substring_marker)

        self.remove_duplicates()
        return changed

    # Incorporates the given rule into the grammar
    def incorporate(self, meaning, string):
        parsable, _, _ = self.parsable(meaning)
        if not parsable:
            self.rules.append(Rule("S", meaning, string))
            self.generalise()

    # Checks whether a given meaning can be parsed by the grammar
    # Returns bool parsable and Rule for the start rule to parse
    # TODO: Fix this
    def parsable(self, meaning):
        start_rules = self.get_rules_by_label("S", False)
        for rule in start_rules:
            non_t_labels = {non_t.split(":")[1]: non_t.split(":")[0] for non_t in rule.non_terminals}
            sub_rules = {}

            if rule.meaning[0] not in self.a_comp:
                sub_rule = self.get_rule(non_t_labels[rule.meaning[0]], meaning[0], True)
                if sub_rule is not None:
                    sub_rules[rule.meaning[0]] = sub_rule

            if rule.meaning[1] not in self.b_comp:
                sub_rule = self.get_rule(non_t_labels[rule.meaning[1]], meaning[1], True)
                if sub_rule is not None:
                    sub_rules[rule.meaning[1]] = sub_rule

            if rule.meaning[0] == meaning[0] or rule.meaning[0] in sub_rules.keys():
                if rule.meaning[1] == meaning[1] or rule.meaning[1] in sub_rules.keys():
                    return True, rule, sub_rules

        return False, None, None

    # Parses a meaning using a given start rule, only used on meanings that are known to be parsable
    def parse_rule(self, meaning, start_rule, sub_rules):
        output = []

        for item in start_rule.string:
            if len(item) == 1:
                output += item
            else:
                for sub_item in sub_rules[item.split(":")[1]].string:
                    output += sub_item

        return output