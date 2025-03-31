from .ent import Ent, Object
from .section import Section
from .normalization import date_to_str
from .dates_parser import all_dates_extractor

from natasha import MorphVocab, DatesExtractor, ORG, PER

morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)

class Organizations(Section):
    def __init__(self, text):
        """
        Функция извлекает из текста даты и организации, преобразовывает их в объекты Ent и объединяет в объекты Object.
        """
        super().__init__(text)
        self.connected_dates = False
        self.connections_type = None
        self.objects = None

        # Извлекаем даты
        dates_text = text.replace('\n', '  ')
        dates = [date for date in all_dates_extractor.findall(dates_text)]
        # Находим связи между датами
        dates = self.__connected_dates(dates, dates_text)

        ents = list()

        # Добавляем организации в ents
        for span in self.spans:
            if span.type == ORG:
                ents.append(Ent("ORG", span.text, span.start, span.stop, span.tokens))

        # Добавляем даты в ents
        for date in dates:
            if type(date) == list:
                texted_pair = f"{date_to_str(date[0].fact)} - {date_to_str(date[-1].fact)}"
                ents.append(Ent("DATE", texted_pair, date[0].span.start, date[-1].span.stop, date[0].tokens + date[-1].tokens))
                continue
            ents.append(Ent("DATE", date_to_str(date.fact), date.span.start, date.span.stop, date.tokens))

        # Сортируем ents
        self.ents = sorted(ents, key=lambda x: x.start)

        if len(self.ents) == 0:
            return

        # Определяем тип связей между DATE и ORGs
        self.__define_connections_type()

        # Объединяем ents в объекты Object
        self.objects = self.__set_objects()


    def __define_connections_type(self):
        """
        Функция определяет тип связи между датами и организациями в тексте.
        :return: количество организаций до даты в каждом фрагменте или -1, если дата в конце фрагмента
        """
        if self.ents[-1].type == "DATE":
            self.connections_type = -1
            return

        i = 0
        while self.ents[i].type != "DATE":
            i += 1
            if i >= len(self.ents):
                break
        self.connections_type = i


    def __set_objects(self) -> list[Object]:
        """
        Функция делит list[Ent] на фрагменты, где есть одна дата и связанные с ней организации.
        Затем оборачивает каждый фрагмент в объект класса Object.
        :return: список объектов Object
        """
        # Делим ents на объекты date + ORGs
        objects = []

        orgs = []
        date = None
        j = self.connections_type

        # Если тип соединения -1 (дата в конце)
        if self.connections_type == -1:
            for ent in self.ents:
                if ent.type == "DATE":
                    if date and len(orgs) > 0:
                        objects.append(Object(date, orgs.copy()))
                        orgs.clear()
                    date = ent
                else:
                    orgs.append(ent)
            if date and len(orgs) > 0:
                objects.append(Object(date, orgs.copy()))
            return objects

        # Если тип соединения >= 0
        for i in range(len(self.ents) - j):
            if self.ents[i].type == "DATE" and i != i + j:
                continue
            if self.ents[i+j].type == "DATE":
                if date and len(orgs) > 0:
                    objects.append(Object(date, orgs.copy()))
                    orgs.clear()
                date = self.ents[i+j]
            if self.ents[i].type != "DATE":
                orgs.append(self.ents[i])

        for i in range(len(self.ents) - j, len(self.ents)):
            if self.ents[i].type == "ORG":
                orgs.append(self.ents[i])
        if date and len(orgs) > 0:
            objects.append(Object(date, orgs.copy()))
        return objects

    def __connected_dates(self, dates, text):
        """
        Функция находит связанные между собой даты и объединяет их в пары.
        Также функция устанавливает флаг self.connected_dates = True, если в тексте есть связанные даты, и False иначе.
        :param dates: список дат
        :return: если self.connected_dates = True, то список из пар связанных дат, иначе - список одиночных дат
        """
        connected_dates = []
        i = 1
        while i < len(dates):
            # dates[i] и dates[i-1] связаны
            start = dates[i-1].span.stop
            stop = dates[i].span.start
            # Если между датами есть символ '-'
            if (stop - start < 10) and any([symb in text[start:stop] for symb in ['-', '–', '—']]):
                connected_dates.append([dates[i-1], dates[i]])
                self.connected_dates = True
                i += 2
            else:
                connected_dates.append(dates[i-1])
                i += 1
        if len(dates) > 1:
            start = dates[-2].span.stop
            stop = dates[-1].span.start
            if not ((stop - start < 10) and any([symb in text[start:stop] for symb in ['-', '–', '—']])):
                connected_dates.append(dates[-1])
        if len(dates) == 1:
            connected_dates.append(dates[0])

        # Возвращаем либо список пар, либо список одиночных дат
        if self.connected_dates:
            return [date for date in connected_dates if type(date) == list]
        return connected_dates



