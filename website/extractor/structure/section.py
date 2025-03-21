from document import Document, Date
import re
import locale

from ent import Ent

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    DatesExtractor,

    Doc
)

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
        spans_doc = Doc(text.replace('\n', ". "))
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

    def __add_tokens_to_spans(self, spans: list):
        """
        Функция добавляет правильные токены именованным сущностям.
        """
        i, j = 0, 0
        token_list = list()

        while i < len(self.doc.tokens) and j < len(spans):
            token, span = self.doc.tokens[i], spans[j]

            if token.text in [span_token.text for span_token in span.tokens]:
                token_list.append(token)
            elif len(token_list) > 0:
                span.tokens = token_list.copy()
                span.start = span.tokens[0].start
                span.stop = span.tokens[-1].stop
                token_list.clear()
                j += 1
                continue
            i += 1

        if len(token_list) > 0:
            spans[j].tokens = token_list
            spans[j].start = spans[j].tokens[0].start
            spans[j].stop = spans[j].tokens[-1].stop

        return spans

    def token_to_span(self, spans: list):
        """
        :return: словарь, где каждому токену соответствует индекс cущности, которой он принадлежит
        """
        token_to_span = {i: -1 for i in range(len(self.doc.tokens))}
        for i, span in enumerate(spans):
            for token in span.tokens:
                token_to_span[token.i] = i
        return token_to_span


class Skills(Section):
    def __init__(self, text: str):
        super().__init__(text)
        self.skills = [Ent(obj.strip()) for obj in re.split(r'[., \n]', text) if obj.strip() != '']

    def get_info(self):
        return self.skills
