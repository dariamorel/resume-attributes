import re
import locale
from .ent import Pair
from .dictionaries import languages_list
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    DatesExtractor,

    Doc, ORG, PER
)

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)


class Section:
    def __init__(self, text):
        spans_text = text.replace('\n', ", ")

        doc = Doc(spans_text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        # Извлекаем именованные сущности
        doc.tag_ner(ner_tagger)

        self.doc = doc

    def lemmatize(self, text):
        # Убираем лишние спецсимволы и пробелы в начале
        text = text.strip()
        if len(text) > 0 and not (text[0].isalpha() or text[0].isdigit()):
            text = text[1:].strip()

        # Переводим текст в нижний регистр
        text = text
        return text


class Position(Section):
    def __init__(self, text, position=None):
        self.position = None
        if not position:
            position = self.__get_position(text)
            super().__init__(position)
            position_array = []
            for sent in self.doc.sents:
                position_array.append(self.__normalize_sent(sent))
            self.position = position_array
        else:
            self.position = position

    def __normalize_sent(self, sent):
        string = sent.text
        while not string[0].isalpha():
            string = string[1:]
        return string

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


class Skills(Section):
    def __init__(self, text):
        super().__init__(text)
        self.skills = None
        # Если слова разделены несколькими пробелами
        if "  " in text:
            text = text.replace(',', ' ').replace('.', ' ').replace(';', ' ')
            self.skills = [skill.strip() for skill in text.split()]
        else:
            text = text.replace('\n', ', ').replace('.', ' ').replace(';', ' ')
            self.skills = [skill.strip() for skill in text.split(',')]

class Languages(Section):
    def __init__(self, text):
        super().__init__(text)

        languages = []
        for language_name in languages_list:
            info = self.__find_section(text, language_name)
            if info:
                info = self.lemmatize(info)
                languages.append(Pair(language_name, info))
        self.languages = languages

    def __find_section(self, text, section_name):
        pattern = '|'.join([f"\s{lang}\s|\s{lang}:" for lang in languages_list if lang != section_name])
        groups = re.search(rf'({section_name}\s|\s{section_name}:)(.*?)({pattern}|\Z)', text,
                            re.DOTALL | re.IGNORECASE)

        if groups:
            return groups.group(2)
        return None

