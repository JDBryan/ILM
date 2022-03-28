class Rule:
    def __init__(self, label, meaning, output):
        self.label = label
        self.meaning = meaning
        self.output = output

    def __repr__(self):
        string_str = ""
        for item in self.output:
            string_str += item

        if self.label == "S":
            meaning_str = "(" + self.meaning[0] + "," + self.meaning[1] + ")"
        else:
            meaning_str = self.meaning
        return self.label + ": " + meaning_str + " -> " + string_str

    def __eq__(self, other):
        return self.label == other.label and self.meaning == other.meaning and self.output == other.output

    def validate(self, l_parameters):
        valid = True
        if len(self.output) == 0:
            valid = False

        if self.label != "S":
            for item in self.output:
                if item not in l_parameters.alphabet:
                    valid = False
        else:

            # if self.meaning[0] == self.meaning[1]:
            #     valid = False

            meaning_labels = []
            for i in range(2):
                if self.meaning[i] not in l_parameters.a_comp + l_parameters.b_comp:
                    meaning_labels += self.meaning[i]
            output_labels = []
            for item in self.output:
                if item not in l_parameters.alphabet:
                    output_labels += item
            meaning_labels.sort()
            output_labels.sort()
            if meaning_labels != output_labels:
                valid = False

        if not valid:
            raise Exception("Invalid rule: " + str(self))

    def get_domain(self, sub_rules, meaning_comps):
        a_comp = []
        b_comp = []

        if self.meaning[0] in meaning_comps:
            a_comp = [self.meaning[0]]
        else:
            for rule in sub_rules:
                if rule.label == self.meaning[0]:
                    a_comp.append(rule.meaning)

        if self.meaning[1] in meaning_comps:
            b_comp = [self.meaning[1]]
        else:
            for rule in sub_rules:
                if rule.label == self.meaning[1]:
                    b_comp.append(rule.meaning)

        return [(a,b) for a in a_comp for b in b_comp]

    def is_proper_substring(self, rule):
        if len(self.output) >= len(rule.output):
            return None
        for i in range(len(rule.output)):
            # i = 0
            for j in range(len(self.output)):
                if i+j > len(rule.output) - 1 or rule.output[i+j] != self.output[j]:
                    break
                elif rule.output[i+j] == self.output[j] and j == len(self.output) - 1:
                    return i

        return None
