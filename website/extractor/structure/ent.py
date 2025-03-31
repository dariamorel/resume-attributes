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
        self.__date = date
        self.__orgs = self.__filter_orgs(orgs)

    def __filter_orgs(self, orgs):
        """
        Функция фильтрует список организаций, чтобы лишние токены, к примеру, глаголы, не попали в список.
        """
        filtered_orgs = []
        for org in orgs:
            flag = True
            for token in org.tokens:
                # Анализируем отдельное слово, смотрим часть речи
                token_pos = morph_vocab(token.text)[0].pos
                if token_pos == 'VERB':
                    flag = False
            if flag:
                filtered_orgs.append(org)
        return filtered_orgs

    @property
    def orgs(self):
        result = ""

        for el in self.__orgs:
            result += f"{el.text}\n"

        return result

    @property
    def date(self):
        return self.__date.text

class Lang:
    def __init__(self, name, info):
        self.name = name
        self.info = info

class Name:
    def __init__(self, fact, text):
        self.fact = fact
        self.text = text



