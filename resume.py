from organizations import Organizations
from section import MainInfo, Skills
import re

sections_dict = {
    "main_info": [],
    "work_experience": ["Опыт работы", "Опыт", "Experience", "Work experience"],
    "education": ["Образование", "Education"],
    "skills": ["Навыки", "навыки", "Skills"]
}

class Resume:
    def __init__(self, text: str):
        self.__main_info = None
        self.__work_experience = None
        self.__education = None
        self.__skills = None

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
        pattern = '|'.join(
            ['|'.join(names) for key, names in sections_dict.items() if key != "main_info"])

        sections = re.search(rf'(.*?)({pattern})(.*?)({pattern})(.*?)({pattern})(.*)', text,
                             re.DOTALL | re.IGNORECASE)

        main_info = sections.group(1)
        work_experience, education, skills = None, None, None

        for i in range(2, 7, 2):
            if sections.group(i) in sections_dict["work_experience"]:
                work_experience = sections.group(i + 1)
            elif sections.group(i) in sections_dict["education"]:
                education = sections.group(i + 1)
            elif sections.group(i) in sections_dict["skills"]:
                skills = sections.group(i + 1)

        self.__main_info = MainInfo(main_info)
        self.__work_experience = Organizations(work_experience)
        self.__education = Organizations(education)
        self.__skills = Skills(skills)