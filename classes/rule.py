class Rule:
    def __init__(self, label, meaning, output, l_parameters):
        self.label = label
        self.meaning = list(meaning)
        self.output = output
        self.l_parameters = l_parameters

    def __repr__(self):
        string_str = ""
        for item in self.output:
            string_str += item

        if self.label == "S":
            meaning_str = "(" + self.meaning[0] + "," + self.meaning[1] + ")"
        else:
            meaning_str = self.meaning[0]
        return self.label + ": " + meaning_str + " -> " + string_str

    def __eq__(self, other):
        return self.label == other.label and self.meaning == other.meaning and self.output == other.output

    def set_parameters(self, new_params):
        self.l_parameters = new_params

    def relabel(self, old_label, new_label):
        if self.label == old_label:
            self.label = new_label

        for i in range(len(self.meaning)):
            if self.meaning[i] == old_label:
                self.meaning[i] = new_label

        for i in range(len(self.output)):
            if self.output[i] == old_label:
                self.output[i] = new_label

    def validate(self, l_parameters):
        valid = True
        if len(self.output) == 0:
            valid = False

        if self.label != "S":
            for item in self.output:
                if item not in l_parameters.alphabet:
                    valid = False
        else:
            meaning_labels = []
            for i in range(2):
                if self.meaning[i] not in l_parameters.m_comp:
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

    def is_proper_substring(self, rule):
        if len(self.output) >= len(rule.output):
            return None
        for i in range(len(rule.output)):
            for j in range(len(self.output)):
                if i+j > len(rule.output) - 1 or rule.output[i+j] != self.output[j]:
                    break
                elif rule.output[i+j] == self.output[j] and j == len(self.output) - 1:
                    return i

        return None
