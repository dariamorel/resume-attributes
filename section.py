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

segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)


def format_date(date: Date):
    """  
    Функция форматирует дату объекта Date    :param date: объект Date    :return: строка отформатированной даты  
    """
    if date.fact.day and date.fact.month and date.fact.year:
        formated_date = datetime(year=date.fact.year, month=date.fact.month, day=date.fact.day)
        return formated_date.strftime("%d %B %Y года")
    elif date.fact.month and date.fact.year:
        formated_date = datetime(year=date.fact.year, month=date.fact.month, day=1)
        return formated_date.strftime("%B %Y года")
    elif date.fact.year:
        formated_date = datetime(year=date.fact.year, month=1, day=1)
        return formated_date.strftime("%Y год")


class Section:
    def __init__(self, text: str):
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)

        self.doc = Document(doc)

        self.__dates = None

    @property
    def dates(self):
        """  
        Функция заполняет поле __dates, если оно None, или возвращает существующее поле __dates.        :return: список из объектов Date  
        """
        if self.__dates is not None:
            return self.__dates

        dates = [Date(match) for match in dates_extractor(self.doc.text)]

        # заполянем поле tokens для каждой даты
        dates = self.__add_tokens_to_dates(dates)

        # добавляем пропущенные даты
        dates = self.__add_date_connections(dates)
        self.__dates = dates
        return self.dates

    def __add_tokens_to_dates(self, dates: list):
        """  
        Функция заполняет поля tokens для каждой date in dates.        :param dates: список объектов Date        :return: dates с добавленными tokens  
        """
        i, j = 0, 0
        token_list = list()

        while i < len(self.doc.tokens) and j < len(dates):
            token = self.doc.tokens[i]
            date = dates[j]
            if len(token_list) > 0 and token.stop >= date.stop:
                token_list.append(token)
                date.tokens = token_list.copy()
                token_list.clear()
                i += 1
                j += 1
            elif len(token_list) > 0:
                token_list.append(token)
                i += 1
            elif token.start == date.start and token.stop == date.stop:
                date.tokens = [token]
                i += 1
                j += 1
            elif token.start == date.start:
                token_list.append(token)
                i += 1
            else:
                i += 1

        return dates

    def __add_date_connections(self, dates: list):
        """  
        Функция заполняет объекту Date поле connection, если дата соединена с другой через '-'.        Также функция добавляет пропущенные в DatesExtractor одиноко стоящие года.        :param dates: список из объектов Date        :return: отформатированный список с датами  
        """
        dates_to_add = list()
        for ind, date in enumerate(dates):
            # проверяем, не связана ли эта дата с предыдущей
            if ind > 0 and date.tokens[0].i - dates[ind - 1].tokens[-1].i == 2 and self.doc.tokens[
                date.tokens[0].i - 1].text in ['-', '—']:
                if date.connection is None and dates[ind - 1].connection is None:
                    date.connection = dates[ind - 1]
                    dates[ind - 1].connection = date

                    # смотрим на два предыдущих токена
            if date.tokens[0].i - 2 < 0:
                continue
            prev_token_1 = self.doc.tokens[date.tokens[0].i - 1]
            prev_token_2 = self.doc.tokens[date.tokens[0].i - 2]

            # если дата связана через - с одиноко стоящим годом
            if prev_token_1.text in ['-', '—'] and (prev_token_2.text.isdigit() and len(prev_token_2.text) == 4):
                # если это не уже добавленная дата, которая стоит до
                if not (date.connection is not None and (
                        date.connection.tokens[0].i <= prev_token_2.i <= date.connection.tokens[-1].i)):
                    new_match = Match(prev_token_2.start, prev_token_2.stop,
                                      fact=obj.Date(day=None, month=None, year=int(prev_token_2.text)))
                    new_date = Date(new_match)
                    new_date.tokens = [prev_token_2]

                    # добавляем новые соединения
                    date.connection = new_date
                    new_date.connection = date

                    dates_to_add.append(new_date)
                    continue

                    # смотрим на два последующих токена
            if date.tokens[0].i - 2 < 0:
                continue
            next_token_1 = self.doc.tokens[date.tokens[0].i - 1]
            next_token_2 = self.doc.tokens[date.tokens[0].i - 2]

            # если дата связана через - с одиноко стоящим годом
            if next_token_1.text in ['-', '—'] and (next_token_2.text.isdigit() and len(next_token_2.text) == 4):
                # если это не уже добавленная дата, которая стоит после
                if not (date.connection is not None and (
                        date.connection.tokens[0].i <= next_token_2.i <= date.connection.tokens[-1].i)):
                    new_match = Match(next_token_2.start, next_token_2.stop,
                                      fact=obj.Date(day=None, month=None, year=int(next_token_2.text)))
                    new_date = Date(new_match)
                    new_date.tokens = [next_token_2]

                    # добавляем новые соединения
                    date.connection = new_date
                    new_date.connection = date

                    dates_to_add.append(new_date)
                    continue

        return dates + dates_to_add

    def get_info(self):
        result = list()

        # токены, принадлежащие датам
        token_to_date = {i: -1 for i in range(len(self.doc.tokens))}
        for i, date in enumerate(self.dates):
            for token in date.tokens:
                token_to_date[token.i] = i

                # токены, принадлежащие сущностям
        token_to_span = {i: -1 for i in range(len(self.doc.tokens))}
        for i, span in enumerate(self.doc.spans):
            for token in span.tokens:
                token_to_span[token.i] = i

                # добавляем в result именованные сущности и даты
        i = 0
        while i < len(self.doc.tokens):
            token = self.doc.tokens[i]
            if token_to_date[token.i] != -1:
                result.append(self.dates[token_to_date[token.i]])
                i = self.dates[token_to_date[token.i]].tokens[-1].i + 1
            elif token_to_span[token.i] != -1 and self.doc.spans[token_to_span[token.i]].type == ORG:
                result.append(self.doc.spans[token_to_span[token.i]])
                i = self.doc.spans[token_to_span[token.i]].tokens[-1].i + 1
            else:
                i += 1

                # форматируем return
        formated_result = str()

        for i, cur_obj in enumerate(result):
            # текущий объект дата и следующий - дата, связанная с текущей
            if type(cur_obj) == Date and (i + 1 < len(result) and result[i + 1] == cur_obj.connection):
                formated_result += format_date(cur_obj) + ' - '
                # текущий объект просто дата
            elif type(cur_obj) == Date:
                formated_result += '\n' + format_date(cur_obj) + '\n'
                # текущий объект именованная сущность
            elif type(cur_obj) == natasha.doc.DocSpan:
                formated_result += cur_obj.text + '\n'

        return formated_result


class MainInfo(Section):
    pass


class WorkExperience(Section):
    pass


class Education(Section):
    pass


class Skills(Section):
    pass