class Rule:
    def __init__(self, label, meaning, string):
        self.label = label
        self.meaning = meaning
        self.string = string
        self.non_terminals = []
        for item in self.string:
            if len(item) > 1:
                self.non_terminals.append(item)

    def __repr__(self):
        string_str = ""
        for item in self.string:
            string_str += item

        if self.label == "S":
            meaning_str = "(" + self.meaning[0] + "," + self.meaning[1] + ")"
        else:
            meaning_str = self.meaning
        return self.label + ": " + meaning_str + " -> " + string_str

    def meaning_match(self, meaning):
        if self.label == "S":
            if meaning[0] == self.meaning[0] or self.meaning[0] not in A_COMP:
                if meaning[1] == self.meaning[1] or self.meaning[1] not in B_COMP:
                    return True
        return False

    def is_substring(self, rule):
        for i in range(len(rule.string)):
            for j in range(len(self.string)):
                if i+j > len(rule.string) - 1 or rule.string[i+j] != self.string[j]:
                    break
                elif rule.string[i+j] == self.string[j] and j == len(self.string) - 1:
                    return i

        return None