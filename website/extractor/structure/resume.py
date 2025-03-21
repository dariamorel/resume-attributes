from organizations import Organizations
from section import Skills
from  main_info import MainInfo
import re
import time

sections_dict = {
    "work_experience": ["опыт работы", "experience", "work experience", "место работы"],
    "education": ["высшее образование", "образование высшее", "образование", "education"],
    "skills": ["ключевые навыки", "навыки", "skills"]
}

def clean_text(text: str):
    # Убираем лишние переносы строки
    text = re.sub(r'(\w)-(\W)', r'\1\2', text)

    return text

class Resume:
    def __init__(self, text: str):
        self.__main_info = None
        self.__work_experience = None
        self.__education = None
        self.__skills = None

        text = clean_text(text)
        self.__divide_to_sections(text)

    def get_main_info(self) -> MainInfo:
        return self.__main_info

    def get_work_experience(self) -> Organizations:
        return self.__work_experience

    def get_education(self) -> Organizations:
        return self.__education

    def get_skills(self) -> Skills:
        return self.__skills

    def __divide_to_sections(self, text: str):
        """    
        Функция выделяет секцию из исходного текста.
        """
        sections = [["main_info", text]]
        used_sections = []

        while self.__determine_section(sections, used_sections):
            self.__determine_section(sections, used_sections)

        for section in sections:
            if section[0] == "main_info":
                self.__main_info = section[-1].strip()
            elif section[0] == "work_experience":
                self.__work_experience = Organizations(section[-1].strip())
            elif section[0] == "education":
                self.__education = section[-1].strip()
            elif section[0] == "skills":
                self.__skills = section[-1].strip()

    def __determine_section(self, sections: list, used_sections: list):
        pattern = '|'.join(
            ['|'.join(names) for key, names in sections_dict.items() if key not in used_sections])

        groups = re.search(rf'(.*?)({pattern})(.*)', sections[-1][-1],
                             re.DOTALL | re.IGNORECASE)
        if groups:
            # Определяем, какую секцию нашли
            group_name = None
            if groups.group(2).lower() in sections_dict["work_experience"]:
                group_name = "work_experience"
            elif groups.group(2).lower() in sections_dict["education"]:
                group_name = "education"
            elif groups.group(2).lower() in sections_dict["skills"]:
                group_name = "skills"

            if not group_name:
                return False
            sections[-1][-1] = groups.group(1)
            sections.append([group_name, groups.group(3)])
            used_sections.append(group_name)

            return True
        return False
