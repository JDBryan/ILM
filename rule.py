class Rule:
    def __init__(self, label, meaning, string):
        self.label = label
        self.meaning = meaning
        self.string = string
        self.non_terminals = {}

        for item in self.string:
            if len(item) > 1:
                meaning = item.split(":")[1]
                label = item.split(":")[0]
                self.non_terminals[meaning] = label

        if not self.is_valid():
            raise Exception("Invalid rule: " + str(self))

    def __repr__(self):
        string_str = ""
        for item in self.string:
            string_str += item

        if self.label == "S":
            meaning_str = "(" + self.meaning[0] + "," + self.meaning[1] + ")"
        else:
            meaning_str = self.meaning
        return self.label + ": " + meaning_str + " -> " + string_str

    def __eq__(self, other):
        return self.label == other.label and self.meaning == other.meaning and self.string == other.string

    def is_valid(self):
        if self.label != "S" or (self.meaning[0] != "x" and self.meaning[1] != "y"):
            valid = len(self.non_terminals) == 0
        elif self.meaning[1] != "y":
            valid = len(self.non_terminals) == 1 and "x" in self.non_terminals.keys()
        elif self.meaning[0] != "x":
            valid = len(self.non_terminals) == 1 and "y" in self.non_terminals.keys()
        else:
            valid = len(self.non_terminals) == 2 and "x" in self.non_terminals.keys() and "y" in self.non_terminals.keys()

    def is_substring(self, rule):
        for i in range(len(rule.string)):
            for j in range(len(self.string)):
                if i+j > len(rule.string) - 1 or rule.string[i+j] != self.string[j]:
                    break
                elif rule.string[i+j] == self.string[j] and j == len(self.string) - 1:
                    return i

        return None
