from section import Section
from normalization import normalize_sent

import re
from natasha import Segmenter

segmenter = Segmenter()

class Position(Section):
    def __init__(self, text, position=None):
        """
        :param text: исходный текст
        :param position: готовый список позиций, если он есть
        """
        super().__init__(text)
        self.position = None

        # Если нет готового списка с позициями, то извлекаем позиции из текста
        if not position:
            position = self.__get_position()
            position = position.replace('.', ',').replace('\n', ', ').replace(';', ',')
            position = position.split(',')

        position_array = []
        for sent in position:
            # Берем максимум 5 позиций
            if len(position_array) >= 5:
                break
            # Нормализуем позицию
            normalized_sent = normalize_sent(sent, True)
            if normalized_sent:
                position_array.append(f"{normalized_sent}.")
        self.position = position_array

    def __get_position(self):
        """
        Функция извлекает из текста конкретную долэность и специализацию, если она есть.
        :return: фрагмент текста с должностью и специализацией
        """
        text = self.doc.text
        position, specialization = None, None

        # Изщем подсекцию внутри секции
        unnecessary = ['специализация', 'специализации', 'занятость', 'график работы',
                       'Желательное время в пути до работы']
        other = ['занятость', 'график работы',
                       'Желательное время в пути до работы']
        # Шаблон для поиска подсекции должность
        pattern1 = '|'.join([f"\s{name}\s|\s{name}:" for name in unnecessary])
        # Шаблон для поиска подсекции специализация
        pattern2 = '|'.join([f"\s{name}\s|\s{name}:" for name in ['специализация', 'специализации']])
        # Шаблон с остальными подсекциями
        pattern3 = '|'.join([f"\s{name}\s|\s{name}:" for name in other])

        # Ищем подсекцию должность
        specific_groups = re.search(rf'(.*?)({pattern1})', text,
                                    re.DOTALL | re.IGNORECASE)
        if specific_groups:
            position = specific_groups.group(1).strip()

        # Ищем подсекцию специализация
        specific_groups = re.search(rf'({pattern2})(.*?)({pattern3}|\Z)', text,
                                    re.DOTALL | re.IGNORECASE)
        if specific_groups:
            specialization = specific_groups.group(2).strip()

        # Если есть и должность, и специализация, берем все.
        if position and specialization:
            return position + '\n' + specialization
        # Если есть только должность, берем ее.
        if position:
            return position
        # Иначе возвращаем исходный текст (это значит, что в тексте нет подсекций и весь текст подходит).
        return text