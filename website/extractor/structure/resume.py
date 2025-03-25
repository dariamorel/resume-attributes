from organizations import Organizations
from section import Skills, Position
from  main_info import MainInfo
import re
import time
import yake
from dictionaries import sections_dict

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

        main_info = self.__find_section(text, "main_info")
        if main_info:
            self.main_info = MainInfo(main_info)

        position = self.__find_section(text, "position")
        if position:
            self.position = Position(position.strip())
        else:
            self.position = Position(None, self.__add_position())

        work_experience = self.__find_section(text, "work_experience")
        if work_experience:
            self.work_experience = Organizations(work_experience.strip())

        education = self.__find_section(text, "education")
        if education:
            self.education = Organizations(education.strip())

        skills = self.__find_section(text, "skills")
        if skills:
            self.skills = Skills(skills.strip())

        languages = self.__find_section(text, "languages")
        if languages:
            self.languages = languages.strip()

    def __add_position(self):
        position = []
        extractor = yake.KeywordExtractor(lan="ru", top=3)
        keywords = extractor.extract_keywords(self.text)
        for kw in keywords:
            if self.main_info.name and self.main_info.name in kw[0]:
                continue
            position.append(kw[0])
        return position

    def __find_section(self, text, section_name):
        if section_name == "main_info":
            pattern = '|'.join(
                ['|'.join([f"\s{name}\s|\s{name}:" for name in names]) for key, names in sections_dict.items()])
            groups = re.search(rf'(.*?)({pattern}|\Z)', text,
                                re.DOTALL | re.IGNORECASE)
            if groups:
                return groups.group(1)
            return None

        pattern1 = '|'.join([f"\s{name}\s|\s{name}:" for name in sections_dict[section_name]])
        pattern2 = '|'.join(
            ['|'.join([f"\s{name}\s|\s{name}:" for name in names]) for key, names in sections_dict.items() if key != section_name])
        groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z)', text,
                            re.DOTALL | re.IGNORECASE)

        # Смотрим специфичные ситуации для секции навыков
        if section_name == "skills" and groups:
            pattern2 = '|'.join([f"\s{name}\s|\s{name}:" for name in sections_dict["languages"]])
            specific_groups = re.search(rf'({pattern1})(.*?)({pattern2}|\Z)', groups.group(2),
                       re.DOTALL | re.IGNORECASE)
            if specific_groups:
                return specific_groups.group(2)

        if groups:
            # return max((group[1] for group in groups), key=len)
            return groups.group(2)
        return None
