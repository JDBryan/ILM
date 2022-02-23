from rule import Rule
import random


class Grammar:
    def __init__(self, a_comp, b_comp, alphabet):
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.alphabet = alphabet
        self.meanings = [(x, y) for x in self.a_comp for y in self.b_comp]
        self.a_count = 1
        self.categories = {"S": []}

    def __repr__(self):
        output = ""
        for rule in self.get_all_rules():
            output += rule.__repr__()
            output += "\n"
        return output

    def get_all_rules(self):
        rules = []
        for category in self.categories:
            rules += category
        return rules

    def get_sub_rule(self, label, meaning):
        if label in self.categories.keys():
            for rule in self.categories[label]:
                if rule.meaning == meaning:
                    return rule

    def get_category(self, label):
        if label in self.categories.keys():
            return self.categories[label]
        else:
            return []

    def add_rule(self, rule):
        if rule.label in self.categories.keys():
            self.categories[rule.label] += [rule]
        else:
            self.categories[rule.label] = [rule]

    def remove_rule(self, rule):
        if rule.label in self.categories.keys():
            self.categories[rule.label].remove(rule)

    def relabel(self, old_label, new_label):
        if old_label in self.categories.keys():
            category = self.categories.pop(old_label)
            self.categories[new_label] = category

        for start_rule in self.get_category("S"):
            if old_label in start_rule.non_terminals.values():


    def generate_label(self):
        label = "A" + str(self.a_count)
        self.a_count += 1
        return label

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

    # Get all rules under a given label


    # Use grammar to find string for a given meaning
    # returns None if no string can be generated
    def parse(self, meaning):
        parsable, start_rule, sub_rules = self.parsable(meaning)
        if parsable:
            return self.parse_rule(start_rule, sub_rules)
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
        len_a = len(string_a)
        len_b = len(string_b)

        while i < min(len_a, len_b) and string_a[i] == string_b[i]:
            i += 1

        while j < min(len_a, len_b) and string_a[len_a - (1+j)] == string_b[len_b - (1+j)]:
            j += 1

        chunk_a = string_a[i:len_a - j]
        chunk_b = string_b[i:len_b - j]
        remaining = string_a[:i] + ["-"] + string_a[len_a - j:]

        if (i == 0 and j == 0) or len(chunk_a) == 0 or len(chunk_b) == 0:
            return None, None, None
        else:
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
            intersection = ("d1", meaning[1])
        else:
            intersection = ("d1", "d2")

        d1_rule = ""
        if intersection[0] == "d1":
            d1_rule = Rule("X", "d1", self.generate_random_string())
            self.add_rule(d1_rule)

        d2_rule = ""
        if intersection[1] == "d2":
            d2_rule = Rule("X", "d2", self.generate_random_string())
            self.add_rule(d2_rule)

        invention = self.parse(intersection)
        if invention is None:
            invention = self.generate_random_string()

        if intersection[0] == "d1":
            self.remove_rule(d1_rule)

        if intersection[1] == "d2":
            self.remove_rule(d2_rule)

        return invention

    def remove_duplicates(self):
        changed = True
        while changed:
            changed = False
            all_rules = self.get_all_rules()
            for i in range(len(all_rules)):
                for j in range(len(all_rules)):
                    if i == j:
                        continue
                    if changed:
                        break
                    if all_rules[i] == all_rules[j]:
                        self.remove_rule(all_rules[i])
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
        # changed = True
        # if len(self.rules) <= 1:
        #     return
        # while changed:
        #     i = 0
        #     j = 0
        #     while i == j:
        #         i = random.randint(0, len(self.rules) - 1)
        #         j = random.randint(0, len(self.rules) - 1)
        #     changed = self.generalise_pair(self.rules[i], self.rules[j])

        changed = True
        while changed:
            changed = False
            all_rules = self.get_all_rules()
            for i in range(len(all_rules)):
                if changed:
                    break
                else:
                    rule_a = all_rules[i]
                for j in range(len(all_rules)):
                    if i == j or changed:
                        break
                    else:
                        rule_b = all_rules[j]
                        changed = self.generalise_pair(rule_a, rule_b)

    def do_chunk(self, rule_a, rule_b, chunk_a, chunk_b, remaining):
        comparison = []

        if chunk_a is None or chunk_b is None:
            return False

        for i in range(2):
            if rule_a.meaning[i] == rule_b.meaning[i] and rule_a.meaning[i] in (self.a_comp + self.b_comp):
                comparison += ["c=c"]
            elif rule_a.meaning[i] == rule_b.meaning[i] and rule_a.meaning[i] not in (self.a_comp + self.b_comp):
                comparison += ["v=v"]
            elif rule_a.meaning[i] not in (self.a_comp + self.b_comp) or rule_b.meaning[i] not in (self.a_comp + self.b_comp):
                comparison += ["c=v"]
            else:
                comparison += ["-"]

        if comparison[0] == "c=v" and comparison[1] != "-":
            if len(chunk_a) == 1 and len(chunk_a[0]) > 1:
                label = chunk_a[0].split(":")[0]
                self.add_rule(Rule(label, rule_b.meaning[0], chunk_b))
                self.remove_rule(rule_b)
                return True
            elif len(chunk_b) == 1 and len(chunk_b[0]) > 1:
                label = chunk_b[0].split(":")[0]
                self.add_rule(Rule(label, rule_a.meaning[0], chunk_a))
                self.remove_rule(rule_a)
                return True
        elif comparison[1] == "c=v" and comparison[0] != "-":
            if len(chunk_a) == 1 and len(chunk_a[0]) > 1:
                label = chunk_a[0].split(":")[0]
                self.add_rule(Rule(label, rule_b.meaning[1], chunk_b))
                self.remove_rule(rule_a)
                return True
            elif len(chunk_b) == 1 and len(chunk_b[0]) > 1:
                label = chunk_b[0].split(":")[0]
                self.add_rule(Rule(label, rule_a.meaning[1], chunk_a))
                self.remove_rule(rule_a)
                return True

        for item in chunk_a + chunk_b:
            if len(item) > 1:
                return False

        if comparison[0] == "c=c" or comparison[0] == "v=v" and comparison[1] == "-":
            new_label = "B"
            splits = self.split_list(remaining, "-")
            non_terminal = new_label + ":" + "y"
            new_string = splits[0] + [non_terminal] + splits[1]
            new_a_rule = Rule(new_label, rule_a.meaning[1], chunk_a)
            new_b_rule = Rule(new_label, rule_b.meaning[1], chunk_b)
            self.add_rule(new_a_rule)
            self.add_rule(new_b_rule)
            self.add_rule(Rule("S", (rule_a.meaning[0], "y"), new_string))
            self.remove_rule(rule_a)
            self.remove_rule(rule_b)
            return True
        elif comparison[1] == "c=c" or comparison[1] == "v=v" and comparison[0] == "-":
            new_label = "A"
            splits = self.split_list(remaining, "-")
            non_terminal = new_label + ":" + "x"
            new_string = splits[0] + [non_terminal] + splits[1]
            new_a_rule = Rule(new_label, rule_a.meaning[0], chunk_a)
            new_b_rule = Rule(new_label, rule_b.meaning[0], chunk_b)
            new_s_rule = Rule("S", ("x", rule_a.meaning[1]), new_string)
            self.add_rule(new_a_rule)
            self.add_rule(new_b_rule)
            self.add_rule(new_s_rule)
            self.remove_rule(rule_a)
            self.remove_rule(rule_b)

            return True
        return False

    def do_substring(self, rule_a, rule_b, substring_marker):
        if substring_marker is None:
            return False
        if rule_a.meaning == rule_b.meaning[0]:
            new_string = rule_b.string[:substring_marker] + [rule_a.label + ":x"]
            new_string += rule_b.string[substring_marker + len(rule_a.string):]
            new_rule = Rule("S", ("x", rule_b.meaning[1]), new_string)
            self.add_rule(new_rule)
            self.remove_rule(rule_b)
        if rule_a.meaning == rule_b.meaning[1]:
            new_string = rule_b.string[:substring_marker] + [rule_a.label + ":y"]
            new_string += rule_b.string[substring_marker + len(rule_a.string):]
            new_rule = Rule("S", (rule_b.meaning[0], "y"), new_string)
            self.add_rule(new_rule)
            self.remove_rule(rule_b)
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

        elif rule_a.meaning == rule_b.meaning and rule_a.string == rule_b.string:
            rule_b.label = rule_a.label
            return True

        else:
            return False

        for rule in self.get_all_rules():
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

        # Attempt chunk
        if not changed:
            changed = self.do_chunk(rule_a, rule_b, chunk_a, chunk_b, remaining)

        # Attempt substring
        if not changed:
            changed = self.do_substring(rule_a, rule_b, substring_marker)

        self.remove_duplicates()
        return changed

    # Incorporates the given rule into the grammar
    def incorporate(self, meaning, string):
        parsable, _, _ = self.parsable(meaning)
        if not parsable:
            new_rule = Rule("S", meaning, string)
            self.add_rule(new_rule)
            self.generalise()

    # Checks whether a given meaning can be parsed by the grammar
    # Returns bool parsable and Rule for the start rule to parse
    # TODO: Fix this
    def parsable(self, meaning):
        start_rules = self.get_category("S")
        for rule in start_rules:
            sub_rules = {}

            if rule.meaning[0] not in self.a_comp:
                sub_rule = self.get_sub_rule(rule.non_terminals[rule.meaning[0]], meaning[0])
                if sub_rule is not None:
                    sub_rules[rule.meaning[0]] = sub_rule

            if rule.meaning[1] not in self.b_comp:
                sub_rule = self.get_sub_rule(rule.non_terminals[rule.meaning[1]], meaning[1])
                if sub_rule is not None:
                    sub_rules[rule.meaning[1]] = sub_rule

            if rule.meaning[0] == meaning[0] or rule.meaning[0] in sub_rules.keys():
                if rule.meaning[1] == meaning[1] or rule.meaning[1] in sub_rules.keys():
                    return True, rule, sub_rules

        return False, None, None

    # Parses a meaning using a given start rule, only used on meanings that are known to be parsable
    def parse_rule(self, start_rule, sub_rules):
        output = []

        for item in start_rule.string:
            if len(item) == 1:
                output += item
            else:
                for sub_item in sub_rules[item.split(":")[1]].string:
                    output += sub_item

        return output