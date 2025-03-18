import re

from natasha import PER

from ent import Ent
from section import Section


class MainInfo(Section):
    def __init__(self, text: str):
        super().__init__(text)

        name = self.__get_name()
        if name:
            self.name = Ent(name)

        phone_number = self.__get_phone_number(text)
        if phone_number:
            self.phone_number = Ent(phone_number)

        email = self.__get_email(text)
        if email:
            self.email = Ent(email)

        website = self.__get_website(text)
        if website:
            self.website = Ent(website)

        position = self.__get_position()
        if position:
            self.position = Ent(position)

    def get_info(self):
        result = [self.name, self.phone_number, self.email, self.website, self.position]
        return result

    def __get_name(self):
        for span in self.spans:
            if span.type == PER:
                return span

    def __get_phone_number(self, text: str):
        phone_pattern = re.compile(
            r"((\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})")
        return phone_pattern.search(text).group(1)

    def __get_email(self, text: str):
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        result = re.findall(email_pattern, text)
        if len(result) > 0:
            return result[0]

    def __get_website(self, text: str):
        link_pattern = r'https?://\S+|www\.\S+'
        result = re.findall(link_pattern, text)
        if len(result) > 0:
            return result[0]

    def __get_position(self):
        token_to_span = self.token_to_span(self.spans)

        # Ищем по ключевым словам
        for i, token in enumerate(self.doc.tokens):
            if token.text.lower() in ["должность", "position", "позиция"]:
                # Ищем первое существительное
                j = i + 1
                while self.doc.tokens[j].pos != "NOUN":
                    j += 1
                position = self.doc.tokens[j]
                # Проверяем, является ли сущностью
                if token_to_span[position.i] != -1:
                    return self.spans[token_to_span[position.i]]
                return position

        # Ищем первое существительное в именительном падеже
        for token in self.doc.tokens:
            if not (token.pos == "NOUN" and token.feats.get("Case") == "Nom"):
                continue
            # является ли именем
            if token_to_span[token.i] != -1 and self.spans[token_to_span[token.i]] == "PER":
                continue
            # является ли номером телефона
            if token.text in self.phone_number.text:
                continue
            # является ли какой-то другой свущностью
            if token_to_span[token.i] != -1:
                return self.spans[token_to_span[token.i]]
            return token