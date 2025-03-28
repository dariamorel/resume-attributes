from natasha import MorphVocab
morph_vocab = MorphVocab()

class Ent:
    def __init__(self, input_type, input_text, start, stop, tokens=None):
        if input_type not in ["DATE", "ORG"]:
            raise ValueError("Invalid type of object.")
        self.type = input_type
        self.text = input_text
        self.start = start
        self.stop = stop
        self.tokens = tokens

class Object:
    def __init__(self, date, orgs: list):
        self.date = date
        self.org = self.__filter_orgs(orgs)

    def __filter_orgs(self, orgs):
        filtered_orgs = []
        for org in orgs:
            flag = True
            for token in org.tokens:
                # анализируем отдельное слово, смотрим часть речи
                token_pos = morph_vocab(token.text)[0].pos
                if token_pos == 'VERB':
                    flag = False
            if flag:
                filtered_orgs.append(org)
        return filtered_orgs

    @property
    def text(self):
        result = ""

        for el in self.org:
            result += f"{el.text}\n"

        return result

class Pair:
    def __init__(self, name, info):
        self.name = name
        self.info = info





