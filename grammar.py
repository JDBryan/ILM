from rule import Rule
import random


class Grammar:
    def __init__(self, a_comp, b_comp, alphabet, name):
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.name = name
        self.alphabet = [x for x in alphabet]
        self.meanings = [(x, y) for x in self.a_comp for y in self.b_comp]
        self.a_count = 1
        self.categories = {"S": []}
        self.log = open("logs/" + name + ".txt", "w+")
        self.log.write("AGENT " + name + ":\n")

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

    def get_all_sub_rules(self):
        rules = []
        for label in self.categories.keys():
            if label != "S":
                rules += self.get_category(label)
        return rules

    def measure_compositionality(self):
        return len(self.get_all_rules())

    def get_category(self, label):
        if label in self.categories.keys():
            return self.categories[label]
        else:
            return []

    def validate_domain(self):
        domain = []
        for rule in self.get_category("S"):
            new_domain = rule.get_domain(self.get_all_sub_rules(), self.a_comp + self.b_comp)
            for meaning in new_domain:
                if meaning in domain:
                    raise Exception("Multiple utterances for meaning: " + meaning)

    def validate(self):
        for rule in self.get_all_rules():
            rule.validate(self.alphabet, self.a_comp, self.b_comp)

    def learn(self, teacher):
        meaning = self.meanings[random.randint(0, len(self.meanings) - 1)]
        utterance = teacher.parse(meaning)
        if utterance is None:
            utterance = teacher.invent(meaning)
        utterance_string = ""
        for char in utterance:
            utterance_string += char
        self.log.write("Learning utterance " + utterance_string + " for meaning " + str(meaning) + " from teacher " + teacher.name + "\n")
        self.incorporate(meaning, utterance)

    def add_rule(self, rule):
        rule.validate(self.alphabet, self.a_comp, self.b_comp)
        self.log.write("Adding rule " + str(rule) + "\n")
        if rule.label in self.categories.keys():
            self.categories[rule.label] += [rule]
        else:
            self.categories[rule.label] = [rule]

    def remove_rule(self, rule):
        self.log.write("Removing rule " + str(rule) + "\n")
        if rule.label in self.categories.keys():
            self.categories[rule.label].remove(rule)

    def relabel(self, old_label, new_label):

        self.log.write("Relabelling " + old_label + " to " + new_label + "\n")

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

    def get_word_table(self):
        output = " xx "
        for a in self.a_comp:
            output += "| " + a + " "
        output += "\n"
        for b in self.b_comp:
            output += " " + b + " "
            for a in self.a_comp:
                meaning = (a, b)
                result = self.parse(meaning)
                if result is None:
                    new_result = "-"
                else:
                    new_result = ""
                    for item in result:
                        new_result += item
                output += "| " + new_result + " "
            output += "\n"
        return output

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
        max_closeness = -1
        closest_meaning = None
        meaning_list = self.meanings
        random.shuffle(meaning_list)

        for full_meaning in meaning_list:
            if self.find_start_rule(full_meaning) is not None:
                closeness = 0
                for i in range(2):
                    if full_meaning[i] == meaning[i]:
                        closeness += 1
                if closeness > max_closeness:
                    max_closeness = closeness
                    closest_meaning = full_meaning

        return closest_meaning

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
                    elif all_rules[i].meaning == all_rules[j].meaning and all_rules[i].label == all_rules[j].label:
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

    def generalise_pair(self, rule_a, rule_b):
        old_grammar = str(self)

        changed = False

        # Attempt relabel
        if not changed:
            changed = self.attempt_relabel(rule_a, rule_b)
            if changed:
                self.remove_duplicates()
                self.log.write("Relabelling occurred on rules:\n" + str(rule_a) + "\n" + str(rule_b) + "\n")
                self.log.write("Old Grammar:\n" + old_grammar + "\nNew Grammar:\n" + str(self))
                self.validate()

        # Attempt chunk
        if not changed:
            changed = self.attempt_chunk(rule_a, rule_b)
            if changed:

                self.remove_duplicates()
                self.log.write("Chunking occurred on rules:\n" + str(rule_a) + "\n" + str(rule_b) + "\n")
                self.log.write("Old Grammar:\n" + old_grammar + "\nNew Grammar:\n" + str(self))
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

        comparison = []
        meaning_components = self.a_comp + self.b_comp

        if chunk_a is None or chunk_b is None:
            return False

        chunk_a_contains_label = False
        for item in chunk_a:
            if item not in self.alphabet:
                chunk_a_contains_label = True

        chunk_b_contains_label = False
        for item in chunk_b:
            if item not in self.alphabet:
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

        a_comp_single_chunkable = comparison[0] == "c=v" and (comparison[1] == "c=c" or comparison[1] == "v=v")
        b_comp_single_chunkable = comparison[1] == "c=v" and (comparison[0] == "c=c" or comparison[0] == "v=v")
        chunk_a_is_label = len(chunk_a) == 1 and chunk_a_contains_label
        chunk_b_is_label = len(chunk_b) == 1 and chunk_b_contains_label

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

    def attempt_substring(self, rule_a, rule_b):
        substring_marker = None

        if rule_b.label == "S" and rule_a.label != "S":
            if rule_a.meaning == rule_b.meaning[0] or rule_a.meaning == rule_b.meaning[0]:
                substring_marker = rule_a.is_substring(rule_b)

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

    def attempt_relabel(self, rule_a, rule_b):
        if rule_a.label != "S" and rule_a.meaning == rule_b.meaning:
            self.relabel(rule_b.label, rule_a.label)
            return True

        if rule_a.label == "S" and rule_b.label == "S":

            relabel = {}
            for i in range(2):
                if rule_a.meaning[i] in self.alphabet and rule_b.meaning[i] in self.alphabet:
                    if rule_a.meaning[i] != rule_b.meaning[i]:
                        return False
                elif rule_a.meaning[i] not in self.alphabet and rule_b.meaning[i] not in self.alphabet:
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

    def incorporate(self, meaning, string):
        start_rule = self.find_start_rule(meaning)
        if start_rule is None:
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
            self.log.write("Already have utterance for meaning" + str(meaning) + "\n\n")

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

