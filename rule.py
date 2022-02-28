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

    def validate(self, alphabet, comp_a, comp_b):
        valid = True
        if len(self.output) == 0:
            valid = False

        if self.label != "S":
            for item in self.output:
                if item not in alphabet:
                    valid = False
        else:
            if len(self.output) <= 1:
                valid = False

            meaning_labels = []
            for i in range(2):
                if self.meaning[i] not in comp_a + comp_b:
                    meaning_labels += self.meaning[i]
            output_labels = []
            for item in self.output:
                if item not in alphabet:
                    output_labels += item
            meaning_labels.sort()
            output_labels.sort()
            if meaning_labels != output_labels:
                valid = False

        if not valid:
            raise Exception("Invalid rule: " + str(self))

    def is_substring(self, rule):
        for i in range(len(rule.output)):
            for j in range(len(self.output)):
                if i+j > len(rule.output) - 1 or rule.output[i+j] != self.output[j]:
                    break
                elif rule.output[i+j] == self.output[j] and j == len(self.output) - 1:
                    return i

        return None
