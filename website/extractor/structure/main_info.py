import re
from section import Section
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    DatesExtractor,
    NamesExtractor, Doc, PER
)
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)
names_extractor = NamesExtractor(morph_vocab)

def name_to_str(fact):
    result = ""
    if fact.last:
        last = fact.last[0].upper() + fact.last[1:].lower()
        result += f"{last} "
    if fact.first:
        first = fact.first[0].upper() + fact.first[1:].lower()
        result += f"{first} "
    if fact.middle:
        middle = fact.middle[0].upper() + fact.middle[1:].lower()
        result += f"{middle} "
    return result


class MainInfo(Section):
    def __init__(self, text: str):
        super().__init__(text)
        self.name = None
        self.phone_number = None
        self.email = None
        self.website = None
        self.position = None

        name = self.__get_name(text)
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


    def __get_name(self, text):
        result = None

        names = names_extractor(text)
        for name in names:
            result = name
            break

        names_text = re.sub(r'\s+', ' ', text)
        names = names_extractor(names_text)
        for name in names:
            if not result:
                return name_to_str(name.fact)
            return max(name_to_str(result.fact), name_to_str(name.fact), key=len)
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
        result = re.findall(link_pattern, text, re.IGNORECASE)
        if len(result) > 0:
            return result[0].strip()

        link_pattern = r'\b[a-zA-Z0-9-/]+\.[a-zA-Z0-9/]+'
        result = re.findall(link_pattern, text, re.IGNORECASE)
        for res in result:
            # Проверяем,чтобы не являлся частью email
            if res.strip() not in self.email:
                return res.strip()
        return None