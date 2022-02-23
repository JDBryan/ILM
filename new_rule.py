class StartCategory:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule):
        self.rules[rule.meaning] = rule

    def remove_rule(self, rule):
        self.rules.pop(rule.meaning)

    def meaning_match(self, meaning):
        matches = []
        for rule_meaning in self.rules.keys():
            if is_match(meaning, rule_meaning):
                matches += rule_meaning
        return matches

    def get_start_rule(self, meaning):
        matches = self.meaning_match(meaning)
        for rule_meaning in matches:
            parsable = True
            for meaning_component in rule_meaning:
                if is_meaning_var(meaning_component):
                    concrete_component = get_concrete_from_var(meaning_component, meaning)
                    if not self.rules[rule_meaning].can_parse(concrete_component):
                        parsable = False
                else:
                    if not self.rules[rule_meaning].can_parse(meaning_component):
                        parsable = False
            if parsable:
                return rule_meaning
        return None

    def parse(self, meaning):
        start_rule = self.get_start_rule(meaning)
        top_level = self.rules[meaning]
        output = []


        for item in top_level:
            if is_meaning_var(item[0]):
                concrete_meaning = get_concrete_from_var(item[0], meaning)
                output += item[1].parse(concrete_meaning)
            else:
                output += item

class SubCategory:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule):
        self.rules[rule.meaning] = rule

    def remove_rule(self, rule):
        self.rules.pop(rule.meaning)

    def can_parse(self, meaning):
        return meaning in self.rules.keys()

    def parse(self, meaning):
        if self.can_parse(meaning):
            return self.rules[meaning].string


class CatGrammar:
    def __init__(self, alphabet, comp_a, comp_b):
        self.alphabet = alphabet
        self.comp_a = comp_a
        self.comp_b = comp_b
        self.meanings = [(x, y) for x in comp_a for y in comp_b]
        self.start_category = StartCategory()
        self.sub_categories = {}

    def parse(self, meaning):
        if self.start_category.contains_meaning(meaning):
            return self.start_category.parse(meaning)

# =====================================================================================================================

def is_meaning_var(input):
    return input == "X" or input == "Y"

def get_concrete_from_var(var, meaning):
    if var == "X":
        return meaning[0]
    else:
        return meaning[1]

def is_match(concrete_meaning, rule_meaning):
    if concrete_meaning[0] == rule_meaning[0] or is_meaning_var(concrete_meaning[0]):
        if concrete_meaning[1] == rule_meaning[1] or is_meaning_var(concrete_meaning[1]):
            return True