from .section import Section
from .dictionaries import sections_dict
from .normalization import normalize_sent

import re

class Skills(Section):
    def __init__(self, text):
        # Ищем подсекцию навыки в секции, если она есть, чтобы отделить от лишней информации.
        pattern1 = '|'.join([f"\s{name}\s|\s{name}:" for name in sections_dict["skills"]])
        pattern2 = '|'.join([f"\s{name}\s|\s{name}:" for name in sections_dict["languages"]])
        specific_groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z)', text,
                                    re.DOTALL | re.IGNORECASE)
        if specific_groups:
            text = specific_groups.group(2).strip()

        super().__init__(text)
        self.skills = self.__set_skills()

    def __set_skills(self) -> list[str]:
        """
        Функция определяет, как именно выглядят навыки в данном резюме, делит текст на список навыков и нормализует их.
        :return: список навыков
        """
        text = self.doc.text

        # Case 1. Навыки разделены пробелами
        if "   " in text:
            text = text.replace('\n', '   ').replace(',', '   ').replace(';', '   ')
            return [normalized_skill for skill in text.split("   ") if
                    (normalized_skill := normalize_sent(skill))]
        if not any([symb in text for symb in [',', '.', ';']]):
            text = text.replace('\n', ' ')
            return [normalized_skill for skill in text.split() if (normalized_skill := normalize_sent(skill))]

        # Case 2. Навыки разделены запятыми
        if ',' in [token.text for token in self.doc.tokens[:5]]:
            text = text.replace('\n', ' ').replace(';', ',')
            return [normalized_skill for skill in text.split(',') if (normalized_skill := normalize_sent(skill))]

        # Case 3. Навыки имеют структуру предложений
        text = text.replace('\n', ' ')
        return [f"{normalized_skill}." for skill in text.split('.') if
                (normalized_skill := normalize_sent(skill))]