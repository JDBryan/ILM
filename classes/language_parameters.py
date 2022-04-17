class LanguageParameters:
    def __init__(self, alphabet, a_comp, b_comp, a_freqs=None, b_freqs=None):
        self.a_comp = a_comp
        self.b_comp = b_comp
        self.m_comp = a_comp + b_comp
        self.alphabet = [char for char in alphabet]
        self.meanings = [[x, y] for x in a_comp for y in b_comp]
        self.freq_list = []
        if a_freqs is None:
            a_freqs = {}
        if b_freqs is None:
            b_freqs = {}

        for a in self.a_comp:
            if a in a_freqs.keys():
                a_freq = a_freqs[a]
            else:
                a_freq = 1
            for b in self.b_comp:
                if b in b_freqs.keys():
                    b_freq = a_freqs[a]
                else:
                    b_freq = 1

                for i in range(a_freq + b_freq - 1):
                    self.freq_list.append((a, b))