from natasha import (Segmenter, Doc)
from dictionaries import sections_dict

class Sections:
    def __init__(self, text: str):
        self.__main_info = None
        self.__work_experience = None
        self.__education = None
        self.__skills = None

        self.__divide_into_sections(text)

    # public:
    def get_main_info(self) -> list:
        return self.__main_info

    def get_work_experience(self) -> list:
        return self.__work_experience

    def get_education(self) -> list:
        return self.__education

    def get_skills(self) -> list:
        return self.__skills

    # private:
    def __divide_into_sections(self, text: str) -> None:
        if not isinstance(text, str):
            ValueError("Invalid argument type.")

        # токенизация текста
        segmenter = Segmenter()
        doc = Doc(text)
        doc.segment(segmenter)

        # выделение секций по ключевым словам
        start = 0
        cur_section = "main_info"
        for i, token in enumerate(doc.tokens):
            if token.text.lower() in sections_dict["work_experience"]:
                self.__add_to_section(doc, cur_section, start, i)
                start = i + 1
                cur_section = "work_experience"
            elif token.text.lower() in sections_dict["education"]:
                self.__add_to_section(doc, cur_section, start, i)
                start = i + 1
                cur_section = "education"
            elif token.text.lower() in sections_dict["skills"]:
                self.__add_to_section(doc, cur_section, start, i)
                start = i + 1
                cur_section = "skills"

        self.__add_to_section(doc, cur_section, start, len(doc.tokens))

    # добавляет секцию в нужное поле
    def __add_to_section(self, doc: Doc, cur_section: str, start: int, end: int) -> None:
        if start < 0 or end >= len(doc.tokens):
            ValueError("Index is out of range.")

        match cur_section:
            case "main_info":
                self.__main_info = doc.tokens[start:end]
                return
            case "work_experience":
                self.__work_experience = doc.tokens[start:end]
                return
            case "education":
                self.__education = doc.tokens[start:end]
                return
            case "skills":
                self.__skills = doc.tokens[start:end]
                return
        raise ValueError("Invalid section name.")
