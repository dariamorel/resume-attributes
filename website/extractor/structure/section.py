import re
import locale

import yake

from ent import Ent
from ent import Object
from dictionaries import sections_dict

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


class Position(Section):
    def __init__(self, text, position=None):
        self.position = None
        if not position:
            super().__init__(text)
            self.position = self.__get_position(text)
        else:
            self.position = position

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
            return [position, specialization]
        if position:
            return [position]
        return [text]


class Skills(Section):
    def __init__(self, text):
        super().__init__(text)
        text = text.replace(',', ' ')
        self.objects = text.split()
