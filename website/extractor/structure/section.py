import re
import locale
from .ent import Pair
from .dictionaries import languages_list
from .normalization import delete_additional_info, normalize_sent

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
        # Отчищаем текст от дополнительной информации
        text = delete_additional_info(text)

        # Заменяем символ '\n' на ',', чтобы упростить поиск именованных сущностей
        spans_text = text.replace('\n', ", ")

        doc = Doc(spans_text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        # Извлекаем именованные сущности
        doc.tag_ner(ner_tagger)

        self.doc = doc

class Skills(Section):
    def __init__(self, text):
        super().__init__(text)
        self.skills = None

        # Если слова разделены несколькими пробелами
        if "   " in text:
            text = text.replace('\n', '   ').replace(',', '   ').replace(';', '   ')
            self.skills = [normalize_sent(skill, True) for skill in text.split("   ") if normalize_sent(skill, True)]
        elif ',' in [token.text for token in self.doc.tokens[:5]]:
            text = text.replace('\n', ' ').replace(';', ',')
            self.skills = [normalize_sent(skill, True) for skill in text.split(',') if normalize_sent(skill, True)]
        else:
            text = text.replace('\n', ' ')
            self.skills = [f"{normalize_sent(skill, True)}." for skill in text.split('.') if normalize_sent(skill, True)]

class Languages(Section):
    def __init__(self, text):
        super().__init__(text)

        languages = []
        for language_name in languages_list:
            info = self.__find_section(text, language_name)
            if info:
                info = normalize_sent(info)
                languages.append(Pair(language_name, info))

        self.languages = languages

    def __find_section(self, text, section_name):
        pattern1 = f"{section_name} язык|{section_name} язык:|{section_name}\s|\s{section_name}:"
        pattern2 = '|'.join([f"\s{lang}\s|\s{lang}:" for lang in languages_list if lang != section_name])
        groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z|\n)', text,
                            re.DOTALL | re.IGNORECASE)

        if groups:
            return groups.group(2)
        return None

