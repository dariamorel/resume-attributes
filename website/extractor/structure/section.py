from .normalization import delete_additional_info

import locale
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

class Section:
    def __init__(self, text, delete_add_info=True):
        """
        Функция извлекает именованные сущности из текста, токенизирует текст и делает синтаксический и морфологический анализ.
        :param text: исходный текст
        :param delete_add_info: флаг, отвечающий за то, нужно ли убирать дополнительную информацию в скобках из текста
        """
        # Отчищаем текст от дополнительной информации
        if delete_add_info:
            text = delete_additional_info(text)

        # Заменяем символ '\n' на ',', чтобы упростить поиск именованных сущностей
        spans_text = text.replace('\n', ", ")

        doc = Doc(spans_text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        # Извлекаем именованные сущности
        doc.tag_ner(ner_tagger)

        self.spans = doc.spans

        # Токенизация изначального текста
        doc = Doc(text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        self.doc = doc

    @property
    def text(self):
        return self.doc.text