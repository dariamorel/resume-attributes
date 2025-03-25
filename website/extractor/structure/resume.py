from organizations import Organizations
from section import Skills
from  main_info import MainInfo
import re
import time
from dictionaries import sections_dict

def clean_text(text: str):
    # Убираем лишние переносы строки
    text = re.sub(r'(\w)-(\W)', r'\1\2', text)

    return text

class Resume:
    def __init__(self, text: str):
        text = clean_text(text)
        self.main_info = self.__find_section(text, "main_info")
        self.position = self.__find_section(text, "position")
        work_experience = self.__find_section(text, "work_experience")
        if work_experience:
            self.work_experience = Organizations(work_experience.strip())
        education = self.__find_section(text, "education")
        if education:
            self.education = education.strip()
        self.courses = self.__find_section(text, "courses")
        self.projects = self.__find_section(text, "projects")
        self.achievements = self.__find_section(text, "achievements")
        self.skills = self.__find_section(text, "skills")
        self.languages = self.__find_section(text, "languages")

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
        groups = re.findall(rf'({pattern1})(.*?)({pattern2}|\Z)', text,
                            re.DOTALL | re.IGNORECASE)
        if groups:
            return max((group[1] for group in groups), key=len)
        return None
