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
from dictionaries import sections_dict

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)

class Resume:
    def __init__(self, text: str):
        self.__main_info = None
        self.__work_experience = None
        self.__education = None
        self.__skills = None

        self.__divide_into_sections(text)

    # public:
    def get_main_info(self) -> Doc:
        return self.__main_info

    def get_work_experience(self) -> Doc:
        return self.__work_experience

    def get_education(self) -> Doc:
        return self.__education

    def get_skills(self) -> Doc:
        return self.__skills

    # private:
    def __divide_into_sections(self, text: str) -> None:
        if not isinstance(text, str):
            ValueError("Invalid argument type.")

        # токенизация текста
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

        # делаем срез дока
        start_ind = doc.tokens[start].start
        end_ind = doc.tokens[end-1].stop

        new_doc = Doc(doc.text[start_ind:end_ind])
        new_doc.segment(segmenter)
        new_doc.tag_morph(morph_tagger)
        new_doc.parse_syntax(syntax_parser)
        new_doc.tag_ner(ner_tagger)

        match cur_section:
            case "main_info":
                self.__main_info = new_doc
                return
            case "work_experience":
                self.__work_experience = new_doc
                return
            case "education":
                self.__education = new_doc
                return
            case "skills":
                self.__skills = new_doc
                return
        raise ValueError("Invalid section name.")
