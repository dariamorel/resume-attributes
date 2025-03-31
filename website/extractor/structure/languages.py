from .section import Section
from .ent import Lang
from .dictionaries import  languages_list
from .normalization import normalize_sent

import re

class Languages(Section):
    def __init__(self, text):
        text = text.replace('\n', '')
        super().__init__(text, False)
        self.languages = self.__set_languages()

    def __set_languages(self) -> list[Lang]:
        """
        Функция делит тест на секции по языкам из languages_list
        :return: список с языками и информацией о них
        """
        languages = []
        for language_name in languages_list:
            # Пробегаемся по языкам
            info = self.__find_section(language_name)
            # Нашли секцию с таким языком
            if info:
                info = normalize_sent(info)
                if info:
                    languages.append(Lang(language_name, info))

        return languages

    def __find_section(self, section_name):
        """
        Функция ищет секцию с языком section_name в тексте
        :param section_name: название языка
        :return: информация об этом языке из текста
        """
        text = self.doc.text

        # Шаблон для поиска языка section_name
        pattern1 = f"{section_name} язык|{section_name} язык:|{section_name}\s|\s{section_name}:"
        # Шаблон для поиска любого другого языка, кроме section_name
        pattern2 = '|'.join([f"\s{lang}\s|\s{lang}:" for lang in languages_list if lang != section_name])
        # Поиск по шаблону
        groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z|\n)', text,
                            re.DOTALL | re.IGNORECASE)

        if groups:
            return groups.group(2)
        return None