from .section import Section
from .normalization import delete_additional_info, normalize_sent
import re
from natasha import Doc, Segmenter
segmenter = Segmenter()


class Position(Section):
    def __init__(self, text, position=None):
        super().__init__(text)
        text = delete_additional_info(text)
        self.position = None
        if not position:
            position = self.__get_position(text)
            position = position.replace('.', ',').replace('\n', ', ').replace(';', ',')
            position = position.split(',')

        position_array = []
        for sent in position:
            # Берем максимум 10 позиций
            if len(position_array) >= 5:
                break
            normalized_sent = normalize_sent(sent, True)
            if normalized_sent:
                position_array.append(f"{normalized_sent}.")
        self.position = position_array

    def __get_position(self, text):
        position, specialization = None, None
        unnecessary = ['специализация', 'специализации', 'занятость', 'график работы',
                       'Желательное время в пути до работы']
        other = ['занятость', 'график работы',
                       'Желательное время в пути до работы']
        pattern1 = '|'.join([f"\s{name}\s|\s{name}:" for name in unnecessary])
        pattern2 = '|'.join([f"\s{name}\s|\s{name}:" for name in ['специализация', 'специализации']])
        pattern3 = '|'.join([f"\s{name}\s|\s{name}:" for name in other])
        specific_groups = re.search(rf'(.*?)({pattern1})', text,
                                    re.DOTALL | re.IGNORECASE)
        if specific_groups:
            position = specific_groups.group(1).strip()

        specific_groups = re.search(rf'({pattern2})(.*?)({pattern3}|\Z)', text,
                                    re.DOTALL | re.IGNORECASE)
        if specific_groups:
            specialization = specific_groups.group(2).strip()

        if position and specialization:
            return position + '\n' + specialization
        if position:
            return position
        return text