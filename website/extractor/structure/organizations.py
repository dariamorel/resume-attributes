from datetime import datetime

from document import Date
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

    Doc, ORG, PER
)
from natasha.extractors import Match
from natasha import obj

from dates_parser import all_dates_extractor

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)

def date_to_text(fact):
    months = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
    }

    if fact.day and fact.month and fact.year:
        formated_date = datetime(year=fact.year, month=fact.month, day=fact.day)
        return formated_date.strftime("%d %B %Y года")
    elif fact.month and fact.year:
        return f"{months[fact.month]} {fact.year} года"
    elif fact.year:
        formated_date = datetime(year=fact.year, month=1, day=1)
        return formated_date.strftime("%Y год")

class Organizations(Section):
    def __init__(self, text: str):
        self.connected_dates = False
        self.objects = None

        spans_text = text.replace('\n', ", ")

        doc = Doc(spans_text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        # Извлекаем именованные сущности
        doc.tag_ner(ner_tagger)

        # Извлекаем даты
        dates_text = text.replace('\n', '  ')
        dates = [date for date in all_dates_extractor.findall(dates_text)]
        dates = self.__connected_dates(dates, dates_text)

        ents = list()

        # Добавляем организации в ents
        for span in doc.spans:
            if span.type == ORG or span.type == PER:
                ents.append(Ent("ORG", span.text, span.start, span.stop))

        # Добавляем даты в ents
        for date in dates:
            if type(date) == list:
                texted_pair = f"{date_to_text(date[0].fact)} - {date_to_text(date[-1].fact)}"
                ents.append(Ent("DATE", texted_pair, date[0].span.start, date[-1].span.stop))
                continue
            ents.append(Ent("DATE", date_to_text(date.fact), date.span.start, date.span.stop))

        # Сортируем ents
        self.ents = sorted(ents, key=lambda x: x.start)

        # Объединяем ents в объекты Object
        self.objects = self.__set_objects()

    def __set_objects(self):
        # Делим ents на объекты date + ORGs
        objects = []

        orgs = []
        date = None
        for ent in self.ents:
            if date and ent.type == "DATE":
                objects.append(Object(date, orgs.copy()))
                date = ent
                orgs.clear()
            elif ent.type == "DATE":
                date = ent
            else:
                orgs.append(ent)
        if date:
            objects.append(Object(date, orgs.copy()))
        return objects

    def __connected_dates(self, dates, text):
        connected_dates = []
        i = 1
        while i < len(dates):
            # dates[i] и dates[i-1] связаны
            start = dates[i-1].span.stop
            stop = dates[i].span.start
            if (stop - start < 10) and ('-' in text[start:stop] or '—' in text[start:stop]):
                connected_dates.append([dates[i-1], dates[i]])
                self.connected_dates = True
                i += 2
            else:
                connected_dates.append(dates[i-1])
                i += 1
        if len(dates) > 1:
            start = dates[-2].span.stop
            stop = dates[-1].span.start
            if not ((stop - start < 10) and ('-' in text[start:stop] or '—' in text[start:stop])):
                connected_dates.append(dates[-1])
        if len(dates) == 1:
            connected_dates.append(dates[0])

        # Возвращаем либо список пар, либо список одиночных дат
        if self.connected_dates:
            return [date for date in connected_dates if type(date) == list]
        return connected_dates



