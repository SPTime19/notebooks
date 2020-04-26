from nltk.data import load

from nltk.stem.api import StemmerI

class RSLPStemmer(StemmerI):
    """
    A stemmer for Portuguese.

        >>> from nltk.stem import RSLPStemmer
        >>> st = RSLPStemmer()
        >>> # opening lines of Erico Verissimo's "Música ao Longe"
        >>> text = '''
        ... Clarissa risca com giz no quadro-negro a paisagem que os alunos
        ... devem copiar . Uma casinha de porta e janela , em cima duma
        ... coxilha .'''
        >>> for token in text.split():
        ...     print(st.stem(token))
        clariss risc com giz no quadro-negr a pais que os alun dev copi .
        uma cas de port e janel , em cim dum coxilh .
    """

    def __init__(self):
        self._model = []

        self._model.append(self.read_rule("step0.pt"))
        self._model.append(self.read_rule("step1.pt"))
        self._model.append(self.read_rule("step2.pt"))
        self._model.append(self.read_rule("step3.pt"))
        self._model.append(self.read_rule("step4.pt"))
        self._model.append(self.read_rule("step5.pt"))
        self._model.append(self.read_rule("step6.pt"))

    def read_rule(self, filename):
        rules = load("nltk:stemmers/rslp/" + filename, format="raw").decode("utf8")
        lines = rules.split("\n")

        lines = [line for line in lines if line != ""]  # remove blank lines
        lines = [line for line in lines if line[0] != "#"]  # remove comments

        # NOTE: a simple but ugly hack to make this parser happy with double '\t's
        lines = [line.replace("\t\t", "\t") for line in lines]

        # parse rules
        rules = []
        for line in lines:
            rule = []
            tokens = line.split("\t")

            # text to be searched for at the end of the string
            rule.append(tokens[0][1:-1])  # remove quotes

            # minimum stem size to perform the replacement
            rule.append(int(tokens[1]))

            # text to be replaced into
            rule.append(tokens[2][1:-1])  # remove quotes

            # exceptions to this rule
            rule.append([token[1:-1] for token in tokens[3].split(",")])

            # append to the results
            rules.append(rule)

        return rules


    def stem(self, word):
        word = word.lower()

        # the word ends in 's'? apply rule for plural reduction
        if word[-1] == "s":
            word = self.apply_rule(word, 0)

        # the word ends in 'a'? apply rule for feminine reduction
        if word[-1] == "a":
            word = self.apply_rule(word, 1)

        # augmentative reduction
        word = self.apply_rule(word, 3)

        # adverb reduction
        word = self.apply_rule(word, 2)

        # noun reduction
        prev_word = word
        word = self.apply_rule(word, 4)
        if word == prev_word:
            # verb reduction
            prev_word = word
            word = self.apply_rule(word, 5)
            if word == prev_word:
                # vowel removal
                word = self.apply_rule(word, 6)

        return word


    def apply_rule(self, word, rule_index):
        rules = self._model[rule_index]
        for rule in rules:
            suffix_length = len(rule[0])
            if word[-suffix_length:] == rule[0]:  # if suffix matches
                if len(word) >= suffix_length + rule[1]:  # if we have minimum size
                    if word not in rule[3]:  # if not an exception
                        word = word[:-suffix_length] + rule[2]
                        break

        return word