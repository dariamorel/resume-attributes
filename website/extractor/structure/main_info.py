from .section import Section
from .ent import Name
from .normalization import name_to_str, lemmatize_phone_number

import re
from natasha import MorphVocab, NamesExtractor

morph_vocab = MorphVocab()
names_extractor = NamesExtractor(morph_vocab)

def is_upper(fact):
    """
    Функция проверяет, написан ли каждый элемент fact с заглавной буквы. Если нет, то возвращает false, так как это не имя.
    :param fact: ФИО формата fact
    """
    if fact.first and not fact.first[0].isupper():
        return False
    if fact.last and not fact.last[0].isupper():
        return False
    if fact.middle and not fact.middle[0].isupper():
        return False
    return True

class MainInfo(Section):
    def __init__(self, text: str):
        super().__init__(text, False)
        self.name = None
        self.phone_number = None
        self.email = None
        self.website = None
        self.position = None

        name_fact, name_text = self.__get_name()
        if name_fact:
            self.name = Name(name_fact, name_text)

        phone_number = self.__get_phone_number()
        if phone_number:
            self.phone_number = phone_number

        email = self.__get_email()
        if email:
            self.email = email

        website = self.__get_website()
        if website:
            self.website = website


    def __get_name(self):
        """
        Функция извлекает ФИО из исходного текста.
        :return: fact имени и его строковое представление
        """
        text = self.doc.text
        result = None

        # Извлекаем имена из исходного текста
        names = names_extractor(text)
        for name in names:
            result = name
            break

        # Форматируем текст, убирая все знаки пробела ли переноса строки
        names_text = re.sub(r'\s+', ' ', text)
        # Извлекаем имена из отформатированного текста
        names = names_extractor(names_text)

        for name in names:
            # Если на первом этапе имен не нашли, берем name
            if not result:
                return name.fact, name_to_str(name.fact)

            # Иначе берем самое длинное имя (Так больше вероятности, что в return попадет полное ФИО)
            result_text = name_to_str(result.fact)
            name_text = name_to_str(name.fact)
            if len(result_text) > len(name_text):
                # Дополнительная проверка, что найденная сущность действительно имя
                if is_upper(result.fact):
                    return result.fact, result_text
                return None, None
            # Дополнительная проверка, что найденная сущность действительно имя
            if is_upper(name.fact):
                return name.fact, name_text
            return None, None
        return None, None

    def __get_phone_number(self):
        """
        Функция ищет номер телефона в исходном тексте.
        """
        text = self.doc.text

        phone_pattern = re.compile(
            r"((\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})")
        groups = phone_pattern.search(text)
        if groups:
            number = groups.group(1)
            # Приводим номер телефона к единному формату
            return lemmatize_phone_number(number)
        return None

    def __get_email(self):
        """
        Функция ищет email в исходном тексте.
        """
        text = self.doc.text
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        result = re.findall(email_pattern, text)
        if len(result) > 0:
            return result[0]

    def __get_website(self):
        """
        Функция ищет вебсайт в исходном тексте.
        """
        text = self.doc.text

        link_pattern = r'https?://\S+|www\.\S+'
        result = re.findall(link_pattern, text, re.IGNORECASE)
        if len(result) > 0:
            return result[0].strip()

        link_pattern = r'\b[a-zA-Z0-9-/]+\.[a-zA-Z0-9/]+'
        result = re.findall(link_pattern, text, re.IGNORECASE)
        for res in result:
            # Проверяем,чтобы не являлся частью email
            if res.strip() not in self.email:
                return res.strip()
        return None