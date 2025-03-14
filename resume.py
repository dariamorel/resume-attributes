from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    DatesExtractor,

    Doc
)
from natasha import (Segmenter, Doc)
from section import MainInfo, WorkExperience, Education, Skills
from document import Document
import re
import time

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)

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

    def get_work_experience(self) -> WorkExperience:
        return self.__work_experience

    def get_education(self) -> Education:
        return self.__education

    def get_skills(self) -> Skills:
        return self.__skills

        # private:

    def __divide_to_sections(self, text: str):
        """    
        Функция выделяет секцию из исходного текста.  
        :param text: исходный текст        """
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
        self.__work_experience = WorkExperience(work_experience)
        self.__education = Education(education)
        self.__skills = Skills(skills)