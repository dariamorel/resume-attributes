import re

from natasha import PER

from ent import Ent, Object
from section import Section
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    DatesExtractor,

    Doc, ORG, PER, LOC
)
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)

class MainInfo(Section):
    def __init__(self, text: str):
        super().__init__(text)
        self.name = None
        self.phone_number = None
        self.email = None
        self.website = None
        self.position = None

        name = self.__get_name()
        if name:
            self.name = name

        phone_number = self.__get_phone_number(text)
        if phone_number:
            self.phone_number = phone_number

        email = self.__get_email(text)
        if email:
            self.email = email

        website = self.__get_website(text)
        if website:
            self.website = website

        position = self.__get_position()
        if position:
            self.position = position

    def get_info(self):
        result = [self.name, self.phone_number, self.email, self.website, self.position]
        return result

    def __get_name(self):
        for span in self.doc.spans:
            if span.type == PER:
                return span.text
        return None

    def __get_phone_number(self, text: str):
        phone_pattern = re.compile(
            r"((\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})")
        groups = phone_pattern.search(text)
        if groups:
            return groups.group(1)
        return None

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
        for span in self.doc.spans:
            if span.type != PER and span.type != LOC:
                return span.text
        return None