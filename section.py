from document import Document, Date
import re
import time
from datetime import datetime
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

    PER, ORG, LOC,
    NamesExtractor,
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


class MainInfo(Section):
    def __init__(self, text: str):
        super().__init__(text)

        name = self.__get_name()
        if name:
            self.name = Ent(name)

        phone_number = self.__get_phone_number(text)
        if phone_number:
            self.phone_number = Ent(phone_number)

        email = self.__get_email(text)
        if email:
            self.email = Ent(email)

        website = self.__get_website(text)
        if website:
            self.website = Ent(website)

        position = self.__get_position()
        if position:
            self.position = Ent(position)

    def get_info(self):
        result = [self.name, self.phone_number, self.email, self.website, self.position]
        return result

    def __get_name(self):
        for span in self.spans:
            if span.type == PER:
                return span

    def __get_phone_number(self, text: str):
        phone_pattern = re.compile(
            r"((\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})")
        return phone_pattern.search(text).group(1)

    def __get_email(self, text: str):
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        result = re.findall(email_pattern, text)
        if len(result) > 0:
            return result[0]

    def __get_website(self, text: str):
        link_pattern = r'https?://\S+|www\.\S+'
        result = re.findall(link_pattern, text)
        if len(result) > 0:
            return result[0]

    def __get_position(self):
        token_to_span = self.token_to_span(self.spans)

        # Ищем по ключевым словам
        for i, token in enumerate(self.doc.tokens):
            if token.text.lower() in ["должность", "position", "позиция"]:
                # Ищем первое существительное
                j = i + 1
                while self.doc.tokens[j].pos != "NOUN":
                    j += 1
                position = self.doc.tokens[j]
                # Проверяем, является ли сущностью
                if token_to_span[position.i] != -1:
                    return self.spans[token_to_span[position.i]]
                return position

        # Ищем первое существительное в именительном падеже
        for token in self.doc.tokens:
            if not (token.pos == "NOUN" and token.feats.get("Case") == "Nom"):
                continue
            # является ли именем
            if token_to_span[token.i] != -1 and self.spans[token_to_span[token.i]] == "PER":
                continue
            # является ли номером телефона
            if token.text in self.phone_number.text:
                continue
            # является ли какой-то другой свущностью
            if token_to_span[token.i] != -1:
                return self.spans[token_to_span[token.i]]
            return token


class Skills(Section):
    def __init__(self, text: str):
        super().__init__(text)
        self.skills = [Ent(obj.strip()) for obj in re.split(r'[., \n]', text) if obj.strip() != '']

    def get_info(self):
        return self.skills
