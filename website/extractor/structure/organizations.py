from document import Date
from ent import Ent
from section import Section
from natasha import DatesExtractor, MorphVocab
from natasha.extractors import Match
from natasha import obj

morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)

def is_year(token):
    return token.text.isdigit() and len(token.text) == 4


class Organizations(Section):
    def __init__(self, text: str):
        super().__init__(text)
        self.__dates = None

    @property
    def dates(self):
        """
        Функция заполняет поле __dates, если оно None, или возвращает существующее поле __dates.
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
        Функция заполняет поле tokens для каждой date in dates.
        """
        i, j = 0, 0
        token_list = list()

        while i < len(self.doc.tokens) and j < len(dates):
            token, date = self.doc.tokens[i], dates[j]

            if date.start <= token.start <= date.stop:
                token_list.append(token)
            elif len(token_list) > 0:
                date.tokens = token_list.copy()
                token_list.clear()
                j += 1
                continue
            i += 1

        if len(token_list) > 0:
            dates[j].tokens = token_list

        return dates

    def __add_date_connections(self, dates: list):
        """
        Функция заполняет объекту Date поле connection, если дата соединена с другой через '-'.
        Также функция добавляет пропущенные в DatesExtractor одиноко стоящие года.
        """
        # Добавляем одиноко стоящие года
        j = 0
        token_to_date = self.token_to_span(dates)
        for date in dates.copy():
            token, ind = None, None
            if (date.start_i - 2 >= 0) and is_year(self.doc.tokens[date.start_i - 2]) and (token_to_date[date.start_i - 2] == -1):
                token, ind = self.doc.tokens[date.start_i - 2], j

            if (date.stop_i + 2 < len(self.doc.tokens)) and is_year(self.doc.tokens[date.stop_i + 2]) and (token_to_date[date.stop_i + 2] == -1):
                token, ind = self.doc.tokens[date.stop_i + 2], j + 1

            if token:
                new_match = Match(token.start, token.stop,
                                  fact=obj.Date(day=None, month=None, year=int(token.text)))
                new_date = Date(new_match)
                new_date.tokens = [token]
                dates.insert(ind, new_date)
                j += 1
            j += 1

        # Добавляем связи между датами
        for i in range(1, len(dates)):
            cur_date, prev_date = dates[i], dates[i-1]
            if cur_date.connection:
                continue

            ind = cur_date.start_i
            if self.doc.tokens[ind - 1].text in ['-', '—'] and (prev_date.start_i <= self.doc.tokens[ind - 2].i <= prev_date.stop_i):
                cur_date.connection = prev_date
                prev_date.connection = cur_date

        return dates

    def get_info(self):
        """
        :return: список объектов Ent
        """
        # токены, принадлежащие датам
        token_to_date = self.token_to_span(self.dates)

        # токены, принадлежащие сущностям
        token_to_span = self.token_to_span(self.spans)

        result, ent_list = list(), list()

        i, last_was_span = 0, False
        while i < len(self.doc.tokens):
            token, el = self.doc.tokens[i], None
            if token_to_date[token.i] == -1 and token_to_span[token.i] == -1:
                i += 1
                continue

            if token_to_date[token.i] != -1:
                if last_was_span:
                    ent_list.append(Ent(result.copy()))
                    result.clear()

                el = self.dates[token_to_date[token.i]]
                last_was_span = False
            elif token_to_span[token.i] != -1:
                el = self.spans[token_to_span[token.i]]
                last_was_span = True

            result.append(el)
            i = el.tokens[-1].i + 1

        ent_list.append(Ent(result.copy()))
        return ent_list

