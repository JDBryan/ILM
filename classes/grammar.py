from classes.rule import Rule
import random


class Grammar:
    def __init__(self, l_parameters, log):
        self.a_count = 1
        self.l_parameters = l_parameters
        self.categories = {"S": []}
        self.latest_rule = None
        self.log = log

    def __repr__(self):
        output = ""
        for rule in self.get_all_rules():
            output += rule.__repr__()
            output += "\n"
        return output

    # --SETTERS--

    def add_rule(self, rule):
        rule.validate(self.l_parameters)
        self.log.write("Adding rule " + str(rule) + "\n")
        if rule.label in self.categories.keys():
            self.categories[rule.label] += [rule]
        else:
            self.categories[rule.label] = [rule]
        self.latest_rule = rule

    def remove_rule(self, rule):
        self.log.write("Removing rule " + str(rule) + "\n")
        if rule.label in self.categories.keys():
            self.categories[rule.label].remove(rule)

    # --GETTERS--

    def get_random_meaning(self):
        # randint = random.randint(0, len(self.l_parameters.freq_list)-1)
        randint = random.randint(0, len(self.l_parameters.meanings) - 1)
        return self.l_parameters.meanings[randint]

    def get_all_rules(self):
        rules = []
        for category in self.categories.values():
            rules += category
        return rules

    def get_size(self):
        return len(self.get_all_rules())

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

    def get_all_sub_rules(self):
        rules = []
        for label in self.categories.keys():
            if label != "S":
                rules += self.get_category(label)
        return rules

    def get_closest_meaning(self, meaning):
        max_closeness = -1
        closest_meaning = None
        meaning_list = self.l_parameters.meanings
        random.shuffle(meaning_list)

        for full_meaning in meaning_list:
            if len(self.find_start_rules(full_meaning)) != 0:
                closeness = 0
                for i in range(2):
                    if full_meaning[i] == meaning[i]:
                        closeness += 1
                if closeness > max_closeness:
                    max_closeness = closeness
                    closest_meaning = full_meaning

        return closest_meaning

    # --VALIDATION--

    def validate_domain(self):
        domain = []
        a_comp = self.l_parameters.a_comp
        b_comp = self.l_parameters.b_comp
        for rule in self.get_category("S"):
            new_domain = rule.get_domain(self.get_all_sub_rules(), a_comp + b_comp)
            for meaning in new_domain:
                if meaning in domain:
                    raise Exception("Multiple utterances for meaning: " + meaning)

    def validate(self):
        for rule in self.get_all_rules():
            rule.validate(self.l_parameters)

    # --OTHER--

    def parse(self, meaning):
        start_rules = self.find_start_rules(meaning)
        shortest_parse = None

        for start_rule in start_rules:
            output = []

            for item in start_rule.output:
                if item in self.l_parameters.alphabet:
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

            if shortest_parse is None or len(shortest_parse) >= len(output):
                shortest_parse = output

        return shortest_parse

    def relabel(self, old_label, new_label):

        self.log.write("Relabelling " + old_label + " to " + new_label + "\n")

        if old_label == "S":
            return

        if old_label in self.categories.keys():
            new_category = self.categories.pop(old_label)
            if new_label in self.categories.keys():
                self.categories[new_label] += new_category
            else:
                self.categories[new_label] = new_category
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

    def invent(self, meaning):
        closest_meaning = self.get_closest_meaning(meaning)
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

        self.incorporate(meaning, invention)

        return invention

    def find_start_rules(self, meaning):
        meaning_components = self.l_parameters.a_comp + self.l_parameters.b_comp
        start_rules = []

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
                start_rules.append(rule)
        return start_rules

    def incorporate(self, meaning, string):
        start_rules = self.find_start_rules(meaning)
        if len(start_rules) == 0 or len(self.parse(meaning)) > len(string):
            print_string = ""
            for item in string:
                print_string += item
            self.log.write("Incorporating string '" + print_string + "' for meaning " + str(meaning) + "\n")
            self.add_rule(Rule("S", meaning, string))
            self.log.write("\n")
            self.log.write("Beginning generalisation\n")
            self.generalise()
            self.log.write("Finished generalisation\n\n")
        else:
            self.log.write("Already have shorter utterance for meaning" + str(meaning) + "\n\n")

    def generate_random_string(self):
        length = random.randint(1, 10)
        string = []
        for i in range(length):
            string += [self.l_parameters.alphabet[random.randint(0, 25)]]
        return string

    # --GENERALISATION

    def generalise(self):
        changed = True
        while changed:
            changed = False
            all_rules = self.get_all_rules()
            for i in range(len(all_rules)):
                if not changed:
                    rule_a = all_rules[i]
                    for j in range(len(all_rules)):
                        rule_b = all_rules[j]
                        if rule_a == rule_b:
                            continue
                        elif changed:
                            break
                        else:
                            changed = self.generalise_pair(rule_a, rule_b)
                else:
                    break
        # changed = True
        # while changed:
        #     changed = False
        #     all_rules = self.get_all_rules()
        #     if len(all_rules) > 1:
        #         for i in range(len(all_rules)):
        #             if changed:
        #                 break
        #             elif all_rules[i] == self.latest_rule:
        #                 continue
        #             else:
        #                 changed = self.generalise_pair(self.latest_rule, all_rules[i])
        #     else:
        #         changed = False

    def generalise_pair(self, rule_a, rule_b):
        old_grammar = str(self)

        changed = False

        # Attempt relabel
        if not changed:
            changed = self.attempt_relabel(rule_a, rule_b)
            if changed:
                self.remove_duplicates()
                self.log.write("Relabelling occurred on rules:\n" + str(rule_a) + "\n" + str(rule_b) + "\n\n")
                self.log.write("Old Grammar:\n" + old_grammar + "\nNew Grammar:\n" + str(self))
                self.validate()

        # Attempt chunk
        if not changed:
            changed = self.attempt_chunk(rule_a, rule_b)
            if changed:

                self.remove_duplicates()
                self.log.write("Chunking occurred on rules:\n" + str(rule_a) + "\n" + str(rule_b) + "\n")
                self.log.write("Old Grammar:\n" + old_grammar + "\nNew Grammar:\n" + str(self) + "\n")
                self.validate()

        # Attempt substring
        if not changed:
            changed = self.attempt_substring(rule_a, rule_b)
            if changed:
                self.remove_duplicates()
                self.log.write("Substring occurred on rules:\n" + str(rule_a) + "\n" + str(rule_b) + "\n")
                self.log.write("Old Grammar:\n" + old_grammar + "\nNew Grammar:\n" + str(self))
                self.validate()

        return changed

    def attempt_chunk(self, rule_a, rule_b):
        if rule_a.label == "S" and rule_b.label == "S":
            chunk_a, chunk_b, remaining = self.chunk(rule_a.output, rule_b.output)
        else:
            chunk_a = None
            chunk_b = None
            remaining = None

        if chunk_a is None or chunk_b is None:
            return False

        comparison = []
        meaning_components = self.l_parameters.a_comp + self.l_parameters.b_comp

        chunk_a_contains_label = False
        for item in chunk_a:
            if item not in self.l_parameters.alphabet:
                chunk_a_contains_label = True

        chunk_b_contains_label = False
        for item in chunk_b:
            if item not in self.l_parameters.alphabet:
                chunk_b_contains_label = True

        if chunk_a_contains_label and chunk_b_contains_label:
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

        changed = self.attempt_double_chunk(rule_a, rule_b, chunk_a, chunk_b, remaining, comparison)

        if changed:
            return True
        else:
            return self.attempt_single_chunk(rule_a, rule_b, chunk_a, chunk_b, comparison)

    def attempt_single_chunk(self, rule_a, rule_b, chunk_a, chunk_b, comparison):
        chunk_a_contains_label = False
        for item in chunk_a:
            if item not in self.l_parameters.alphabet:
                chunk_a_contains_label = True

        chunk_b_contains_label = False
        for item in chunk_b:
            if item not in self.l_parameters.alphabet:
                chunk_b_contains_label = True

        a_comp_single_chunkable = comparison[0] == "c=v" and (comparison[1] == "c=c" or comparison[1] == "v=v")
        b_comp_single_chunkable = comparison[1] == "c=v" and (comparison[0] == "c=c" or comparison[0] == "v=v")
        chunk_a_is_label = len(chunk_a) == 1 and chunk_a_contains_label
        chunk_b_is_label = len(chunk_b) == 1 and chunk_b_contains_label

        if (a_comp_single_chunkable or b_comp_single_chunkable) and (chunk_a_is_label or chunk_b_is_label):
            if chunk_a_is_label:
                if a_comp_single_chunkable:
                    new_rule = Rule(chunk_a[0], rule_b.meaning[0], chunk_b)
                else:
                    new_rule = Rule(chunk_a[0], rule_b.meaning[1], chunk_b)
                remove_rule = rule_b
            else:
                if a_comp_single_chunkable:
                    new_rule = Rule(chunk_b[0], rule_a.meaning[0], chunk_a)
                else:
                    new_rule = Rule(chunk_b[0], rule_a.meaning[1], chunk_a)
                remove_rule = rule_a

            self.add_rule(new_rule)
            self.remove_rule(remove_rule)

            return True

        return False

    def attempt_double_chunk(self, rule_a, rule_b, chunk_a, chunk_b, remaining, comparison):
        for item in (chunk_a + chunk_b):
            if item not in self.l_parameters.alphabet:
                return False

        b_comp_double_chunkable = (comparison[0] == "c=c" or comparison[0] == "v=v") and comparison[1] == "-"
        a_comp_double_chunkable = (comparison[1] == "c=c" or comparison[1] == "v=v") and comparison[0] == "-"

        if a_comp_double_chunkable or b_comp_double_chunkable:
            new_label = self.generate_label()
            splits = self.split_list(remaining, "-")
            new_string = splits[0] + [new_label] + splits[1]

            if b_comp_double_chunkable:
                new_a_rule = Rule(new_label, rule_a.meaning[1], chunk_a)
                new_b_rule = Rule(new_label, rule_b.meaning[1], chunk_b)
                new_s_rule = Rule("S", (rule_a.meaning[0], new_label), new_string)
            else:
                new_a_rule = Rule(new_label, rule_a.meaning[0], chunk_a)
                new_b_rule = Rule(new_label, rule_b.meaning[0], chunk_b)
                new_s_rule = Rule("S", (new_label, rule_a.meaning[1]), new_string)

            self.add_rule(new_s_rule)
            self.add_rule(new_a_rule)
            self.add_rule(new_b_rule)
            self.remove_rule(rule_a)
            self.remove_rule(rule_b)
            return True

        return False

    def attempt_substring(self, rule_a, rule_b):
        substring_marker = None

        if rule_b.label == "S" and rule_a.label != "S":
            if rule_a.meaning == rule_b.meaning[0] or rule_a.meaning == rule_b.meaning[1]:
                substring_marker = rule_a.is_proper_substring(rule_b)

        if substring_marker is None:
            return False
        if rule_a.meaning != rule_b.meaning[0] and rule_a.meaning != rule_b.meaning[1]:
            return False

        new_string = rule_b.output[:substring_marker] + [rule_a.label]
        new_string += rule_b.output[substring_marker + len(rule_a.output):]

        if rule_a.meaning == rule_b.meaning[0]:
            new_rule = Rule("S", (rule_a.label, rule_b.meaning[1]), new_string)
        else:
            new_rule = Rule("S", (rule_b.meaning[0], rule_a.label), new_string)

        self.add_rule(new_rule)
        self.remove_rule(rule_b)

        return True

    def attempt_relabel(self, rule_a, rule_b):
        alphabet = self.l_parameters.alphabet
        if rule_a.label != rule_b.label and rule_a.meaning == rule_b.meaning and rule_a.output == rule_b.output:
            self.relabel(rule_b.label, rule_a.label)
            return True

        if rule_a.label == "S" and rule_b.label == "S":

            relabel = {}
            for i in range(2):
                if rule_a.meaning[i] in alphabet and rule_b.meaning[i] in alphabet:
                    if rule_a.meaning[i] != rule_b.meaning[i]:
                        return False
                elif rule_a.meaning[i] not in alphabet and rule_b.meaning[i] not in alphabet:
                    relabel[rule_b.meaning[i]] = rule_a.meaning[i]
                else:
                    return False

            relabelled_b = []
            for char in rule_b.output:
                if char not in relabel.keys():
                    relabelled_b.append(char)
                else:
                    relabelled_b.append(relabel[char])

            if relabelled_b == rule_a.output:
                for old_label in relabel.keys():
                    new_label = relabel[old_label]
                    self.relabel(old_label, new_label)
                return True

        return False

    def remove_duplicates(self):
        changed = True
        while changed:
            changed = False
            all_rules = self.get_all_rules()
            for i in range(len(all_rules)):
                for j in range(len(all_rules)):
                    if i == j:
                        continue
                    elif all_rules[i].meaning == all_rules[j].meaning and all_rules[i].label == all_rules[j].label:
                        self.remove_rule(all_rules[j])
                        changed = True
                        break
                if changed:
                    break
        self.validate()

    # --STATIC--

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

        # if i >= j:
        #     chunk_a = string_a[i:]
        #     chunk_b = string_b[i:]
        #     remaining = string_a[:i] + ["-"]
        # else:
        #     chunk_a = string_a[:len_a-j]
        #     chunk_b = string_b[:len_b-j]
        #     remaining = ["-"] + string_a[len_a-j:]

        if (i == 0 and j == 0) or len(chunk_a) == 0 or len(chunk_b) == 0:
            return None, None, None
        else:
            return chunk_a, chunk_b, remaining

    def split_list(self, list_l, split_marker):
        marker = -1
        new_list = []
        for i in range(len(list_l)):
            if list_l[i] == split_marker:
                new_list.append(list_l[marker + 1:i])
                marker = i

        new_list.append(list_l[marker + 1:])
        return new_list

