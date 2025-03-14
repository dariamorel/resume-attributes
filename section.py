import time
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

import natasha
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER, ORG, LOC,
    NamesExtractor,
    DatesExtractor,

    Doc
)
from document import Document, Date
import re
from natasha.extractors import Match
from natasha import obj
from ent import Ent

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)

class Section:
    def __init__(self, text: str):
        # поиск именованных сущностей
        spans_doc = Doc(text.replace('\n', ", "))
        spans_doc.segment(segmenter)
        spans_doc.tag_ner(ner_tagger)
        spans_doc = Document(spans_doc)
        spans = spans_doc.spans

        # очистка текста и токенизация
        doc = Doc(re.sub(r'[.,?!]', '', text))
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)

        self.doc = Document(doc)

        self.spans = self.__add_tokens_to_spans(spans)

    def __add_tokens_to_spans(self, input_list: list):
        i, j = 0, 0
        token_list = list()

        while i < len(self.doc.tokens) and j < len(input_list):
            token = self.doc.tokens[i]
            cur_obj = input_list[j]
            if len(token_list) > 0 and cur_obj.tokens[-1].text in token.text:
                token_list.append(token)
                cur_obj.tokens = token_list.copy()
                cur_obj.start = token_list[0].start
                cur_obj.stop = token_list[-1].stop
                token_list.clear()
                i += 1
                j += 1
            elif len(token_list) > 0 and (len(token_list) < len(cur_obj.tokens) and cur_obj.tokens[len(token_list)].text in token.text):
                token_list.append(token)
                i += 1
            elif cur_obj.tokens[0].text in token.text and cur_obj.tokens[-1].text in token.text:
                cur_obj.tokens = [token]
                cur_obj.start = token.start
                cur_obj.stop = token.stop
                i += 1
                j += 1
            elif cur_obj.tokens[0].text in token.text:
                token_list.append(token)
                i += 1
            else:
                i += 1
        return input_list


class MainInfo(Section):
    pass


class Skills(Section):
    pass