from rule import Rule
import random


class Grammar:
    def __init__(self, a_comp, b_comp, alphabet):
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.alphabet = [x for x in alphabet]
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
        for category in self.categories.values():
            rules += category
        return rules

    def get_sub_rule(self, label, meaning):
        sub_rule = None
        if label in self.categories.keys():
            for rule in self.categories[label]:
                if rule.meaning == meaning:
                    sub_rule = rule
        return sub_rule

    def get_category(self, label):
        if label in self.categories.keys():
            return self.categories[label]
        else:
            return []

    def validate(self):
        for rule in self.get_all_rules():
            rule.validate(self.alphabet, self.a_comp, self.b_comp)

    def add_rule(self, rule):
        rule.validate(self.alphabet, self.a_comp, self.b_comp)
        if rule.label in self.categories.keys():
            self.categories[rule.label] += [rule]
        else:
            self.categories[rule.label] = [rule]

    def remove_rule(self, rule):
        if rule.label in self.categories.keys():
            self.categories[rule.label].remove(rule)

    def relabel(self, old_label, new_label):
        if old_label == "S":
            return

        if old_label in self.categories.keys():
            category = self.categories.pop(old_label)
            self.categories[new_label] = category
            for rule in self.categories[new_label]:
                rule.label = new_label

        for start_rule in self.get_category("S"):
            if old_label == start_rule.meaning[0] or old_label == start_rule.meaning[1]:
                for i in range(len(start_rule.output)):
                    if start_rule.output[i] == old_label:
                        start_rule.output[i] = new_label
            if old_label == start_rule.meaning[0]:
                start_rule.meaning = (new_label, start_rule.meaning[1])
            if old_label == start_rule.meaning[1]:
                start_rule.meaning = (start_rule.meaning[0], new_label)

        self.validate()

    def generate_label(self):
        label = "L" + str(self.a_count)
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

    def parse(self, meaning):
        start_rule = self.find_start_rule(meaning)
        self.validate()
        if start_rule is not None:
            output = []

            for item in start_rule.output:
                if item in self.alphabet:
                    output += item
                else:
                    if start_rule.meaning[0] == item:
                        sub_meaning = meaning[0]
                    else:
                        sub_meaning = meaning[1]
                    sub_rule = self.get_sub_rule(item, sub_meaning)
                    if sub_rule is None:
                        sub_rule = self.get_sub_rule("X", sub_meaning)
                    output += sub_rule.output

            return output
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
            if self.find_start_rule((i, meaning[1])) is not None:
                closest_meaning = (i, meaning[1])
                return closest_meaning

        for i in self.b_comp:
            if self.find_start_rule((meaning[0], i)) is not None:
                closest_meaning = (meaning[0], i)
                return closest_meaning

        for i in self.a_comp:
            for j in self.b_comp:
                if self.find_start_rule((i, j)) is not None:
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

        d1_rule = None
        d2_rule = None
        if intersection[0] == "d1":
            d1_rule = Rule("X", "d1", self.generate_random_string())
            self.add_rule(d1_rule)
        if intersection[1] == "d2":
            d2_rule = Rule("X", "d2", self.generate_random_string())
            self.add_rule(d2_rule)

        invention = self.parse(intersection)
        if invention is None:
            invention = self.generate_random_string()

        if d1_rule is not None:
            self.remove_rule(d1_rule)
        if d2_rule is not None:
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
                    elif all_rules[i] == all_rules[j]:
                        self.remove_rule(all_rules[j])
                        changed = True
                        break
                if changed:
                    break
        self.validate()

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
        meaning_components = self.a_comp + self.b_comp

        if chunk_a is None or chunk_b is None:
            return False

        for i in range(2):
            if rule_a.meaning[i] == rule_b.meaning[i] and rule_a.meaning[i] in meaning_components:
                comparison += ["c=c"]
            elif rule_a.meaning[i] not in meaning_components and rule_b.meaning[i] not in meaning_components:
                comparison += ["v=v"]
            elif rule_a.meaning[i] not in meaning_components or rule_b.meaning[i] not in meaning_components:
                comparison += ["c=v"]
            else:
                comparison += ["-"]

        a_comp_single_chunkable = comparison[0] == "c=v" and (comparison[1] == "c=c" or comparison[1] == "v=v")
        b_comp_single_chunkable = comparison[1] == "c=v" and (comparison[0] == "c=c" or comparison[0] == "v=v")
        chunk_a_is_label = len(chunk_a) == 1 and chunk_a[0] not in self.alphabet
        chunk_b_is_label = len(chunk_b) == 1 and chunk_b[0] not in self.alphabet

        if (a_comp_single_chunkable or b_comp_single_chunkable) and (chunk_a_is_label or chunk_b_is_label):
            if chunk_a_is_label:
                if a_comp_single_chunkable:
                    self.add_rule(Rule(chunk_a[0], rule_b.meaning[0], chunk_b))
                else:
                    self.add_rule(Rule(chunk_a[0], rule_b.meaning[1], chunk_b))
                self.remove_rule(rule_b)
            else:
                if a_comp_single_chunkable:
                    self.add_rule(Rule(chunk_b[0], rule_a.meaning[0], chunk_a))
                else:
                    self.add_rule(Rule(chunk_b[0], rule_a.meaning[1], chunk_a))
                self.remove_rule(rule_a)

            return True

        for item in (chunk_a + chunk_b):
            if item not in self.alphabet:
                return False

        b_comp_double_chunkable = (comparison[0] == "c=c" or comparison[0] == "v=v") and comparison[1] == "-"
        a_comp_double_chunkable = (comparison[1] == "c=c" or comparison[1] == "v=v") and comparison[0] == "-"

        if a_comp_double_chunkable or b_comp_double_chunkable:
            new_label = self.generate_label()
            splits = self.split_list(remaining, "-")
            new_string = splits[0] + [new_label] + splits[1]

            if b_comp_double_chunkable:
                self.add_rule(Rule(new_label, rule_a.meaning[1], chunk_a))
                self.add_rule(Rule(new_label, rule_b.meaning[1], chunk_b))
                self.add_rule(Rule("S", (rule_a.meaning[0], new_label), new_string))
            else:
                self.add_rule(Rule(new_label, rule_a.meaning[0], chunk_a))
                self.add_rule(Rule(new_label, rule_b.meaning[0], chunk_b))
                self.add_rule(Rule("S", (new_label, rule_a.meaning[1]), new_string))

            self.remove_rule(rule_a)
            self.remove_rule(rule_b)
            return True

        return False

    def do_substring(self, rule_a, rule_b, substring_marker):
        if substring_marker is None:
            return False
        if rule_a.meaning != rule_b.meaning[0] and rule_a.meaning != rule_b.meaning[1]:
            return False

        new_string = rule_b.output[:substring_marker] + [rule_a.label]
        new_string += rule_b.output[substring_marker + len(rule_a.output):]

        if rule_a.meaning == rule_b.meaning[0]:
            self.add_rule(Rule("S", (rule_a.label, rule_b.meaning[1]), new_string))
            self.remove_rule(rule_b)
        else:
            self.add_rule(Rule("S", (rule_b.meaning[0], rule_a.label), new_string))
            self.remove_rule(rule_b)
        return True

    def do_relabel(self, rule_a, rule_b):
        alpha = [i for i in self.alphabet]
        if rule_a.output == rule_b.output and rule_a.meaning == rule_b.meaning:
            self.relabel(rule_b.label, rule_a.label)
            return True

        if rule_a.label == "S" and rule_b.label == "S":
            if len(rule_a.output) == len(rule_b.output) and rule_a.output != rule_b.output:
                old_label = ""
                new_label = ""
                for i in range(len(rule_a.output)):
                    a_char = rule_a.output[i]
                    b_char = rule_b.output[i]
                    if a_char != b_char and a_char not in self.alphabet and b_char not in self.alphabet:
                        old_label = b_char
                        new_label = a_char
                    elif a_char != b_char:
                        return False
                if old_label != "":
                    self.relabel(old_label, new_label)

        return False

    # Uses the generalisation rules on a specific pair of rules
    def generalise_pair(self, rule_a, rule_b):
        changed = False
        substring_marker = None

        if rule_b.label == "S" and rule_a.label != "S":
            if rule_a.meaning == rule_b.meaning[0] or rule_a.meaning == rule_b.meaning[0]:
                substring_marker = rule_a.is_substring(rule_b)

        if rule_a.label == "S" and rule_b.label == "S":
            chunk_a, chunk_b, remaining = self.chunk(rule_a.output, rule_b.output)
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
        start_rule = self.find_start_rule(meaning)
        if start_rule is None:
            self.add_rule(Rule("S", meaning, string))
            self.generalise()

    def find_start_rule(self, meaning):
        meaning_components = self.a_comp + self.b_comp

        for rule in self.get_category("S"):
            found = True
            sub_rules = []
            for i in range(2):
                if rule.meaning[i] not in meaning_components:
                    sub_rule = self.get_sub_rule(rule.meaning[i], meaning[i])
                    if sub_rule is None:
                        sub_rule = self.get_sub_rule("X", meaning[i])
                    if sub_rule is None:
                        found = False
                    else:
                        sub_rules += [sub_rule]
                if rule.meaning[i] in meaning_components and rule.meaning[i] != meaning[i]:
                    found = False

            if found:
                return rule
        return None

