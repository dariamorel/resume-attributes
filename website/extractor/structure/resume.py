from organizations import Organizations
from skills import Skills
from languages import Languages
from position import Position
from main_info import MainInfo
from dictionaries import sections_dict, forbidden_words
import re
import yake

class Resume:
    def __init__(self, text: str):
        text = re.sub(r'(\w)-(\W)', r'\1\2', text)
        self.text = text
        self.main_info = None
        self.position = None
        self.work_experience = None
        self.education = None
        self.skills = None
        self.languages = None

        main_info = self.__find_section("main_info")
        if main_info:
            self.main_info = MainInfo(main_info)

        position = self.__find_section("position")
        # Если есть секция с должностью
        if position:
            self.position = Position(position.strip())
        # Если нет, то берем должность из списка ключевых слов.
        else:
            position = self.__add_position()
            if len(position) > 0:
                self.position = Position("", position)

        work_experience = self.__find_section("work_experience")
        if work_experience:
            self.work_experience = Organizations(work_experience.strip())

        education = self.__find_section("education")
        if education:
            self.education = Organizations(education.strip())

        skills = self.__find_section("skills")
        if skills:
            self.skills = Skills(skills.strip())

        languages = self.__find_section("languages")
        if languages:
            self.languages = Languages(languages.strip())

    def get_name(self):
        if self.main_info and self.main_info.name:
            return self.main_info.name.text
        return None

    def get_position(self):
        if self.position:
            return self.position.position

    def get_phone_number(self):
        if self.main_info:
            return self.main_info.phone_number

    def get_email(self):
        if self.main_info:
            return self.main_info.email
        return None

    def get_website(self):
        if self.main_info:
            return self.main_info.website
        return None

    def get_work_experience(self):
        if self.work_experience:
            return self.work_experience.objects
        return None

    def get_education(self):
        if self.education:
            return self.education.objects
        return None

    def get_skills(self):
        if self.skills:
            return self.skills.skills
        return None

    def get_languages(self):
        if self.languages:
            return self.languages.languages
        return None

    def __add_position(self):
        """
        Функция составляет список позиций за счет ключевых слов.
        :return: список ключевых слов, подходящих под секцию должность
        """
        position = []
        # Находим топ-10 ключевых слов в тексте
        extractor = yake.KeywordExtractor(lan="ru", top=10)
        keywords = extractor.extract_keywords(self.text)
        for kw in keywords:
            # Берем не более трех подходящих позиций.
            if len(position) >= 3:
                break

            # Проверяем, что найденное ключевое слово не часть имени.
            if self.main_info and self.main_info.name:
                name = self.main_info.name.fact
                if any([el in kw[0] for el in [str(name.first), str(name.last), str(name.middle)]]):
                    continue
            position.append(kw[0])
        return position

    def __find_section(self, section_name):
        """
        Функция ищет в тексте секцию с названием section_name.
        :param section_name: название секции, которую ищем
        :return: текст найденной секции
        """
        # Если ищем секцию main_info, то берем самый первый фрагмент
        if section_name == "main_info":
            pattern = '|'.join(
                ['|'.join([f"\s{name}\s|\s{name}:" for name in names]) for key, names in sections_dict.items()])
            groups = re.search(rf'(.*?)({pattern}|\Z)', self.text,
                                re.DOTALL | re.IGNORECASE)
            if groups:
                return groups.group(1)
            return None

        # Шаблон для поиска секции section_name
        pattern1 = '|'.join([f"\s{name}\s|\s{name}:" for name in sections_dict[section_name]])
        # Если ищем секцию с опытом работы или образованием, то исключаем некоторые слова для поиска.
        if section_name in ["work_experience", "education"]:
            pattern2 = '|'.join(
                ['|'.join([f"\s{name}\s|\s{name}:" for name in names if name not in forbidden_words]) for key, names in sections_dict.items() if
                 key != section_name])
        # Иначе используем обычный шаблон
        else:
            pattern2 = '|'.join(
                ['|'.join([f"\s{name}\s|\s{name}:" for name in names]) for key, names in sections_dict.items() if
                 key != section_name])
        groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z)', self.text,
                           re.DOTALL | re.IGNORECASE)


        if groups:
            return groups.group(2)
        return None
