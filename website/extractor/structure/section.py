import re
import locale
from ent import Pair
from dictionaries import languages_list

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

def normalize_sent(sent):
    sent = sent.strip()
    if len(sent) == 0:
        return None
    # Убираем спец символы в начале и в конце
    while not sent[0].isalpha():
        sent = sent[1:]
        if len(sent) == 0:
            return None

    doc = Doc(sent)
    doc.segment(segmenter)
    while not sent[-1].isalpha():
        sent = sent[:-1]
        if len(sent) == 0:
            return None

    # Добавляем точку, если длинное предложение
    if len(doc.tokens) > 3:
        sent += '.'

    # Форматируем строчные и заглавные буквы
    sent = sent.lower()
    return sent[0].upper() + sent[1:]

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


class Skills(Section):
    def __init__(self, text):
        super().__init__(text)
        self.skills = None
        # Если слова разделены несколькими пробелами
        if "  " in text:
            text = text.replace(',', ' ').replace('.', ' ').replace(';', ' ')
            self.skills = [normalize_sent(skill) for skill in text.split()]
        else:
            text = text.replace('\n', ', ').replace('.', ' ').replace(';', ' ')
            self.skills = [normalize_sent(skill) for skill in text.split(',')]

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
        groups = re.search(rf'({section_name}\s|\s{section_name}:)(.*?)({pattern}|\Z|\n)', text,
                            re.DOTALL | re.IGNORECASE)

        if groups:
            return groups.group(2)
        return None

